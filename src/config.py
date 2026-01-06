"""
Configuration settings for the Gravity Spy Glitch Explorer pipeline.

This module defines all hyperparameters and paths used throughout the pipeline,
making experiments reproducible and parameters easy to tune.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class PathConfig:
    """File and directory paths for the pipeline."""
    
    # Input paths (relative to repo root)
    embeddings_file: str = "data/gravityspy_processed/embeddings.npy"
    metadata_file: str = "data/gravityspy_processed/embeddings_metadata.csv"
    
    # Output directories
    output_dir: str = "findings/outputs"
    figures_dir: str = "findings/figures"
    
    def resolve(self, repo_root: Path) -> "PathConfig":
        """Convert relative paths to absolute paths."""
        self.embeddings_file = str((repo_root / self.embeddings_file).resolve())
        self.metadata_file = str((repo_root / self.metadata_file).resolve())
        self.output_dir = str((repo_root / self.output_dir).resolve())
        self.figures_dir = str((repo_root / self.figures_dir).resolve())
        return self


@dataclass
class UMAPConfig:
    """UMAP hyperparameters for manifold learning."""
    
    n_neighbors: int = 30
    min_dist: float = 0.1
    metric: str = "cosine"
    n_components: int = 2
    random_state: int = 42


@dataclass
class HDBSCANConfig:
    """HDBSCAN hyperparameters for density-based clustering."""
    
    min_cluster_size: int = 50
    min_samples: Optional[int] = None  # Defaults to min_cluster_size if None
    metric: str = "euclidean"
    cluster_selection_method: str = "eom"  # 'eom' or 'leaf'


@dataclass
class VisualizationConfig:
    """Settings for figure generation."""
    
    # Contact sheet settings
    top_k_labels: int = 6
    samples_per_label: int = 5
    
    # UMAP scatter settings
    scatter_sample_size: int = 12000
    point_size: int = 6
    figure_dpi: int = 200
    
    # Intensity strip settings
    strip_max_panels: int = 12
    
    # Interactive dashboard settings
    dashboard_sample_size: int = 5000
    hover_image_size: int = 220


@dataclass 
class PipelineConfig:
    """Master configuration combining all settings."""
    
    paths: PathConfig = field(default_factory=PathConfig)
    umap: UMAPConfig = field(default_factory=UMAPConfig)
    hdbscan: HDBSCANConfig = field(default_factory=HDBSCANConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    
    # Pipeline behavior
    random_seed: int = 42
    recompute_umap: bool = False
    recompute_clusters: bool = False
    
    # Deep-dive clusters (discovered as most ambiguous)
    deep_dive_clusters: List[int] = field(default_factory=lambda: [33, 41])
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.umap.n_components != 2:
            raise ValueError("UMAP n_components must be 2 for visualization")
        if self.hdbscan.min_cluster_size < 2:
            raise ValueError("HDBSCAN min_cluster_size must be >= 2")


def get_default_config() -> PipelineConfig:
    """Return the default pipeline configuration."""
    return PipelineConfig()
