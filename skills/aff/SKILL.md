---
name: aff
description: Arcaea AFF 谱面文件的 Python 解析、检查、修改、生成与序列化指南。处理 .aff 文件、Arcaea 谱面物件，或使用 aff Python 库操作 Timing、Tap、Hold、Arc、Arctap、Camera、SceneControl、Flick、TimingGroup 时使用。
---

# aff 库使用指南

使用 `aff` Python 库解析、修改和生成 Arcaea File Format（AFF）谱面。Python 版本须为 3.10 或更高。

## 工作流程

1. 先检查仓库现有代码、依赖与本地约定，复用已有的谱面处理入口和辅助函数。
2. 用 `aff.from_file` 读取路径，或用 `aff.load`、`aff.loads` 读取文件对象或字符串。
3. 遍历 `chart.notes`；遇到 `TimingGroup` 时递归处理其 `notes`。
4. 构建或修改 dataclass。注意字段顺序与 AFF 语法参数顺序一致，并遵守各物件约束。
5. 用 `chart.save`、`aff.dump` 或 `aff.dumps` 输出。
6. 重新读取输出并验证：必须存在 `t=0` 的 `Timing`，时间与范围合法，嵌套组结构完整，序列化可往返。

需要确认 AFF 原始语法、easing 含义、特殊物件、坐标或版本行为时，读取 [AFF 格式参考](references/aff-format.md)。

## 安装

在库源码目录中安装可编辑版本：

```bash
python -m pip install -e .
```

## 核心 API

```python
import aff
```

### 读取与写入

| 操作 | API |
|---|---|
| 从路径加载 | `aff.from_file("chart.aff")` |
| 从文件对象加载 | `aff.load(open("chart.aff"))`，类似 `json.load` |
| 从字符串加载 | `aff.loads("AudioOffset:0\n-\n...")`，类似 `json.loads` |
| 写入路径 | `chart.save("out.aff")` |
| 写入文件对象 | `aff.dump(chart, open("out.aff", "w"))`，类似 `json.dump` |
| 序列化为字符串 | `aff.dumps(chart)`，类似 `json.dumps` |

### 访问谱面数据

```python
chart.header                 # AffHeader
chart.header.audio_offset    # int，音频偏移量
chart.header.timing_point_density_factor  # float
chart.notes                  # list[AffNote]，所有谱面物件
```

### 遍历物件

```python
def visit(notes):
    for note in notes:
        if isinstance(note, aff.Timing):
            print(note.time, note.bpm, note.beats)
        elif isinstance(note, aff.Tap):
            print(note.time, note.lane)
        elif isinstance(note, aff.Hold):
            print(note.start_time, note.end_time, note.lane)
        elif isinstance(note, aff.Arc):
            print(note.start_time, note.end_time, note.easing, note.color)
            for arctap in note.arctaps:
                print(arctap.time)
        elif isinstance(note, aff.Camera):
            print(note.time, note.trans_x, note.trans_y, note.easing)
        elif isinstance(note, aff.SceneControl):
            print(note.time, note.type, note.param1, note.param2)
        elif isinstance(note, aff.Flick):
            print(note.time, note.x, note.y, note.vx, note.vy)
        elif isinstance(note, aff.TimingGroup):
            print(note.options)
            visit(note.notes)

visit(chart.notes)
```

### 构建谱面

```python
from aff import AffChart, AffHeader, Timing, Tap, Hold, Arc, Arctap

chart = AffChart(
    header=AffHeader(audio_offset=0),
    notes=[
        Timing(time=0, bpm=180.0, beats=4.0),
        Tap(time=1000, lane=1),
        Hold(start_time=2000, end_time=3000, lane=2),
        Arc(
            start_time=4000,
            end_time=5000,
            start_x=0.0,
            end_x=1.0,
            easing="s",
            start_y=1.0,
            end_y=1.0,
            color=0,
            hitsound="none",
            arctype="true",
            arctaps=[Arctap(time=4500)],
        ),
    ],
)
```

## Python 对象速查

| 类 | AFF 语法 | 关键字段 |
|---|---|---|
| `AffHeader` | `AudioOffset:0`、`TimingPointDensityFactor:1.00` | `audio_offset`, `timing_point_density_factor` |
| `Timing` | `timing(t,bpm,beats);` | `time`, `bpm`, `beats` |
| `Tap` | `(t,lane);` | `time`, `lane`（float） |
| `Hold` | `hold(t1,t2,lane);` | `start_time`, `end_time`, `lane` |
| `Arc` | `arc(...)[arctap(),...];` | `start_time`, `end_time`, `start_x`, `end_x`, `easing`, `start_y`, `end_y`, `color`, `hitsound`, `arctype`, `smoothness`, `arctaps` |
| `Arctap` | `arctap(t)` | `time` |
| `Camera` | `camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);` | `time`, `trans_x`, `trans_y`, `trans_z`, `angle_xoz`, `angle_yoz`, `angle_xoy`, `easing`, `duration` |
| `SceneControl` | `scenecontrol(t,type[,param1,param2]);` | `time`, `type`, `param1`, `param2` |
| `Flick` | `flick(t,x,y,vx,vy);` | `time`, `x`, `y`, `vx`, `vy` |
| `TimingGroup` | `timinggroup(options){notes};` | `options`, `notes` |

## 关键约束

- `Arc.easing` 只能为 `b`、`s`、`si`、`so`、`siso`、`sisi`、`soso`、`sosi`。
- `si` 表示 x 方向 sine out，`so` 表示 x 方向 sine in；组合 easing 的第一个部分控制 x，第二个部分控制 y。
- `Arc.color` 必须为 0–3 的整数。
- 每个 `Arctap.time` 必须落在对应 Arc 的 `[start_time, end_time]` 内；`Arc.__post_init__` 会验证 easing、color 和 arctap 时间范围。
- `TimingGroup.options` 中的字符串以 `_` 连接，如 `["noinput", "anglex200"]` 序列化为 `noinput_anglex200`。
- 浮点数统一保留两位；整数值的 `Tap.lane` 不输出小数；float 类型的 `BaseArc.lane` 保留两位。
- “天键”指 arctap。“单天键/单 arctap”指首尾坐标相同、持续 1 ms、且开始时刻含一个 arctap 的黑线。
- 不要在解析或修改 `Arc.arctaps` 时混淆所属 Arc 的时间范围。

本指南内容按 MIT 许可提供；原始兼容性标注为 `opencode`。
