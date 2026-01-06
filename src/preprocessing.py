"""
Preprocessing utilities for Gravity Spy metadata.

This module handles the critical task of extracting correct labels from file paths,
fixing a common bug where folder names get misinterpreted as labels.
"""

from pathlib import Path
from typing import Optional

import pandas as pd


def parse_gravityspy_id(filepath: str) -> str:
    """
    Extract the Gravity Spy sample ID from a filename.
    
    Expected filename format: {IFO}_{ID}_spectrogram_{duration}.png
    Example: H1_09HE6k6EaS_spectrogram_0.5.png -> 09HE6k6EaS
    
    Args:
        filepath: Full path or filename
        
    Returns:
        The extracted Gravity Spy ID
    """
    filename = Path(filepath).name
    parts = filename.split("_")
    
    if len(parts) >= 3:
        return parts[1]
    
    # Fallback: return filename stem
    return Path(filepath).stem


def parse_interferometer(filepath: str) -> str:
    """
    Extract the interferometer (IFO) from a filename.
    
    Expected filename format: {IFO}_{ID}_spectrogram_{duration}.png
    Example: H1_09HE6k6EaS_spectrogram_0.5.png -> H1
    
    Args:
        filepath: Full path or filename
        
    Returns:
        The interferometer code (H1, L1, or 'unknown')
    """
    filename = Path(filepath).name
    parts = filename.split("_")
    
    if len(parts) >= 1 and parts[0] in ("H1", "L1"):
        return parts[0]
    
    # Fallback: search path for H1 or L1
    path_upper = filepath.upper()
    if "/H1/" in path_upper or "\\H1\\" in path_upper or path_upper.startswith("H1"):
        return "H1"
    if "/L1/" in path_upper or "\\L1\\" in path_upper or path_upper.startswith("L1"):
        return "L1"
    
    return "unknown"


def parse_label_from_path(filepath: str) -> str:
    """
    Extract the true glitch label from the folder structure.
    
    The Gravity Spy dataset has structure:
        .../trainingsetv1d0/H1L1/{GLITCH_CLASS}/{filename}.png
    
    The immediate parent folder contains the authoritative label.
    
    Args:
        filepath: Full path to the image file
        
    Returns:
        The glitch class label
    """
    parent = Path(filepath).parent.name
    
    if not parent or parent in (".", ""):
        return "unknown"
    
    return parent


def fix_metadata_labels(metadata: pd.DataFrame) -> pd.DataFrame:
    """
    Fix and enrich metadata by parsing information from file paths.
    
    This addresses a common bug where the dataset loader assigns incorrect labels
    (e.g., "H1L1" instead of the actual glitch class). The true label is always
    available in the folder structure.
    
    Added columns:
        - gravityspy_id: Unique sample identifier
        - ifo: Interferometer (H1 or L1)
        - label_from_path: True label extracted from folder name
        - label: Cleaned label for analysis (uses label_from_path)
    
    Args:
        metadata: DataFrame with 'path' column
        
    Returns:
        Enriched DataFrame with fixed labels
    """
    df = metadata.copy()
    
    print("[Preprocessing] Extracting metadata from file paths...")
    
    # Parse identifiers
    df["gravityspy_id"] = df["path"].apply(parse_gravityspy_id)
    df["ifo"] = df["path"].apply(parse_interferometer)
    df["label_from_path"] = df["path"].apply(parse_label_from_path)
    
    # Create clean label column (this is what we'll use for analysis)
    df["label"] = df["label_from_path"]
    
    # Validation
    n_unknown_labels = (df["label"] == "unknown").sum()
    if n_unknown_labels > 0:
        print(f"[Preprocessing] Warning: {n_unknown_labels} samples have unknown labels")
    
    # Report unique labels found
    unique_labels = sorted(df["label"].unique())
    print(f"[Preprocessing] Found {len(unique_labels)} unique labels")
    print(f"[Preprocessing] Top labels: {df['label'].value_counts().head(5).to_dict()}")
    
    return df


def filter_valid_samples(
    metadata: pd.DataFrame,
    min_label_count: int = 10
) -> pd.DataFrame:
    """
    Filter metadata to keep only valid samples.
    
    Args:
        metadata: DataFrame with processed metadata
        min_label_count: Minimum samples per label to keep
        
    Returns:
        Filtered DataFrame
    """
    df = metadata.copy()
    initial_count = len(df)
    
    # Remove unknown labels
    df = df[df["label"] != "unknown"]
    
    # Remove rare labels
    label_counts = df["label"].value_counts()
    valid_labels = label_counts[label_counts >= min_label_count].index
    df = df[df["label"].isin(valid_labels)]
    
    final_count = len(df)
    if final_count < initial_count:
        print(f"[Preprocessing] Filtered: {initial_count:,} -> {final_count:,} samples")
    
    return df
