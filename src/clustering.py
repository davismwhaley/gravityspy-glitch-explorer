"""
Clustering pipeline using UMAP and HDBSCAN.

This module implements the core unsupervised learning workflow:
1. UMAP for dimensionality reduction (preserving local structure)
2. HDBSCAN for density-based clustering (no need to specify k)
"""

from typing import Tuple

import numpy as np
import pandas as pd
import umap
import hdbscan

from .config import UMAPConfig, HDBSCANConfig


def compute_umap(
    embeddings: np.ndarray,
    config: UMAPConfig
) -> np.ndarray:
    """
    Compute 2D UMAP embedding for visualization and clustering.
    
    UMAP (Uniform Manifold Approximation and Projection) is used to project
    high-dimensional CNN embeddings into 2D while preserving local structure.
    We use cosine metric since CNN features are often better compared by angle.
    
    Args:
        embeddings: High-dimensional feature vectors (n_samples, n_features)
        config: UMAP hyperparameters
        
    Returns:
        2D coordinates (n_samples, 2)
    """
    print(f"[UMAP] Computing 2D embedding for {embeddings.shape[0]:,} samples...")
    print(f"[UMAP] Config: n_neighbors={config.n_neighbors}, "
          f"min_dist={config.min_dist}, metric={config.metric}")
    
    reducer = umap.UMAP(
        n_neighbors=config.n_neighbors,
        min_dist=config.min_dist,
        metric=config.metric,
        n_components=config.n_components,
        random_state=config.random_state,
        verbose=True
    )
    
    coords = reducer.fit_transform(embeddings)
    
    print(f"[UMAP] Complete. Coordinate ranges: "
          f"x=[{coords[:, 0].min():.2f}, {coords[:, 0].max():.2f}], "
          f"y=[{coords[:, 1].min():.2f}, {coords[:, 1].max():.2f}]")
    
    return coords


def compute_hdbscan(
    coords: np.ndarray,
    config: HDBSCANConfig
) -> np.ndarray:
    """
    Compute density-based clusters using HDBSCAN.
    
    HDBSCAN finds clusters of varying densities without requiring the number
    of clusters to be specified. Points that don't belong to any cluster are
    labeled as noise (-1).
    
    Args:
        coords: 2D coordinates from UMAP (n_samples, 2)
        config: HDBSCAN hyperparameters
        
    Returns:
        Cluster labels (n_samples,), with -1 indicating noise
    """
    print(f"[HDBSCAN] Clustering {coords.shape[0]:,} points...")
    print(f"[HDBSCAN] Config: min_cluster_size={config.min_cluster_size}, "
          f"metric={config.metric}")
    
    min_samples = config.min_samples or config.min_cluster_size
    
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=config.min_cluster_size,
        min_samples=min_samples,
        metric=config.metric,
        cluster_selection_method=config.cluster_selection_method
    )
    
    labels = clusterer.fit_predict(coords)
    
    # Report clustering results
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    noise_pct = 100 * n_noise / len(labels)
    
    print(f"[HDBSCAN] Found {n_clusters} clusters, {n_noise:,} noise points ({noise_pct:.1f}%)")
    
    return labels


def add_clustering_to_metadata(
    metadata: pd.DataFrame,
    embeddings: np.ndarray,
    umap_config: UMAPConfig,
    hdbscan_config: HDBSCANConfig
) -> pd.DataFrame:
    """
    Run full clustering pipeline and add results to metadata.
    
    This is the main entry point for clustering, adding these columns:
        - umap_x, umap_y: 2D UMAP coordinates
        - cluster_id: HDBSCAN cluster assignment (-1 = noise)
    
    Args:
        metadata: DataFrame with sample information
        embeddings: CNN embeddings aligned with metadata
        umap_config: UMAP hyperparameters
        hdbscan_config: HDBSCAN hyperparameters
        
    Returns:
        Metadata with clustering columns added
    """
    df = metadata.copy()
    
    # Step 1: UMAP
    coords = compute_umap(embeddings, umap_config)
    df["umap_x"] = coords[:, 0]
    df["umap_y"] = coords[:, 1]
    
    # Step 2: HDBSCAN
    labels = compute_hdbscan(coords, hdbscan_config)
    df["cluster_id"] = labels.astype(int)
    
    return df


def get_cluster_sizes(metadata: pd.DataFrame) -> pd.Series:
    """
    Get the size of each cluster (excluding noise).
    
    Args:
        metadata: DataFrame with 'cluster_id' column
        
    Returns:
        Series of cluster sizes indexed by cluster_id
    """
    sizes = metadata[metadata["cluster_id"] != -1]["cluster_id"].value_counts()
    return sizes.sort_index()
