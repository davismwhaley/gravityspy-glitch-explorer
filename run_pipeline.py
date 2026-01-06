#!/usr/bin/env python3
"""
Gravity Spy Glitch Explorer
============================

A research-grade audit framework for detecting systematic failure modes
in human-labeled glitch taxonomies using unsupervised learning.

This script implements the full pipeline:
1. Load pre-computed CNN embeddings (ResNet-18)
2. Fix labels by parsing from folder structure
3. Compute UMAP embedding for visualization
4. Run HDBSCAN clustering
5. Compute audit metrics (purity, ambiguity, entropy)
6. Generate figures for deep-dive clusters

Usage:
    python run_pipeline.py
    python run_pipeline.py --repo_root /path/to/repo
    python run_pipeline.py --deep_dive_clusters 33 41 16

Author: Davis Whaley
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import PipelineConfig, PathConfig, UMAPConfig, HDBSCANConfig
from src.data_loader import load_data
from src.preprocessing import fix_metadata_labels
from src.clustering import add_clustering_to_metadata, get_cluster_sizes
from src.analysis import (
    compute_cluster_stats,
    rank_by_ambiguity,
    identify_failure_modes,
    generate_summary_report
)
from src.visualization import (
    plot_umap_scatter,
    plot_contact_sheet,
    plot_intensity_strip,
    create_interactive_dashboard,
    ensure_dir
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Gravity Spy Glitch Explorer - Audit Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_pipeline.py
    python run_pipeline.py --repo_root ~/projects/gravityspy
    python run_pipeline.py --deep_dive_clusters 33 41
        """
    )
    
    parser.add_argument(
        "--repo_root", type=str, default=".",
        help="Path to repository root (default: current directory)"
    )
    
    parser.add_argument(
        "--embeddings", type=str,
        default="data/gravityspy_processed/embeddings.npy",
        help="Path to embeddings file (relative to repo_root)"
    )
    
    parser.add_argument(
        "--metadata", type=str,
        default="data/gravityspy_processed/embeddings_metadata.csv",
        help="Path to metadata CSV (relative to repo_root)"
    )
    
    parser.add_argument(
        "--output_dir", type=str,
        default="findings",
        help="Output directory for results (relative to repo_root)"
    )
    
    parser.add_argument(
        "--deep_dive_clusters", type=int, nargs="+",
        default=[33, 41],
        help="Cluster IDs to generate deep-dive figures for"
    )
    
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--skip_interactive", action="store_true",
        help="Skip generating interactive Plotly dashboard"
    )
    
    return parser.parse_args()


