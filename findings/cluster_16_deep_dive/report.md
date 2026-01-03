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

`correction_table.csv`

---
This visualization shows the 2-D UMAP projection of Cluster 16. Even though the points lie almost perfectly along a 1-D curve, the human labels form inconsistent blocks of color:

- Light blue = Whistles (lower segment)
- Mixed pink/red = Mislabels (middle segment)
- Green/red = Narrow-line vs. Power Line (upper segment)

This mismatch between manifold geometry and label distribution is the core motivation for the audit.

## 🧬 Morphological Evolution: A 3-Segment Drift Line

Visual inspection of the cluster shows a **smooth drift** along the manifold:

1. **Lower Segment — High-Frequency Whistles**  
   - Sharp, vertical, whistle-like signatures  
   - True labels often (correctly) “Whistle,” but also mislabeled as:  
     - *Air_Compressor*  
     - *No_Glitch*  
     - *Power_Line*  
     - *1080Lines*  

2. **Middle Segment — Narrow Spectral Lines**  
   - Thin, stable horizontal lines  
   - A mixture of “Low_Frequency_Lines,” “Power_Line,” and “No_Glitch”  
   - Nearly symmetrical along the UMAP drift

3. **Upper Segment — Broadband Bursts**  
   - Wide energy bands at low frequency  
   - Consistency sharply improves here  
   - Almost all samples match  
     - *Low_Frequency_Burst*  
     - *Light_Modulation*  
     - *Low_Frequency_Lines*  

The atlas image (`atlas_3row.png`) visually demonstrates this continuous evolution.

---

## 🔎 Human–AI Label Discrepancy

Cluster 16 exposes systematic patterns of human error:

### **1. Segment-Level Error Rates**
| Segment | Total | Core (Consistent) | Inconsistent | Error Rate |
|--------|-------|------------------|--------------|------------|
| Lower  | 100   | 71               | 29           | **29%** |
| Middle | 100   | 51               | 49           | **49%** |
| Upper  | 102   | 94               | 8            | **7.8%** |

**Insight:**  
The center of the manifold is the least intuitive for humans and contains the highest mistake rate.

---

### **2. Label-Level Error Rates**
Classes with *100% error* inside this cluster:

- Air_Compressor  
- Helix  
- Power_Line  
- None_of_the_Above  
- No_Glitch  
- Scratchy  
- Violin_Mode  
- Scattered_Light  
- 1080Lines  

These labels appear in positions where the morphology is unambiguously “Whistle-like” or “Narrow-line-like,” revealing inconsistent human labeling.

In contrast, the following labels were **100% consistent**:

- Light_Modulation  
- Low_Frequency_Lines  
- Low_Frequency_Burst  
- Wandering_Line  
- Whistle  

---

## 🏷 Segment-Based Relabeling Strategy

To correct noisy human labels while preserving physical interpretability, we apply a **simple rule**:

- **Lower segment → relabel everything to `Whistle`**
- **Middle segment → relabel everything to `Low_Frequency_Lines`**
- **Upper segment → keep original labels (morphology is stable here)**

This yields a consistent, physically meaningful relabeling across the manifold.

The full per-sample proposed corrections are stored in:  
`correction_table.csv`

---

## 🖼 Evidence: Cluster Atlas

The file `atlas_3row.png` shows the 3-row structure:

- **Row 1: Lower (Whistles)**  
- **Row 2: Middle (Lines)**  
- **Row 3: Upper (Bursts)**  

Each subplot title includes the original human label, visually revealing misclassifications.

---

## 📊 Key Insight

> **Cluster 16 reveals a 1-D frequency-drifting glitch family with a 28.5% human error rate.**  
> This demonstrates that unsupervised deep-learning morphology mapping can meaningfully improve or correct Gravity Spy labels.

This single cluster alone shows the scientific value of machine-guided auditing in gravitational-wave instrumentation.

---

## 🧭 Impact

This case study illustrates:

- **Unsupervised Discovery** — Finding structures that are not part of the official Gravity Spy taxonomy  
- **Data Quality Audit** — Quantifying where citizen science labels fail  
- **Interpretability** — Connecting CNN-UMAP geometry to physical detector behavior  
- **Governance** — Proposing a clean, physics-based relabeling rule  

This is the first fully documented deep-dive of a Gravity Spy drift-line manifold and will support future phases:

- **Phase B:** Detector auxiliary channel correlation (GWpy)  
- **Phase C:** Impact ranking & explainable ML  

---

## 📁 Files Included in This Folder

- `atlas_3row.png` — Visual atlas (lower/middle/upper segments)  
- `correction_table.csv` — Proposed relabeling for all 302 samples  
- `metadata.json` — Summary statistics for Cluster 16  
- `report.md` — This document  

---

## ✉️ Contact

*Davis Whaley*  
GitHub: https://github.com/davismwhaley  
Email: davismwhaley@gmail.com


