# Repository Preparation Plan

## Immediate arXiv-Ready Version

- Create a public GitHub repository.
- Upload this scaffold.
- Add the repository URL to the arXiv submission metadata or paper if needed.

## Before arXiv Becomes Public

- Add cleaned evaluation scripts under `src/`.
- Add dataset construction metadata under `data/`.
- Add selected figures under `figures/`.
- Add the arXiv link to `README.md`.
- Add `CITATION.cff` after the arXiv record is available.

## Do Not Commit

- DINOv3 model weights (`*.pth`)
- full video datasets (`*.mp4`)
- large ZIP archives
- generated caches
- private or licensing-unclear source files

## Suggested Repository Name

```text
temporally-localized-video-manipulation-detection
```
