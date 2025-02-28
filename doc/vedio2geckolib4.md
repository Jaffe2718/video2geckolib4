# Video2GeckoLib4 User Documentation

## Introduction
This project aims to perform pose estimation on video files and convert the pose data for further use. It utilizes the `mediapipe` library for pose estimation and `cv2` (OpenCV) for video processing.

## Installation

Download it from https://github.com/Jaffe2718/video2geckolib4/releases

```shell
pip install opencv-contrib-python mediapipe numpy scipy
pip install path/to/video2geckolib4-<version>.tar.gz
```

or

```shell
pip install opencv-contrib-python mediapipe numpy scipy
pip install path/to/video2geckolib4-<version>-py3-none-any.whl
```

## Modules

- [\_\_init\_\_](__init__.md)
- [pose_estimator](pose_estimator.md)
- [pose_converter](pose_converter.md)
- [animation_unit](animation_unit.md)

## Example

```python
from video2geckolib4 import gen_basemodel, PoseConverter, PoseEstimator, AnimationBuilder, AnimationSet, auto_build_animations, BONES

# generate a base Blockbench model (optional)
gen_basemodel("gecko.bbmodel")

# example files
v0 = 'example.mp4'
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']
pictures = ['picture1.jpg', 'picture2.jpg', 'picture3.jpg']

# Case 1: auto build animations
auto_build_animations(videos, 'auto.animation.json', sample_fps=10, allow_translate=True)

# Case 2: manual

## Step 1: estimate poses
estimator = PoseEstimator()
wlm0, lm0 = estimator.auto_estimate(v0)  # use your own video
### or
wlm1, lm1 = estimator.estimate_timestamp(v0, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])  # 0.1s, 0.2s, ..., 1.0s
### or
wlm2, lm2 = estimator.estimate_frames(v0, [2, 3, 5, 7, 9, 11, 13, 15, 17, 19]) # the 2nd, 3rd, 5th, ... frames
### or
wlm3, lm3 = estimator.estimate_pictures(pictures)  # use a set of pictures to estimate poses

## Step 2: convert poses
pose_frames_list, transform_frames_list = [], []
for wlm, lm in zip([wlm0, wlm1, wlm2, wlm3], [lm0, lm1, lm2, lm3]):
    pose_frames_list.append(PoseConverter.calculate_poses(wlm0, smooth=True))
    transform_frames_list.append(
        PoseConverter.apply_translation(lm0))  # do not use pose world landmarks to calculate translation

## Step 3: build animations
aset = AnimationSet()
for i in range(len(pose_frames_list)):
    pose_frames = pose_frames_list[i]
    transform_frames = transform_frames_list[i]
    builder = AnimationBuilder(animation_name=f"animation{i}", animation_length=len(pose_frames) / 10, loop=False)
    for i, pose in enumerate(pose_frames):
        trans = transform_frames[i]  # [x, y, z]
        builder.add_keyframe("Body", time=i / 10, flag="position", values=trans)  # add translation
        for bone in BONES:                                                        # add rotation (pose)
            builder.add_keyframe(bone, time=1 / 10, flag="rotation", values=pose[bone])
    aset.append(builder)

# Step 4: save
aset.save("manual.animation.json")
```