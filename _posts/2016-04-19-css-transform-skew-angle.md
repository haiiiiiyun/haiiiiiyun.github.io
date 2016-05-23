---
title: CSS扭曲变形skewX transform的扭曲角度值按逆时针方向计算
date: 2016-04-19 22:46
categories: Web
tags: Programming Web CSS
---

CSS3的变形属性transform的语法如下:

```
transform ： none | <transform-function> [ <transform-function> ]* 
也就是：
transform: rotate | scale | skew | translate |matrix;
```

参见: [w3cplus css3 transform](http://www.w3cplus.com/content/css3-transform)

其中的扭曲变形skew具有三种情况:

1. skewX(&lt;angle&gt;): 在X轴(水平)方向进行扭曲变形,angle值为正数时,沿逆时针方向扭曲,值为负数时,沿顺时针方向扭曲。这和linear-gradient等属性的angle值为正数时,沿顺时钟方向计算正好相反。
例：transform: skewX(30deg)

![skewX(30deg)]({{ site.url }}/assets/images/skewX-30deg.png)

2. skewY(&lt;angle&gt;): 在Y轴(垂直)方向进行扭曲变形,angle值为正数时,沿顺时针方向扭曲,负数时沿逆时针方向扭曲。
例：transform: skewY(10deg)

![skewY(10deg)]({{ site.url }}/assets/images/skewY-10deg.png)

3. skew(&lt;angle&gt; [, &lt;angle&gt;]): 第一个参数对应X轴, 第二个参数对应Y轴.若第二个参数未提供,则默认为0。
例：transform: skew(30deg, 10deg)

![skewY(10deg)]({{ site.url }}/assets/images/skew-x30-y10.png)
