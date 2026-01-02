import cv2
import logging
from pathlib import Path
from typing import Iterator, Tuple, Optional
import numpy as np

from .config import TARGET_FPS, DEFAULT_FPS

logger = logging.getLogger(__name__)


class VideoReader:
    def __init__(self, video_path: str, target_fps: Optional[int] = None):
        self.video_path = Path(video_path)
        self.target_fps = target_fps or TARGET_FPS

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")

        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS) or DEFAULT_FPS
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration_seconds = self.total_frames / self.original_fps

        self.frame_skip = max(1, int(self.original_fps / self.target_fps))

        logger.info(
            f"VideoReader initialized: {self.video_path.name} "
            f"({self.width}x{self.height}, {self.original_fps:.2f} FPS, "
            f"{self.total_frames} frames, {self.duration_seconds:.2f}s)"
        )
        logger.info(
            f"Sampling at {self.target_fps} FPS (skipping every {self.frame_skip} frames)"
        )

    def __iter__(self) -> Iterator[Tuple[np.ndarray, int, int]]:
        frame_count = 0
        sampled_frame_id = 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            if frame_count % self.frame_skip == 0:
                timestamp_ms = int((frame_count / self.original_fps) * 1000)

                yield frame, timestamp_ms, sampled_frame_id
                sampled_frame_id += 1

            frame_count += 1

        logger.info(f"VideoReader finished: processed {sampled_frame_id} frames")

    def get_metadata(self) -> dict:
        return {
            "video_path": str(self.video_path),
            "width": self.width,
            "height": self.height,
            "original_fps": self.original_fps,
            "target_fps": self.target_fps,
            "total_frames": self.total_frames,
            "duration_seconds": self.duration_seconds,
            "frame_skip": self.frame_skip,
        }

    def reset(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        logger.info("VideoReader reset to start")

    def release(self):
        if self.cap:
            self.cap.release()
            logger.info("VideoReader released")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def __del__(self):
        self.release()
