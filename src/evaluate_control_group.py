"""Evaluate false alarms on pure authentic control videos."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from evaluate_merged_videos import add_predictions, read_table, resolve_columns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-predictions", type=Path)
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--z-threshold", type=float, default=1.5)
    parser.add_argument("--min-distance", type=float, default=0.01)
    parser.add_argument("--stabilizer", type=float, default=0.005)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = read_table(args.input)
    columns = resolve_columns(df)

    evaluated = add_predictions(
        df=df,
        columns=columns,
        window=args.window,
        z_threshold=args.z_threshold,
        min_distance=args.min_distance,
        stabilizer=args.stabilizer,
    )

    total_frames = len(evaluated)
    false_positive_frames = int(evaluated["prediction"].sum())
    true_negative_frames = total_frames - false_positive_frames

    per_video = evaluated.groupby(columns["video"])["prediction"].sum()
    videos_with_false_alarms = int((per_video > 0).sum())
    videos_with_zero_errors = int((per_video == 0).sum())
    total_videos = len(per_video)

    video_level_accuracy = videos_with_zero_errors / total_videos if total_videos else 0.0
    frame_level_accuracy = true_negative_frames / total_frames if total_frames else 0.0

    print("Pure Authentic Control Group Performance")
    print(f"Total Tested Videos       : {total_videos:,}")
    print(f"Videos with Zero Errors   : {videos_with_zero_errors:,}")
    print(f"Videos with False Alarms  : {videos_with_false_alarms:,}")
    print(f"Video-Level Accuracy      : {video_level_accuracy * 100:.2f}%")
    print(f"Total Processed Frames    : {total_frames:,}")
    print(f"True Negative Frames      : {true_negative_frames:,}")
    print(f"False Positive Frames     : {false_positive_frames:,}")
    print(f"Frame-Level Accuracy      : {frame_level_accuracy * 100:.2f}%")

    if args.output_predictions:
        args.output_predictions.parent.mkdir(parents=True, exist_ok=True)
        evaluated.to_csv(args.output_predictions, index=False)
        print(f"Saved predictions to {args.output_predictions}")


if __name__ == "__main__":
    main()
