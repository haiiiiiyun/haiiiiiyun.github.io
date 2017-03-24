---
title: 响应式编程(Reactive Programming) 入门
date: 2017-03-24
writing-time: 2017-03-24 10:10
categories: Programming
tags: Programming JavaScript Reactive&nbsp;Programming RX Design&nbsp;Pattern Observable
---

# 概述

学习响应式编程最难部分在于用响应式思维。

# 什么是响应式编程

## 响应式编程就是用异步数据流进行编程

这不是新理念。即使是最典型的点击事件也是一个异步事件流，从而你可以对其进行侦测（observe）并进行相应操作。

你可以根据任何东西创建数据流，不仅仅只能根据点击事件等。流非常轻便，并且无处不在，任何东西都可以是一个流：变量，用户输入，属性，缓存，数据结构等等。例如，想象一下微博推文也可以是一个数据流，和点击事件一样。你可以对其进行侦听，并作相应反应。

**除些之外，我们有很多功能强大的函数，可以对这些流进行合并、过滤、转变等**。这就是 "函数式编程" 的强大之处。流可以作为另一个流的输入。甚至多个流也可以作为另一个流的输入。你也可以合并流，从流中过滤出你感兴趣的事件。你也可以将流中的数据值映射转换成另一个流。

流是响应式的核心，因此要再仔细研究下，下面是 "在按钮上点击" 事件流。

![按键点击事件流](https://camo.githubusercontent.com/36c0a9ffd8ed22236bd6237d44a1d3eecbaec336/687474703a2f2f692e696d6775722e636f6d2f634c344d4f73532e706e67)

流就是一个按时间顺序正在进行的事件序列(A stream is a sequence of ongoing events ordered in time)。

它可以发送 3 种不同的事物：

+ 一个值（任何不限）
+ 一个错误
+ 或一个已完成(completed) 信号


例如，当包含该按键的视图或窗口关闭时，流会发送 "completed" 信号。

我们只能异步捕获这些发送的事件，即定义：

+ 一个函数，用于当一个值发送出来时再执行
+ 定义另一个函数，用于当发错误发送出来时执行
+ 再定义函数，用于当 'completed' 信号发送出来时执行

有时可以只定义第一个函数，而忽略定义后两个函数。

在流的 “侦听” 称为 **订阅(subscribing)**，而我们定义的函数即为 **观察者(observer)**，而流就是 **主题(subject, observable)**。这是一个典型的观察者模式。

也可以用 ASCII 来画示意图：

```
--a---b-c---d---X---|->

a, b, c, d 都是发送出的值
X 是错误
| 是 'completed' 信号
---> 是时间线
```

下面演示将原始的点击事件流转变成一个新的流。

首先，创建一个计数流来指示一个按键的点击次数。在常见的响应式库中，每个流都会绑定很多的函数，如 map, filter, scan 等。当你调用这些函数时，如 `clickStream.map(f)`，会基于 clickStream 返回一个新流。但它不会修改原来的 clickStream 流。这是响应式流的一个核心特性： **不变性(immutability)**。因而它能让我们进行函数串联，如 `clickStream.map(f).scan(g)`:

```
clickStream:  ---c----c--c----c------c-->
              vvvvv map(c 变成 1) vvvv
              ---1----1--1----1------1-->
              vvvvvvvvv scan(+) vvvvvvvvv
counterStream:---1----2--3----4------5-->
```

map(f) 函数根据提供的 f 函数将发送出的值转换到另一个新流中，这里是将每次点击映射成数据  1。scan(g) 函数聚合流中所有之前的值，产生值 x = g(accumulated, current)，这里 g 是一个简单的加函数。最后，counterStream 每当点击事件发生时就发送出一个代表总点击数的值。

要显示响应式的真正强大之处，假设瑞想创建一个 “双击” 事件流，为使更有趣，该流可以将多击（多于 2 次）都认为是双击。

在响应式中，这非常简单。画示意图进行思考是理解和创建流的最好方式，无论你是新手还是专家。

![多击事件流](https://camo.githubusercontent.com/995c301de2f566db10748042a5a67cc5d9ac45d9/687474703a2f2f692e696d6775722e636f6d2f484d47574e4f352e706e67)




# 参考 

原文来自 [@andrestaltz](https://twitter.com/andrestaltz) 的 [The introduction to Reactive Programming you've been missing](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754)，可能需要翻墙阅读。

