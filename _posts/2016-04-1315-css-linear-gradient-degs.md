---
title: CSS3线性渐变linear-gradient的angle参数值
date: 2016-04-15 15:38
categories: Web
tags: Programming Web CSS
---

CSS线性渐变属性linear-gradient的语法格式如下：

```
linear-gradient(
    [ <angle> | to <side-or-corner> ,]? <color-stop> [, <color-stop>]+ )
```

参考：[MDS linear-gradient()](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient)

<img src="{% site.url %}/assets/images/clock.jpg">

当用angle参数来指定渐变方向时，正数值表示按顺时针方向的偏移角度，而负数值是按逆时针方向的偏移角度值。
45度是时针指向1:30时的方向，90度是时针指向3:00时的方向，315度是时针指向10:30时的方向，0度/360度是时针指向
12:00时的方向。
因此，angle值为-45度和315度时所表示的激变方向指向是相同的。

<div style="padding: 0;background:linear-gradient(0deg, reg, green); width:15em;height:15em;">
</div>

以下通过观察<angle>为不同值时，从红色到绿色的渐变效果，来总结<angle>值的效果。

{% highlight css linenos %}
div {
    padding: 0em;
    background: linear-gradient(0deg, red, green);
    height: 15em;
    width: 15em;
}
{% endhighlight %}
