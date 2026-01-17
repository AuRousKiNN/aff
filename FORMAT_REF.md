解析
标识信息
所有谱面文件开始部分都一定包含这一行：

AudioOffset:x
这行代码表示谱面整体向前(-)/向后(+)移动x毫秒
一般情况下x=0，这样物件对应的毫秒数即为歌曲播放进度的毫秒数
但是如果x≠0，物件在音乐中实际对应的毫秒数=物件时间+x
鉴于有些音源以开头为基准的第一个采音不在整拍上，所以可能有时候的确需要x≠0

有些谱面会加入一行TimingPointDensityFactor：

TimingPointDensityFactor:y
这行代码表示全局的音弧与长条的物量密度调整为正常值的y倍
y=1时效果与省略此行相同
如果y的值特别大的话...

分隔符
-
物件的读取从第一个"-"所在的行之后开始
在第一个"-"所在的行之前，你可以写自己的“标识信息”
例如“ChartVersion:2”，游戏会正常读取并记录相关数据，但是并不会有任何效果

Timing
Timing代码如下

timing(t,bpm,beats);
t(ms)：Timing起始位置，数字为非负整数
每个Timing都会在t处生成一条小节线
bpm(拍/分钟)：节奏速度，数字为小数
beats(四分音个数(拍))：表示每多少个四分音符(拍)为一小节（出现一条小节线），数字为小数
当bpm不为0时不可为0(为0代表每0个四分音符为1小节，会出现除零错误使游戏崩溃)比如4.00就是4/4拍，代表四拍一小节

每个谱面必须有一个t=0的Timing，并且第一个t=0的Timing的bpm/beats数值要大于等于0，才可被正常读取。

地面Note & 地面Hold
地面Note & 地面Hold代码如下

(t,lane);
hold(t1,t2,lane);
t(ms):地面Note所在时间，数字为非负整数
t1,t2(ms):地面Hold物件开始/结束的时间，数字为非负整数，t1＜t2
lane(0～5/float): 物件所在轨道，数字为0～5或float
轨道的编号从左到右依次为0，1，2，3，4，5。正常情况下仅使用1～4号
4.0.0版本起新增“enwidenlanes”的scenecontrol类型（见下文）在标记为启用后，轨道由4条扩充至6条，在1轨左侧新增0轨，在4轨右侧新增5轨
lane为float时，以坐标作为该note的位置，float轨道坐标与arc坐标的映射公式为 -0.5 + lane * 2
如果要使用float轨道note最好是将它作为演出note使用，而不是当正常note，因为它的判定不同于正常轨道note的判定
在谱面文件内标记开启“enwidenlanes”时，点击每条轨道的中间时，无法被判定上
Arc & 天空音符（Arctap）
Arc & 天空Note（Arctap）代码如下

arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,arctype,*smoothness);
带“*”的为可选参数

t1,t2(ms)：Arc物件开始/结束的时间，数字为非负整数，t1可以等于t2，当t1=t2时，Arc与判定线平行，物量为0，且此种类型的Arc可以起到连接Arc组的作用（即宏观上算作不分立的Arc，不能换手）
只有skylineBoolean=true时t1可以大于t2
x1,x2：代表Arc物件开始/结束时的横坐标，数字为小数
easing(b,s,si,so)：Arc滑动方式。b =Bezier，s=Straight，si=Sine Out，so=Sine In。当t1=t2时该参数无意义（都是直的）
si与so可以两个在一起自由组合(如siso,sisi等)，siso代表x方向上滑动方式为si、y方向上滑动方式为so
y1,y2：代表Arc物件开始/结束时的纵坐标，数字为小数
color：Arc颜色，0蓝，1红，2绿[1]，3灰，0~3以外均为黑色，在arctype=true时该参数无意义，且能被游戏正常读取
color=3的Arc在5.5.6版本中新增了横缩放Arctap的形态。（目前，该Arc在HIVEMIND INTERLINKED、Live Faster Die Younger中出现，在其他谱面的表现形式不同，请谨慎使用）
hitsound：v4.0.0实装，给予Arctap特殊打击音效，对整条黑线上所有的Arctap生效，将它们替换为特殊样式，并应用特殊打击音效。举例：填写glass_wav时，将把 songs/(songid)/glass.wav 作为打击音效，填写“none”代表不应用特殊音效，无arctap或arcType=false时，该参数无意义（但是不能乱填，起码不能让游戏崩溃），等价于填写“none”
arctype(false,true,designant)：当填写false/true时，判断该Arc是否为音轨（黑线）。false为音弧（普通Arc），true为音轨，但是只要有Arctap且该值不为designant时会将此Arc的类型强制转换为音轨；填写designant时，该Arc表现为红偏粉的音轨，且该Arc上的ArcTap也会被染色。请注意，designant类型的Arc上的ArcTap不会被记入总Combo数，击打时也不会增加HP，且只会在Designant./Lament Rain异象时生效。[2]
当arctype=true，并且该Arc上有天空音符（Arctap）时，代码如下
*smoothness：平滑度，v6.8.0实装，用于控制 segment 的细分数量（默认和最小值都为 1），数字为小数
arc(t1,t2,x1,x2,easing,y1,y2,color,hitsound,true,*smoothness)[arctap(tn1),arctap(tn2),……,arctap(tnm)];
tn1,tn2,……,tnm(ms)：m个天空物件在这条判定线上的时间点，数字为非负整数，且不能超出t1和t2的区间(超出时arctap的坐标会有问题)
实际上arctap的关键字也可以用at代替，但官方谱面中从未使用过这一别名，请谨慎使用
横缩放Arctap
此为color=3的Arc在5.5.6版本中新增的形态，代码如下

