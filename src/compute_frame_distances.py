"""Compute consecutive-frame cosine distances from saved feature files."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--feature-dir", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--pattern", default="*_features.npy")
    parser.add_argument(
        "--metadata-csv",
        type=Path,
        help="Optional metadata with start_frame and end_frame columns.",
    )
    parser.add_argument(
        "--default-label",
        type=int,
        default=0,
        help="Label used when metadata is not provided or a video is missing.",
    )
    return parser.parse_args()


def load_metadata(metadata_csv: Path | None) -> pd.DataFrame | None:
    if metadata_csv is None:
        return None
    metadata = pd.read_csv(metadata_csv)
    required = {"video_name", "start_frame", "end_frame"}
    missing = required.difference(metadata.columns)
    if missing:
        raise ValueError(f"Metadata is missing required columns: {sorted(missing)}")
    return metadata


def video_key_from_feature_path(path: Path) -> str:
    name = path.stem
    for suffix in ["_features", "_patch_matrix", "_merged"]:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
    return name


def flatten_features(features: np.ndarray) -> np.ndarray:
    if features.ndim == 1:
        raise ValueError("Expected at least two dimensions: frames x features")
    if features.ndim > 2:
        return features.reshape(features.shape[0], -1)
    return features


def cosine_distances(features: np.ndarray) -> np.ndarray:
    features = flatten_features(features).astype(np.float64)
    distances = np.zeros(features.shape[0], dtype=np.float64)

    previous = features[:-1]
    current = features[1:]
    numerator = np.sum(previous * current, axis=1)
    denominator = np.linalg.norm(previous, axis=1) * np.linalg.norm(current, axis=1)
    denominator = np.maximum(denominator, 1e-12)
    distances[1:] = 1.0 - numerator / denominator
    return distances


def labels_for_video(
    video_key: str,
    frame_numbers: np.ndarray,
    metadata: pd.DataFrame | None,
    default_label: int,
) -> np.ndarray:
    labels = np.full(frame_numbers.shape, default_label, dtype=int)
    if metadata is None:
        return labels

    rows = metadata[metadata["video_name"].astype(str) == video_key]
    if rows.empty:
        return labels

    start_frame = int(rows.iloc[0]["start_frame"])
    end_frame = int(rows.iloc[0]["end_frame"])
    labels[(frame_numbers >= start_frame) & (frame_numbers <= end_frame)] = 1
    return labels


def main() -> None:
    args = parse_args()
    metadata = load_metadata(args.metadata_csv)
    rows = []

    feature_paths = sorted(args.feature_dir.glob(args.pattern))
    if not feature_paths:
        raise FileNotFoundError(f"No feature files matched {args.feature_dir / args.pattern}")

    for feature_path in feature_paths:
        video_key = video_key_from_feature_path(feature_path)
        features = np.load(feature_path)
        distances = cosine_distances(features)
        frame_numbers = np.arange(1, len(distances) + 1)
        labels = labels_for_video(video_key, frame_numbers, metadata, args.default_label)

        rows.append(
            pd.DataFrame(
                {
                    "video_name": video_key,
                    "frame_no": frame_numbers,
                    "distance": distances,
                    "label": labels,
                }
            )
        )

    output = pd.concat(rows, ignore_index=True)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output_csv, index=False)
    print(f"Saved {len(output):,} frame-distance rows to {args.output_csv}")


if __name__ == "__main__":
    main()
