# Detecting Temporally Localized Manipulations in Authentic Video Streams

This repository provides code, metadata, and release notes for the paper:

**Detecting Temporally Localized Manipulations in Authentic Video Streams**

Authors: Okan Umur, Ali Emre Güşlü, Ibrahim Delibasoglu

## Status

This repository is being prepared for release. The paper, code, dataset metadata, and evaluation artifacts are being cleaned and organized.

- Paper: coming soon
- arXiv: coming soon
- Dataset download: [Zenodo v1.0](https://doi.org/10.5281/zenodo.20548572)
- Citation: dataset DOI available; paper citation coming soon

## Dataset Description

This work studies a realistic video forensics scenario where a short manipulated segment is inserted into an otherwise authentic video stream and the original footage resumes afterward. This differs from many existing video forgery datasets that focus on fully manipulated videos, face-centric deepfakes, object removal, or audio-only manipulations.

The custom evaluation set contains:

- 100 pure authentic control videos
- 100 generated manipulation segments
- 100 partially manipulated merged videos

The merged videos follow this temporal structure:

```text
authentic frames -> inserted manipulated segment -> authentic continuation
```

Dense frame-level labels mark the inserted manipulation intervals.

## Dataset Structure

The dataset release is organized conceptually as follows:

```text
dataset/
+-- authentic/       Pure authentic control videos
+-- fake_segments/   Generated manipulation segments
+-- merged/          Partially manipulated videos
+-- metadata/        Frame insertion logs and labels
```

The full video files are not included in this GitHub repository. The complete dataset is available on Zenodo:

- Dataset v1.0 DOI: [10.5281/zenodo.20548572](https://doi.org/10.5281/zenodo.20548572)
- All versions DOI: [10.5281/zenodo.20548571](https://doi.org/10.5281/zenodo.20548571)

## Metadata

The `data/` directory contains lightweight metadata describing the frame insertion process:

- `video_name`
- `original_frames`
- `fake_frames_added`
- `start_frame`
- `end_frame`
- `total_frames_after_merge`
- `fps_original`
- `fps_fake`

See [data/frame_insertion_metadata.csv](data/frame_insertion_metadata.csv).

## Manipulation Scenario

For each authentic source video, the 100th frame is used as the transition point. A generated manipulation segment is inserted after the first 99 authentic frames, and the remaining authentic video continues after the inserted segment.

This creates a challenging temporally localized manipulation setting where the forged region is short relative to the full video and must remain visually coherent with the surrounding authentic content.

## Detection Methods

The paper evaluates two complementary approaches:

1. **Linear Probe on DINOv3 Features**
   - Supervised baseline using frozen DINOv3 features.
   - Evaluated with fixed, adaptive, and sliding-window thresholding.

2. **DINOv3 Feature Similarity**
   - Training-free temporal anomaly detection method.
   - Uses consecutive-frame cosine distance, local Z-score normalization, and a minimum distance threshold.

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
+-- data/         Dataset metadata and release notes
+-- docs/         Reproducibility and repository preparation notes
+-- figures/      Selected figures and result visualizations
+-- paper/        Paper and citation notes
+-- src/          Code organization notes and scripts
+-- README.md
+-- requirements.txt
```

## Examples

### Temporal Manipulation Sequence

The core dataset scenario inserts a short manipulated segment into an otherwise authentic video stream:

```text
Step 1: authentic video frames -> Step 2: inserted manipulated segment -> Step 3: authentic continuation
```

The table below shows three representative examples of this temporal structure.

| Example | Step 1: Original video | Step 2: Manipulated segment | Step 3: Original continuation |
| --- | --- | --- | --- |
| Example 1 | ![Example 1 original frame](figures/example1_original.png) | ![Example 1 manipulated segment](figures/example1_manipulated.png) | ![Example 1 original continuation](figures/example1_continuation.png) |
| Example 2 | ![Example 2 original frame](figures/example2_original.png) | ![Example 2 manipulated segment](figures/example2_manipulated.png) | ![Example 2 original continuation](figures/example2_continuation.png) |
| Example 3 | ![Example 3 original frame](figures/example3_original.png) | ![Example 3 manipulated segment](figures/example3_manipulated.png) | ![Example 3 original continuation](figures/example3_continuation.png) |

### Detection Trajectories

Example output from the DINOv3 feature similarity approach:

![Successful manipulation localization](figures/feature_similarity_success_video39.png)

Example true-negative trajectory from the pure authentic control group:

![Pure authentic control group true negative](figures/control_group_true_negative_video10.png)

## Code

The `src/` directory contains cleaned scripts for the DINOv3 feature-similarity pipeline:

- `extract_dinov3_features.py`: extract DINOv3 frame features from videos.
- `compute_frame_distances.py`: compute consecutive-frame cosine distances.
- `evaluate_merged_videos.py`: reproduce merged-video frame-level metrics.
- `evaluate_control_group.py`: reproduce pure authentic control-group metrics.
- `plot_detection_trajectories.py`: generate Z-score trajectory plots.

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Dataset Availability

The full dataset is publicly available on Zenodo under the Creative Commons Attribution 4.0 International (CC BY 4.0) license:

https://doi.org/10.5281/zenodo.20548572

## Citation

Dataset citation:

```text
Umur, O., & Güşlü, A. E. (2026). Detecting Temporally Localized Manipulations in Authentic Video Streams Dataset (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.20548572
```

Paper citation information will be added after the arXiv record is available.

## License

The dataset is released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license via Zenodo.

The source code in this repository is released under the MIT License.

## Contact

For questions about the dataset, code, or paper, please contact Okan Umur at umuro2124@gmail.com.
