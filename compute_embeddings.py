from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models


# =============================================================================
# CONFIGURATION: EDIT THESE PATHS IF NEEDED
# =============================================================================

# =============================================================================
# CONFIGURATION: PROJECT-RELATIVE PATHS (NO WINDOWS "C:\..." STRINGS)
# =============================================================================

# Project root = folder where this script lives
PROJECT_ROOT = Path(__file__).resolve().parent

# Gravity Spy data folder (relative to project root)
GRAVITYSPY_ROOT = PROJECT_ROOT / "data" / "gravityspy_raw" / "trainingsetv1d0"

# Output folder for embeddings
OUTPUT_DIR = PROJECT_ROOT / "data" / "gravityspy_processed"

BATCH_SIZE = 64
NUM_WORKERS = 0  # keep 0 on Windows to avoid multiprocessing issues



# =============================================================================
# DATA LOADING
# =============================================================================

def get_gravityspy_dataloader(root_dir: str,
                              batch_size: int = 64,
                              num_workers: int = 0) -> tuple:
    """
    Build an ImageFolder dataset + DataLoader for Gravity Spy.

    root_dir should point directly to the trainingsetv1d0 folder,
    which contains subfolders for each glitch class.
    """
    root_path = Path(root_dir)
    if not root_path.exists():
        raise FileNotFoundError(f"Gravity Spy root directory not found: {root_path}")

    # Spectrograms are grayscale; we convert to 3-channel for ResNet.
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet means
            std=[0.229, 0.224, 0.225],   # ImageNet stds
        ),
    ])

    dataset = datasets.ImageFolder(
        root=str(root_path),
        transform=transform
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,          # keep deterministic order
        num_workers=num_workers,
        pin_memory=True
    )

    return dataset, dataloader


# =============================================================================
# MODEL: RESNET18 EMBEDDER
# =============================================================================

def build_resnet18_embedder(device: torch.device) -> nn.Module:
    """
    Load a pretrained ResNet18 and replace the final FC layer with Identity,
    so the model outputs a 512-dim embedding.
    """
    # Newer torchvision uses "weights" instead of pretrained=True
    weights = models.ResNet18_Weights.IMAGENET1K_V1
    model = models.resnet18(weights=weights)

    # Replace the final classification layer with identity
    model.fc = nn.Identity()

    model.eval()
    model.to(device)

    return model


# =============================================================================
# MAIN EMBEDDING FUNCTION
# =============================================================================

def compute_and_save_embeddings():
    """
    Run the full embedding pipeline:
      - load data
      - compute embeddings with ResNet18
      - save embeddings.npy and embeddings_metadata.csv
    """
    gravityspy_root = GRAVITYSPY_ROOT
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Using Gravity Spy data from: {gravityspy_root}")
    print(f"Will save outputs to:        {output_dir}")

    dataset, dataloader = get_gravityspy_dataloader(
        root_dir=gravityspy_root,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = build_resnet18_embedder(device=device)

    all_embeddings = []
    all_labels = []

    # ImageFolder stores (path, class_index) in .samples
    samples = dataset.samples  # list of (path, label_idx)

    # Safety check: DataLoader iterates samples in index order,
    # so we expect the same length.
    print(f"Total images in dataset: {len(samples)}")

    with torch.no_grad():
        for batch_idx, (images, labels) in enumerate(tqdm(dataloader, desc="Embedding")):
            images = images.to(device, non_blocking=True)
            feats = model(images)  # shape: (B, 512)
            feats = feats.cpu().numpy().astype(np.float32)

            all_embeddings.append(feats)
            all_labels.append(labels.numpy())

    # Stack everything
    embeddings = np.concatenate(all_embeddings, axis=0)
    label_idx = np.concatenate(all_labels, axis=0)

    # Extract paths in order
    paths = [p for (p, _) in samples]

    # Sanity checks
    assert embeddings.shape[0] == len(paths) == label_idx.shape[0], \
        "Mismatch between embeddings, paths, and labels lengths."

    # Class index -> class name
    class_names = dataset.classes
    label_names = [class_names[i] for i in label_idx]

    # Save embeddings as .npy
    emb_path = output_dir / "embeddings.npy"
    np.save(emb_path, embeddings)

    # Save metadata as .csv
    meta_df = pd.DataFrame({
        "path": paths,
        "label_idx": label_idx,
        "label_name": label_names,
    })
    meta_path = output_dir / "embeddings_metadata.csv"
    meta_df.to_csv(meta_path, index=False)

    print("\nDone!")
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Saved embeddings to: {emb_path}")
    print(f"Saved metadata to:   {meta_path}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    compute_and_save_embeddings()
