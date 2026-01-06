"""
Visualization utilities for the Gravity Spy audit.

This module generates all figures for the analysis:
- Global UMAP scatter plots
- Contact sheets for cluster deep-dives
- Intensity-ordered strips (continuum evidence)
- Interactive Plotly dashboards
"""

import base64
import io
import os
import random
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def ensure_dir(path: Path) -> Path:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_load_image(filepath: str) -> Optional[Image.Image]:
    """
    Safely load an image, returning None on failure.
    
    Args:
        filepath: Path to image file
        
    Returns:
        PIL Image in RGB mode, or None if loading fails
    """
    try:
        img = Image.open(filepath)
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img
    except Exception:
        return None


def set_seed(seed: int) -> None:
    """Set random seeds for reproducible sampling."""
    random.seed(seed)
    np.random.seed(seed)


# =============================================================================
# Static Figures (Matplotlib)
# =============================================================================

def plot_umap_scatter(
    metadata: pd.DataFrame,
    output_path: str,
    color_by: str = "cluster_id",
    sample_size: int = 12000,
    point_size: int = 6,
    dpi: int = 200,
    seed: int = 42
) -> None:
    """
    Create a global UMAP scatter plot colored by cluster or label.
    
    Args:
        metadata: DataFrame with umap_x, umap_y, and color_by column
        output_path: Where to save the figure
        color_by: Column to use for coloring ('cluster_id' or 'label')
        sample_size: Number of points to plot (for performance)
        point_size: Size of scatter points
        dpi: Figure resolution
        seed: Random seed for sampling
    """
    set_seed(seed)
    df = metadata.copy()
    
    # Sample if needed
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=seed)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if color_by == "cluster_id":
        # Handle noise points separately
        noise_mask = df["cluster_id"] == -1
        
        if noise_mask.any():
            ax.scatter(
                df.loc[noise_mask, "umap_x"],
                df.loc[noise_mask, "umap_y"],
                c="lightgray", s=point_size/2, alpha=0.3, label="noise"
            )
        
        non_noise = df[~noise_mask]
        if len(non_noise) > 0:
            scatter = ax.scatter(
                non_noise["umap_x"],
                non_noise["umap_y"],
                c=non_noise["cluster_id"],
                s=point_size,
                cmap="tab20",
                alpha=0.7
            )
            plt.colorbar(scatter, ax=ax, label="Cluster ID")
    else:
        # Color by categorical label
        unique_labels = df[color_by].unique()
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_labels)))
        color_map = dict(zip(unique_labels, colors))
        
        for label in unique_labels:
            mask = df[color_by] == label
            ax.scatter(
                df.loc[mask, "umap_x"],
                df.loc[mask, "umap_y"],
                c=[color_map[label]],
                s=point_size,
                alpha=0.7,
                label=label if len(unique_labels) <= 20 else None
            )
        
        if len(unique_labels) <= 20:
            ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title(f"Gravity Spy UMAP Embedding (n={len(df):,})")
    
    ensure_dir(Path(output_path).parent)
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close()
    
    print(f"[Viz] Saved: {output_path}")


def plot_contact_sheet(
    metadata: pd.DataFrame,
    cluster_id: int,
    output_path: str,
    top_k_labels: int = 6,
    samples_per_label: int = 5,
    dpi: int = 200,
    seed: int = 42
) -> bool:
    """
    Create a contact sheet showing sample images from a cluster.
    
    Rows represent different labels, columns show sample images.
    This reveals over-splitting (many labels for similar morphology).
    
    Args:
        metadata: DataFrame with cluster_id, label, and path columns
        cluster_id: Which cluster to visualize
        output_path: Where to save the figure
        top_k_labels: Number of labels (rows) to show
        samples_per_label: Number of samples (columns) per label
        dpi: Figure resolution
        seed: Random seed for sampling
        
    Returns:
        True if successful, False if cluster not found
    """
    set_seed(seed)
    df = metadata[metadata["cluster_id"] == cluster_id].copy()
    
    if df.empty:
        print(f"[Viz] Warning: Cluster {cluster_id} not found, skipping contact sheet")
        return False
    
    # Get top labels
    top_labels = df["label"].value_counts().head(top_k_labels).index.tolist()
    
    nrows = len(top_labels)
    ncols = samples_per_label
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(3*ncols, 3*nrows))
    
    # Ensure axes is 2D
    if nrows == 1:
        axes = axes.reshape(1, -1)
    
    for row, label in enumerate(top_labels):
        label_data = df[df["label"] == label]
        paths = label_data["path"].tolist()
        
        # Sample images
        n_samples = min(samples_per_label, len(paths))
        sampled_paths = random.sample(paths, n_samples)
        
        for col in range(ncols):
            ax = axes[row, col]
            ax.axis("off")
            
            if col < len(sampled_paths):
                img = safe_load_image(sampled_paths[col])
                if img is not None:
                    ax.imshow(img)
                else:
                    ax.text(0.5, 0.5, "Load\nError", ha="center", va="center")
            
            # Add label on first column
            if col == 0:
                count = len(label_data)
                ax.set_title(f"{label}\n(n={count})", fontsize=10, loc="left")
    
    fig.suptitle(f"Cluster {cluster_id} — Top {top_k_labels} Labels", fontsize=14, y=1.02)
    
    ensure_dir(Path(output_path).parent)
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close()
    
    print(f"[Viz] Saved: {output_path}")
    return True


