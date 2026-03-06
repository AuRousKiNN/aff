# aff-parser

`aff-parser` 提供了一套用于解析、处理和生成 Arcaea File Format (AFF) 谱面的 Python 工具库。

## 特性 (Features)

- **解析与序列化**：轻松地将 `.aff` 文件读取为 Python 对象，或将 Python 对象输出为标准的 AFF 格式字符串。
- **全物件支持**：完整支持 Tap, Hold, Arc, Arctap, Camera, SceneControl, TimingGroup 等几乎所有的 AFF 谱面物件。
- **类型安全**：核心代码基于 `dataclass` 构建，支持严格的 Mypy 类型检查，提供良好的 IDE 提示。
- **易于修改**：通过面向对象的方式轻松修改、遍历和分析现有谱面。

## 安装 (Installation)

目前推荐通过源码进行本地安装。支持 Python 3.10 及以上版本。

```bash
# 克隆仓库
git clone <repository_url>
cd aff

# 使用 pip 进行可编辑安装
python -m pip install -e .
```

## 快速开始 (Quick Start)

### 1. 读取谱面 (Load)

```python
import aff

# 推荐：直接从文件路径读取
chart = aff.from_file("path/to/chart.aff")

# 从文件对象读取
with open("path/to/chart.aff", "r", encoding="utf-8") as f:
    chart = aff.load(f)

# 从字符串读取
raw_content = "..."
chart = aff.loads(raw_content)
```

### 2. 访问和修改数据

一旦读取了谱面（返回 `aff.AffChart` 对象），就可以访问其属性进行修改或分析。

```python
import aff

chart = aff.from_file("song.aff")

# 访问头部信息
print(f"AudioOffset: {chart.header.audio_offset}")
print(f"Density: {chart.header.timing_point_density_factor}")

# 遍历物件
for note in chart.notes:
    if isinstance(note, aff.Timing):
        print(f"Timing point: BPM {note.bpm} at {note.time}ms")
    elif isinstance(note, aff.Tap):
        print(f"Tap Note at {note.time}ms on lane {note.lane}")
    elif isinstance(note, aff.Arc):
        print(f"Arc: {note.start_time} -> {note.end_time}, Type: {note.arctype}")
```

### 3. 创建与写入谱面 (Dump)

您可以从零开始构建谱面，并将其写入文件或序列化为字符串。

```python
import aff

# 创建头部
header = aff.AffHeader(audio_offset=0, timing_point_density_factor=1.0)

# 组建物件列表
notes = [
    aff.Timing(time=0, bpm=160.0, beats=4.0),
    aff.Tap(time=1000, lane=1),
    aff.Hold(start_time=1500, end_time=2000, lane=3),
    aff.Arc(
        start_time=2000, end_time=3000,
        start_x=0.0, end_x=1.0, easing='s',
        start_y=1.0, end_y=1.0,
        color=0, hitsound='none', arctype='false'
    )
]

# 组装 Chart 对象
chart = aff.AffChart(header=header, notes=notes)

# 写入到文件
with open("new_chart.aff", "w", encoding="utf-8") as f:
    aff.dump(chart, f)

# 或者直接获取字符串
print(aff.dumps(chart))
```

## API / 物件参考 (API Reference)

所有对象均位于 `aff` 命名空间下。以下是各对象的构造函数参数及其对应 AFF 语法的详细说明。

### AffHeader (头部信息)

对应 AFF 中的 `AudioOffset` 和 `TimingPointDensityFactor`。

*   **`audio_offset` (int)**:
    *   对应 `AudioOffset:x` 中的 `x`。
    *   谱面整体向前(-)/向后(+)移动的毫秒数。一般情况下为 0。
    *   如果不为 0，物件实际时间 = 物件定义时间 + audio_offset。

*   **`timing_point_density_factor` (float)**:
    *   对应 `TimingPointDensityFactor:y` 中的 `y`。
    *   全局音弧与长条的物量密度调整系数。默认值为 1.0。

### Timing

对应 AFF 语法: `timing(t,bpm,beats);`

*   **`time` (int)**:
    *   对应 `t`。起始位置（毫秒），非负整数。
    *   每个 Timing 都会在此处生成一条小节线。
*   **`bpm` (float)**:
    *   对应 `bpm`。节奏速度（Beats Per Minute）。
*   **`beats` (float)**:
    *   对应 `beats`。每小节的四分音符个数（拍数）。
    *   例如 `4.00` 代表 4/4 拍。注意：当 `bpm` 不为 0 时，`beats` 不可为 0。

### Tap

对应 AFF 语法: `(t,lane);`

*   **`time` (int)**:
    *   对应 `t`。打击时间点（毫秒）。
*   **`lane` (float)**:
    *   对应 `lane`。物件所在轨道。
    *   **0-5**: 轨道编号（0 为最左，5 为最右）。正常模式下使用 1-4 轨。
    *   **小数**: 表示精确坐标定位。映射公式为 `-0.5 + lane * 2`。

### Hold

对应 AFF 语法: `hold(t1,t2,lane);`

*   **`start_time` (int)**:
    *   对应 `t1`。开始时间（毫秒）。
*   **`end_time` (int)**:
    *   对应 `t2`。结束时间（毫秒）。必须满足 `t1 < t2`。