arc(t,t,x1,x2,easing,y,y,3,hitsound,false,*smoothness);
t：Arctap的时间点，数字为非负整数。
x1,x2：Arctap缩放起始/终止时的横坐标，数字为小数
以轨道俯视图为平面，作一条以x1为端点，x2为延长点的线段，线段长度即为Arctap缩放后的具体长度。
easing：在此形态下无意义，可以填写普通Arc的任意一个参数。
y：Arctap的纵坐标，数字为小数
hitsound：Arctap的特殊打击音效，与普通Arc的hitsound一致。
如果此参数填入了信息，Arctap也会被替换为特殊样式，但Arctap的大小保持正常形态（其实际判定按照原Arctap判定）
*smoothness：在此形态下无意义。
Camera[3]
于v1.6.1实装，代码如下：
camera(t,x,y,z,xozAng,yozAng,xoyAng,ease,duration);
以垂直判定面为基准，设横向为x轴，纵向为y轴，沿轨道方向为z轴，建立空间直角坐标系
t (ms): 开始时间
x (px): x轴移动，左负右正
y (px): y轴移动，下负上正
z (px): z轴移动，前负后正
xozAng (deg°): xoy平面角度，逆时针-正 顺时针-负
yozAng (deg°): yoz平面角度，抬头-正 低头-负
xoyAng (deg°): xoz平面角度，逆时针-正 顺时针-负
ease (string): qi, qo, reset (qi=Cubic in，qo=Cubic out，reset=重置Camera状态，非上述三个值均为Linear)
duration (ms): 语句持续时间
当ease不为reset时将关闭Arc对Camera的倾斜控制。

请注意，xyz轴移动的坐标并非与Arc位置坐标相同 (为世界坐标) 。Arc x坐标1.00对应850的移动距离；y坐标1.00对应450的移动距离。

Scenecontrol
于v2.6.1实装，代码如下：

scenecontrol(t,type,*param1(float),*param2(int));
t(ms)：开始时间
type：要执行的场景控制类型
param：参数，“*”代表可选，但是两个参数必须同时出现/不出现
目前已知可填写的type及其参数情况如下：

