"""
Data loading and validation for Gravity Spy embeddings and metadata.

This module handles loading pre-computed CNN embeddings and their associated
metadata, with validation to catch common issues early.
"""

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


def load_embeddings(embeddings_path: str) -> np.ndarray:
    """
    Load pre-computed CNN embeddings from a .npy file.
    
    Args:
        embeddings_path: Path to the embeddings .npy file
        
    Returns:
        np.ndarray of shape (n_samples, embedding_dim)
        
    Raises:
        FileNotFoundError: If embeddings file doesn't exist
        ValueError: If embeddings have unexpected shape
    """
    path = Path(embeddings_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Embeddings file not found: {path}\n"
            "Please run the feature extraction pipeline first."
        )
    
    embeddings = np.load(path)
    
    if embeddings.ndim != 2:
        raise ValueError(
            f"Expected 2D embeddings array, got shape {embeddings.shape}"
        )
    
    print(f"[Data] Loaded embeddings: {embeddings.shape}")
    return embeddings


def load_metadata(metadata_path: str) -> pd.DataFrame:
    """
    Load metadata CSV containing image paths and labels.
    
    Args:
        metadata_path: Path to the metadata CSV file
        
    Returns:
        DataFrame with at minimum a 'path' column
        
    Raises:
        FileNotFoundError: If metadata file doesn't exist
        ValueError: If required columns are missing
    """
    path = Path(metadata_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {path}\n"
            "Please run the feature extraction pipeline first."
        )
    
    df = pd.read_csv(path)
    
    if "path" not in df.columns:
        raise ValueError(
            "Metadata CSV must contain a 'path' column pointing to image files"
        )
    
    print(f"[Data] Loaded metadata: {len(df):,} rows")
    return df


def load_data(
    embeddings_path: str, 
    metadata_path: str
) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Load and validate both embeddings and metadata.
    
    This is the main entry point for data loading, ensuring that embeddings
    and metadata are properly aligned.
    
    Args:
        embeddings_path: Path to embeddings .npy file
        metadata_path: Path to metadata CSV file
        
    Returns:
        Tuple of (embeddings array, metadata DataFrame)
        
    Raises:
        ValueError: If row counts don't match
    """
    embeddings = load_embeddings(embeddings_path)
    metadata = load_metadata(metadata_path)
    
    if len(metadata) != embeddings.shape[0]:
        raise ValueError(
            f"Row count mismatch: "
            f"embeddings has {embeddings.shape[0]} rows, "
            f"metadata has {len(metadata)} rows"
        )
    
    print(f"[Data] Validation passed: {len(metadata):,} samples aligned")
    return embeddings, metadata


def validate_image_paths(
    metadata: pd.DataFrame, 
    sample_size: int = 100
) -> dict:
    """
    Validate that image paths in metadata actually exist.
    
    Args:
        metadata: DataFrame with 'path' column
        sample_size: Number of paths to check (for speed)
        
    Returns:
        Dict with validation statistics
    """
    sample = metadata["path"].sample(min(sample_size, len(metadata)), random_state=42)
    
    exists_count = sum(1 for p in sample if Path(p).exists())
    missing_count = len(sample) - exists_count
    
    stats = {
        "checked": len(sample),
        "exists": exists_count,
        "missing": missing_count,
        "missing_rate": missing_count / len(sample) if len(sample) > 0 else 0
    }
    
    if missing_count > 0:
        print(f"[Data] Warning: {missing_count}/{len(sample)} sampled paths don't exist")
    else:
        print(f"[Data] Path validation passed: {exists_count}/{len(sample)} exist")
    
    return stats
