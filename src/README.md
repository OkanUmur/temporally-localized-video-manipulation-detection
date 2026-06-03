# Source Code

This directory contains cleaned scripts for reproducing the feature-similarity
experiments reported in the paper.

## Scripts

```text
extract_dinov3_features.py
compute_frame_distances.py
evaluate_control_group.py
evaluate_merged_videos.py
plot_detection_trajectories.py
```

## Pipeline

The evaluation pipeline is:

```text
videos
  -> extract_dinov3_features.py
  -> compute_frame_distances.py
  -> evaluate_merged_videos.py / evaluate_control_group.py
  -> plot_detection_trajectories.py
```

## Example Commands

Extract DINOv3 features:

```bash
python src/extract_dinov3_features.py \
  --video-dir path/to/videos \
  --output-dir outputs/features \
  --checkpoint path/to/dinov3_checkpoint.pth \
  --pattern "*_merged.mp4"
```

Compute consecutive-frame cosine distances:

```bash
python src/compute_frame_distances.py \
  --feature-dir outputs/features \
  --output-csv outputs/merged_distances.csv \
  --metadata-csv data/frame_insertion_metadata.csv
```

Evaluate merged videos:

```bash
python src/evaluate_merged_videos.py \
  --input outputs/merged_distances.csv \
  --output-predictions outputs/merged_predictions.csv
```

Evaluate pure authentic control videos:

```bash
python src/evaluate_control_group.py \
  --input outputs/control_distances.csv \
  --output-predictions outputs/control_predictions.csv
```

Plot selected trajectories:

```bash
python src/plot_detection_trajectories.py \
  --input outputs/merged_distances.csv \
  --output-dir outputs/plots \
  --videos Ornek_39_merged
```

## Notes

- Video files and DINOv3 checkpoints are not stored in this repository.
- The scripts use precomputed frame-distance tables for evaluation.
- Default parameters match the reported feature-similarity experiments:
  `window=30`, `z_threshold=1.5`, `min_distance=0.01`, and `stabilizer=0.005`.
