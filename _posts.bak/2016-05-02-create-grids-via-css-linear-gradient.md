---
title: 使用CSS linear-gradient属性实现网格背景和桌布效果
date: 2016-05-02 22:37
categories: Web
tags: Programming Web CSS 《CSS&nbsp;Secrets》
---

## 一: 效果

![image](/assets/images/css-blueprint-grid.png)

## 二: 代码

{% highlight html %}
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>blueprint grid</title>
<style type="text/css">
div.grid {
    background: #58a;
    background-image:
        linear-gradient(rgba(255,255,255,.3) 1px, transparent 0),
        linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 0),
        linear-gradient(white 1px, transparent 0),
        linear-gradient(90deg, white 1px, transparent 0);
    background-size: 15px 15px, 15px 15px, 75px 75px, 75px 75px;
    width: 450px;
    height: 450px;
}
</style>
</head>
<body>
<div class="grid"></div>
</body>
</html>
{% endhighlight %}


## 三: 实现

### 设置背景颜色、元素大小

```css
div.grid {
    background: #58a;
    width: 450px;
    height: 450px;
}
```
![image](/assets/images/css-blueprint-grid1.png)

### 设置水平细网格线

```css
div.grid {
    background: #58a;
    background-image: linear-gradient(rgba(255,255,255,.3) 1px, transparent 0);
    background-size: 15px 15px;
    width: 450px;
    height: 450px;
}

```
元素的背景图片通过[linear-gradient属性](/css-linear-gradient-degs/)动态生成。
`background-size: 15px 15px;`设置背景图片的宽度和高度都为15px;
`background-image: linear-gradient(rgba(255,255,255,.3) 1px, transparent 1px);`设置背景图片的线性渐变角度为0度，即渐变方向是向上（向北）的。
其中底部1px为半透明白色，底部以上的14px为透明色（可看到背景色蓝色）。`linear-gradient`中的`color-stop`，如果位置值紧接着上一个`color-stop`的位置值，那么
该`color-stop`的位置值可以简单记作0，因此`background-image: linear-gradient(rgba(255,255,255,.3) 1px, transparent 1px);`也可以写成
`background-image: linear-gradient(rgba(255,255,255,.3) 1px, transparent 0);`。
由于没有指定`background-repeat`属性，元素的背景图片默认在水平和垂直方向上重复平铺，效果如下：
![image](/assets/images/css-blueprint-grid2.png)


### 设置垂直细网格线
```css
div.grid {
    background: #58a;
    linear-gradient(rgba(255,255,255,.3) 1px, transparent 0),
        linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 0);
    background-size: 15px 15px, 15px 15px;
    width: 450px;
    height: 450px;
}

```
背景图片可以通过多个线性渐变叠加生成，多个渐变描述由**,**分隔，同时每个线性渐变生成的背景图片大小都由background-size设置。`linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 0);`设置背景图片的线性渐变角度为90度，即渐变方向是向右（向东）的。其中最左侧1px为半透明白色，其它部分为透明色（可看到背景蓝色）。设置了水平和垂直细网格线后的效果如下：
![image](/assets/images/css-blueprint-grid3.png)


### 设置水平和垂直的白色粗网格线

```css
div.grid {
    background: #58a;
    background-image:
        linear-gradient(rgba(255,255,255,.3) 1px, transparent 0),
        linear-gradient(90deg, rgba(255,255,255,.3) 1px, transparent 0),
        linear-gradient(white 1px, transparent 0),
        linear-gradient(90deg, white 1px, transparent 0);
    background-size: 
            15px 15px,
            15px 15px,
            75px 75px,
            75px 75px;

    width: 450px;
    height: 450px;
}

```

通过类似的技术，还可以实现桌布效果的背景。

```css
div.tablecloth {
    background: white;
    background-image:
        linear-gradient(90deg, rgba(200,0,0,.5) 50%, transparent 0),
        linear-gradient(rgba(200,0,0,.5) 50%, transparent 0);
    background-size: 30px 30px;
    width: 451px;
    height: 451px;
}
```
![image](/assets/images/css-tablecloth.png)
