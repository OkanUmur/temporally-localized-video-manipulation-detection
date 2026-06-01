# Detecting Temporally Localized Manipulations in Authentic Video Streams

Official repository for the paper:

**Detecting Temporally Localized Manipulations in Authentic Video Streams**

This project investigates a realistic video forensics scenario where a short manipulated segment is inserted into an otherwise authentic video stream and the original footage resumes afterward. The repository will host code, metadata, evaluation scripts, and reproducibility notes for the paper.

## Status

This repository is being prepared for release. The paper, code, dataset metadata, and evaluation artifacts are being cleaned and organized. Public links and citation information will be added after the arXiv submission is available.

## Method Overview

The paper evaluates two complementary approaches:

1. **Linear Probe on DINOv3 Features**
   - A supervised baseline using frozen DINOv3 features.
   - Evaluated with fixed, adaptive, and sliding-window thresholding.

2. **DINOv3 Feature Similarity**
   - A training-free temporal anomaly detection method.
   - Uses consecutive-frame cosine distance, local Z-score normalization, and a minimum distance threshold.

## Dataset Summary

The custom evaluation set contains:

- 100 pure authentic control videos
- 100 generated manipulation segments
- 100 partially manipulated merged videos

The merged videos follow this temporal structure:

```text
authentic frames -> inserted manipulated segment -> authentic continuation
```

Dense frame-level labels are used to mark the inserted manipulation intervals.

## Main Results

### Feature Similarity on Merged Videos

| Metric | Value |
| --- | ---: |
| Total processed frames | 52,889 |
| Total actual fake frames | 15,566 |
| Total detected fake frames | 10,059 |
| Global accuracy | 83.12% |
| Global precision | 83.00% |
| Global recall | 53.64% |
| Global F1-score | 65.16% |

### Pure Authentic Control Group

| Metric | Value |
| --- | ---: |
| Total tested videos | 100 |
| Videos with zero errors | 95 |
| Videos with false alarms | 5 |
| Video-level accuracy | 95.00% |
| Total processed frames | 37,423 |
| True negative frames | 36,558 |
| False positive frames | 865 |
| Frame-level accuracy | 97.69% |

## Repository Layout

```text
.
+-- data/      Dataset metadata and release notes
+-- docs/      Reproducibility and repository preparation notes
+-- figures/   Figure release notes and selected result visualizations
+-- paper/     Paper and citation notes
+-- src/       Code organization notes and scripts
```

## Dataset Availability

The dataset contains mixed-source authentic videos, generated manipulation segments, and derived merged videos. Because licensing and redistribution permissions may vary by source, the full dataset release will be documented separately.

Metadata and dataset construction notes will be provided in `data/`.

## Citation

Citation information will be added after the arXiv record is available.

## License

License information will be added before the first stable release. Dataset redistribution terms may differ from code licensing terms.
