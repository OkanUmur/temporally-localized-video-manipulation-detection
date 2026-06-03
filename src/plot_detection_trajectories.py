"""Plot Z-score trajectories for selected videos."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from evaluate_merged_videos import add_predictions, read_table, resolve_columns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--videos", nargs="*", help="Optional list of video names to plot.")
    parser.add_argument("--max-videos", type=int, default=None)
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--z-threshold", type=float, default=1.5)
    parser.add_argument("--min-distance", type=float, default=0.01)
    parser.add_argument("--stabilizer", type=float, default=0.005)
    return parser.parse_args()


def safe_filename(name: str) -> str:
    return (
        name.replace("\\", "_")
        .replace("/", "_")
        .replace(":", "_")
        .replace(" ", "_")
    )


def plot_video(
    video_df: pd.DataFrame,
    columns: dict[str, str],
    output_path: Path,
    z_threshold: float,
) -> None:
    video_name = str(video_df[columns["video"]].iloc[0])
    frame_col = columns["frame"]
    label_col = columns["label"]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        video_df[frame_col],
        video_df["z_score"],
        label="Z-Score (noise filtered)",
        color="#1f77b4",
        linewidth=2,
    )
    ax.axhline(
        y=z_threshold,
        color="gray",
        linestyle="--",
        linewidth=1.5,
        label=f"Z-threshold ({z_threshold})",
    )

    positive_labels = video_df[video_df[label_col] == 1]
    if not positive_labels.empty:
        start_frame = positive_labels[frame_col].min()
        end_frame = positive_labels[frame_col].max()
        ax.axvspan(
            start_frame,
            end_frame,
            color="red",
            alpha=0.15,
            label="Ground truth manipulated region",
        )

    predicted = video_df[video_df["prediction"] == 1]
    if not predicted.empty:
        boundary_frames = [predicted[frame_col].min(), predicted[frame_col].max()]
        for index, frame_no in enumerate(boundary_frames):
            point = video_df[video_df[frame_col] == frame_no].iloc[0]
            ax.plot(
                frame_no,
                point["z_score"],
                marker="*",
                color="red",
                markersize=16,
                label="Detected boundary" if index == 0 else "",
            )

    ax.set_title(f"Noise-filtered manipulation detection: {video_name}")
    ax.set_xlabel("Frame index")
    ax.set_ylabel("Z-score value")
    ax.grid(True, linestyle=":", alpha=0.7)
    ax.legend(loc="upper left")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close(fig)


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

    video_names = list(evaluated[columns["video"]].drop_duplicates())
    if args.videos:
        requested = set(args.videos)
        video_names = [name for name in video_names if str(name) in requested]
    if args.max_videos is not None:
        video_names = video_names[: args.max_videos]

    for video_name in video_names:
        video_df = evaluated[evaluated[columns["video"]] == video_name]
        output_path = args.output_dir / f"{safe_filename(str(video_name))}.png"
        plot_video(video_df, columns, output_path, args.z_threshold)
        print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