def compute_image_intensity(filepath: str) -> float:
    """Compute total pixel intensity as a morphology proxy."""
    img = safe_load_image(filepath)
    if img is None:
        return np.nan
    return float(np.sum(np.array(img)))


def plot_intensity_strip(
    metadata: pd.DataFrame,
    cluster_id: int,
    output_path: str,
    max_panels: int = 12,
    dpi: int = 200,
    seed: int = 42
) -> bool:
    """
    Create an intensity-ordered strip showing morphological continuum.
    
    Images are ordered from lowest to highest total intensity, revealing
    gradual morphological evolution that humans collapsed into one label.
    
    Args:
        metadata: DataFrame with cluster_id and path columns
        cluster_id: Which cluster to visualize
        output_path: Where to save the figure
        max_panels: Number of images to show
        dpi: Figure resolution
        seed: Random seed
        
    Returns:
        True if successful, False if cluster not found
    """
    set_seed(seed)
    df = metadata[metadata["cluster_id"] == cluster_id].copy()
    
    if df.empty:
        print(f"[Viz] Warning: Cluster {cluster_id} not found, skipping intensity strip")
        return False
    
    print(f"[Viz] Computing intensities for {len(df)} images...")
    
    # Compute intensities
    intensities = [compute_image_intensity(p) for p in df["path"]]
    df["intensity"] = intensities
    
    # Remove failed loads and sort
    df = df.dropna(subset=["intensity"])
    df = df.sort_values("intensity").reset_index(drop=True)
    
    if df.empty:
        print(f"[Viz] Warning: No valid images in cluster {cluster_id}")
        return False
    
    # Sample evenly across intensity range
    if len(df) > max_panels:
        indices = np.linspace(0, len(df)-1, max_panels).astype(int)
        df = df.iloc[indices]
    
    # Create figure
    n = len(df)
    fig, axes = plt.subplots(1, n, figsize=(3*n, 3.5))
    
    if n == 1:
        axes = [axes]
    
    for ax, (_, row) in zip(axes, df.iterrows()):
        ax.axis("off")
        img = safe_load_image(row["path"])
        if img is not None:
            ax.imshow(img)
        ax.set_title(f"{row.get('ifo', '')}\n{row['label']}", fontsize=9)
    
    fig.suptitle(
        f"Cluster {cluster_id} — Ordered by Intensity (Low → High)",
        fontsize=14, y=1.02
    )
    
    ensure_dir(Path(output_path).parent)
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close()
    
    print(f"[Viz] Saved: {output_path}")
    return True


# =============================================================================
# Interactive Dashboard (Plotly)
# =============================================================================

def image_to_base64(filepath: str, max_size: int = 220) -> str:
    """Convert image to base64 data URI for Plotly hover."""
    img = safe_load_image(filepath)
    if img is None:
        return ""
    
    # Resize for faster loading
    w, h = img.size
    scale = max_size / max(w, h)
    if scale < 1:
        img = img.resize((int(w*scale), int(h*scale)), Image.Resampling.LANCZOS)
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return f"data:image/png;base64,{b64}"


def create_interactive_dashboard(
    metadata: pd.DataFrame,
    output_path: str,
    sample_size: int = 5000,
    color_by: str = "cluster_id",
    include_images: bool = True,
    seed: int = 42
) -> None:
    """
    Create an interactive Plotly dashboard with hover images.
    
    Args:
        metadata: DataFrame with umap_x, umap_y, path, label, cluster_id
        output_path: Where to save the HTML file
        sample_size: Number of points to include
        color_by: Column for coloring points
        include_images: Whether to encode images for hover
        seed: Random seed for sampling
    """
    try:
        import plotly.express as px
    except ImportError:
        print("[Viz] Warning: Plotly not installed, skipping interactive dashboard")
        return
    
    set_seed(seed)
    df = metadata.copy()
    
    # Sample for performance
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=seed).reset_index(drop=True)
    
    # Encode hover images
    if include_images:
        print(f"[Viz] Encoding {len(df)} thumbnails for hover...")
        df["hover_image"] = df["path"].apply(
            lambda p: image_to_base64(p, max_size=220)
        )
    
    # Create filename for display
    df["filename"] = df["path"].apply(lambda p: os.path.basename(p))
    
    # Create figure
    fig = px.scatter(
        df,
        x="umap_x",
        y="umap_y",
        color=color_by,
        hover_data={"label": True, "cluster_id": True, "filename": True,
                   "umap_x": False, "umap_y": False},
        title=f"Gravity Spy UMAP Explorer (n={len(df):,})",
        height=800,
        width=1000
    )
    
    # Add image hover if available
    if include_images and "hover_image" in df.columns:
        fig.update_traces(
            customdata=np.stack([
                df["hover_image"], df["label"], df["cluster_id"], df["filename"]
            ], axis=-1),
            hovertemplate=(
                "<b>Label:</b> %{customdata[1]}<br>"
                "<b>Cluster:</b> %{customdata[2]}<br>"
                "<b>File:</b> %{customdata[3]}<br><br>"
                "<img src='%{customdata[0]}' style='max-width:240px;'>"
                "<extra></extra>"
            )
        )
    
    fig.update_traces(marker=dict(size=6))
    fig.update_layout(legend=dict(itemsizing="constant"))
    
    ensure_dir(Path(output_path).parent)
    fig.write_html(output_path, include_plotlyjs="cdn")
    
    print(f"[Viz] Saved interactive dashboard: {output_path}")
