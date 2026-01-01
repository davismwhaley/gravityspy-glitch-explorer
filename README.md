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
LIGO detectors are so sensitive that they can detect the collision of black holes billions of light-years away, but they also detect trucks driving by, wind, and electronic "glitches." This project applies **Computer Vision** and **Unsupervised Machine Learning** to categorize over 34,000 noise transients, creating a "topographical map" of detector interference to improve gravitational-wave search sensitivity.

---

## 🔍 [View the Live Interactive Dashboard](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)
*Note: This interactive UMAP lets you hover over data points to see specific spectrogram morphology associated with each cluster in real-time.* 

---

## 💡 Key Achievements (Phase A)
*   **Deep Feature Extraction:** Engineered a pipeline using a **Pre-trained ResNet-18 (Transfer Learning)** to convert raw spectrogram images into 512-dimensional feature vectors, capturing nuances human observers might miss.
*   **Manifold Learning:** Utilized **UMAP (Uniform Manifold Approximation and Projection)** to compress high-dimensional noise patterns into an interpretable 2D "Glitch Map," preserving both local and global data structures.
*   **Unsupervised Discovery:** Implemented **HDBSCAN** to automatically identify 50+ distinct glitch families. This revealed hidden substructures within known classes (like H1L1) that manual labeling often overlooks.
*   **Front-End Engineering:** Successfully processed and visualized **34,332 records**, optimizing the dashboard with Base64 image encoding for seamless performance on GitHub Pages.

---

## 🧠 Data Science Methodology

### 1. The Embedding Pipeline
Instead of relying on human-defined features (like duration or frequency), I used a **Convolutional Neural Network (CNN)** to "learn" the morphology. By stripping the final classification layer of a ResNet-18 model and using the 512-D identity output, I repurposed the model to act as a high-level visual descriptor for astrophysical noise.

### 2. Discovering the "Unknown Unknowns"
Traditional classification only finds what we tell it to look for. By using **HDBSCAN (Density-Based Clustering)**, this project identifies "Noise" (Cluster -1) and outliers. This helps LIGO researchers to identify **new instrumental faults** before the collaboration officially names them.

### 3. Human-Machine Disagreement
By overlaying human labels on machine-generated clusters, this tool highlights where citizen science labels (Gravity Spy) diverge from mathematical morphology. This serves as a powerful **Data Quality Assurance (QA)** tool for the LIGO/Virgo/KAGRA collaboration.

---

## 🛠 Technical Stack
*   **Deep Learning:** PyTorch (ResNet-18 feature extraction)
*   **Dimensionality Reduction:** UMAP (Cosine metric)
*   **Clustering:** HDBSCAN (Density-based)
*   **Data Engineering:** Pandas, NumPy
*   **Visualization:** Plotly (Interactive HTML), Matplotlib/Seaborn

---

## 🗺 Strategic Roadmap

### **Phase A: Morphology Discovery (Completed)** 
*   [x] 34k+ Image Embedding via Transfer Learning
*   [x] Interactive UMAP Explorer with Image Previews
*   [x] Cluster Purity & Metadata Analysis

### **Phase B: Detector Coupling (In Progress)** 
*   [ ] Correlation of glitch clusters with **LIGO Auxiliary Channels** (Seismic, Magnetic, Voltage) using `GWpy`.
*   [ ] Identifying predictive precursors in environmental sensors to forecast glitches.

### **Phase C: Impact & Explainability**
*   [ ] Quantifying "Glitch Cost" by measuring the dip in binary neutron star (BNS) inspiral range during high-activity periods.
*   [ ] Using **SHAP Values** to determine which specific sensors are the primary drivers of glitch production.

---

## 🛠 Installation & Local Development

1. **Clone the repo:**
   ```bash
   git clone https://github.com/davismwhaley/gravityspy-glitch-explorer.git

pip install -r notebooks/requirements.txt

---
## **Contact & Portfolio**
Davis Whaley

davismwhaley@gmail.com

https://github.com/davismwhaley/gravityspy-glitch-explorer/
