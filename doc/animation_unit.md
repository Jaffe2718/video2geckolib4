# Documentation (`animation_unit.py`)

## Class `AnimationBuilder`

Build animation from video.

### Method `__init__()`

```
def __init__(self, animation_name: str, animation_length: float, loop: bool = False):
```

#### Parameters
- `animation_name`: Name of the animation.
- `animation_length`: Length of the animation in seconds.
- `loop`: Whether the animation should loop.

### Method `add_keyframe()`

Add keyframe to animation

```
def add_keyframe(self,
                 bone: Literal["Body", "Head", "LeftUpperArm", "LeftForearm", "LeftThigh", "LeftCalf", "RightUpperArm", "RightForearm", "RightThigh", "RightCalf"],
                 time: float,
                 flag: Literal["rotation", "position", "scale"],
                 values: List[float],
                 easing: Dict | str | None = None,
                 **kwargs):
```

#### Parameters
- `bone`: bone name of `basemodel.bbmodel` model.
- `time`: time of animation. (unit: seconds)
- `flags`: flags of animation. (rotation, position, scale)
- `values`: values of animation. [x, y, z]
- `easing`: easing function of this keyframe.
- `**kwargs`: add <parameter>: <value> to animation.

### Method `get_animation()`
Get animation data.
```
def get_animation(self) -> Dict:
```

#### Return
- `Dict`: Animation data.

### Example
```python
from video2geckolib4 import AnimationBuilder
animation = AnimationBuilder("animation_name", 10)
animation.add_keyframe("Body", 0, "rotation", [0, 0, 0])
animation.add_keyframe("Body", 10, "rotation", [0, 90, 0])
print(animation.get_animation())
```

## Class `AnimationSet`
Merge multiple animation into a single animation set that can be exported to a single json file.

### Method `__init__()`

```
def __init__(self):
```

### Method `append()`

Add a animation builder to an existing animation set.

```
def append(self, animation_builder: AnimationBuilder):
```

#### Parameters
- `animation_builder`: The animation builder to add.

### Method `save()`
Save the animation set to a json file.

```
def save(self, file: Path | str):
```

#### Parameters
- `file`: The path to the json file.

### Example
```python
from video2geckolib4 import AnimationBuilder, AnimationSet

animation1 = AnimationBuilder("animation_name", 10)
animation1.add_keyframe("Body", 0, "rotation", [0, 0, 0])
animation1.add_keyframe("Body", 10, "rotation", [0, 90, 0])

animation2 = AnimationBuilder("animation_name", 5)
animation2.add_keyframe("Head", 0, "rotation", [0, 0, 90])
animation2.add_keyframe("Head", 5, "rotation", [0, 90, 0])

animation_set = AnimationSet()
animation_set.append(animation1)
animation_set.append(animation2)

animation_set.save("export.animation.json")
```
