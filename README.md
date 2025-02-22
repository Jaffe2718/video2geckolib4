# Video2Geckolib4 Project

## Overview
This project aims to perform pose estimation on video files and convert the pose data for further use. It utilizes the `mediapipe` library for pose estimation and `cv2` (OpenCV) for video processing.

## Installation
Before running the code, make sure you have the following dependencies installed:
- `opencv-contrib-python`
- `mediapipe`
- `numpy`
- `scipy`

You can install them using `pip`:
```bash
pip install opencv-contrib-python mediapipe numpy scipy
```

## Usage

### VideoPoseEstimator Class
The `VideoPoseEstimator` class in `pose_estimator.py` is responsible for estimating the pose in video files.

#### Initialization
```python
from video2geckolib4.pose_estimator import VideoPoseEstimator

# Initialize the VideoPoseEstimator with optional arguments
estimator = VideoPoseEstimator()
```

#### Methods
- `auto_estimate(video_path)`: Estimate pose for all frames in the given video path.
    - `video_path`: Path to the video file (can be a string or a `Path` object).
    - Returns a tuple of two lists: `(world_pose_frames, pose_frames)` containing the pose estimation results for all frames.

```python
world_pose_frames, pose_frames = estimator.auto_estimate("path/to/video.mp4")
```

- `estimate_frames(video_path, frames)`: Estimate pose for the given frames in the given video path.
    - `video_path`: Path to the video file (can be a string or a `Path` object).
    - `frames`: An iterable of frame indices to estimate pose for.
    - Returns a tuple of two lists: `(world_pose_frames, pose_frames)` containing the pose estimation results for the given frames.

```python
frames_to_estimate = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
world_pose_frames, pose_frames = estimator.estimate_frames("path/to/video.mp4", frames_to_estimate)
```

- `estimate_timestamp(video_path, timestamps)`: Estimate pose for the given timestamps in the given video path.
    - `video_path`: Path to the video file (can be a string or a `Path` object).
    - `timestamps`: An iterable of timestamps (in seconds) to estimate pose for.
    - Returns a tuple of two lists: `(world_pose_frames, pose_frames)` containing the pose estimation results for the given timestamps.

```python
timestamps_to_estimate = [1.5, 2.0, 2.5]   # in seconds
world_pose_frames, pose_frames = estimator.estimate_timestamp("path/to/video.mp4", timestamps_to_estimate)
```

### PoseConverter Class
The `PoseConverter` class (not fully shown here) has a static method `apply_translation` in `pose_converter.py` that applies translation to the landmark frames.

```python
from video2geckolib4.pose_converter import PoseConverter

# Assume landmark_frames is an iterable of namedtuple objects
translation_frames = PoseConverter.apply_translation(landmark_frames)
```

### AnimationBuilder Class

```python
from video2geckolib4.animation_unit import AnimationBuilder

# Assume landmark_frames is an iterable of namedtuple objects
b = AnimationBuilder("kun.animation", 10)  # 10 seconds
b.add_keyframe("Body", 0.5, "position", [1, 2, 3])  # add a keyframe at 0.5 seconds
```

### AnimationSet Class

```python
from video2geckolib4.animation_unit import AnimationSet, AnimationBuilder

# create any `AnimationBuilder` here
b = AnimationBuilder("ji_ni_tai_mei.animation", 10)
b.add_keyframe("Body", 2.5, "position", [1, 2, 3])

c = AnimationBuilder("cai_xu_kun.animation", 2.5)
c.add_keyframe("Body", 1.25, "position", [4, 5, 6])

# init `AnimationSet`
animations = AnimationSet()

# add animations into AnimationSet
animations.append(b)
animations.append(c)

# save
animations.save("ikun.animations.json")
```

## Example
To easily use this project, you can use the `auto_estimate` method.
```python
import video2geckolib4

# generate a base model (optional)
video2geckolib4.gen_basemodel('ikun.bbmodel')

# prepare videos
videos = [
    "path/to/video1.mp4",
    "path/to/video2.mp4",
    "path/to/video3.mp4",
]

# estimate pose to animation
video2geckolib4.auto_estimate(videos, 'ikun.animations.json', sample_fps=20)
```

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.