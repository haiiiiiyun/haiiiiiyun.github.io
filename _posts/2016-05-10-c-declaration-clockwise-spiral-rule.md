---
title: 解析C语言复杂声明的“顺时针/螺旋式法则”
date: 2016-05-10 10:28
categories: Programming
tags: C Programming
---

> [This was posted to comp.lang.c by its author, David Anderson, on 1994-05-06.]
> The **Clockwise/Spiral Rule**
> 
> By David Anderson
> 
> Copyright © 1993,1994 David Anderson
> This article may be freely distributed as long as the author's name and this notice are retained.
>
___

本文英文原文在: [http://c-faq.com/decl/spiral.anderson.html](http://c-faq.com/decl/spiral.anderson.html)

_______


江湖中流传一种[“顺时针/螺旋式法则”](http://c-faq.com/decl/spiral.anderson.html)，能让任何C程序员在头脑中解析任意C声明！

只需以下三个简单的步骤：

1. 从待解项开始，并以螺旋式/顺时针方向移动;将后面碰到的每一声明项用相应的英文语句代替：
    + `[X] 或 []`: Array X size of... or Array undefined size of...
    + `(type1, type2)`:  function passing type1 and type2 returning...
    + `*`: pointer(s) to...
2. 继续按螺旋式/顺时针方向解析直到所有符号都处理完毕。
3. 总是优先处理括号里的项！

## 例1: 简单声明

<pre>
                     +-------+
                     | +-+   |
                     | ^ |   |
                char *str[10];
                 ^   ^   |   |
                 |   +---+   |
                 +-----------+
</pre>

我们自问：str是什么？

`"str is an ...`

+ 从`str`开始我们按螺旋式顺时针方向移动， 看到的第一个字符是`[` , 这意味着有一个数组，那么...
    `"str is an array 10 of...`
+ 继续按螺旋式顺时针方向移动，碰到的下一个字符是`*`, 意味着有一个指针，那么...
    `"str is an array 10 of pointers to...`
+ 继续按螺旋式顺时针方向移动，看到了行结束符`;`，于是继续移动，直到碰到类型`char`, 那么...
    `"str is an array 10 of pointers to char"`
+ 我们已经`访问`了所有的声明项，因此完成解析！

将解析得到的语句翻译成中文: `str`是大小为10，元素类型是指向char的指针的数组。

## 例2： 函数指针声明

<pre>
                     +--------------------+
                     | +---+              |
                     | |+-+|              |
                     | |^ ||              |
                char *(*fp)( int, float *);
                 ^   ^ ^  ||              |
                 |   | +--+|              |
                 |   +-----+              |
                 +------------------------+
</pre>

我们自问：fp是什么？

`“fp is a...`

+ 按螺旋式顺时针方向移动，我们看到的第一个字符是`)`, 因此，`fp`是在一个括号内，于是在括号内继续螺旋式移动，看到的下一个字符是`*`, 那么...
    `"fp is a pointer to...`
+ 我们现已在括号外面了，继续螺旋式顺时针移动，看到`(`, 这意味着有一个函数，那么...
    `"fp is a pointer to a function passing an int and a pointer to float returning...`
+ 继续按螺旋式移动，看到`*`, 那么...
    `"fp is a pointer to a function passing an int and a pointer to float returning a pointer to...`
+ 继续按螺旋式移动，看到`;`, 但是我们还没有访问完所有的声明项, 于是我们继续移动，最后看到类型`char`, 那么...
    `"fp is a pointer to a function passing an int and a pointer to float returning a pointer to a char"`

将解析得到的语句翻译成中文: `fp`是一个函数指针，该函数传入一个`int`和一个`float`指针类型的参数，并返回一个`char`指针。

## 例3: 终极篇

<pre>
                      +-----------------------------+
                      |                  +---+      |
                      |  +---+           |+-+|      |
                      |  ^   |           |^ ||      |
                void (*signal(int, void (*fp)(int)))(int);
                 ^    ^      |      ^    ^  ||      |
                 |    +------+      |    +--+|      |
                 |                  +--------+      |
                 +----------------------------------+
</pre>

我们问自己：signal是什么？

注意到`signal`在括号内，我们必须首先对它进行解析。

+ 按顺时针方向移动，看到`(`，那么...
    `"signal is a function passing an int and a...`
+ 呃，我们可以用相同的法规对`fp`进行解析，那么... fp是什么？ fp同样也在括号内，于是继续移动，看到`*`，那么...
    `"fp is a pointer to...`
+ 继续按螺旋式顺时针方向移动，然后看到`(`，那么...
    `"fp is a pointer to a function passing int returning...`
+ 现在我们在函数括号外了，继续移动看到`void`, 那么...
    `"fp is a pointer to a function passing int returning nothing (void)`
+ 我们已完成对`fp`的解析，现在返回`signal`，我们现在有...
    `"signal is a function passing an int and a pointer to a function passing an int returning nothing (void) returning...`
+ 我们仍在括号内，下一个看到的符号是`*`，那么...
    `"signal is a function passing an int and a pointer to a function passing an int returning nothing (void) returning a pointer to...`
+ 我们现在已经解析完括号内的所有声明项了，继续顺时针移动，看到另一个`(`，那么...
    `"signal is a function passing an int and a pointer to a function passing an int returning nothing (void) returning a pointer to a function passing an int returning...`
+ 最后继续移动，现在唯一剩下的项就是`void`了, 于是`signal`的最终完整定义是:
    `“signal is a function passing an int and a pointer to a function passing an int returning nothing (void) returning a pointer to a function passing an int returning nothing (void)"`

翻译成中文：`signal`是一个函数，该函数有一个`int`和一个指向函数的指针类型的参数fp，并返回一个函数指针; 其中，作为参数的函数指针fp所指向的函数，具有一个`int`参数并返回`void`;作为返回值的函数指针所指向的函数，具有一个`int`参数并返回`void`。

相同的法规同样适用于`const`和`volatile`。例如：

`const char *chptr;`

chptr是什么 ??

`"chptr is a pointer to a char constant"`

那么这个呢： `char * const chptr;`

chptr是什么 ??
`”chptr is a constant pointer to char“`

最后: `Volatile char * const chptr;`

chptr是什么 ??
`"chptr is a constant pointer to a char volatile."`

快用本法规来实践`K&R II`第122页上找到的例子吧 ;)
