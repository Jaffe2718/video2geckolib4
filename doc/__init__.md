# Documentation (`__init__.py`)

## Function `auto_build_animations()`
Estimate pose for all videos and merge them into a single GeckoLib4 animation json file, each video will be converted into a
single animation which will be named same as the video file basename

```
def auto_build_animations(videos: Iterable[str | Path],
                          out_json: str | Path,
                          sample_fps: float = 20.0,
                          model_complexity: Literal[0, 1, 2] = 1,
                          smooth: bool = True,
                          allow_translate: bool = False):
```

### Parameters

- `videos`: list of video paths
- `out_json`: to output json file
- `sample_fps`: frame rate to sample
- `model_complexity`: 0 for lite model, 1 for full model, 2 for heavy model
- `smooth`: whether to smooth pose estimation result
- `allow_translate`: allow model to do translation in animation json

### Example

```python
import video2geckolib4 as v2g

videos = ['video0.mp4', 'video1.mp4', 'video2.mp4', 'video3.mp4']
v2g.auto_build_animations(videos, 'out.animation.json', allow_translate=True)
```

## Function `gen_basemodel()`

Copy base model to given path

```
def gen_basemodel(out: str | Path):
```

### Parameters
- `out`: path to output base model

### Example

```python
import video2geckolib4 as v2g

v2g.gen_basemodel("my_model.bbmodel")
```