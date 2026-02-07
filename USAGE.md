# 用法指南

本软件包 (`aff`) 提供了一套用于处理 Arcaea File Format (AFF) 谱面的 Python 工具库。

## 1. 引入库

将 `aff` 文件夹放置在您的项目目录下，并在 Python 脚本中引入：

```python
import aff
```

## 2. 核心功能

### 读取谱面 (Load)

**方式 1：直接从文件路径读取 (推荐)**

```python
chart = aff.from_file("path/to/chart.aff")
```

**方式 2：从文件对象读取**

```python
with open("path/to/chart.aff", "r", encoding="utf-8") as f:
    chart = aff.load(f)
```

**方式 3：从字符串读取**

```python
raw_content = "..."
chart = aff.loads(raw_content)
```

### 写入谱面 (Dump)

**方式 1：写入到文件对象**

```python
# 将 chart 对象写入到 output.aff
with open("output.aff", "w", encoding="utf-8") as f:
    aff.dump(chart, f)
```

**方式 2：序列化为字符串**

```python
# 获取格式化后的 AFF 字符串
aff_string = aff.dumps(chart)
print(aff_string)
```

## 3. 谱面操作示例

一旦读取了谱面（返回 `aff.AffChart` 对象），您就可以访问其属性进行修改或分析。

### 访问数据

```python
import aff

chart = aff.from_file("song.aff")

# 1. 访问头部信息
print(f"AudioOffset: {chart.header.audio_offset}")
print(f"Density: {chart.header.timing_point_density_factor}")

# 2. 遍历物件
for note in chart.notes:
    # 判断物件类型
    if isinstance(note, aff.Timing):
        print(f"Timing point: BPM {note.bpm} at {note.time}ms")
    elif isinstance(note, aff.Tap):
        print(f"Tap Note at {note.time}ms on lane {note.lane}")
    elif isinstance(note, aff.Arc):
        print(f"Arc: {note.start_time} -> {note.end_time}, Type: {note.arctype}")
```

### 创建新谱面

您也可以从零开始构建谱面。所有数据类都可以通过 `aff` 包直接访问。

```python
import aff

# 创建头部
header = aff.AffHeader(audio_offset=0, timing_point_density_factor=1.0)

# 创建物件列表
notes = []

# 添加 Timing (必须)
notes.append(aff.Timing(time=0, bpm=160.0, beats=4.0))

# 添加 Note (Tap)
notes.append(aff.Tap(time=1000, lane=1))  # 1轨道
notes.append(aff.Tap(time=1200, lane=2))  # 2轨道

# 添加 Hold
notes.append(aff.Hold(start_time=1500, end_time=2000, lane=3))

# 添加 Arc
notes.append(aff.Arc(
    start_time=2000, end_time=3000,
    start_x=0.0, end_x=1.0, easing='s',
    start_y=1.0, end_y=1.0,
    color=0, hitsound='none', arctype='false'
))

# 组装 Chart 对象
chart = aff.AffChart(header=header, notes=notes)

# 保存
with open("new_chart.aff", "w", encoding="utf-8") as f:
    aff.dump(chart, f)
```

## 4. 对象参考

所有对象均位于 `aff` 命名空间下。

| 对象类名 | 对应 AFF 语法 | 主要参数 |
| :--- | :--- | :--- |
| **aff.AffHeader** | `AudioOffset:...` | `audio_offset`, `timing_point_density_factor` |
| **aff.Timing** | `timing(t,bpm,beats)` | `time`, `bpm`, `beats` |
| **aff.Tap** | `(t,lane)` | `time`, `lane` |
| **aff.Hold** | `hold(t1,t2,lane)` | `start_time`, `end_time`, `lane` |
| **aff.Arc** | `arc(...)` | `start_time`, `end_time`, `start_x`, `end_x`, `easing`, `start_y`, `end_y`, `color`, `hitsound`, `arctype`, `smoothness` |
| **aff.Arctap** | `arctap(t)` | `time` (Arc 的子元素) |
| **aff.Camera** | `camera(...)` | `time`, `trans_x/y/z`, `angle_...`, `easing`, `duration` |
| **aff.SceneControl**| `scenecontrol(...)`| `time`, `type`, `param1`, `param2` |
| **aff.Flick** | `flick(...)` | `time`, `x`, `y`, `vx`, `vy` |
| **aff.TimingGroup** | `timinggroup(...){}` | `options`, `notes` |

> **注意**：所有物件的通常坐标范围为 x 取 -0.5 到 1.5，y 取 0 到 1。