# Gravity Spy Glitch Explorer  
*A visual and interactive exploration of LIGO glitch morphology using CNN embeddings, UMAP, and HDBSCAN.*

![UMAP Preview](figures/preview/umap_preview.png)

---

## 🚀 Overview

This project builds an **interactive, data-scientist–friendly visual explorer** for the Gravity Spy glitch dataset — the same dataset used by the **LIGO/Virgo/KAGRA collaboration** to classify non-astrophysical noise (“glitches”) in gravitational-wave detectors.

Using:

- **ResNet-18** (transfer learning) to embed 34,332 spectrograms
- **UMAP** to project them into a meaningful 2D morphology space  
- **HDBSCAN** to identify subclusters and outlier structures

This tool allows users to:

- Explore the structure of glitch families visually
- Hover over individual points to see real spectrogram thumbnails
- Inspect latent substructure within large categories
- Identify discrepancies between machine-defined clusters and human labels
- Build the foundation for advanced analysis (Phase B & C below)

This repository currently contains Phase A, the complete embedding + clustering + interactive visualization pipeline.

---

## 🔍 Live Interactive Dashboard

👉 **[Launch the Interactive UMAP Explorer](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)**

- Fast pan/zoom even with thousands of points  
- Hover over any point to view the actual glitch spectrogram 
- Color-coded HDBSCAN clusters 
- Subsampled (<5K points) for web performance
- Fully standalone (runs on GitHub Pages)

---

## 🧠 Methods Summary

### **1. CNN Embeddings (ResNet-18)**
- Spectrograms resized to 224×224  
- Converted to 3-channel grayscale  
- Passed through ImageNet-pretrained ResNet-18  
- Final FC layer replaced with `Identity()`  
- Output: **512-dim embedding per image**  
- Total embeddings: **34,332**

### **2. Dimensionality Reduction (UMAP)**
- UMAP (`n_neighbors=30`, `min_dist=0.1`)  
- Produces smooth, interpretable 2D manifold  
- Captures similarity of glitch morphology

### **3. Clustering (HDBSCAN)**
- Automatically identifies dense “islands”  
- Noise (cluster = -1) retained for future analysis  
- Many clusters show **high purity** relative to Gravity Spy labels

### **4. Interactive Visualization (Plotly)**
- Points are clickable/hoverable  
- Thumbnails encoded in base64  
- Cluster & label data embedded in hover tooltips  
- Exported to standalone HTML for GitHub Pages

---

## 🌌 Scientific Context

LIGO detectors are extraordinarily sensitive — enough to detect distortions in spacetime smaller than a proton.  
However, they are also sensitive to numerous instrumental or environmental “glitches.”  

This project uses deep learning + dimensional reduction to examine:

- How glitch types cluster morphologically  
- Whether new substructure exists within dominant categories  
- Where human labels and machine clusters disagree  
- What patterns may be candidates for follow-up during Phase B

---

## 📅 Roadmap

### **Phase A — Embedding & Visualization (✔ Complete)**  
- CNN embeddings  
- UMAP projection  
- HDBSCAN clustering  
- Interactive explorer  
- Cluster atlas

### **Phase B — Detector Coupling (Next)**  
- Use GWpy to load auxiliary channels  
- Correlate glitch families with instrument states  
- Example: Scattered light vs. ground motion

### **Phase C — Impact & Explainability**  
- Train interpretable models (Random Forest / XGBoost)  
- Use SHAP values to identify channels driving glitch production  
- Produce “Glitch Cost Ranking” dashboard

---
**MIT License — feel free to fork, modify, and build upon this project.**

**Acknowledgments:**

Gravity Spy (GWOSC + Zooniverse)

LIGO/Virgo/KAGRA Collaboration

PyTorch, UMAP-learn, HDBSCAN, Plotly

---

## 🛠 Installation (local)

Requires Python 3.10+.

```bash
pip install -r notebooks/requirements.txt

