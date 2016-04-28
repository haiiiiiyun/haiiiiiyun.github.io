---
title: 定制Checkbox复选框样式
date: 2016-04-26 15:29
categories: Web
tags: Programming Web CSS
---

## 一: 代码

```html
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

/* 隐藏原复选框 */
.custom-checkbox input[type="checkbox"] { 
    position: absolute;
    clip: rect(0,0,0,0);
}

.custom-checkbox input[type="checkbox"] + label::before {
    content: '\a0'; /* non-break space */
    display: inline-block;
    vertical-align: .2em;
    width: .8em;
    height: .8em;
    margin-right: .2em;
    border-radius: .2em;
    background: silver;
    text-indent: .15em;
    line-height: .65;
}

.custom-checkbox input[type="checkbox"]:checked + label::before {
    content: '\2713';
    background: yellowgreen;
}

.custom-checkbox input[type="checkbox"]:focus + label::before {
    box-shadow: 0 0 .1em .1em #58a;
}

.custom-checkbox input[type="checkbox"]:disabled + label::before {
    background: gray;
    box-shadow: none;
    color: #555;
}
</style>
</head>
<body>
<body>

<div class="custom-checkbox">
    <input type="checkbox" id="ckbox" autofocus />
    <label for="ckbox">选项</label>
    <br />
    <input type="checkbox" id="ckbox2" checked />
    <label for="ckbox2">选项</label>
    <br />
    <input type="checkbox" id="ckbox3" disabled />
    <label for="ckbox3">选项</label>
    <br />
    <input type="checkbox" id="ckbox4" checked disabled />
    <label for="ckbox4">选项</label>
</div>

</body>
</html>
```


## 二: 效果

![image]({{ site.url }}/assets/images/css-checkboxes.png)


## 三: 实现

```css
.custom-checkbox input[type="checkbox"] { 
    position: absolute;
    clip: rect(0,0,0,0);
}
```
通过clip属性隐藏掉系统生成的复选框。
clip属性定义一个剪裁区域，在这个区域内的元素内容才可见。语法如下：
```
clip: rect(<top>, <right>, <bottom>, <left>);
```
top, bottom指定的偏移量都是从元素盒子的顶部边缘（border的上外边界)算起的，而right,left的偏移量都是从元素例子的左边缘（border的左外边界)算起的。
详细可参考[w3cpuls上的clip属性相关文章](http://www.w3cplus.com/css3/clip.html)。
用这种方式隐藏后，用户还可以用Tab键对复选框进行轮询访问。


```css
.custom-checkbox input[type="checkbox"] + label::before {
    content: '\a0'; /* non-break space */
    display: inline-block;
    vertical-align: .2em;
    width: .8em;
    height: .8em;
    margin-right: .2em;
    border-radius: .2em;
    background: silver;
    text-indent: .15em;
    line-height: .65;
}
```
在label元素前生成一个伪元素, content: '\a0'表示伪元素的内容是一个空格。
伪元素的content属性内容如果是一个特殊符号，如空格时，不能用**&amp;nbsp;**来表示，需要
用特殊符号对应的unicode码来表示，如空格的unicode码是00A0，则表示为'\00a0',或者'\a0'。
更多特殊字符要参考[常用的HTML特殊字符大全(css3 content)](http://www.phpjz.cn/web/201311/1700.html)。

设置伪元素的样式，生成自定制的复选框。

```css
.custom-checkbox input[type="checkbox"]:checked + label::before {
    content: '\2713';
    background: yellowgreen;
}
```

设置选中状态的复选框样式，**content: '\2713'**是特殊字符勾的符号。 

```css
.custom-checkbox input[type="checkbox"]:focus + label::before {
    box-shadow: 0 0 .1em .1em #58a;
}
```
设置获得输入焦点时的样式为一个模糊边框。

```
.custom-checkbox input[type="checkbox"]:disabled + label::before {
    background: gray;
    box-shadow: none;
    color: #555;
}
```

设置复选框不可用时的样式。
