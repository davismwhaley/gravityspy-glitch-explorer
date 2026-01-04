## 🚀 Gravity Spy Glitch Explorer  
**Auditing Failure Modes in Human-in-the-Loop Glitch Taxonomies Using Unsupervised Learning**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Deep Learning](https://img.shields.io/badge/Framework-PyTorch-EE4C2C.svg)](https://pytorch.org/)
[![Interactive](https://img.shields.io/badge/Dashboard-Plotly-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository documents a research-grade audit of human-labeled glitch taxonomies in LIGO’s Gravity Spy dataset using CNN embeddings, manifold learning, and density-based clustering.

Rather than treating human labels as ground truth, this project asks:
**Where do human taxonomies align with learned morphology — and where do they systematically fail?**

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

## **Explore the UMAP Morphology Map of Gravity Spy Glitches**

Click below to interactively inspect individual spectrograms and cluster assignments in real-time.

[`Global UMAP Morphology Map`](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/umap_interactive_sample.html)

![](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/umap_by_label2.jpg)

---

## **Core Scientific Result: Two Taxonomy Failure Modes**

A global audit of 34,332 spectrograms reveals two opposite and systematic failure modes in human labeling:

### **Failure Mode I — Over-Splitting (Cluster 33)**
*One morphology → Many labels.*

In Cluster 33, a single coherent morphology is fragmented across many categories. Labels such as *Violin_Mode*, *Power_Line*, *Low_Frequency_Lines*, and *1080Lines* are applied to nearly indistinguishable narrow-band line artifacts.

*   **Metric:** High Label Entropy ($H = 2.82$) | Low Cluster Purity (~0.22).
*   **Insight:** Humans subdivided a single physical phenomenon into multiple arbitrary categories.

➡️ **Humans subdivided one physical phenomenon into many categories.**

[`Cluster 33 contact sheet (over-splitting across labels`](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/cluster33_contact_sheet_top6x5.png)	

---

### **Failure Mode II — Over-Compression (Cluster 41)**
*Many morphologies → One label.*

Within Cluster 41, a graded family of morphologies is collapsed into one dominant label. When ordered by intensity, the morphology changes monotonically without discrete boundaries, yet humans labeled the entire continuum as a "Blip."

*   **Metric:** plurality label ("Blip") masks significant structured variation ($H = 2.26$).
*   **Insight:** Humans collapsed a complex continuum into a single catch-all label.

[`Cluster 41 ordered strip by intensity (over-compression)`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/cluster41_ordered_by_intensity_strip.png)

---

_The results are fully explained in_ [`results.md`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/results.md)

---

**Why This Matters**

These results show that **label errors are structured, not random**. Unsupervised learning exposes where human intuition breaks down — in _both_ directions. The broader takeaway is that unsupervised learning can serve as a data governance and quality-assurance tool — helping improve training data before building supervised systems — and the framework generalizes to any large human-labeled scientific dataset.”

This has implications for:

- Training data quality
- Automated veto systems
- Scientific interpretability
- Governance of citizen-science pipelines

---
## **Featured Case Study (Early Phase): Cluster 16 Drift-Line Manifold**

Before the global audit, **Cluster 16** provided the initial motivation for this work.

Cluster 16 forms a 1-D drift manifold where glitch morphology evolves smoothly across frequency regimes, yet human labels disagree nearly **30% of the time**.

![Cluster 16](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/umap_cluster16_segments2.png)

This case study demonstrated:

- Morphological continuity
- Segment-dependent human error rates
- A principled relabeling strategy

📁 **Cluster 16 Files:**

- 📝 **Cluster 16 report:**  
  [`report.md`](findings/cluster_16_deep_dive/report.md)

- 🖼 **Atlas:**  
  [`atlas_3row.png`](findings/cluster_16_deep_dive/atlas_3row.png)

- 📊 **Correction Table:**  
  [`correction_table.csv`](findings/cluster_16_deep_dive/correction_table.csv)

---

## **Figure Index (Evidence Map)**
**Figure**	**Description**

Fig. 1	[`Global UMAP embedding of Gravity Spy spectrograms`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/umap_by_label2.jpg)

Fig. 2	[`Ambiguity-ranked cluster table (purity × size)`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/fig2_ambiguity_ranked_clusters_top15.png)

Fig. 3 [`Cluster 33 contact sheet (over-splitting across labels`](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/cluster33_contact_sheet_top6x5.png)	

Fig. 4	[`Cluster 41 ordered strip by intensity (over-compression)`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/cluster41_ordered_by_intensity_strip.png) 

Fig. 5	[`Entropy comparison between Cluster 33 and 41`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/fig5_label_entropy_cluster33_vs_cluster41.png)

All figures are stored under /findings/ with reproducible notebooks.

---

## **Scope & Scalability**

This project does not currently claim causal mechanisms for individual glitches. It is a **Diagnostic Tool** for data quality. 

Scalability: Although demonstrated on LIGO data, this audit framework applies to any scientific dataset labeled by humans at scale (e.g., medical imaging, remote sensing, microscopy), where human taxonomies may struggle to capture the continuous nature of physical phenomena. 

---

## 🛠 Technical Stack & Methodology

### **Research Pipeline**
1.  **Feature Extraction:** ResNet-18 (Transfer Learning) used to generate 512-D embeddings from spectrograms.
2.  **Manifold Learning:** UMAP (Cosine metric) to reveal low-dimensional morphological structures.
3.  **Unsupervised Clustering:** HDBSCAN to identify density-based clusters without assuming a cluster count.
4.  **Audit Metrics:** Developed **Cluster Purity**, **Ambiguity Scores**, and **Label Entropy** to quantify human-AI disagreement.

### **The Stack**
*   **Core:** PyTorch, Scikit-Learn, UMAP-learn, HDBSCAN
*   **Data Engineering:** Pandas, NumPy, GWpy
*   **Visualization:** Plotly (Interactive), Matplotlib, Seaborn

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