*   **`lane` (float)**:
    *   对应 `lane`。物件所在轨道（同 `Tap`）。

### Arc

对应 AFF 语法: `arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype,smoothness)[...];`

*   **`start_time` (int)**:
    *   对应 `t1`。开始时间。
*   **`end_time` (int)**:
    *   对应 `t2`。结束时间。若 `t1 == t2`，则为无物量的装饰性音弧（黑线）。
*   **`start_x` (float)**:
    *   对应 `x1`。起始横坐标。范围通常为 -0.5 到 1.5。
*   **`end_x` (float)**:
    *   对应 `x2`。结束横坐标。
*   **`easing` (str)**:
    *   对应 `easing`。滑动方式。
    *   `b`: Bezier (贝塞尔), `s`: Straight (直线), `si`: Sine Out (正弦渐出), `so`: Sine In (正弦渐入)。
    *   支持组合（如 `siso`），分别控制 x 和 y 方向。以下是所有组合: `sisi`, `soso`, `siso`, `sosi`，其余的组合非法。
*   **`start_y` (float)**:
    *   对应 `y1`。起始纵坐标。范围通常为 0.0 到 1.0（1.0 为判定线最高点）。
*   **`end_y` (float)**:
    *   对应 `y2`。结束纵坐标。
*   **`color` (int)**:
    *   对应 `color`。颜色索引。
    *   `0`: 蓝, `1`: 红, `2`: 绿, `3`: 灰。
*   **`hitsound` (str)**:
    *   对应 `hitsound`。特殊打击音效（如 `glass_wav`）。`none` 表示无特殊音效。
*   **`arctype` (str)**:
    *   对应 `arctype`。
    *   `false`: 普通音弧（有判定）。
    *   `true`: 黑线/音轨（无判定）。
    *   `designant`: 红色装饰线（仅特定异象生效）。
*   **`smoothness` (float | None)**:
    *   对应 `smoothness`。平滑度（segment 细分数）。默认为 None（即 1.0）。
*   **`arctaps` (list[Arctap])**:
    *   对应 `[...]` 中的 `arctap(tn)`。该 Arc 上附着的天键列表。

### Arctap

对应 AFF 语法: `arctap(t)` (位于 Arc 内部)

*   **`time` (int)**:
    *   对应 `t`。天键的时间点。必须在所属 Arc 的时间范围内。

### Camera

对应 AFF 语法: `camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);`

*   **`time` (int)**:
    *   对应 `t`。动作开始时间。
*   **`trans_x` (float)**:
    *   对应 `x`。X 轴平移距离（像素）。
*   **`trans_y` (float)**:
    *   对应 `y`。Y 轴平移距离（像素）。
*   **`trans_z` (float)**:
    *   对应 `z`。Z 轴平移距离（像素）。
*   **`angle_xoz` (float)**:
    *   对应 `xozAng`。XOZ 平面旋转角度（度）。
*   **`angle_yoz` (float)**:
    *   对应 `yozAng`。YOZ 平面旋转角度（度）。
*   **`angle_xoy` (float)**:
    *   对应 `xoyAng`。XOY 平面旋转角度（度）。
*   **`easing` (str)**:
    *   对应 `ease`。缓动类型。
    *   `qi`: Cubic in, `qo`: Cubic out, `reset`: 重置, `l`: Linear。
*   **`duration` (int)**:
    *   对应 `duration`。持续时间（毫秒）。

### SceneControl

对应 AFF 语法: `scenecontrol(t,type,param1,param2);`

*   **`time` (int)**:
    *   对应 `t`。生效时间。
*   **`type` (str)**:
    *   对应 `type`。控制类型。
    *   常见值: `trackhide` (隐藏轨道), `trackshow` (显示轨道), `redline` (红线背景), `arcahvdistort` (Arcahv特效) 等。
*   **`param1` (float | None)**:
    *   对应 `param1`。可选参数 1（通常为持续时间，单位秒或毫秒，取决于类型）。
*   **`param2` (int | None)**:
    *   对应 `param2`。可选参数 2（如目标 Alpha 值）。

### TimingGroup

对应 AFF 语法: `timinggroup(options){ ... };`

*   **`options` (list[str])**:
    *   对应 `options`。选项列表（以下划线分隔）。
    *   `noinput`: 无判定模式。
    *   `fadingholds`: Hold 漏键渐隐。
    *   `anglex<val>` / `angley<val>`: 旋转天键轨迹。
*   **`notes` (list[AffNote])**:
    *   对应 `{ ... }` 内部的内容。包含该组内的所有物件。

### Flick

对应 AFF 语法: `flick(t,x,y,vx,vy);` (实验性功能)

*   **`time` (int)**:
    *   对应 `t`。时间点。
*   **`x` (float)**, **`y` (float)**:
    *   对应 `x, y`。初始坐标。
*   **`vx` (float)**, **`vy` (float)**:
    *   对应 `vx, vy`。滑动方向向量。

> **注意**：Timing 里的 BPM 用来决定谱面流速，与实际曲目的 BPM 无关。

## 开发与测试 (Development)

本项目使用 `pytest` 进行测试，使用 `mypy` 进行检查。

```bash
# 运行测试
python -m pytest

# 运行基础冒烟测试
python test_real_chart.py

# 运行严格的类型检查
python -m mypy aff
```
