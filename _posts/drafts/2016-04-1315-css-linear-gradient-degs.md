---
layout: post
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

具体参数值可参考：[MDS linear-gradient()](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient)

以下通过观察<angle>为不同值时，从红色到绿色的渐变效果，来总结<angle>值的效果。

{% highlight css linenos %}
div {
    padding: 0em;
    background: linear-gradient(0deg, red, green);
    height: 15em;
    width: 15em;
}
{% endhighlight %}
```
