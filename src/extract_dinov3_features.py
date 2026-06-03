"""Extract DINOv3 frame features from videos.

This script reads videos frame by frame, extracts DINOv3 features, and saves
one NumPy feature file per video. The default output is a pooled feature vector
per frame with shape ``(num_frames, feature_dim)``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from tqdm import tqdm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--pattern", default="*.mp4")
    parser.add_argument("--model-name", default="dinov3_vith16plus")
    parser.add_argument("--image-size", default=224, type=int)
    parser.add_argument(
        "--feature-mode",
        choices=["patch_mean", "patch_tokens"],
        default="patch_mean",
        help="Save one pooled vector per frame or all patch tokens.",
    )
    return parser.parse_args()


def load_dinov3(model_name: str, checkpoint_path: Path, device: torch.device):
    model = torch.hub.load("facebookresearch/dinov3", model_name, pretrained=False)
    state_dict = torch.load(checkpoint_path, map_location=device)

    if isinstance(state_dict, dict):
        if "model" in state_dict:
            state_dict = state_dict["model"]
        elif "teacher" in state_dict:
            state_dict = state_dict["teacher"]

    model.load_state_dict(state_dict, strict=False)
    model.to(device)
    model.eval()
    return model


def build_transform(image_size: int):
    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def extract_video_features(
    video_path: Path,
    model,
    transform,
    device: torch.device,
    feature_mode: str,
) -> np.ndarray:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or None
    features = []

    progress = tqdm(total=frame_count, desc=video_path.name, unit="frame")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            input_tensor = transform(pil_image).unsqueeze(0).to(device)

            with torch.no_grad():
                output = model.forward_features(input_tensor)
                patch_tokens = output["x_norm_patchtokens"].squeeze(0)
                if feature_mode == "patch_mean":
                    feature = patch_tokens.mean(dim=0).cpu().numpy()
                else:
                    feature = patch_tokens.cpu().numpy()

            features.append(feature)
            progress.update(1)
    finally:
        progress.close()
        cap.release()

    if not features:
        raise RuntimeError(f"No frames were read from video: {video_path}")

    return np.asarray(features)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = load_dinov3(args.model_name, args.checkpoint, device)
    transform = build_transform(args.image_size)

    video_paths = sorted(args.video_dir.glob(args.pattern))
    if not video_paths:
        raise FileNotFoundError(f"No videos matched {args.video_dir / args.pattern}")

    for video_path in video_paths:
        output_path = args.output_dir / f"{video_path.stem}_features.npy"
        if output_path.exists():
            print(f"Skipping existing file: {output_path}")
            continue

        feature_array = extract_video_features(
            video_path=video_path,
            model=model,
            transform=transform,
            device=device,
            feature_mode=args.feature_mode,
        )
        np.save(output_path, feature_array)
        print(f"Saved {feature_array.shape} features to {output_path}")


if __name__ == "__main__":
    main()
