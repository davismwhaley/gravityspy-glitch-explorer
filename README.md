# 🚀 Gravity Spy Glitch Explorer  
*LIGO Gravity Spy Glitch Explorer: Unsupervised Morphology Mapping*

![UMAP Preview](figures/preview/umap_preview.png)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Deep Learning](https://img.shields.io/badge/Framework-PyTorch-EE4C2C.svg)](https://pytorch.org/)
[![Interactive](https://img.shields.io/badge/Dashboard-Plotly-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

### 🌟 Project Vision
**How do we find a needle in a haystack when the haystack is vibrating?** 
LIGO detectors are so sensitive they can detect the collision of black holes billions of light-years away—but they also detect trucks driving by, wind, and electronic "glitches." This project applies **Computer Vision** and **Unsupervised Machine Learning** to categorize over 34,000 noise transients, creating a "topographical map" of detector interference to improve gravitational-wave search sensitivity.

---

## 🔍 Live Interactive Dashboard

👉 **[Launch the Interactive UMAP Explorer](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)**

Features:

- Fast pan/zoom  
- Hover to see glitch spectrogram thumbnails  
- Color-coded HDBSCAN clusters  
- Subsampled (< 5K points) for reliable performance  
- Fully self-contained HTML, hosted on GitHub Pages  

---

## 🧠 Technical Overview

### **1. CNN Embeddings (ResNet-18)**
- Spectrograms resized to **224×224**
- Converted to **3-channel grayscale**
- Passed through ImageNet-pretrained **ResNet-18**
- Final FC replaced with `Identity()`
- Output: **512-dimensional embedding**
- Total images processed: **34,332**

### **2. Dimensionality Reduction (UMAP)**
- `n_neighbors=30`, `min_dist=0.1`, `metric="cosine"`
- Produces a smooth, interpretable 2D manifold UMAP from a 512-D space.
- Captures subtle differences in glitch morphology

### **3. Clustering (HDBSCAN)**
- Density-based clustering to identify stable glitch families
- `cluster = -1` retained as a noise group
- Many clusters exhibit high purity relative to Gravity Spy labels
- Useful for discovering latent substructure inside classes like H1L1

### **4. Interactive Visualization (Plotly)**
- Thumbnails embedded as Base64 images
- Hover tooltips display **cluster**, **label**, and **file path**
- Exported to standalone HTML for GitHub Pages hosting

---

## 🌌 Scientific Context

LIGO’s detectors are sensitive enough to detect spacetime distortions smaller than a proton — but this sensitivity also makes them vulnerable to instrumental or environmental “glitches.”

This explorer helps investigate:

- How glitch types organize morphologically, categorizing them by blip glitches, whistles, scattered light, and coincidence class.
- Whether subclasses or subclusters exist within known types
- Where human labels and machine-learned clusters disagree
- Which regions of the embedding deserve deeper investigation (Phase B)


Different clusters appear up/down/left/right because they have different spectrogram shapes. They may share internal structure, or vary continuously along one or two morphological dimensions. This style of exploration mirrors **detector-characterization research** done inside the LIGO Scientific Collaboration.

---

## 🗺 Roadmap

### **✔ Phase A — Embedding & Visualization (Completed)**
- CNN embeddings  
- UMAP projection  
- HDBSCAN clustering  
- Interactive explorer  
- Cluster atlas  

---

### **➡ Phase B — Detector Coupling (Next)**
Use **GWpy** to load auxiliary channels and correlate them with glitch clusters.

Example goals:

- Does ground motion predict scattered-light glitches?  
- Which auxiliary channels “light up” before specific glitch families?  
- Can the model identify precursors seconds before a glitch?

---

### **➡ Phase C — Impact & Explainability**
- Train interpretable models (Random Forest, XGBoost)  
- Use **SHAP values** to quantify which sensors drive glitch production  
- Rank glitch families by their impact on detector sensitivity  
- Build a “Glitch Cost Ranking” dashboard  

---

## 🛠 Installation (Local Development)

Requires **Python 3.10+**

```bash
pip install -r notebooks/requirements.txt


