---
title: 使用CSS background-clip属性实现半透明边框
date: 2016-04-27
writing-time: 2016-04-28 12:09--2016-04-28 13:09
categories: Web
tags: Programming Web CSS 《CSS&nbsp;Secrets》  
---

## 一: 效果

![image]({{ site.url }}/assets/images/translucent-border.jpg)

## 二: 代码

{% highlight html %}
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>使用CSS background-clip属性实现半透明边框</title>
<style type="text/css">
body {
	background: url('/assets/images/zebra.jpg') no-repeat;
}
div {
	border: 10px solid rgba(255, 255, 255, .5);
	background: white;
	background-clip: padding-box;
	/* 基本样式 */
	max-width: 20em;
	padding: 2em;
	margin: 2em auto 0;
    position: absolute;
    top: 200px; left: 200px;
}
</style>
</head>
<body>
<div>
    设置半透明边框后，能透过边框看到背景图片吗?
</div>
</body>
</html>
{% endhighlight %}


## 三: 实现

### 设置body元素背景图片

```css
body {
	background: url('/assets/images/zebra.jpg') no-repeat;
}
```

### 设置半透明边框

```css
div {
	border: 10px solid rgba(255,255,255,.5);
	background: white;
	
	/* 基本样式 */
	max-width: 20em;
	padding: 2em;
	margin: 2em auto 0;
    position: absolute;
    top: 200px; left: 200px;
}
```
设置元素的背景为白色，边框为半透明的白色。效果如下：

![image]({{ site.url }}/assets/images/translucent-border-error.jpg)

此时看不出半透明边框的效果，这是因为元素的背景默认扩展至元素边框的外边界(border)，在设置了border宽度后，元素的背景能透过内容区域(content area)、padding区、border区看到(而透过margin区看到的是父元素背景)。

元素本身的白色背景，透过半透明的边框，看到的还是白色。

![css盒子模型]({{site.url}}/assets/images/css-box.png)

### 通过background-clip属性修正

CSS的[background-clip](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip)属性设置元素背景的扩展范围，值可以为**border-box**, **padding-box**, **content-box**，默认值为border-box。

值为border-box时表示背景扩展至元素边框(border)的外边界, 值为padding-box时表示背景扩展至元素padding的外边界，而值为content-box时表示背景只扩展至内容区域(content)部分。

通过设置`background-clip: padding-box;`，使该元素的白色背景只扩展至padding的外边界，不再扩展至边框(border)部分，此时就能透过边框看到父元素的背景。

修改后的CSS如下：

```css
div {
	border: 10px solid rgba(255,255,255,.5);
	background: white;
    background-clip: padding-box;
	
	/* 基本样式 */
	max-width: 20em;
	padding: 2em;
	margin: 2em auto 0;
    position: absolute;
    top: 200px; left: 200px;
}
```
