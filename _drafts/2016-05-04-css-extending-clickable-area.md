---
title: CSS扩大可点击区域的2种方法
date: 2016-05-04 22:47
categories: Web
tags: Web CSS Programming
---

##一、使用border属性扩大可点击区域

代码如下：

```CSS
.extend-via-border {
    background: #58a;
    cursor: pointer;
    border: 20px solid transparent;
    background-clip: padding-box;
    font: bold 150%/1 sans-serif;
    padding: .3em .5em;
    color: white;
}
```

```HTML
<button class="extend-via-border">点击</button>
```
