# Cluster 16 Deep Dive  
**Morphological Evolution Along a Drift-Line Manifold**  
*Gravity Spy Glitch Explorer – Phase A.2 Case Study*

---

## 🌌 Overview

Cluster 16 emerged as the single most scientifically interesting structure during the Human–AI Discrepancy Audit.  
Unlike most clusters—which correspond cleanly to one Gravity Spy class—Cluster 16 forms a **continuous 1-D manifold** in UMAP space. Along this curve, the glitch morphology evolves smoothly from **high-frequency whistles**, through **narrow spectral lines**, and finally into **broadband low-frequency bursts**.

This continuum reveals that many human labels are **inconsistent** with the true underlying morphology. Cluster 16 alone contains:

- **302 total samples**
- **86 inconsistent human labels**
- **28.5% overall inconsistency rate**

This makes Cluster 16 a perfect case study for demonstrating:
- Unsupervised morphology discovery  
- Human–machine label disagreement  
- Data quality auditing  
- A principled strategy for relabeling citizen-science datasets  

---
![Cluster 16](umap_cluster16_segments2.png)

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
The center of the manifold (narrow-line regime) is the least intuitive for humans and contains the highest mistake rate.

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


