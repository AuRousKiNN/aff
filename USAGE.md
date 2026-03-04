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

所有对象均位于 `aff` 命名空间下。以下是各对象的构造函数参数及其对应 AFF 语法的详细说明。

### 4.1. AffHeader (头部信息)

对应 AFF 中的 `AudioOffset` 和 `TimingPointDensityFactor`。

*   **`audio_offset` (int)**:
    *   对应 `AudioOffset:x` 中的 `x`。
    *   谱面整体向前(-)/向后(+)移动的毫秒数。一般情况下为 0。
    *   如果不为 0，物件实际时间 = 物件定义时间 + audio_offset。

*   **`timing_point_density_factor` (float)**:
    *   对应 `TimingPointDensityFactor:y` 中的 `y`。
    *   全局音弧与长条的物量密度调整系数。默认值为 1.0。

### 4.2. Timing

对应 AFF 语法: `timing(t,bpm,beats);`

*   **`time` (int)**:
    *   对应 `t`。起始位置（毫秒），非负整数。
    *   每个 Timing 都会在此处生成一条小节线。
*   **`bpm` (float)**:
    *   对应 `bpm`。节奏速度（Beats Per Minute）。
*   **`beats` (float)**:
    *   对应 `beats`。每小节的四分音符个数（拍数）。
    *   例如 `4.00` 代表 4/4 拍。注意：当 `bpm` 不为 0 时，`beats` 不可为 0。

### 4.3. Tap

对应 AFF 语法: `(t,lane);`

*   **`time` (int)**:
    *   对应 `t`。打击时间点（毫秒）。
*   **`lane` (float)**:
    *   对应 `lane`。物件所在轨道。
    *   **0-5**: 轨道编号（0 为最左，5 为最右）。正常模式下使用 1-4 轨。
    *   **小数**: 表示精确坐标定位。映射公式为 `-0.5 + lane * 2`。

### 4.4. Hold

对应 AFF 语法: `hold(t1,t2,lane);`

*   **`start_time` (int)**:
    *   对应 `t1`。开始时间（毫秒）。
*   **`end_time` (int)**:
    *   对应 `t2`。结束时间（毫秒）。必须满足 `t1 < t2`。
*   **`lane` (float)**:
    *   对应 `lane`。物件所在轨道（同 `Tap`）。

### 4.5. Arc

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

### 4.6. Arctap

对应 AFF 语法: `arctap(t)` (位于 Arc 内部)

*   **`time` (int)**:
    *   对应 `t`。天键的时间点。必须在所属 Arc 的时间范围内。

### 4.7. Camera

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

### 4.8. SceneControl

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

### 4.9. TimingGroup

对应 AFF 语法: `timinggroup(options){ ... };`

*   **`options` (list[str])**:
    *   对应 `options`。选项列表（以下划线分隔）。
    *   `noinput`: 无判定模式。
    *   `fadingholds`: Hold 漏键渐隐。
    *   `anglex<val>` / `angley<val>`: 旋转天键轨迹。
*   **`notes` (list[AffNote])**:
    *   对应 `{ ... }` 内部的内容。包含该组内的所有物件。

### 4.10. Flick

对应 AFF 语法: `flick(t,x,y,vx,vy);` (实验性功能)

*   **`time` (int)**:
    *   对应 `t`。时间点。
*   **`x` (float)**, **`y` (float)**:
    *   对应 `x, y`。初始坐标。
*   **`vx` (float)**, **`vy` (float)**:
    *   对应 `vx, vy`。滑动方向向量。

**注意**
 - Timing里的bpm是用来决定谱面流速的，它与实际曲目的bpm无关。当timing bpm和歌曲bpm的比值为1时为标准谱面流速，比值为2时快一倍，比值为0.5时为慢一半等。
