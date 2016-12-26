---
title: Jekyll 博客中使用 Mathjax 写数学公式
date: 2016-12-25
writing-time: 2016-12-25 10:33--13:08
categories: Tools
tags: Github Jekyll Utility Mathjax Markdown Math
---

# 简介

MathJax 是一个能将 LaTeX，MathML 和 AsciiMath 表示的数学式在现代浏览器网页上正确呈现现出来的开源 JavaScript 显示引擎。使用时，只需在网页上包含进 MathJax，之后按 LaTeX, MathML 或 AsciiMath 的规则编写的数学式将被 JavaScript 转换成 HTML、SVG 或 MathML 格式的同等式正确显示，它不要求客户端进行插件等的下载。

# 加载 Mathjax

在页面的 `<head>` 中加载如下脚本：

```html
<script type="text/javascript" async src="//cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
```

这里的 `TeX-MML-AM_CHTML` 是最常用的配置，能用来快速上手 Mathjax，更多的配置信息可参考 [Loading and Configuring MathJax](http://docs.mathjax.org/en/latest/configuration.html#loading)。


# 在网页中编写数学式

根据目前的配置，现在可以在网页中使用 TeX, LaTeX, MathML, AsciiMath 表示法的数学式，也可以混合使用。

## TeX 或 LaTeX 格式

这种格式通过用 *数学分隔符* 将数学式包围起来，使 Mathjax 能区分哪些是数学式，哪些是普通文本。有两种形式：一种是在段落内的，叫 **in-line mathematics**；另一种是独立成段的，叫 **displayed mathematics**。

**displayed mathematics** 的默认分隔符是 `$$...$$` 和 `\[...\]`，而 **in-line mathematics** 的默认分隔符是 `(\...\)`,如果要想使用 `$...$` 作为分隔符，需要加上如下的配置：

```html
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
```

下面的页面中使用了 Tex 数学式，代码如下：

```html
<!DOCCTYPE html>
<html>
<head>
<title>MathJax TeX Test Page</title>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_CHTML">
</script>
</head>
<body>
When <span>$a \ne 0$</span>, there are two solutions to <span>$ax^2 + bx + c = 0$</span> and they are
<div>$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$</div>
</body>
</html>
```

显示效果如下：

When <span>$a \ne 0$</span>, there are two solutions to $ax^2 + bx + c = 0$ and they are
<div>$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$</div>


由于 TeX 表达式是网页的一部分，因此要注意输入数学式时不要与 HTML 的符号冲突，特别如 *小于* 号，因为这是 HTML 用于开启一个标签的符号。注意在数学式的小于号两边加空格。

如果使用 Markdown 编写，要注意：TeX 使用下划线来表示下标，而 Markdown 用下划线表示斜体，因此 TeX 表示下标的下划线要用 `\_` 转义。

TeX 中的几个特殊符号：

+ `^` 表示上标
+ `\_` 表示下标
+ `{}` 用于分组

更多的基本使用教程见 [tuicool 上的一篇文章](http://www.tuicool.com/articles/7zqYFb3)。

Markdonw LaTeX 的参数文章：

+ [Mathjax 例子](https://cdn.mathjax.org/mathjax/latest/test/examples.html)
+ [Markdown LaTeX 在线编辑器](https://kerzol.github.io/markdown-mathjax/editor.html)
+ [LaTeX 完整教程](http://www.forkosh.com/mathtextutorial.html)
+ [LaTeX 数学符号表，PDF 文件](http://mirror.lzu.edu.cn/CTAN/info/symbols/math/maths-symbols.pdf)


> 参考文献： [MathJax Docs](http://docs.mathjax.org/en/latest/mathjax.html)
