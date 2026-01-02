## **Results**
Although demonstrated on Gravity Spy, this audit framework applies to any scientific dataset labeled by humans at scale (e.g., medical imaging, microscopy, remote sensing), where taxonomies evolve faster than labeling consistency.

---

## **4.1 Global Ambiguity Ranking**

We present a global audit of human-assigned Gravity Spy labels using unsupervised morphology learning, with the aim of identifying systematic divergences between human taxonomy and learned spectrogram structure.

After embedding 34,332 Gravity Spy spectrograms using a CNN-based feature extractor and projecting them with UMAP, HDBSCAN clustering was applied to identify coherent morphological groups.

To prioritize clusters exhibiting disagreement between human labels and learned morphology, clusters were ranked using an ambiguity score defined as

## **Ambiguity=(1−purity)×N**
where purity is the fraction of samples belonging to the most common human label within a cluster and N is the cluster size.

This metric highlights large clusters with substantial label mixing.
Figure 2 shows the top-ranked ambiguous clusters. Two clusters—Cluster 33 and Cluster 41—exhibit particularly strong and interpretable disagreement patterns and are examined in detail below.

---

## **4.2 Failure Mode I: Over-Splitting (Cluster 33)**

Cluster 33 contains 2,106 samples and exhibits low label purity (~0.22). No single Gravity Spy label dominates; instead, labels such as _Violin_Mode_, _Power_Line_, _Low_Frequency_Lines_, and _1080Lines_ appear with comparable frequency.

A controlled contact-sheet visualization (five samples per label for the six most frequent labels) is shown in Figure 3. Despite divergent human-assigned labels, the spectrograms display nearly indistinguishable narrow-band, line-like morphologies.

This cluster therefore exemplifies **over-splitting**, in which a single coherent instrumental morphology is subdivided across multiple human taxonomies without corresponding physical distinctions.

---

## **4.3 Failure Mode II: Over-Compression (Cluster 41)**

Cluster 41 is the largest ambiguous cluster, containing 3,915 samples. While Blip is the plurality label (~48%), substantial fractions of samples are labeled as _Koi_Fish_, _Low_Frequency_Burst_, and _Light_Modulation_.

To determine whether this label mixing reflects random variation or structured morphology, samples within Cluster 41 were ordered by **total spectrogram intensity**, a simple proxy for signal strength and bandwidth. The resulting ordered visualization _(Figure 4)_ reveals a smooth, monotonic progression from thin, impulsive features to increasingly thick and temporally smeared morphologies, without discrete boundaries.

Cluster 41 therefore demonstrates over-compression, in which a graded family of related morphologies is collapsed into a single dominant human label.

---

## **4.4 Quantitative Contrast via Label Entropy**

To quantify label diversity within clusters, Shannon label entropy was computed for each cluster:

H=−i∑​pi​log2​pi​,

where _pi_ is the fraction of samples assigned to label _i_.

Cluster 33 exhibits higher entropy (H=2.82) than Cluster 41 (H=2.26) as shown in Figure 5. This difference reflects distinct structural causes: near-uniform fragmentation across labels in Cluster 33 versus dominance of a single label over a graded continuum in Cluster 41.

---

## **4.5 Summary of Observed Failure Modes**

Together, these results identify two opposite but systematic failure modes in human-in-the-loop glitch taxonomies:

- Over-splitting: one morphology fragmented into many labels (Cluster 33).
- Over-compression: multiple related morphologies collapsed into one dominant label (Cluster 41).

  Both failure modes are detectable using the same unsupervised audit pipeline and do not require physical attribution via auxiliary channels.






