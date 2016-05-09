---
title: CSS扩大可点击区域的2种方法
date: 2016-05-04 22:47
categories: Web
tags: Web CSS Programming 《Css&nbsp;Secrets》
---

根据[费茨法则(Fitts' Law)](http://baike.baidu.com/link?url=tFJ2ZI7ilVwpwa8VYU_ZPZ8g-zgtP3Dt9YSLb6KN4I8uoyBezgBZftlZBriCAlXoTSBz7c2kXscME-JAIzvr9a), 使用指点设备到达一个目标的时间同以下两个因素有关：

1. 设备当前位置和目标位置的距离(D)。距离越长，所用时间越长;
2. 目标的大小(S)。目标越大，所用时间越短。

![Fitt's Law]({{ site_url }}/assets/images/fitts-law.jpg)

因此，扩大目标大小是提高UI易用性的很好方法。

以下记录扩大元素可点击区域的两种方法。

两种方法的初始CSS代码如下：

```css
button {
    background: #58a;
    cursor: pointer;
    font: bold 150%/1 sans-serif;
    padding: .3em .5em;
    color: white;
}
```

初始HTML代码如下：

```html
<button>点击</button>
```

## 一、使用border属性扩大可点击区域

HTML修改为:

```html
<button class="extend-via-border">点击</button>
```

为button添加20px的透明边框:

```css
.extend-via-border {
    border: 20px solid transparent;
}
```
由于元素背景颜色默认扩展到边框下，如果此时边框设置为透明，元素背景颜色会从边框处透出来，
给人以元素变大了的效果：
![边框扩大元素的效果]({{ site.url }}/assets/images/css-extending-clickable-area-error.png)


将元素的`background-clip`属性修改为`padding-box`后，元素背景颜色只扩展到padding区域，不再扩展到边框。
元素边框的颜色是父元素的背景色，因此不再给人以元素变大了的效果，但已经扩大了元素的边框边界和可点击区域。

![通过border属性扩大可点击区域]({{ site.url }}/assets/images/css-extending-clickable-area.png)

完整的CSS代码下：

```css
.extend-via-border {
    border: 20px solid transparent;
    background-clip: padding-box;
}
```

## 二、使用伪元素扩大可点击区域

伪元素能为其父元素捕获鼠标交互动作，因此，只需通过伪元素扩大父元素的空间大小，就能扩大可点击区域。

代码如下：

```html
<button class="extend-via-pseudo-elem">点击</button>
```

```css
.extend-via-pseudo-elem {
	position: relative;
}

.extend-via-pseudo-elem::before {
    content: '';
    position: absolute;
    top: -20px;
    right: -20px;
    bottom: -20px;
    left: -20px;
}
```

这种方法扩大的区域，不必在父元素的附近，它可以在伪元素能够定位的任何地方。
