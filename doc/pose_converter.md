# Documentation (`pose_converter.py`)

## Field `BONES`

```python
BONES = ["Body", "Head", "LeftUpperArm", "LeftForearm", "LeftThigh", "LeftCalf", "RightUpperArm", "RightForearm", "RightThigh", "RightCalf"]
```

## Class `PoseConverter`
Convert pose landmarks to Blockbench rotation angles and translation vectors

### Method `convert_pose()`

convert pose landmarks to Blockbench rotation angles

```
@staticmethod
def convert_pose(lm: NamedTuple) -> Dict[str, List[float]]:
```

#### Parameters
- `lm`: pose landmarks

#### Return

- `Dict[str, List[float]]`: rotation angles dictionary (keys are BONES, unit is degrees)

### Method `apply_translation()`

Apply translation to all frames, the landmarks in `landmark_frames` should be `pose_landmarks`

```
@staticmethod
def apply_translation(landmark_frames: Iterable[NamedTuple]) -> List[List[float]]:
```

#### Parameters

- `landmark_frames`: an iterable of namedtuple objects, each object contains the pose landmarks of a frame

#### Return

- `List[List[float]]`: [[x, y, z], ...] where x, y, z is the translation vector in Blockbench coordinate system

### Method `calculate_poses()`

Calculate rotation angles for all frames

```
@staticmethod
def calculate_poses(landmark_frames: Iterable[NamedTuple], smooth: bool = True) -> List[Dict[str, List[float]]]:
```

#### Parameters

- `landmark_frames`: an iterable of namedtuple objects, each object contains the pose landmarks of a frame
- `smooth`: whether to smooth the rotation angles

#### Return

- `List[Dict[str, List[float]]]`: a list of rotation angles dictionaries (keys are BONES, unit is degrees)

### Method `statistic_skeleton()`

Statistic the average length and position of skeleton

```
@staticmethod
def statistic_skeleton(landmark_frames: Iterable[NamedTuple]) -> Dict[str, float]:
```
#### Parameters

- `landmark_frames`: an iterable of namedtuple objects, each object contains the pose landmarks of a frame

#### Return

- `Dict[str, float]`: a dictionary of average length and position of skeleton

## Example
```python
from video2geckolib4 import PoseEstimator, PoseConverter

video = "example.mp4"
pose_estimator = PoseEstimator()
pose_world_landmarks, pose_landmarks = pose_estimator.auto_estimate(video)

print(PoseConverter.statistic_skeleton(pose_landmarks))

pose_frams = PoseConverter.calculate_poses(pose_world_landmarks)
translation_frames = PoseConverter.apply_translation(pose_landmarks)
```