---
layout: post
title: 十进制负数如何转成二进制补码表示
date: 2015-12-15 09:25
categories: Programming
tags: Programming
---

## 一、概述 ##

有符号整数通常用补码表示，补码表示的二进制串中，最高有效位能够表示正负数，最高有效位为1表示为负数，为0表示非负数。

## 二、十六进制和二进制间的转换 ##

在Intel体系结构的处理器中，整数字节序用big-endian法表示，即最高有效位在最左边。在转换时，记住0xA为1010<sub>2</sub>, 0xC为1100<sub>2</sub>, 0xE为1110<sub>2</sub>，其它0xA以上的数字和这些数字对比就能写出。例如：0xCFC7转化后为1100 1111 1100 0100<sub>2</sub>。

## 三、给出补码，计算出十进制整数  ##

w位的有符号整数，给出补码，计算出十进制整数的公式如下：T2U<sub>w</sub>(x)=-x<sub>(w-1).2<sup>(w-1)</sup>+x<sub>(w-2)</sub>.2<sup>(w-2)</sup>+...+x<sub>0</sub>.2<sup>0</sup>

