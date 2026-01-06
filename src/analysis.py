"""
Analysis utilities for quantifying human-AI label disagreement.

This module computes metrics that reveal systematic failure modes in human labeling:
- Purity: What fraction of a cluster has the majority label?
- Ambiguity: How many "misclassified" samples exist? (size * (1 - purity))
- Entropy: How much label diversity exists within a cluster?

These metrics expose two failure modes:
1. Over-splitting (high entropy): One morphology fragmented into many labels
2. Over-compression (low purity): Many morphologies collapsed into one label
"""

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def compute_entropy(labels: pd.Series) -> float:
    """
    Compute Shannon entropy (base 2) of a label distribution.
    
    Higher entropy indicates more label diversity within a cluster,
    which can signal over-splitting (humans disagree about what to call it).
    
    Args:
        labels: Series of categorical labels
        
    Returns:
        Entropy in bits (0 = pure, higher = more diverse)
    """
    # Get probability distribution
    probs = labels.value_counts(normalize=True)
    
    # Remove zero probabilities to avoid log(0)
    probs = probs[probs > 0]
    
    if len(probs) <= 1:
        return 0.0
    
    # Shannon entropy: -sum(p * log2(p))
    return float(-np.sum(probs * np.log2(probs)))


def compute_cluster_stats(metadata: pd.DataFrame) -> pd.DataFrame:
    """
    Compute comprehensive statistics for each cluster.
    
    Metrics computed:
        - n: Number of samples in cluster
        - top_label: Most common label
        - top_label_count: Count of most common label
        - purity: Fraction with majority label (higher = more consistent)
        - ambiguity: n * (1 - purity), prioritizes large impure clusters
        - entropy: Label diversity in bits
        - n_labels: Number of distinct labels
    
    Args:
        metadata: DataFrame with 'cluster_id' and 'label' columns
        
    Returns:
        DataFrame indexed by cluster_id with computed metrics
    """
    # Exclude noise cluster
    df = metadata[metadata["cluster_id"] != -1].copy()
    
    if df.empty:
        print("[Analysis] Warning: No non-noise clusters found")
        return pd.DataFrame()
    
    print(f"[Analysis] Computing statistics for {df['cluster_id'].nunique()} clusters...")
    
    stats = []
    for cluster_id, group in df.groupby("cluster_id"):
        label_counts = group["label"].value_counts()
        top_label = label_counts.index[0]
        top_count = label_counts.iloc[0]
        n = len(group)
        purity = top_count / n
        
        stats.append({
            "cluster_id": int(cluster_id),
            "n": n,
            "top_label": top_label,
            "top_label_count": top_count,
            "purity": purity,
            "ambiguity": n * (1 - purity),
            "entropy": compute_entropy(group["label"]),
            "n_labels": group["label"].nunique()
        })
    
    result = pd.DataFrame(stats).set_index("cluster_id").sort_index()
    print(f"[Analysis] Statistics computed for {len(result)} clusters")
    
    return result


def rank_by_ambiguity(cluster_stats: pd.DataFrame) -> pd.DataFrame:
    """
    Rank clusters by ambiguity score (descending).
    
    Ambiguity = n * (1 - purity) highlights clusters that are:
    - Large AND impure (important to fix)
    - Indicative of systematic labeling failures
    
    Args:
        cluster_stats: DataFrame from compute_cluster_stats()
        
    Returns:
        Same DataFrame sorted by ambiguity (highest first)
    """
    return cluster_stats.sort_values("ambiguity", ascending=False)


def get_label_distribution(
    metadata: pd.DataFrame,
    cluster_id: int
) -> pd.Series:
    """
    Get the label distribution for a specific cluster.
    
    Args:
        metadata: DataFrame with 'cluster_id' and 'label' columns
        cluster_id: Which cluster to analyze
        
    Returns:
        Series of label counts
    """
    cluster_data = metadata[metadata["cluster_id"] == cluster_id]
    return cluster_data["label"].value_counts()


def identify_failure_modes(
    cluster_stats: pd.DataFrame,
    entropy_threshold: float = 2.0,
    purity_threshold: float = 0.5
) -> Dict[str, List[int]]:
    """
    Identify clusters exhibiting systematic failure modes.
    
    Failure Mode I (Over-splitting): High entropy indicates humans applied
    many different labels to morphologically similar glitches.
    
    Failure Mode II (Over-compression): Low purity indicates humans applied
    a single label to morphologically diverse glitches.
    
    Args:
        cluster_stats: DataFrame from compute_cluster_stats()
        entropy_threshold: Minimum entropy to flag as over-splitting
        purity_threshold: Maximum purity to flag as over-compression
        
    Returns:
        Dict with 'over_splitting' and 'over_compression' cluster lists
    """
    # Over-splitting: high label entropy (many labels for one morphology)
    over_splitting = cluster_stats[
        cluster_stats["entropy"] >= entropy_threshold
    ].index.tolist()
    
    # Over-compression: low purity (one label for many morphologies)
    over_compression = cluster_stats[
        cluster_stats["purity"] <= purity_threshold
    ].index.tolist()
    
    print(f"[Analysis] Found {len(over_splitting)} over-splitting clusters "
          f"(entropy >= {entropy_threshold})")
    print(f"[Analysis] Found {len(over_compression)} over-compression clusters "
          f"(purity <= {purity_threshold})")
    
    return {
        "over_splitting": over_splitting,
        "over_compression": over_compression
    }


def generate_summary_report(
    metadata: pd.DataFrame,
    cluster_stats: pd.DataFrame
) -> str:
    """
    Generate a text summary of the clustering analysis.
    
    Args:
        metadata: Full metadata DataFrame
        cluster_stats: DataFrame from compute_cluster_stats()
        
    Returns:
        Formatted summary string
    """
    total_samples = len(metadata)
    n_clusters = len(cluster_stats)
    n_noise = (metadata["cluster_id"] == -1).sum()
    
    # Get top ambiguous clusters
    top_ambiguous = rank_by_ambiguity(cluster_stats).head(5)
    
    lines = [
        "=" * 60,
        "GRAVITY SPY AUDIT SUMMARY",
        "=" * 60,
        f"Total samples:     {total_samples:,}",
        f"Clusters found:    {n_clusters}",
        f"Noise points:      {n_noise:,} ({100*n_noise/total_samples:.1f}%)",
        f"Unique labels:     {metadata['label'].nunique()}",
        "",
        "TOP 5 MOST AMBIGUOUS CLUSTERS:",
        "-" * 40,
    ]
    
    for cid, row in top_ambiguous.iterrows():
        lines.append(
            f"  Cluster {cid:3d}: n={int(row['n']):5d}, "
            f"purity={row['purity']:.2f}, "
            f"entropy={row['entropy']:.2f}, "
            f"top='{row['top_label']}'"
        )
    
    lines.append("=" * 60)
    
    return "\n".join(lines)
