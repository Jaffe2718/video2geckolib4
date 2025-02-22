from typing import *
from pathlib import Path
import cv2
import mediapipe as mp

class VideoPoseEstimator:
    def __init__(self, *args, **kwargs):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(*args, **kwargs)

    def __del__(self):
        self.pose.close()

    def auto_estimate(self, video_path: str | Path) -> Tuple[List[NamedTuple], List[NamedTuple]]:
        """
        estimate pose for all frames in given video path
        :param video_path:  to video file
        :return: pose estimation result for all frames
        """
        cap = cv2.VideoCapture(video_path)
        frame_cnt = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # 总帧数
        world_pose_frames, pose_frames = [], []
        for i in range(frame_cnt):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            world_pose_frames.append(results.pose_world_landmarks.landmark)
            pose_frames.append(results.pose_landmarks.landmark)
        cap.release()
        return world_pose_frames, pose_frames

    def estimate_frames(self, video_path: str | Path, frames: Iterable[int]) -> Tuple[List[NamedTuple], List[NamedTuple]]:
        """
        Estimate pose for given frames in given video path
        :param video_path:  to video file
        :param frames:  index of frames to estimate pose for
        :return: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)
        """
        cap = cv2.VideoCapture(video_path)
        world_pose_frames, pose_frames = [], []
        for i in frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            world_pose_frames.append(results.pose_world_landmarks.landmark)
            pose_frames.append(results.pose_landmarks.landmark)
        cap.release()
        return world_pose_frames, pose_frames

    def estimate_timestamp(self, video_path: str | Path, timestamps: Iterable[float]) -> Tuple[List[NamedTuple], List[NamedTuple]]:
        """
        Estimate pose for given timestamps in given video path
        :param video_path:  to video file
        :param timestamps:  timestamp of frames to estimate pose for
        :return: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)
        """
        cap = cv2.VideoCapture(video_path)
        world_pose_frames, pose_frames = [], []
        for t in timestamps:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ret, frame = cap.read()
            if not ret:
                print("break")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame)
            world_pose_frames.append(results.pose_world_landmarks.landmark)
            pose_frames.append(results.pose_landmarks.landmark)
        cap.release()
        return world_pose_frames, pose_frames