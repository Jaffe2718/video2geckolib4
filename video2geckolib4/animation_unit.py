from pathlib import Path
from typing import *
import json

class AnimationBuilder:
    """
    Build animation from video.
    """

    def __init__(self, animation_name: str, animation_length: float, loop: bool = False):
        self.animation_name = animation_name
        self.animation_data = {
            "loop": loop,
            "animation_length": animation_length,
            "bones": {}
        }


    def add_keyframe(self,
                     bone: Literal["Body", "Head", "LeftUpperArm", "LeftForearm", "LeftThigh", "LeftCalf", "RightUpperArm", "RightForearm", "RightThigh", "RightCalf"],
                     time: float,
                     flag: Literal["rotation", "position", "scale"],
                     values: List[float],
                     easing: Dict | str | None = None,
                     **kwargs):
        """
        Add keyframe to animation.
        :param bone: bone name of `basemodel.bbmodel` model.
        :param time: time of animation. (unit: seconds)
        :param flag: flags of animation. (rotation, position, scale)
        :param values: values of animation. [x, y, z]
        :param easing: easing function of this keyframe.
        :param kwargs: add <parameter>: <value> to animation.
        """
        if bone not in self.animation_data["bones"]:
            self.animation_data["bones"][bone] = {}
        if flag not in self.animation_data["bones"][bone]:
            self.animation_data["bones"][bone][flag] = {}
        self.animation_data["bones"][bone][flag][f"{time}"] = {
            "vector": values
        }
        if easing is not None:
            self.animation_data["bones"][bone][flag][f"{time}"]["easing"] = easing
        for key, value in kwargs.items():
            self.animation_data["bones"][bone][flag][f"{time}"][key] = value



    def get_animation(self) -> Dict:
        return self.animation_data


class AnimationSet:
    """
    Merge multiple animation into a single animation set that can be exported to a single json file.
    """

    def __init__(self):
        self.data = {
            "format_version": "1.8.0",
            "animations": {}
        }

    def append(self, animation_builder: AnimationBuilder):
        """
        Add a animation builder to an existing animation set.
        :param animation_builder: The animation builder to add.
        :return:
        """
        self.data["animations"][animation_builder.animation_name] = animation_builder.animation_data


    def save(self, file: Path | str):
        with open(file, "w") as f:
            json.dump(self.data, f, indent=4)