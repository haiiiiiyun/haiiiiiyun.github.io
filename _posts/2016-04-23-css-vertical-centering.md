---
title: CSS3中实现垂直居中的3种方法
date: 2016-04-23 22:04
categories: Web
tags: Programming Web CSS
---

## 目标：垂直居中main块

hTML代码如下：

{% highlight html %}
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title></title>
<style type="text/css">
body {
    font: 100%/1.5 "Myriad Pro","Myriad Web","Lucida Grande","Trebuchet MS","Tahoma","Helvetica","Arial",sans-serif;
    color: #434343;
}
main {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
</head>
<body>
<main>
    <h1>Am I centered yet?</h1>
    <p>Center me, please!</p>
</main>
</body>
</html>
{% endhighlight %}


## 方法一: 通过绝对定位实现

```css
main {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
```

绝对定位的top: 50%; left: 50%将main块的左上角定位到main块父节点（即body元素）的中心点，也就是页面的中心点。
transform translate移位变换，当位移值是百分数时，是相对于当前块的尺寸大小的。因此main块在X轴向左位移本身宽度的50%，在Y轴
向上位移本身高度的50%后，恰当使main块在当前页面垂直中心。


## 方法二: 通过viewport相关尺寸单位实现

```css
main {
    width: 18em;
    margin: 50vh auto 0;
    transform: translateY(-50%);
}
```

1vh是viewport高度的1%，50vh指viewport高度的50%；相应的，1vw是viewport宽度的1%。
通过设置main块的上边距margin-top值为50vh，使main块的上边沿正好在页面的垂直方向的等分线上的。而左右边距都为auto，实现了main块
在水平方向上居中。
再通过与方法一中一样的移位方法，使main块在当前页面上垂直居中。
需要注意的是，要使用这种方法，main块的宽度width值必需要设置。

## 方法三：通过flex布局实现

```css
body {
    display: flex;
    min-height: 100vh;
    margin: 0;
}
main {
    margin: auto;
}
```

要对main块进行flex布局，需要将display: flex的属性值设置在main块的父节点（即body元素)上，同时还要设置最小高度值
为viewport的高度值。
之后只要简单main块的页边距为auto，就自动实现垂直和水平方向上的自动居中。
