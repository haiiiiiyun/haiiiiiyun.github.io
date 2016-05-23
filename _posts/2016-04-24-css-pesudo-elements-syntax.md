---
title: CSS伪元素语法表示为::before还是:before?
date: 2016-04-24 09:24
categories: Web
tags: Programming Web CSS
---

CSS3创建before[伪元素](https://developer.mozilla.org/en/CSS/Pseudo-elements)的语法为::before, 而CSS2的对应语法为:before。

因此，:before这种语法是过时的，只用来支持IE8等较老的浏览器。

CSS3只所以将表示法从原来的:before改为::before，是为了将[伪元素](https://developer.mozilla.org/en/CSS/Pseudo-elements)与[伪类](https://developer.mozilla.org/en-US/docs/CSS/Pseudo-classes)(比如:hover)等区别开来。
