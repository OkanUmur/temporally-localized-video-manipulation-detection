# Source Code Notes

This directory will contain cleaned scripts for reproducing the paper experiments.

Planned script organization:

```text
extract_features.py
compute_frame_distances.py
evaluate_feature_similarity.py
evaluate_control_group.py
plot_results.py
model_loader.py
```

## Local Script Mapping

The current local project contains phase-based experimental scripts. The most relevant scripts for the paper are:

- `model_loader.py`: DINOv3 model loading and frame feature extraction utilities.
- `matris_cikarici.py`: feature matrix extraction for merged videos.
- `faz1_orijinal_matris_cikarimi.py`: feature matrix extraction for authentic videos.
- `faz2_orijinal_mesafeleri_hesapla.py`: consecutive-frame distance computation for authentic videos.
- `Frame_Merged_Videolar.py`: merged-video feature similarity evaluation and plotting.
- `Frame_Bazli_Kontrol_Orijinal_EN.py`: pure authentic control group evaluation and plotting. The local working copy may use Turkish characters in the filename.

These scripts will be cleaned, renamed, and documented before the first stable repository release.