trackhide：隐藏轨道
trackshow：显示轨道
不填参数
使用例：scenecontrol(10240,trackhide);
当前版本使用trackhide/trackshow时等效于 scenecontrol(t,trackdisplay,1.00,0/255);
trackdisplay：轨道透明度控制
param1：轨道从当前alpha变换到目标alpha(param2)所要花费的时间，数字为小数，单位为秒，填0.00等价于填1.00
param2：轨道需要变换到的目标alpha值，可以填非负整数；<255时有黑色背景特效，否则没有；=0为轨道完全透明，=255为轨道不透明，>=256时透明度溢出（可看作透明度对256取余数计算）。
使用例：scenecontrol(20480,trackdisplay,6.00,0);
redline（v3.0.0新增）：背景红线效果（见Arcahv和Désive）
param1：红线存在的时间，数字为小数，单位为秒
param2：未使用
使用例： scenecontrol(40960,redline,1.88,0);
arcahvdistort（v3.0.0新增）：Arcahv解锁演出时的背景变形效果
arcahvdebris（v3.0.0新增）：Arcahv解锁演出时的背景碎片效果
param1：从当前alpha变换为指定alpha的持续时间，数字为小数，单位为秒
param2：目标alpha值
使用例：scenecontrol(1000,arcahvdebris,1.00,128);
hidegroup（v3.5.3新增）：是否隐藏该时间组(timinggroup)内的note(由param2决定)
param1：未使用
param2：隐藏或显示该时间组的note（1/0）
使用例：scenecontrol(81920,hidegroup,0.00,1);
enwidencamera（v4.0.0新增）：使Camera按一定比例远离轨道，同时skyinput也会变高
enwidenlanes（v4.0.0新增）：使轨道两侧的ExtraLane展示
两种enwiden类型的scenecontrol的param用法如下:
param1：持续时长（ms）
param2：淡入或淡出该事件展示的效果（1/0）
使用例：scenecontrol(1000,enwidencamera,1000.00,1);
enwidencamera会同时将Sky Input线移动至Arc坐标下y=1.61处，同时不会禁用接Arc时的相机倾斜。
Timinggroup
于v3.0.0实装，代码如下：

timinggroup(){
 //正常aff语句
};
每一个timinggroup语句块中的语句（物件）使用其内部单独的timing语句（并且至少包含一个timing语句），因此可以实现同时刻不同note流速
timinggroup语句块中的timing语句不会产生小节线，小节线是由所有timinggroup语句块外面的timing语句决定的
一张谱面理论可以存在无限多个timinggroup语句块，也可以仅由t=0的timing和无数timinggroup组成
可以通过在括号内添加标识来达到特殊效果，不填或添加无效标识时，则没有任何特殊效果。不同特殊效果之间可以叠加，用下划线隔开即可，如timinggroup(noinput_anglex200)。
目前已有特殊效果标识有：

noinput（v3.5.3新增）：
此时本timinggroup内的物件只有显示效果，没有打击效果和物量，不会判定为击中
noinput中的实体Arc和hold在经过判定线后依然会消失而不会直接穿过（v3.12.6起）
noinput中的实体Arc保留了部分判定，因此依然可以实现一些正常的判定特性，如当异色Arc相交时，可以用任意一只手去接/换手
v3.12.6的愚人节曲目 Mistempered Malignance 中的同色Arc段便是利用这个特性实现的，原理是在其中一条同色Arc上放了一条完全重叠的异色noinput隐藏Arc
fadingholds（v3.12.2新增）：
此时在未击中Hold时，Hold会进行alpha渐变效果，直到变成未击中时的alpha
此效果仅对timinggroup中的Hold生效，其他物件不受影响
与noinput叠加时会正常触发fadingholds效果（但是你仍然无法击中hold）
anglex/angley（v3.12.6新增）[4]：
分别表示对timinggroup内的天键的轨迹进行旋转，旋转轴为经过天键在判定平面落点的平行于x/y轴的直线，其后需要接一个非负整数参数，表示旋转角（单位：度）的10倍
实际落点和判定位置不受影响
此特殊效果仅影响天键，不影响地面tap/实体Arc/黑线
x轴旋转时正方向为上转，y轴旋转时正方向为向左转
两者可以叠加，叠加时先绕x轴平行线转再绕y轴平行线转，不受参数顺序影响
例：timinggroup(angley3400_anglex200)则会将所有天键的轨迹绕其对应的x轴平行线向上旋转20°然后绕其对应的y轴平行线向右旋转20°
Flick[5]
代码如下：

flick(t,x,y,vx,vy);
t(ms):Flick所在时间
x,y:Flick初始位置的横、纵坐标，数字为小数
vx,vy:Flick滑动方向向量的横向、纵向值，数字为小数，实际滑动方位角为正右方基础上逆时针arctan(vy/vx)
官方谱面目前还没有实装过Flick，请谨慎使用Flick
综合
代码排列顺序为
标识信息
分隔符
正常aff语句
其中第一个单独"-"作为分隔，标识信息与正常aff语句各自的内容排序不受限制。