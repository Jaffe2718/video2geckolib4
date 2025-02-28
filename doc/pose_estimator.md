# Documentation (`pose_estimator.py`)

## Class `PoseEstimator`

### Method `__init__()`
```
def __init__(self, *args, **kwargs):
```

#### Parameters

see ` mediapipe.python.solutions.pose.Pose.__init__()`

### Method `auto_estimate()`

Estimate pose for all frames in given video path

```
def auto_estimate(self, video_path: str | Path) -> Tuple[List[NamedTuple], List[NamedTuple]]:
```

#### Parameters

- `video_path` (str | Path): Path to video file

#### Returns

- `Tuple[List[NamedTuple], List[NamedTuple]]`: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)


### Method `estimate_frames()`

Estimate pose for given frames in given video path

```
def estimate_frames(self, video_path: str | Path, frames: Iterable[int]) -> Tuple[List[NamedTuple], List[NamedTuple]]:
```

#### Parameters

- `video_path` (str | Path): Path to video file
- `frames` (Iterable[int]): Index of frames to estimate pose for

#### Returns

- `Tuple[List[NamedTuple], List[NamedTuple]]`: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)


### Method `estimate_timestamp()`

Estimate pose for given timestamps in given video path

```
def estimate_timestamp(self, video_path: str | Path, timestamps: Iterable[float]) -> Tuple[List[NamedTuple], List[NamedTuple]]:
```

#### Parameters

- `video_path` (str | Path): Path to video file
- `timestamps` (Iterable[float]): Timestamps to estimate pose for

#### Returns

- `Tuple[List[NamedTuple], List[NamedTuple]]`: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)


### Method `estimate_pictures()`

Estimate pose for given pictures

```
def estimate_pictures(self, pictures: Iterable[str | Path]) -> Tuple[List[NamedTuple], List[NamedTuple]]:
```

#### Parameters

- `pictures` (Iterable[str | Path]):  path list to pictures

#### Returns

- `Tuple[List[NamedTuple], List[NamedTuple]]`: pose estimation result for given timestamps, (pose_world_landmarks, pose_landmarks)


### Example
```python
import video2geckolib4 as v2g

pose_estimator = v2g.PoseEstimator()

r1 = pose_estimator.auto_estimate("video.mp4")

r2 = pose_estimator.estimate_frames("video.mp4", [2, 3, 5, 7, 11])
r3 = pose_estimator.estimate_timestamp("video.mp4", [0.1, 0.2, 0.3, 0.4, 0.5])
r4 = pose_estimator.estimate_pictures(["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"])
```