def run_pipeline(
    repo_root: Path,
    embeddings_path: Path,
    metadata_path: Path,
    output_dir: Path,
    deep_dive_clusters: List[int],
    seed: int = 42,
    skip_interactive: bool = False
) -> None:
    """
    Execute the full audit pipeline.
    
    Args:
        repo_root: Repository root directory
        embeddings_path: Path to embeddings .npy file
        metadata_path: Path to metadata CSV
        output_dir: Where to save results
        deep_dive_clusters: Which clusters to analyze in detail
        seed: Random seed for reproducibility
        skip_interactive: Whether to skip Plotly dashboard
    """
    print("=" * 70)
    print("GRAVITY SPY GLITCH EXPLORER")
    print("Auditing Human-AI Disagreement in Glitch Taxonomies")
    print("=" * 70)
    print(f"\nRepository root: {repo_root}")
    print(f"Embeddings:      {embeddings_path}")
    print(f"Metadata:        {metadata_path}")
    print(f"Output:          {output_dir}")
    print(f"Seed:            {seed}")
    print()
    
    # Create output directories
    figures_dir = ensure_dir(output_dir / "figures")
    outputs_dir = ensure_dir(output_dir / "outputs")
    
    # =========================================================================
    # STEP 1: Load Data
    # =========================================================================
    print("-" * 70)
    print("STEP 1: Loading Data")
    print("-" * 70)
    
    embeddings, metadata = load_data(
        str(embeddings_path),
        str(metadata_path)
    )
    
    # =========================================================================
    # STEP 2: Preprocess (Fix Labels)
    # =========================================================================
    print("\n" + "-" * 70)
    print("STEP 2: Preprocessing")
    print("-" * 70)
    
    metadata = fix_metadata_labels(metadata)
    
    # =========================================================================
    # STEP 3: Clustering (UMAP + HDBSCAN)
    # =========================================================================
    print("\n" + "-" * 70)
    print("STEP 3: Clustering")
    print("-" * 70)
    
    umap_config = UMAPConfig(random_state=seed)
    hdbscan_config = HDBSCANConfig()
    
    metadata = add_clustering_to_metadata(
        metadata, embeddings, umap_config, hdbscan_config
    )
    
    # =========================================================================
    # STEP 4: Analysis
    # =========================================================================
    print("\n" + "-" * 70)
    print("STEP 4: Analysis")
    print("-" * 70)
    
    cluster_stats = compute_cluster_stats(metadata)
    ambiguity_ranked = rank_by_ambiguity(cluster_stats)
    failure_modes = identify_failure_modes(cluster_stats)
    
    # Print summary
    summary = generate_summary_report(metadata, cluster_stats)
    print("\n" + summary)
    
    # =========================================================================
    # STEP 5: Save Results
    # =========================================================================
    print("\n" + "-" * 70)
    print("STEP 5: Saving Results")
    print("-" * 70)
    
    # Save metadata with clustering
    meta_out = outputs_dir / "metadata_clustered.csv"
    metadata.to_csv(meta_out, index=False)
    print(f"[Save] {meta_out}")
    
    # Save cluster statistics
    stats_out = outputs_dir / "cluster_stats.csv"
    cluster_stats.to_csv(stats_out)
    print(f"[Save] {stats_out}")
    
    # Save ambiguity ranking
    ambig_out = outputs_dir / "ambiguity_ranked.csv"
    ambiguity_ranked.to_csv(ambig_out)
    print(f"[Save] {ambig_out}")
    
    # =========================================================================
    # STEP 6: Generate Figures
    # =========================================================================
    print("\n" + "-" * 70)
    print("STEP 6: Generating Figures")
    print("-" * 70)
    
    # Global UMAP by cluster
    plot_umap_scatter(
        metadata,
        str(figures_dir / "umap_by_cluster.png"),
        color_by="cluster_id",
        seed=seed
    )
    
    # Global UMAP by label
    plot_umap_scatter(
        metadata,
        str(figures_dir / "umap_by_label.png"),
        color_by="label",
        seed=seed
    )
    
    # Deep-dive figures for specified clusters
    available_clusters = set(metadata["cluster_id"].unique()) - {-1}
    
    for cluster_id in deep_dive_clusters:
        if cluster_id not in available_clusters:
            print(f"[Viz] Warning: Cluster {cluster_id} not found, skipping")
            continue
        
        cluster_dir = ensure_dir(output_dir / f"cluster_{cluster_id}_deep_dive")
        
        # Contact sheet
        plot_contact_sheet(
            metadata,
            cluster_id,
            str(cluster_dir / f"cluster{cluster_id}_contact_sheet.png"),
            seed=seed
        )
        
        # Intensity strip
        plot_intensity_strip(
            metadata,
            cluster_id,
            str(cluster_dir / f"cluster{cluster_id}_intensity_strip.png"),
            seed=seed
        )
    
    # Interactive dashboard
    if not skip_interactive:
        create_interactive_dashboard(
            metadata,
            str(figures_dir / "umap_interactive.html"),
            seed=seed
        )
    
    # =========================================================================
    # Done!
    # =========================================================================
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to: {output_dir}")
    print("\nKey outputs:")
    print(f"  - {outputs_dir / 'metadata_clustered.csv'}")
    print(f"  - {outputs_dir / 'cluster_stats.csv'}")
    print(f"  - {figures_dir / 'umap_by_cluster.png'}")
    print(f"  - {figures_dir / 'umap_interactive.html'}")
    
    for cluster_id in deep_dive_clusters:
        if cluster_id in available_clusters:
            print(f"  - {output_dir / f'cluster_{cluster_id}_deep_dive/'}")


def main():
    """Main entry point."""
    args = parse_args()
    
    # Resolve paths
    repo_root = Path(args.repo_root).resolve()
    embeddings_path = repo_root / args.embeddings
    metadata_path = repo_root / args.metadata
    output_dir = repo_root / args.output_dir
    
    try:
        run_pipeline(
            repo_root=repo_root,
            embeddings_path=embeddings_path,
            metadata_path=metadata_path,
            output_dir=output_dir,
            deep_dive_clusters=args.deep_dive_clusters,
            seed=args.seed,
            skip_interactive=args.skip_interactive
        )
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure you have run the feature extraction pipeline first.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
