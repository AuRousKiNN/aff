from __future__ import annotations
from dataclasses import dataclass, field
import re

# ==============================================================================
# 1. 标识信息 (Header Info)
# ==============================================================================

@dataclass
class AffHeader:
    """
    谱面头部信息
    """
    audio_offset: int = 0
    """
    AudioOffset:x
    谱面整体向前(-)/向后(+)移动的毫秒数。
    """
    
    timing_point_density_factor: float = 1.0
    """
    TimingPointDensityFactor:y
    全局音弧与长条的物量密度调整为正常值的 y 倍。
    """

    def to_aff(self) -> str:
        return f"AudioOffset:{self.audio_offset}\nTimingPointDensityFactor:{self.timing_point_density_factor:.2f}\n-"

# ==============================================================================
# 3. Timing (定时器)
# ==============================================================================

@dataclass
class Timing:
    """
    timing(t,bpm,beats);
    """
    time: int
    """t (ms): 起始位置，非负整数。"""
    
    bpm: float
    """bpm: 节奏速度，小数。"""
    
    beats: float
    """
    beats: 每小节的四分音符个数（拍），小数。
    当 bpm 不为 0 时，beats 不可为 0。
    """

    def to_aff(self) -> str:
        return f"timing({self.time},{self.bpm:.2f},{self.beats:.2f});"

# ==============================================================================
# 4. 地面物件 (Tap & Hold)
# ==============================================================================

@dataclass
class Tap:
    """
    (t,lane);
    地面 Note
    """
    time: int
    """t (ms): 时间点。"""
    
    lane: float
    """
    lane (0-5 / float): 物件所在轨道。
    0-5 为轨道编号，float 为坐标定位 (-0.5 + lane * 2)。
    """

    def to_aff(self) -> str:
        lane_str = f"{self.lane:.2f}" if isinstance(self.lane, float) and not self.lane.is_integer() else f"{int(self.lane)}"
        return f"({self.time},{lane_str});"

@dataclass
class Hold:
    """
    hold(t1,t2,lane);
    地面 Hold
    """
    start_time: int
    """t1 (ms): 开始时间。"""
    
    end_time: int
    """t2 (ms): 结束时间。"""
    
    lane: float
    """lane (0-5 / float): 物件所在轨道。"""

    def to_aff(self) -> str:
        lane_str = f"{self.lane:.2f}" if isinstance(self.lane, float) and not self.lane.is_integer() else f"{int(self.lane)}"
        return f"hold({self.start_time},{self.end_time},{lane_str});"

# ==============================================================================
# 5. Arc & 天空音符 (Arctap)
# ==============================================================================

@dataclass
class Arctap:
    """
    arctap(tn)
    位于 Arc 内部的天键
    """
    time: int
    """tn (ms): 天键的时间点。"""

    def to_aff(self) -> str:
        return f"arctap({self.time})"

@dataclass
class Arc:
    """
    arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype,*smoothness)[...];
    音弧 / 音轨
    """
    start_time: int
    """t1 (ms): 开始时间。"""
    
    end_time: int
    """t2 (ms): 结束时间。"""
    
    start_x: float
    """x1: 开始时的横坐标 (小数)。"""
    
    end_x: float
    """x2: 结束时的横坐标 (小数)。"""
    
    easing: str
    """
    easing: 滑动方式 (b, s, si, so, siso, sisi 等)。
    """
    
    start_y: float
    """y1: 开始时的纵坐标 (小数)。"""
    
    end_y: float
    """y2: 结束时的纵坐标 (小数)。"""
    
    color: int
    """
    color: Arc 颜色。
    0: 蓝, 1: 红, 2: 绿, 3: 灰
    """
    
    hitsound: str
    """
    hitsound: 特殊打击音效 (e.g., 'glass_wav', 'none')。
    """
    
    arctype: str
    """
    arctype: 类型。
    'false': 音弧 (普通 Arc)
    'true': 音轨 (黑线)
    'designant': 表现为红偏粉音轨
    """
    
    smoothness: float | None = None
    """smoothness: (可选) 平滑度，控制 segment 细分数。"""
    
    arctaps: list[Arctap] = field(default_factory=list)
    """
    包含的天键列表。
    当 arctype=true 时，在 Arc 后接方括号定义。
    """

    def to_aff(self) -> str:
        smoothness_str = f",{int(self.smoothness)}" if self.smoothness is not None else ""
        base = f"arc({self.start_time},{self.end_time},{self.start_x:.2f},{self.end_x:.2f},{self.easing},{self.start_y:.2f},{self.end_y:.2f},{self.color},{self.hitsound},{self.arctype}{smoothness_str})"
        if self.arctaps:
            taps_str = ",".join([t.to_aff() for t in self.arctaps])
            return f"{base}[{taps_str}];"
        else:
            return f"{base};"

