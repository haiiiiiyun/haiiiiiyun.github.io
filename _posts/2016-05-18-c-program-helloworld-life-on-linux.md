---
title: helloword程序在Linux系统上的一生
date: 2016-05-18
writing-time: 2016-05-19 09:24--11:01
categories: Programming
tags: C Programming Linux CSAPP
---

记录C语言程序helloworld在Linux系统上从编写、编译到调用的全过程。

# 一、编写源代码

经典的helloworld程序，源代码`hello.c`如下：

```c
#include <stdio.h>

int main()
{
    printf("hello, world\n");
}
```

程序员在IDE中，或者文本编辑器（如Vim、Emacs等）中敲入程序源代码，并保存为文本文件`hello.c`，文件的后缀名为`.c`。

文件的内容是由0、1组成的比特串。而每8个比特又组成一组，称为一个字节，因此文件也可以说是由字节串组成的。

大多数电脑用ASCII码表示英文字母及符号，因此，对于上面的源代码，每一个字符在文件中对应保存为一个字节。

在ASCII编码标准中，每个字符对应唯一一个8比特串，也即每个字符对应一个字节值。比如`#`对应一个字节，它的整数值为35，`i`对应另一个字节，它的整数值为105，等等。

对于中文等字符，因为字符数较多，已经不够用一个字节来比较一个字符了（因为一个字节最多能表示256个）。

因此，如果文件中包含有中文等字符的话，文件中的字符一般用unicode编码等表示。

从比特串层面上看，所有信息都表示为0、1的串，这些0、1是解释成一个英文符、汉字、还是整数或者浮点数，是由上下文决定的。因此，信息就是比特串+上下文。

# 二、编译成可执行文件

源代码需要通过编译的过程才能转变成一个可执行文件。

对于在Linux系统上的C源程序`hello.c`来说， 一般调用**gcc**程序来编译：

```
linux> gcc -o hello hello.c 
```

编译过程要经历以下4个阶段：

![编译过程]({{site.url}}/assets/images/c_compile_process.png)

## 1、预处理阶段

在预处理阶段, 预处理程序`cpp`将`#include`指令处的文件内空插入到当前的源程序中，并展开源代码中的宏等操作，处理后，生成一个`.i`后缀的C语言源程序`hello.i`。

## 2、编译阶段

编译程序`cc`将C源程序`hello.i`翻译成汇编程序的源程序，并输出`hello.s`。

## 3、汇编阶段

编译程序`as`将汇编源程序`hello.s`翻译成机器语言指令文件，并输出目标文件`hello.o`，该文件也叫**relocatable object program**。

`hello.o`已经是一个二进制文件了，但是它还不是一个可执行文件。因为像`printf`等函数的目标文件还没有包含进我们的程序中。

## 4、链接阶段

`printf`函数包含在另一个预编译的目标文件`printf.o`中，链接程序`ld`将这些第三方目标文件和`hello.o`合并成一个文件，最终生成我们的可执行文件`hello`。

# 三、调用与执行

我们的可执行文件`hello`保存在硬盘中，可以在shell中调用执行：

```
linux> ./hello
hello, world
linux>
```

`shell`是一个命令行解译程序，它输出一个提示符，并等待用户输入命令名，一旦用户输入命令名并按回车键确定。shell便读取程序的内容，然后执行。

以执行`hello`为例。

shell程序运行后，等待我们输入命令。当我们输入`./hello`时，shell将每个字符读入到寄存器中，再存到内存中。当输入回车键后，shell知道输入完毕了，然后将`hello`文件的内容从硬盘复制到内存中。

之后，处理器依次执行内存中`hello`程序的机器指令，将`hello`程序数据段中的`hello, world\n`字符串中的每个字符依次从内存复制到寄存器中，再从寄存器复制到显示设备中，实现`hello, world`字符串的输出。