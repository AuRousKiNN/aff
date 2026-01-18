from .core import (
    AffChart,
    AffHeader,
    Timing,
    Tap,
    Hold,
    Arc,
    Arctap,
    Camera,
    SceneControl,
    Flick,
    TimingGroup,
    AffNote,
    AffParser,
)

def load(fp) -> AffChart:
    """
    Deserialize fp (a .read()-supporting file-like object) to an AffChart.
    """
    return AffChart.from_string(fp.read())

def loads(s: str) -> AffChart:
    """
    Deserialize s (a str instance) to an AffChart.
    """
    return AffChart.from_string(s)

def dump(obj: AffChart, fp):
    """
    Serialize obj as a AFF formatted stream to fp (a .write()-supporting file-like object).
    """
    fp.write(obj.serialize())

def dumps(obj: AffChart) -> str:
    """
    Serialize obj to a AFF formatted str.
    """
    return obj.serialize()

def from_file(path: str) -> AffChart:
    """
    Load an AffChart from a file path.
    """
    return AffChart.from_file(path)

__all__ = [
    "AffChart",
    "AffHeader",
    "Timing",
    "Tap",
    "Hold",
    "Arc",
    "Arctap",
    "Camera",
    "SceneControl",
    "Flick",
    "TimingGroup",
    "AffNote",
    "AffParser",
    "load",
    "loads",
    "dump",
    "dumps",
    "from_file",
]
