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
