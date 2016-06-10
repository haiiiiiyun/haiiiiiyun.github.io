---
title: Full Stack Python 系列之 4.1 Web 开发
meta: Web 开发是对网站和 Web 应用程序相关活动的统称。请到 Full Stack Python 上了解理解信息。
date: 2016-06-10
writing-time: 2016-06-10 09:11--13:47
categories: Full&nbsp;Stack&nbsp;Python
tags: Full&nbsp;Stack&nbsp;Python 翻译 Python
---

> 本系列文章来自 [Full Stack Python简体中文翻译项目](https://github.com/haiiiiiyun/fullstackpython.cn)。
>
> 翻译网站地址是 [fullstackpython.atjiang.com](http://fullstackpython.atjiang.com)。
>
> 查看原文请访问 [www.fullstackpython.com](http://www.fullstackpython.com/)。

# 第四章 、一  Web 开发

Web 开发是对概念化、构建、 [部署](http://fullstackpython.atjiang.com/deployment.html) 和运营　Web 应用程序及 Web [应用程序接口](http://fullstackpython.atjiang.com/application-programming-interfaces.html) 的统称。

## 为什么 Web 开发很重要？
自从 [第一个网站](http://info.cern.ch/hypertext/WWW/TheProject.html) 于 [1989](http://home.cern/topics/birth-web) 年诞生以来，网络在网站数量、用户数和容量上取得了难以置信的发展。 Web 开发这个概念包含了与网站及 Web 应用程序相关的所有活动。

## Python 如何用于 Web 开发？
Python 能用于创建服务端 Web 应用程序。虽然 [Web 框架](http://fullstackpython.atjiang.com/web-frameworks.html) 对于创建 Web 应用来说不是必需的，但是不用现存的开源库来加快开发进度的开发人员还是很少的。

Python 不能用于浏览器。能在 Chrome、 Firefox 和 Internet Explorer 等浏览器上运行的语言是 [JavaScript](http://fullstackpython.atjiang.com/javascript.html)。像 [pyjs](http://pyjs.org/) 等项目能将 Python 程序编译成 JavaScript 程序。但是，大多数 Python 开发人员使用混合的方式开发他们的 Web 应用程序，服务端用 Python，浏览器客户端用 JavaScript。 

### Web 开发相关资源
* [Web 应用开发是不同的并且更好](http://radar.oreilly.com/2014/01/web-application-development-is-different-and-better.html) 提供了 Web 开发如何从只需要写静态 HTML 文件进化到如今需要由复杂的 JavaScript 客户端应用动态生成的相关背景。

* 虽然不是只针对 Python，Mozilla 为想学习建网站的初学者和中级网络用户整理了一份 [Web 学习](https://developer.mozilla.org/en-US/Learn) 的教程。它对于想学习通用 Web 开发知识的人来说还是值得一看的。

* [Web 的进化](http://www.evolutionoftheweb.com/) 形象化地展示了浏览器及其相关技术的发展历程，以及 Internet 数据传输量的总体发展状况。值得注意的是上面的数据只统计到 2013 年年初，但对于探索最初 24 年中所发生的事件，也不啻为一种很好的途径。

* Web 开发涉及到与服务器的 HTTP 通信，托管网站或 Web 应用，以及客户端－一个浏览器。理解浏览器的工作原理对于一个开发者来说是很重要的，因此建议看下这篇文章
  [Web 浏览器里都有些什么](https://medium.com/@camaelon/what-s-in-a-web-browser-83793b51df6c)。

* [经历两周痛苦的慢速网络后给网站开发者的三个忠告](https://medium.com/@zengabor/three-takeaways-for-web-developers-after-two-weeks-of-painfully-slow-internet-9e7f6d47726e) 对于每位 Web 开发人员来说都是必读的。不是每个人都使用高速网络服务的，因为他可能地处世界边远地区，或者刚好在地铁隧道中。优化网站以适应这些情况是非常重要的，它能保持用户的满意度。
