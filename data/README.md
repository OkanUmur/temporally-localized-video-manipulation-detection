# Dataset Notes

This directory will document the custom evaluation dataset used in the paper.

## Dataset Composition

The evaluation set contains:

- 100 pure authentic control videos
- 100 generated manipulation segments
- 100 partially manipulated merged videos

Each merged video starts with authentic footage, contains an inserted manipulated segment beginning at frame 100, and then resumes the authentic continuation.

## Metadata

This directory includes `frame_insertion_metadata.csv`, a lightweight metadata file derived from the local frame insertion logs. It documents the temporal boundaries of the inserted segments without including video files.

The metadata fields are:

- `video_name`
- `original_frames`
- `fake_frames_added`
- `start_frame`
- `end_frame`
- `total_frames_after_merge`
- `fps_original`
- `fps_fake`

## Important Note

Large video files are intentionally excluded from the GitHub repository. The complete dataset is publicly available on Zenodo:

https://doi.org/10.5281/zenodo.20548572
