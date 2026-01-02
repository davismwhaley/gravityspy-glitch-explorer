## 🚀 Gravity Spy Glitch Explorer  
**Auditing Failure Modes in Human-in-the-Loop Glitch Taxonomies Using Unsupervised Learning**
This repository documents a research-grade audit of human-labeled glitch taxonomies in LIGO’s Gravity Spy dataset using CNN embeddings, manifold learning, and density-based clustering.

Rather than treating human labels as ground truth, this project asks:
**Where do human taxonomies align with learned morphology — and where do they systematically fail?**

The result is a reproducible framework for data quality assurance, taxonomy validation, and interpretability in scientific ML pipelines.

---
## **Project Overview**

**How do we find a needle in a haystack when the haystack is vibrating?** 
LIGO detectors are so sensitive that they can detect the collision of black holes billions of light-years away, but they also detect trucks driving by, wind, and electronic "glitches." This project applies **Computer Vision** and **Unsupervised Machine Learning** to categorize over 34,000 noise transients, creating a "topographical map" of detector interference to improve gravitational-wave search sensitivity. The Gravity Spy dataset combines citizen science and expert labeling to classify instrumental glitches in LIGO spectrograms. While highly valuable, such hybrid labeling systems are susceptible to inconsistency, drift, and structural bias.

This project applies:

- **CNN embeddings** (ResNet-18)
- **UMAP** for manifold learning
- **HDBSCAN** for unsupervised clustering

to audit where human labels diverge from learned morphology, and why.

---

## **Core Scientific Result: Two Taxonomy Failure Modes**

A global audit of 34,332 spectrograms reveals two opposite and systematic failure modes in human labeling:

**Failure Mode I — Over-Splitting (Cluster 33)**

_A single coherent morphology fragmented across many labels._

Human labels such as _Violin_Mode_, _Power_Line_, _Low_Frequency_Lines_, and _1080Lines_ are applied to nearly indistinguishable narrow-band line artifacts.

- High label entropy (H = 2.82)
- Low cluster purity (~0.22)
- Visual contact sheets show near-identical morphology across labels

➡️ **Humans subdivided one physical phenomenon into many categories.**

---

**Failure Mode II — Over-Compression (Cluster 41)**
_A graded family of morphologies collapsed into one dominant label._

Within Cluster 41, a central “blip-like” impulse anchors a smooth continuum of increasing bandwidth and temporal smearing. When ordered by total spectrogram intensity, morphology changes monotonically without discrete boundaries.

- Blip is the plurality, not the majority
- Label entropy remains high (H = 2.26)
- Ordered visual strips reveal structured variation, not noise

➡️ Humans collapsed a continuum into a single catch-all label (“Blip”).

---

**Why This Matters**

These results show that **label errors are structured, not random**.
Unsupervised learning exposes where human intuition breaks down — in _both_ directions.

This has implications for:

- Training data quality
- Automated veto systems
- Scientific interpretability
- Governance of citizen-science pipelines

---

## 🧠 Data Science Methodology

## **Figure Index (Evidence Map)**
**Figure**	**Description**

Fig. 1	Global UMAP embedding of Gravity Spy spectrograms

Fig. 2	Ambiguity-ranked cluster table (purity × size)

Fig. 3	Cluster 33 contact sheet (over-splitting across labels)

Fig. 4	Cluster 41 ordered strip by intensity (over-compression)

Fig. 5	Entropy comparison between Cluster 33 and 41

All figures are stored under /findings/ with reproducible notebooks.

---
## **Featured Case Study (Early Phase): Cluster 16 Drift-Line Manifold**

Before the global audit, **Cluster 16** provided the initial motivation for this work.

Cluster 16 forms a 1-D drift manifold where glitch morphology evolves smoothly across frequency regimes, yet human labels disagree nearly **30% of the time**.

This case study demonstrated:

- Morphological continuity
- Segment-dependent human error rates
- A principled relabeling strategy

📁 **Cluster 16 Files:**

- 🖼 **Atlas:**  
  [`atlas_3row.png`](findings/cluster_16_deep_dive/atlas_3row.png)

- 📊 **Correction Table:**  
  [`correction_table.csv`](findings/cluster_16_deep_dive/correction_table.csv)

- 📝 **Case Study Summary:**  
  [`report.md`](findings/cluster_16_deep_dive/report.md)

---

## 🛠 Technical Stack
*   **Deep Learning:** PyTorch (ResNet-18 feature extraction)
*   **Dimensionality Reduction:** UMAP (Cosine metric)
*   **Clustering:** HDBSCAN (Density-based)
*   **Data Engineering:** Pandas, NumPy
*   **Visualization:** Plotly (Interactive HTML), Matplotlib/Seaborn

---

## **Methods (Brief)**

- **Embedding:** ResNet-18 (transfer learning)
- **Manifold Learning:** UMAP (cosine metric)
- **Clustering:** HDBSCAN
- **Diagnostics:** Cluster purity, ambiguity score, label entropy
- **Visualization:** Matplotlib, Plotly (interactive dashboard)

---

## **Interactive Explorer**
(https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)

## 🗺 Strategic Roadmap

### **Phase A: Morphology Discovery (Completed)** 
*   [x] 34k+ Image Embedding via Transfer Learning
*   [x] Interactive UMAP Explorer with Image Previews
*   [x] Cluster Purity & Metadata Analysis

### Phase B: Human-AI Discrepancy Audit (Current Sprint)
*   [x] Tuning HDBSCAN parameters to identify "Impure" clusters (where AI and human labels diverge).
*   [x] Identifying "None of the Above" and "Noisy" sub-clusters to discover potential new glitch morphologies.
*   [x] Auditing human label consistency: Identifying where the AI groups different labels together based on superior morphological similarity.

![UMAP Preview](figures/preview/umap_preview.png)

## 🔍 [View the Live Interactive Dashboard](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)
*Note: This interactive UMAP lets you hover over data points to see specific spectrogram morphology associated with each cluster in real-time.* 

### 📂 Cluster 16 Files


*spectrogram morphology map showing clusters of glitches*


[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Deep Learning](https://img.shields.io/badge/Framework-PyTorch-EE4C2C.svg)](https://pytorch.org/)
[![Interactive](https://img.shields.io/badge/Dashboard-Plotly-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🛠 Installation & Local Development

1. **Clone the repo:**

   ```bash
   git clone https://github.com/davismwhaley/gravityspy-glitch-explorer.git
   cd gravityspy-glitch-explorer
   pip install -r notebooks/requirements.txt

---
## **Contact**
Davis Whaley

davismwhaley@gmail.com

https://github.com/davismwhaley/gravityspy-glitch-explorer/
