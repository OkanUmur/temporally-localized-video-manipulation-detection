"""Evaluate temporally localized manipulation detection on merged videos."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-predictions", type=Path)
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--z-threshold", type=float, default=1.5)
    parser.add_argument("--min-distance", type=float, default=0.01)
    parser.add_argument("--stabilizer", type=float, default=0.005)
    return parser.parse_args()


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def resolve_columns(df: pd.DataFrame) -> dict[str, str]:
    candidates = {
        "video": ["video_name", "Video_Adi"],
        "frame": ["frame_no", "Frame_No"],
        "distance": ["distance", "Distance"],
        "label": ["label", "Gercek_Etiket"],
    }
    resolved = {}
    for key, names in candidates.items():
        for name in names:
            if name in df.columns:
                resolved[key] = name
                break
        if key not in resolved:
            raise ValueError(f"Could not find a column for {key}. Tried {names}")
    return resolved


def add_predictions(
    df: pd.DataFrame,
    columns: dict[str, str],
    window: int,
    z_threshold: float,
    min_distance: float,
    stabilizer: float,
) -> pd.DataFrame:
    all_videos = []

    for _, video_df in df.groupby(columns["video"], sort=False):
        video_df = video_df.copy()
        distances = video_df[columns["distance"]]

        rolling_mean = distances.rolling(window=window, min_periods=1).mean()
        rolling_std = distances.rolling(window=window, min_periods=1).std().fillna(0)
        video_df["z_score"] = (distances - rolling_mean) / (rolling_std + stabilizer)
        video_df.loc[distances < min_distance, "z_score"] = 0.0

        video_df["prediction"] = 0
        candidates = video_df.loc[video_df["z_score"] > z_threshold, columns["frame"]]
        if len(candidates) >= 2:
            start_frame = candidates.min()
            end_frame = candidates.max()
            mask = (
                (video_df[columns["frame"]] >= start_frame)
                & (video_df[columns["frame"]] <= end_frame)
            )
            video_df.loc[mask, "prediction"] = 1

        all_videos.append(video_df)

    return pd.concat(all_videos, ignore_index=True)


def binary_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())

    accuracy = (tp + tn) / len(y_true) if len(y_true) else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


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

    y_true = evaluated[columns["label"]].to_numpy(dtype=int)
    y_pred = evaluated["prediction"].to_numpy(dtype=int)
    metrics = binary_metrics(y_true, y_pred)

    print("Global Frame-Level Performance")
    print(f"Total Processed Frames     : {len(evaluated):,}")
    print(f"Total Actual Fake Frames   : {int(y_true.sum()):,}")
    print(f"Total Detected Fake Frames : {int(y_pred.sum()):,}")
    print(f"Global Accuracy            : {metrics['accuracy'] * 100:.2f}%")
    print(f"Global Precision           : {metrics['precision'] * 100:.2f}%")
    print(f"Global Recall              : {metrics['recall'] * 100:.2f}%")
    print(f"Global F1-score            : {metrics['f1'] * 100:.2f}%")

    if args.output_predictions:
        args.output_predictions.parent.mkdir(parents=True, exist_ok=True)
        evaluated.to_csv(args.output_predictions, index=False)
        print(f"Saved predictions to {args.output_predictions}")


if __name__ == "__main__":
    main()
