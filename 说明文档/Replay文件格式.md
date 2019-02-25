# Replay文件格式

​	初步构想是，将每一帧的传递给Server的通信内容进行存储，最后根据通信内容进行Replay，尽管这样的话相对来说Replay文件格式要大一些，但是在Unity播放的时候不需要与逻辑打交道，而且支持前进后退之类的操作

```json
[{
	"walls":"[[left,right,bottom,top], ...]"		//墙的左右下上坐标，全部为整数
}, 
{
    "humans" : "[[num,[x,y],rotation,hp,grenade_number,fire_time],...]",	
                //编号，坐标实数，旋转角度[0~360]实数，血量，天降正义剩余量，距离下一次开火的时间整数
    "fireballs" : "[[[x,y],rotation],...]",
				//坐标实数，旋转角度[0~360]实数
    "meteors" : "[[[x,y],lasttime],...]",
                 //坐标实数，距离爆炸的帧数整数>0
    "balls" : "[[x,y],belong]",
				//坐标实数，持有者的编号，不存在则返回-1
    "events" : "[[opt,...]]",
    "scores" : [0.0,0.0,...]
},// 开局之前的消息

{
    "humans" : "[[num,[x,y],rotation,hp,grenade_number,fire_time],...]",	
                //编号，坐标实数，旋转角度[0~360]实数，血量，天降正义剩余量，距离下一次开火的时间整数
    "fireballs" : "[[[x,y],rotation],...]",
				//坐标实数，旋转角度[0~360]实数
    "meteors" : "[[[x,y],lasttime],...]",
                 //坐标实数，距离爆炸的帧数整数>0
    "balls" : "[[x,y],belong]",
				//坐标实数，持有者的编号，不存在则返回-1
    "events" : "[[opt,...]]",
    "scores" : [0.0,0.0,...]
},// 第一帧结束

{
    "humans" : "[[num,[x,y],rotation,hp,grenade_number,fire_time],...]",	
                //编号，坐标实数，旋转角度[0~360]实数，血量，天降正义剩余量，距离下一次开火的时间整数
    "fireballs" : "[[[x,y],rotation],...]",
				//坐标实数，旋转角度[0~360]实数
    "meteors" : "[[[x,y],lasttime],...]",
                 //坐标实数，距离爆炸的帧数整数>0
    "balls" : "[[x,y],belong]",
				//坐标实数，持有者的编号，不存在则返回-1
    "events" : "[[opt,...]]",
    "scores" : [0.0,0.0,...]
},// 第二帧结束

...
{
     "scores" : [0.0,0.0.....]
}]
```

