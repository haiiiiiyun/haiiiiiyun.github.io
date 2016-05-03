---
title: CSS3线性渐变linear-gradient的angle角度参数值
date: 2016-04-15 15:38
categories: Web
tags: Programming Web CSS
---

CSS线性渐变属性linear-gradient的语法格式如下：

```
linear-gradient(
    [ <angle> | to <side-or-corner> ,]? <color-stop> [, <color-stop>]+ )
```

参考：[MDN linear-gradient()](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient)

<img src="{{ site.url }}/assets/images/clock.jpg" width="250">

当用angle参数来指定渐变方向时，正数值表示按顺时针方向的偏移角度，而负数值是按逆时针方向的偏移角度值。
45度是时针指向1:30时的方向，90度是时针指向3:00时的方向，315度是时针指向10:30时的方向，0度/360度是时针指向
12:00时的方向。
因此，angle值为-45度和315度时所表示的激变方向指向是相同的。

当angle为0时，从红到绿的渐变效果如下(使用支持css3的最新版本的浏览器来看以下效果，如chrome)：

<div style="padding:2em;background:linear-gradient(0deg, red, green); width:80%;height:15em;">
   linear-gradient: 0deg 
</div>

代码如下：
{% highlight css linenos %}
div.gradient {
    padding: 0em;
    background: linear-gradient(0deg, red, green);
    height: 15em;
    width: 15em;
}
{% endhighlight %}

{% highlight html %}
<div class="gradient">
   linear-gradient: 0deg 
</div>
{% endhighlight %}

以下是angle取各值时对应的效果：


<div style="padding:2em;background:linear-gradient(0deg, red, green); width:80%;height:15em; margin: 2em;">
    background:linear-gradient(0deg, red, green);<br/>
    background:linear-gradient(360deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(45deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(45deg, red, green);<br/>
    background:linear-gradient(-315deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(90deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(90deg, red, green);<br/>
    background:linear-gradient(-270deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(135deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(135deg, red, green);<br/>
    background:linear-gradient(-225deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(180deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(180deg, red, green);<br/>
    background:linear-gradient(-180deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(225deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(225deg, red, green);<br/>
    background:linear-gradient(-135, red, green);
</div>

<div style="padding:2em;background:linear-gradient(270deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(270deg, red, green);<br/>
    background:linear-gradient(-90deg, red, green);
</div>

<div style="padding:2em;background:linear-gradient(315deg, red, green); width:80%;height:15em; margin:2em;">
    background:linear-gradient(315deg, red, green);<br/>
    background:linear-gradient(-45deg, red, green);
</div>
