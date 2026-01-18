# Arcaea File Format (AFF) 格式参考

## 1. 标识信息
所有谱面文件开始部分都必须包含以下内容：

### AudioOffset
```text
AudioOffset:x
```
*   **x**: 谱面整体向前(-)/向后(+)移动的毫秒数。
*   一般情况下 `x=0`，此时物件对应的毫秒数即为歌曲播放进度的毫秒数。
*   如果 `x≠0`，物件在音乐中实际对应的毫秒数 = 物件时间 + x。

### TimingPointDensityFactor
```text
TimingPointDensityFactor:y
```
*   **y**: 全局音弧与长条的物量密度调整为正常值的 y 倍。
*   `y=1` 时效果与省略此行相同。

---

## 2. 分隔符
```text
-
```
*   物件的读取从第一个 `-` 所在的行之后开始。
*   在第一个 `-` 之前，可以编写自定义标识信息（例如 `ChartVersion:2`），游戏会记录相关数据但不会产生实际效果。

---

## 3. Timing
```text
timing(t,bpm,beats);
```
每个谱面必须有一个 `t=0` 的 Timing。

*   **t (ms)**: 起始位置，非负整数。每个 Timing 都会在 t 处生成一条小节线。
*   **bpm**: 节奏速度，小数。
*   **beats**: 每小节的四分音符个数（拍），小数。
    *   当 bpm 不为 0 时，beats 不可为 0（否则会导致除零错误崩溃）。例如 `4.00` 代表 4/4 拍。

---

## 4. 地面物件 (Note & Hold)

### 地面 Note
```text
(t,lane);
```

### 地面 Hold
```text
hold(t1,t2,lane);
```

**参数说明：**
*   **t / t1 / t2 (ms)**: 时间点，非负整数。Hold 须满足 `t1 < t2`。
*   **lane (0-5 / float)**: 物件所在轨道。
    *   轨道编号从左到右依次为 0, 1, 2, 3, 4, 5。
    *   正常情况下仅使用 1-4 号轨。
    *   若开启 `enwidenlanes`，轨道扩充至 6 条（新增 0 轨与 5 轨）。
    *   **lane 为 float 时**: 表示以坐标定位。映射公式为 `-0.5 + lane * 2`。建议仅用于演出类 Note，因为判定与正常轨道不同。

---

## 5. Arc & 天空音符 (Arctap)

### Arc (音弧)
```text
arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype,*smoothness);
```
*(带 `*` 的为可选参数)*

*   **t1, t2 (ms)**: 开始/结束时间。`t1` 可以等于 `t2`（此时与判定线平行，物量为 0）。
*   **x1, x2**: 开始/结束时的横坐标 (小数)。
*   **y1, y2**: 开始/结束时的纵坐标 (小数)。
*   **easing**: 滑动方式。
    *   `b`: Bezier (贝塞尔)
    *   `s`: Straight (直线)
    *   `si`: Sine Out (正弦渐出)
    *   `so`: Sine In (正弦渐入)
    *   可以组合使用（如 `siso`, `sisi`），分别代表 x 方向和 y 方向的滑动方式。
*   **color**: Arc 颜色。`0`: 蓝, `1`: 红, `2`: 绿, `3`: 灰。
*   **hitsound**: 特殊打击音效（v4.0.0）。例如 `glass_wav` 会读取 `songs/(songid)/glass.wav`。`none` 代表不应用。
*   **arctype**: 
    *   `false`: 音弧（普通 Arc）。
    *   `true`: 音轨（黑线）。若有 Arctap 且值不为 `designant`，会自动转为音轨。
    *   `designant`: 表现为红偏粉音轨。不计入 Combo 和 HP，仅在特定异象下生效。
*   **smoothness**: 平滑度（v6.8.0）。控制 segment 细分数，默认和最小值为 1。

### Arctap (天键)
当 `arctype=true` 时，在 Arc 后接方括号：
```text
arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,true,*smoothness)[arctap(tn1),arctap(tn2),...];
```
*   **tn (ms)**: 天键的时间点，须在 `t1` 与 `t2` 之间。
*   关键字 `arctap` 也可以简写为 `at`。

### 横缩放 Arctap (color=3 专用)
```text
arc(t,t,x1,x2,easing,y,y,3,hitsound,false,*smoothness);
```
*   **t**: 时间点。
*   **x1, x2**: 缩放起始/终止的横坐标。线段长度即为缩放后的长度。

---

## 6. Camera
于 v1.6.1 实装：
```text
camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);
```
*   **t (ms)**: 开始时间。
*   **x, y, z (px)**: 三轴移动距离。
    *   Arc 坐标 1.00 约对应 x 轴 850 / y 轴 450 的位移。
*   **xozAng / yozAng / xoyAng (deg°)**: 三轴旋转角度。
*   **ease**: 缓动类型。`qi` (Cubic in), `qo` (Cubic out), `reset` (重置状态), 其它值为 `Linear`。
*   **duration (ms)**: 持续时间。
*   *注意：当 ease 不为 reset 时，将关闭 Arc 对 Camera 的自动倾斜控制。*

---

## 7. Scenecontrol
于 v2.6.1 实装：
```text
scenecontrol(t,type,*param1(float),*param2(int));
```

**常用类型 (type)：**
*   **trackhide / trackshow**: 隐藏/显示轨道。
*   **trackdisplay**: 轨道透明度控制。
    *   `param1`: 变换持续时间（秒）。
    *   `param2`: 目标 alpha 值 (0-255)。
*   **redline**: 背景红线效果（v3.0.0）。
    *   `param1`: 持续时间（秒）。
*   **arcahvdistort / arcahvdebris**: Arcahv 背景特效。
*   **hidegroup**: 隐藏特定 Timinggroup 内的 Note。
    *   `param2`: 1 (隐藏) / 0 (显示)。
*   **enwidencamera / enwidenlanes**: 相机远摄 / 轨道扩充。
    *   `param1`: 持续时长 (ms)。
    *   `param2`: 1 (淡入) / 0 (淡出)。

---

## 8. Timinggroup
于 v3.0.0 实装，允许同时存在不同流速的 Note。
```text
timinggroup(options){
  // 正常 aff 语句
};
```
*   **特性**: 内部必须包含至少一个 `timing` 语句。内部的 `timing` 不产生小节线。
*   **options**: 可通过下划线叠加标识（如 `noinput_anglex200`）。
    *   **noinput**: 物件仅显示，无打击判定，不计入物量。
    *   **fadingholds**: 未击中 Hold 时产生渐变透明效果。
    *   **anglex / angley**: 对天键轨迹进行旋转（v3.12.6）。参数为 `旋转角度 * 10`。仅影响显示轨迹，不影响判定。

---

## 9. Flick
```text
flick(t,x,y,vx,vy);
```
*   **t (ms)**: 时间点。
*   **x, y**: 初始位置坐标。
*   **vx, vy**: 滑动方向向量。
*   *注意：官方谱面目前尚未正式应用此物件，请谨慎使用。*

---

## 10. 综合结构总结
代码排列顺序通常为：
1.  **标识信息** (AudioOffset 等)
2.  **分隔符** (`-`)
3.  **正常 AFF 语句** (Timing, Note, Arc 等)

*标识信息与 AFF 语句各自的内容排序不受限制。*
