from pathlib import Path
from typing import Iterable, Literal
import os
import cv2
import importlib.resources as pkg_resources

from .animation_unit import AnimationBuilder, AnimationSet
from .pose_estimator import VideoPoseEstimator
from .pose_converter import PoseConverter, BONES

__version__ = '0.1.0'
__all__ = ['VideoPoseEstimator', 'PoseConverter', 'AnimationBuilder', 'AnimationSet', 'BONES', "auto_estimate"]

def auto_estimate(videos: Iterable[str | Path],
                   out_json: str | Path,
                   sample_fps: float = 20.0,
                   model_complexity: Literal[0, 1, 2] = 1,
                   smooth: bool = True,
                   allow_translate: bool = False):
    """
    Estimate pose for all videos and merge them into a single animation json file, each video will be converted into a
     single animation which will be named same as the video file basename
    :param videos:  to video file
    :param out_json:  to output json file
    :param sample_fps:  frame rate to sample
    :param model_complexity:  0 for lite model, 1 for full model, 2 for heavy model
    :param smooth: whether to smooth pose estimation result
    :param allow_translate: allow model to do translation in animation json
    """
    animation_set = AnimationSet()
    vpe = VideoPoseEstimator(model_complexity=model_complexity)
    for vpath in videos:
        # open video
        cap = cv2.VideoCapture(vpath)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        animation_len = cap.get(cv2.CAP_PROP_FRAME_COUNT) / video_fps    # unit: seconds
        cap.release()
        world_landmark_frames, landmark_frames = vpe.estimate_timestamp(vpath, [i / sample_fps for i in range(int(animation_len * sample_fps))])
        animation_builder = AnimationBuilder(os.path.basename(vpath).split('.')[0], animation_len)
        for i, frame in enumerate(PoseConverter.calculate_poses(world_landmark_frames, smooth)):
            for bone in BONES:
                animation_builder.add_keyframe(bone, i / sample_fps, "rotation", frame[bone])
        if allow_translate:
            for i, trans in enumerate(PoseConverter.apply_translation(landmark_frames)):
                animation_builder.add_keyframe("Body", i / sample_fps, "position", trans)
        animation_set.append(animation_builder)
    animation_set.save(out_json)




def gen_basemodel(out: str | Path):
    """
    copy base model to given path
    :param out:  to output directory
    """
    bbmodel = pkg_resources.files('video2geckolib4') /'base_model.bbmodel'
    with bbmodel.open("rb") as f:
        with open(out, "wb") as o:
            o.write(f.read())
