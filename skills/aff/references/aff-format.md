# Arcaea File Format（AFF）格式参考

## 目录

- [标识信息](#标识信息)
- [分隔符](#分隔符)
- [Timing](#timing)
- [地面物件](#地面物件)
- [Arc 与 Arctap](#arc-与-arctap)
- [Camera](#camera)
- [SceneControl](#scenecontrol)
- [TimingGroup](#timinggroup)
- [Flick](#flick)
- [结构总结](#结构总结)

## 标识信息

所有谱面文件开头必须包含标识信息。

### AudioOffset

```text
AudioOffset:x
```

- `x`：谱面整体向前（负）或向后（正）移动的毫秒数。
- 一般为 0；此时物件毫秒数就是歌曲播放进度。
- 非 0 时，物件在音乐中实际对应的毫秒数为“物件时间 + x”。

### TimingPointDensityFactor

```text
TimingPointDensityFactor:y
```

- `y`：全局音弧与长条物量密度相对正常值的倍率。
- `y=1` 与省略此行效果相同。

## 分隔符

```text
-
```

从第一个 `-` 所在行之后开始读取谱面物件。其前可加入 `ChartVersion:2` 等自定义标识；游戏会记录，但不会产生实际效果。

## Timing

```text
timing(t,bpm,beats);
```

每个谱面必须有一个 `t=0` 的 Timing。

- `t`（ms）：非负整数起始位置；每个 Timing 都会在 `t` 处生成小节线。
- `bpm`：节奏速度，小数。
- `beats`：每小节的四分音符拍数，小数，如 `4.00` 表示 4/4 拍。`bpm != 0` 时不得为 0，否则可能除零崩溃。

## 地面物件

### Note

```text
(t,lane);
```

### Hold

```text
hold(t1,t2,lane);
```

- `t`、`t1`、`t2`（ms）：非负整数；Hold 必须满足 `t1 < t2`。
- `lane`（0–5 或 float）：从左到右为 0、1、2、3、4、5，通常只用 1–4。
- 开启 `enwidenlanes` 后轨道扩为六条，新增 0 轨和 5 轨。
- float lane 表示坐标定位，映射公式为 `-0.5 + lane * 2`。建议只用于演出 Note，因为判定与普通轨道不同。

## Arc 与 Arctap

### Arc

```text
arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype,*smoothness);
```

带 `*` 的参数可选。

- `t1`、`t2`（ms）：开始和结束时间。允许相等；相等时与判定线平行，物量为 0。
- `x1`、`x2`：开始和结束横坐标。
- `y1`、`y2`：开始和结束纵坐标。
- `easing`：滑动方式。
  - `b`：Bezier，可视为前半 soso、后半 sisi。
  - `s`：直线。
  - `si`：Sine Out；注意名称方向与常见直觉相反。
  - `so`：Sine In。
  - `sisi`、`siso`、`sosi`、`soso`：第一个部分控制 x，第二个部分控制 y。例如 `siso` 表示 x 为 sine out、y 为 sine in。
- `color`：0 蓝、1 红、2 绿、3 灰。
- `hitsound`：v4.0.0 起支持特殊打击音效。`glass_wav` 会读取 `songs/(songid)/glass.wav`；`none` 表示不应用。
- `arctype`：
  - `false`：普通音弧。
  - `true`：黑线音轨；若含 Arctap 且不是 `designant`，会自动转为音轨。
  - `designant`：红偏粉音轨，不计 Combo 和 HP，只在特定异象下生效。
- `smoothness`：v6.8.0 起支持的平滑度，控制 segment 细分数，默认值和最小值均为 1。

Python `Arc` dataclass 字段依次为：`start_time`、`end_time`、`start_x`、`end_x`、`easing`、`start_y`、`end_y`、`color`、`hitsound`、`arctype`、可选 `smoothness`、`arctaps`。

### Arctap

当 `arctype=true` 时，在 Arc 后追加方括号：

```text
arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,true,*smoothness)[arctap(tn1),arctap(tn2),...];
```

- `tn`（ms）必须位于 `[t1, t2]`。
- `arctap` 可简写为 `at`。

### 横缩放 Arctap（color=3 专用）

```text
arc(t,t,x1,x2,easing,y,y,3,hitsound,false,*smoothness);
```

时间点为 `t`，横坐标从 `x1` 到 `x2`，线段长度即缩放后的长度。

## Camera

v1.6.1 实装：

```text
camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);
```

- `t`（ms）：开始时间。
- `x`、`y`、`z`（px）：三轴移动距离。Arc 坐标 1.00 约对应 x 轴 850、y 轴 450 的位移。
- `xozAng`、`yozAng`、`xoyAng`（度）：三轴旋转角度。
- `ease`：`qi` 为 Cubic in，`qo` 为 Cubic out，`reset` 重置状态，其他值按 Linear 处理。
- `duration`（ms）：持续时间。
- `ease` 不是 `reset` 时，会关闭 Arc 对 Camera 的自动倾斜控制。

## SceneControl

v2.6.1 实装：

```text
scenecontrol(t,type,*param1,*param2);
```

`param1` 为可选 float，`param2` 为可选 int。常用类型：

- `trackhide` / `trackshow`：隐藏或显示轨道。
- `trackdisplay`：控制轨道透明度；`param1` 为变换秒数，`param2` 为目标 alpha（0–255）。
- `redline`：v3.0.0 起的背景红线效果；`param1` 为持续秒数。
- `arcahvdistort` / `arcahvdebris`：Arcahv 背景特效。
- `hidegroup`：隐藏特定 TimingGroup 内的 Note；`param2` 为 1 时隐藏、0 时显示。
- `enwidencamera` / `enwidenlanes`：相机远摄或轨道扩充；`param1` 为持续时长（ms），`param2` 为 1 时淡入、0 时淡出。

## TimingGroup

v3.0.0 实装，允许同时存在不同流速的 Note：

```text
timinggroup(options){
  // 正常 AFF 语句
};
```

- 组内必须至少包含一条 `timing`，且组内 Timing 不产生小节线。
- `options` 可用下划线叠加，如 `noinput_anglex200`。
- `noinput`：物件只显示，无判定，不计物量。
- `fadingholds`：未击中 Hold 时渐变透明。
- `anglex` / `angley`：v3.12.6 起旋转天键轨迹，参数为“旋转角度 × 10”；只影响轨迹显示，不影响判定。

Python 中 `TimingGroup.options` 是 `list[str]`，内部物件位于 `notes`，处理时必须递归。

## Flick

```text
flick(t,x,y,vx,vy);
```

- `t`（ms）：时间点。
- `x`、`y`：初始位置。
- `vx`、`vy`：滑动方向向量。
- 官方谱面目前尚未正式应用此物件，谨慎使用。

## 结构总结

通常按以下顺序排列：

1. `AudioOffset` 等标识信息。
2. 分隔符 `-`。
3. Timing、Note、Arc 等正常 AFF 语句。

标识信息内部以及 AFF 语句内部的内容顺序均不受限制。