# ==============================================================================
# 6. Camera (相机)
# ==============================================================================

@dataclass
class Camera:
    """
    camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);
    """
    time: int
    """t (ms): 开始时间。"""
    
    trans_x: float
    """x (px): X轴移动距离。"""
    
    trans_y: float
    """y (px): Y轴移动距离。"""
    
    trans_z: float
    """z (px): Z轴移动距离。"""
    
    angle_xoz: float
    """xozAng (deg): XOZ平面旋转角度。"""
    
    angle_yoz: float
    """yozAng (deg): YOZ平面旋转角度。"""
    
    angle_xoy: float
    """xoyAng (deg): XOY平面旋转角度。"""
    
    easing: str
    """ease: 缓动类型 (qi, qo, reset, linear 等)。"""
    
    duration: int
    """duration (ms): 持续时间。"""

    def to_aff(self) -> str:
        return f"camera({self.time},{self.trans_x:.2f},{self.trans_y:.2f},{self.trans_z:.2f},{self.angle_xoz:.2f},{self.angle_yoz:.2f},{self.angle_xoy:.2f},{self.easing},{self.duration});"

# ==============================================================================
# 7. Scenecontrol (场景控制)
# ==============================================================================

@dataclass
class SceneControl:
    """
    scenecontrol(t,type,*param1,*param2);
    """
    time: int
    """t (ms): 时间点。"""
    
    type: str
    """
    type: 控制类型 (e.g., trackhide, redline, arcahvdistort)。
    """
    
    param1: float | None = None
    """param1 (float): 可选参数1 (如持续时间)。"""
    
    param2: int | None = None
    """param2 (int): 可选参数2 (如 alpha 值)。"""

    def to_aff(self) -> str:
        params = ""
        if self.param1 is not None:
            params += f",{self.param1:.2f}"
            if self.param2 is not None:
                params += f',{self.param2}'
        return f"scenecontrol({self.time},{self.type}{params});"

# ==============================================================================
# 9. Flick (未正式应用)
# ==============================================================================

@dataclass
class Flick:
    """
    flick(t,x,y,vx,vy);
    """
    time: int
    """t (ms): 时间点。"""
    
    x: float
    """x: 初始位置 X。"""
    
    y: float
    """y: 初始位置 Y。"""
    
    vx: float
    """vx: 滑动方向向量 X。"""
    
    vy: float
    """vy: 滑动方向向量 Y。"""

    def to_aff(self) -> str:
        return f"flick({self.time},{self.x:.2f},{self.y:.2f},{self.vx:.2f},{self.vy:.2f});"

# ==============================================================================
# 8. Timinggroup (定时组)
# ==============================================================================

@dataclass
class TimingGroup:
    """
    timinggroup(options){ ... };
    允许同时存在不同流速认的 Note。
    """
    options: list[str]
    """
    options: 选项列表，如 ['noinput', 'anglex200']。
    """
    
    notes: list[AffNote] = field(default_factory=list)
    """
    notes: 组内包含的所有 AFF 物件 (Timing, Note, Arc 等)。
    """

    def to_aff(self) -> str:
        options_str = "_".join(self.options)
        res = [f"timinggroup({options_str}){{"]
        for n in self.notes:
            res.append(f"  {n.to_aff()}")
        res.append("};")
        return "\n".join(res)

# 定义 AffNote 类型别名
AffNote = Timing | Tap | Hold | Arc | Camera | SceneControl | Flick | TimingGroup

