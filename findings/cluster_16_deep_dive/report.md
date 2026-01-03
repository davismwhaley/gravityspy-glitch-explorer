# 🌌 Case Study: Cluster 16 Deep-Dive
**Morphological Evolution Along a 1-D Drift-Line Manifold**

**Executive Summary:** Cluster 16 exposes the limits of discrete citizen-science labeling. By mapping this cluster’s 1-D manifold, I identified a **28.5% human label error rate** across 302 samples and developed an automated, physics-based relabeling strategy.

---

## 🔍 The Discovery

Cluster 16 emerged as the "smoking gun" of the Human-AI Discrepancy Audit. While most glitches fall into discrete buckets, Cluster 16 forms a **continuous 1-D manifold** (a latent continuum) in UMAP space. 

Along this single geometric curve, the glitch morphology evolves smoothly from **high-frequency whistles** to **broadband low-frequency bursts.** This proves that these are not separate "types" of glitches, but different manifestations of the same underlying physical process—a fact that human labelers missed 28.5% of the time.

![Cluster 16](umap_cluster16_segments2.png)

---

## 🧬 The 3-Segment Morphological Drift

By segmenting the UMAP manifold, we can track exactly where human intuition fails.

### **1. Lower Segment: High-Frequency "Whistles"**
*   **Morphology:** Sharp, vertical "V" or "W" signatures.
*   **Human Status:** Generally accurate, but contaminated by "Power_Line" and "Air_Compressor" mislabels.

### **2. Middle Segment: Narrow Spectral Lines**
*   **Morphology:** Transition state; thin horizontal stability.
*   **Human Status:** **Maximum Ambiguity.** This is where labeling consistency collapses as users struggle to distinguish between "Line" and "Whistle."

### **3. Upper Segment: Broadband Bursts**
*   **Morphology:** Morphological expansion into wide energy bands.
*   **Human Status:** High accuracy; the signal becomes unambiguous even for non-experts.

---

## 📊 Quantifying the "Human Intuition Gap"

The following table proves that human error is not distributed randomly—it peaks at the **morphological transition points.**

| Manifold Segment | Total Samples | Consistent Labels | Inconsistent Labels | **Error Rate** |
| :--- | :--- | :--- | :--- | :--- |
| **Lower** (Whistle end) | 100 | 71 | 29 | **29.0%** |
| **Middle** (Transition) | 100 | 51 | 49 | **49.0%** |
| **Upper** (Burst end) | 102 | 94 | 8 | **7.8%** |

**The "Transition Paradox":** In the center of the manifold, human labelers are essentially flipping a coin ($49\%$ error), whereas the CNN-UMAP pipeline identifies a clear, smooth progression.

---

## 🏷 Principled Relabeling Strategy

To correct the training data for future supervised models, I implemented a **Segment-Based Correction Rule**. This replaces inconsistent "catch-all" labels with labels derived from the manifold position:

1.  **Lower Segment** $\rightarrow$ `Whistle`
2.  **Middle Segment** $\rightarrow$ `Low_Frequency_Lines`
3.  **Upper Segment** $\rightarrow$ Retain `Low_Frequency_Burst` / `Light_Modulation`

**Result:** A 100% consistent dataset that preserves the physical evolution of the glitch family.

[`correction_table.csv`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/correction_table.csv)

---
## 🖼 Visual Evidence: The 3-Row Atlas

The [`atlas_3row.png`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/atlas_3row.png) provides the visual proof of this audit. 
*   **Row 1:** Demonstrates the "Whistle" morphology. Note how many subplots are titled "No_Glitch" or "Air_Compressor" despite the clear visual signature.
*   **Row 2:** Shows the "Transition" state where the error rate hits 49%.
*   **Row 3:** Shows the final "Burst" morphology.

---

## 🧭 Impact & Conclusion

Cluster 16 serves as a powerful proof-of-concept for **Machine-Guided Data Governance.** It demonstrates that:
1.  **Unsupervised discovery** can find physical families that are not yet in the official taxonomy.
2.  **Manifold geometry** can be used to "auto-correct" human error in large-scale citizen science projects.
3.  **Data Quality** is not just about removing noise; it’s about identifying where our labeling systems are too rigid for the fluid nature of physical data.

---

## 📁 Files Included in This Folder

- [`atlas_3row.png`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/atlas_3row.png) — Visual atlas (lower/middle/upper segments)  
- [`correction_table.csv`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/correction_table.csv) — Proposed relabeling for all 302 samples  
- [`metadata.json`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/findings/cluster_16_deep_dive/metadata.json) — Summary statistics for Cluster 16

---

## ✉️ Contact

**Contact:** Davis Whaley | [davismwhaley@gmail.com](mailto:davismwhaley@gmail.com)


