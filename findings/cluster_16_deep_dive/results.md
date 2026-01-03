# 📊 Research Results: A Morphological Audit of the Gravity Spy Taxonomy
This page provides a detailed analytical breakdown of the systematic divergences between human-assigned labels and learned spectrogram morphology. 

---

## **4.1 Global Ambiguity Ranking**

To prioritize clusters exhibiting the highest disagreement between human labels and learned morphology, we developed a global **Ambiguity Score**. This metric allows us to rank clusters not just by size, but by the "stress" they place on the existing taxonomy.

The score is defined as:

$$\text{Ambiguity} = (1 - \text{Purity}) \times N$$

Where:
- **Purity**: The fraction of samples belonging to the most common human label within a cluster.
- **N**: The total number of samples in the cluster.

> **Key Finding:** This metric successfully identified Cluster 33 and Cluster 41 as the primary "stress points" in the LIGO glitch taxonomy, representing two fundamentally different failure modes.

[`Figure 2`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/fig2_ambiguity_ranked_clusters_top15.png) shows the top-ranked ambiguous clusters. Two clusters—Cluster 33 and Cluster 41—exhibit particularly strong and interpretable disagreement patterns and are examined in detail below.

---

## **4.2 Failure Mode I: Over-Splitting (Cluster 33)**

Cluster 33 contains **2,106 samples** and exhibits a remarkably low label purity (~0.22). No single Gravity Spy label dominates. Instead, labels such as *Violin_Mode*, *Power_Line*, *Low_Frequency_Lines*, and *1080Lines* appear with nearly equal frequency.

**Evidence:**
A controlled contact-sheet visualization (five samples per label for the six most frequent labels) is shown in [`Figure 3`](https://davismwhaley.github.io/gravityspy-glitch-explorer/figures/cluster33_contact_sheet_top6x5.png). Despite divergent human-assigned labels, the spectrograms display nearly indistinguishable narrow-band, line-like morphologies.

 **Diagnostic:** **Over-splitting.** This cluster exemplifies **over-splitting**, in which a single coherent instrumental morphology is subdivided across multiple human taxonomies without corresponding physical distinctions.

---

## **4.3 Failure Mode II: Over-Compression (Cluster 41)**

Cluster 41 is the largest high-ambiguity group in the dataset (**3,915 samples**). While "Blip" is the plurality label (~48%), it masks substantial fractions of *Koi_Fish*, *Low_Frequency_Burst*, and *Light_Modulation*.

**Evidence:**
When ordered by **Integrated Pixel Intensity (SNR Proxy)**, Cluster 41 reveals a smooth, monotonic progression. It evolves from thin, impulsive spikes into increasingly thick, temporally smeared "bursts." There are no discrete morphological boundaries to justify the separate labels. [`Figure 4`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/cluster41_ordered_by_intensity_strip.png)

**Diagnostic:** **Over-compression.** A graded family of related morphologies is collapsed into a single catch-all label ("Blip"), hiding the continuous physical evolution of the signal.

---

## **4.4 Quantitative Contrast via Label Entropy**

To provide a mathematical foundation for these observations, **Shannon Label Entropy ($H$)** was used to quantify the "disorder" of human labels within each cluster:

$$H = -\sum p_i \log_2(p_i)$$

Where $p_i$ is the fraction of samples assigned to label $i$.

| Cluster | Entropy ($H$) | Failure Mode |
| :--- | :--- | :--- |
| **Cluster 33** | **2.82** | Over-Splitting (Fragmentation) |
| **Cluster 41** | **2.26** | Over-Compression (Spectrum Collapse) |

The higher entropy in Cluster 33 reflects **near-uniform fragmentation**, while the lower (but still significant) entropy in Cluster 41 reflects a **dominant label masking a continuum.**

Cluster 33 exhibits higher entropy (H=2.82) than Cluster 41 (H=2.26) as shown in [`Figure 5`](https://github.com/davismwhaley/gravityspy-glitch-explorer/blob/main/figures/fig5_label_entropy_cluster33_vs_cluster41.png). This difference reflects distinct structural causes: near-uniform fragmentation across labels in Cluster 33 versus dominance of a single label over a graded continuum in Cluster 41.

---

## **4.5 Summary of Observed Failure Modes**

Together, these results identify two opposite but systematic failure modes in human-in-the-loop glitch taxonomies:

- Over-splitting: one morphology fragmented into many labels (Cluster 33).
- Over-compression: multiple related morphologies collapsed into one dominant label (Cluster 41).

Both failure modes are detectable using the same unsupervised audit pipeline and do not require physical attribution via auxiliary channels.

---