class AffParser:
    """
    AFF 文件解析器
    """
    @staticmethod
    def parse_header(lines: list[str]) -> tuple[AffHeader, int]:
        header = AffHeader()
        idx = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if line == "-":
                idx = i + 1
                break
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if key == "AudioOffset":
                    header.audio_offset = int(val)
                elif key == "TimingPointDensityFactor":
                    header.timing_point_density_factor = float(val)
        return header, idx

    @staticmethod
    def parse_note(line: str) -> AffNote | None:
        line = line.strip()
        if not line or line.startswith("//"):
            return None

        # Timing: timing(t,bpm,beats);
        if m := re.match(r"timing\((\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)\);", line):
            return Timing(int(m.group(1)), float(m.group(2)), float(m.group(3)))

        # Tap: (t,lane);
        if m := re.match(r"\((\d+),([-+]?\d*\.?\d+)\);", line):
            return Tap(int(m.group(1)), float(m.group(2)))

        # Hold: hold(t1,t2,lane);
        if m := re.match(r"hold\((\d+),(\d+),([-+]?\d*\.?\d+)\);", line):
            return Hold(int(m.group(1)), int(m.group(2)), float(m.group(3)))

        # Arc: arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype[,smoothness])[arctap(t),...];
        if m := re.match(r"arc\((\d+),(\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),(\w+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),(\d+),(\w+),(\w+)(?:,(\d+))?\)(?:\[(.*)\])?;?", line):
            arctaps = []
            if m.group(12):
                tap_matches = re.findall(r"(?:arctap|at)\((\d+)\)", m.group(12))
                arctaps = [Arctap(int(t)) for t in tap_matches]
            
            return Arc(
                int(m.group(1)), int(m.group(2)),
                float(m.group(3)), float(m.group(4)),
                m.group(5),
                float(m.group(6)), float(m.group(7)),
                int(m.group(8)), m.group(9), m.group(10),
                float(m.group(11)) if m.group(11) else None,
                arctaps
            )

        # Camera: camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);
        if m := re.match(r"camera\((\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),(\w+),(\d+)\);", line):
            return Camera(
                int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)),
                float(m.group(5)), float(m.group(6)), float(m.group(7)),
                m.group(8), int(m.group(9))
            )

        # SceneControl: scenecontrol(t,type[,param1[,param2]]);
        if m := re.match(r"scenecontrol\((\d+),(\w+)(?:,([-+]?\d*\.?\d+))?(?:,(\d+))?\);", line):
            return SceneControl(
                int(m.group(1)), m.group(2),
                float(m.group(3)) if m.group(3) else None,
                int(m.group(4)) if m.group(4) else None
            )

        # Flick: flick(t,x,y,vx,vy);
        if m := re.match(r"flick\((\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)\);", line):
            return Flick(
                int(m.group(1)), float(m.group(2)), float(m.group(3)),
                float(m.group(4)), float(m.group(5))
            )

        return None

    @classmethod
    def parse_timing_group(cls, line: str, lines_iter) -> TimingGroup | None:
        if m := re.match(r"timinggroup\((.*)\)\{", line):
            options = m.group(1).split("_") if m.group(1) else []
            notes = []
            for sub_line in lines_iter:
                sub_line = sub_line.strip()
                if sub_line == "};":
                    break
                if sub_note := cls.parse_note(sub_line):
                    notes.append(sub_note)
            return TimingGroup(options, notes)
        return None

@dataclass
class AffChart:
    header: AffHeader = field(default_factory=AffHeader)
    notes: list[AffNote] = field(default_factory=list)

    def serialize(self) -> str:
        res = [self.header.to_aff()]
        for note in self.notes:
            res.append(note.to_aff())
        return "\n".join(res)

    def save(self, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.serialize())

    @classmethod
    def from_string(cls, content: str) -> 'AffChart':
        lines = content.splitlines()
        header, start_idx = AffParser.parse_header(lines)
        
        notes = []
        lines_iter = iter(lines[start_idx:])

        for line in lines_iter:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("timinggroup"):
                if tg := AffParser.parse_timing_group(line, lines_iter):
                    notes.append(tg)
            elif note := AffParser.parse_note(line):
                notes.append(note)
        
        return cls(header, notes)



    @classmethod

    def from_file(cls, file_path: str) -> 'AffChart':

        with open(file_path, 'r', encoding='utf-8') as f:

            return cls.from_string(f.read())