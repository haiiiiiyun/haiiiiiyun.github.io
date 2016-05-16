---
title: Beej的GDB快速指南
date: 2016-05-16
writing-time: 2016-05-14 20:14--2016-05-14 23:00, 2016-05-15 15:37--2016-05-15 17:24 2016-05-15 20:56--2016-05-15 23:04
categories: Programming
tags: C Programming Debug GDB
---

> Beej's Quick Guide to GDB
> Release 2 (2009 Jun 14)
>
> Beej's Quick Guide to GDB by [Brian "Beej Jorgensen" Hall](http://beej.us/guide/bggdb/) is licensed under a
> [Creative Commons Attribution-Noncommercial-No Derivative Works 3.0 United States License](http://creativecommons.org/licenses/by-nc-nd/3.0/us/).
---

本文英文原文在: [http://beej.us/guide/bggdb/](http://beej.us/guide/bggdb/)

---

这是一篇快捷实用的指南，意在指导你从终端命令行开启GNU调试器**gdb**之旅。
gdb通常由IDE开启运行，但是我们很多人因为各种原因而避免使用IDE，这篇教程就是为像你这样的人而写的。

再次说明，这只是一篇入门教程。相较于这里的几段文字说明的功能，还有很多多多关于这个调试器的资料需要去了解。
要获取更多信息，请参考你的"man"页面，或者下面列出的网上资源。

除了**"其它"**章节，这篇教程要求按序阅读。

# 编译

你必需要告诉你的编译器在编译你的代码时，把符号调试信息包含进来。
这里是如何用**gcc**实现的方法，使用**-g**选项：

```shell
$ gcc -g hello.c -o hello

$ g++ -g hello.cpp -o hello
```

之后，你就能在调试器中查看程序的符号列表等信息了。

# 更多信息

请查看[官方GDB文档](http://www.gnu.org/software/gdb/documentation/)。

另外，**DDD**, 即DataDisplayDebugger, 是一个不错的GNU GDB前端。

# 启动调试器

首先记住：你能在任何**gdb**提示符处输入**help**命令来获取帮助信息。另外，你能输入**quit**命令退出调试器。最后，只输入**回车键**将重复最近一次的命令。
现在我们开始吧！

启动调试器有多种方法 (例如，如果你是IDE，你可以通过不太友好的某种特定模式来开启)，但是我在这里只提及两种方法：vanilla console模式和curses GUI模式。GUI模式更好用，但是让我们先说说简单的那个，并在调试器里加载一个叫**hello**的程序：

```
$ gdb hello
GNU gdb 6.8
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-slackware-linux"...
(gdb) run
Starting program: /home/beej/hello 
Hello, world!

Program exited normally.
(gdb) 
```
最后一行是**gdb**提示符，等待你告诉它需要做什么。输入**r**或**run**来运行程序。(只要没有岐义，**gdb**允许你使用简写式的命令。）

**要想开启更酷的并且强烈推荐的GUI模式**，使用**gdb -tui**。（在下面的许多例子中，我只展示了在**gdb**普通终端模式下的输出内容，但在实际工作中我只使用**TUI**模式。）

这里是你可能看到的截图，类似于：

![gdb hellotui](http://beej.us/guide/bggdb/hellotui.png)

所有普通**gdb**命令在GUI模式下都能使用，另外方向键和翻页键可用来滚动源代码窗口（当窗口获取焦点时，默认就会获取焦点）。同时，通过给**list**命令传送一个位置参数，你可以指定某个文件或函数在源代码窗口中显示，
例如，**list hello.c:5**将*hello.c*文件的第５行显示在窗口中。（需知样例位置值，请参考下面的**断点**节，适用于断点的位置值也同样适用于**list**命令。）附带说明下，**list**同样能在普通终端模式下使用。

现在，注意我们是在命令行上传入可执行文件名字的。
另外一种方式是在命令行上只开启**gdb**，然后运行**file hello**，这样能载入可执行文件"hello"。

命令行参数！传入信息到程序的`argv`要怎么做？在开始运行时作为**run**命令的参数传入：

```shell
$ gdb hello
GNU gdb 6.8
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-slackware-linux"...
(gdb) run arg1 arg2
Starting program: /home/beej/hello arg1 arg2
Hello, world!

Program exited normally.
(gdb) 
```

注意上面的"Starting Program"那行, 里面显示"arg1"和"arg2"参数已传给了"hello"。

# 断点

只是启动调试器来运行一下程序不是很有用－我们需要中断执行然后进入步进模式。

首先，在运行**run**命令前，你需要在你想中断的地方设置一个断点。你可以使用**break**或**b**命令，然后指定一个位置值，位置值可以是函数名，行号，或者源文件名加等号。这些都是位置值的样例，它们适用于**break**,也适用于各种其它命令：

<table style="table-layout:fixed;">
<tr>
    <td>break main</td>
    <td>在main()函数的开始处中断</td>
</tr>
<tr>
    <td>break 5</td>
    <td>在当前文件的第5行中断</td>
</tr>
<tr>
    <td>break hello.c:5</td>
    <td>在hello.c的第5行中断</td>
</tr>
</table>

针对这个测试，我们在main()处设置一个断点，然后运行程序：

```shell
$ gdb hello
GNU gdb 6.8
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-slackware-linux"...
(gdb) b main
Breakpoint 1 at 0x8048395: file hello.c, line 5.
(gdb) r
Starting program: /home/beej/hello 

Breakpoint 1, main () at hello.c:5
5		printf("Hello, world!\n");
(gdb)
```
可以看到，我们已经到达**main()**处，并且程序已在我们设置的断点处暂停了。如果我们在普通终端模式下运行，**gdb**会打印出下一条要执行的代码行。如果在GUI模式下运行，下一条要执行的代码行会在源代码窗口中高亮显示。

要列出当前的断点，使用**info**命令，例如："**info breakpoints**"（或者简写为"**i b**"）：

```shell
(gdb) b main
Breakpoint 1 at 0x8048395: file hello.c, line 5.
(gdb) i b
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x08048395 in main at hello.c:5
```

要清空断点，使用带断点位置值的**clear**命令。你也可以通过**delete**命令删除一个断点。

另外，你可以用**enable**或**disable**来启用或禁用断点，但是这两个命令需要断点编号作为参数，不是位置值。
断点的启用/禁用状态信息在断点列表的"Enb"列里能看到。

```shell
(gdb) i b
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x08048395 in main at hello.c:5
(gdb) disable 1
(gdb) i b
Num     Type           Disp Enb Address    What
1       breakpoint     keep n   0x08048395 in main at hello.c:5
(gdb) clear main
Deleted breakpoint 1 
(gdb) i b
No breakpoints or watchpoints.
```

# 步进

一旦暂停在中断点处，你就能让调试器做一些事情。我们从**next**命令（或**n**）开始说起。这个命令带你到当前函数的下一条语句（或者当在函数末尾时返回到函数调用者处）。
这里有一个运行示例；记住**gdb**在"(gdb)"提示符前会打印出*下一条要执行的语句*。另外注意到，当我们在**printf()**行上运行**next**后，我们看到有输出了。

```shell
(gdb) b main
Breakpoint 1 at 0x8048395: file hello.c, line 5.
(gdb) r
Starting program: /home/beej/hello 

Breakpoint 1, main () at hello.c:5
5		printf("Hello, world!\n");
(gdb) next
Hello, world!
7		return 0;
(gdb) next
8	}
(gdb) next
0xb7d6c6a5 in __libc_start_main () from /lib/libc.so.6
(gdb) next
Single stepping until exit from function __libc_start_main, 
which has no line number information.

Program exited normally.
(gdb)
```
（在后面有关 **__libc\_startmain()** 的那行奇怪的东西，说明了有另一个函数在调用你的**main()**函数！它的调试信息没有被编译进来，所以我们看不到源代码，但是我们仍能步进到那里去--我们步进到了那里--然后程序正常退出了。）

现在，注意**next**是步过(step over)函数调用。这不是说函数没有被调用；它是说**next**将执行函数直到结束，然后返回到当前函数的下一行。

怎样才能从当前函数步进(step into)到另一个函数，然后一行行地跟踪那个函数呢？使用**step**（或**s**）命令来完成。
它和**next**类似，除了它是步进到函数中。

比方说我们现在已经厌倦了单步调试，只想再次运行程序。使用**continue**（或**c**）命令来断续执行。

如果程序已在运行但你忘记设置断点呢？你可以按**CTRL-C**键，这样程序会在当前位置暂停并返回"(gdb)"提示符。
在那里，你可以设置一个合适的断点然后继续执行到断点处。

最后一个快捷方式是：只敲一下回车键将重复最后输入的命令；这将省去你一次次输入**next**的麻烦。

# 检查变量

如果你想在运行过程中查看一些变量值，可以使用**display**，但是只有当前处在变量作用域内才可能。
每次你步进代码，变量的值都会显示（如果在作用域内的话）。

（为清晰起见，以下的输出内容不包含源代码部分--你在GUI模式中可以看到。当你运行下面的示例代码时，想像你能看到高亮条在代码行间跳转:)

```shell
(gdb) b main
Breakpoint 1 at 0x8048365: file hello.c, line 5.
(gdb) r
Starting program: /home/beej/hello 

Breakpoint 1, main () at hello.c:5
(gdb) disp i
1: i = -1207447872
(gdb) next
1: i = 1
(gdb) next
1: i = 1
(gdb) next
1: i = 2
(gdb) next
1: i = 2
(gdb) next
1: i = 4
(gdb) next
1: i = 4
(gdb) next
1: i = 4
(gdb) 
```
上面，"i"左边的数字是变量序号。可以用这个数字来**undisplay**该变量。如果忘了序号，你可以输入**info display**来获取：

```shell
(gdb) b main
Breakpoint 1 at 0x8048365: file hello.c, line 5.
(gdb) r
Starting program: /home/beej/hello 

Breakpoint 1, main () at hello.c:5
(gdb) display i
1: i = -1207447872
(gdb) info display
Auto-display expressions now in effect:
Num Enb Expression
1:   y  i
(gdb) undisplay 1
(gdb)
```

如果你只是一次性的想知道变量值，可以用**print**显示。这里我们看到"i"的值是40：

```shell
(gdb) print i
$1 = 40
(gdb)
```

(数字前面的"$"是有意思的，但是初学者不用深研。)

另外还有一个便捷的**printf**命令，可以用它来格式化输出内容：

```shell
(gdb) printf "%d\n", i
40
(gdb) printf "%08X\n", i
00000028
(gdb)
```

# 其它

本节内容不太好放到之前的章节中，但是还是值得在这里列出来。

## 堆栈操作

**backtrace**命令（或**bt**）显示当前函数的调用堆栈，当前函数在最上面，其它调用者依次在下面。

```shell
(gdb) backtrace
#0  subsubfunction () at hello.c:5
#1  0x080483a7 in subfunction () at hello.c:10
#2  0x080483cf in main () at hello.c:16
(gdb)
```

输入**help stack**获取更多有关堆栈操作的信息。

## 其它步进操作方式

退出当前函数并返回调用者函数中，用**finish**命令。

步进单条汇编指令，使用**stepi**命令(step instruction)。

步进到特定位置，使用**advance**命令，并同上面"断点"那一节中显示的那样，指定一个位置值。
下面的例子展示从当前位置开始步进，直到**subsubfunction()**函数被调用为止：

```shell
Breakpoint 1, main () at hello.c:15
15		printf("Hello, world!\n");
(gdb) advance subsubfunction
Hello, world!
subsubfunction () at hello.c:5
5		printf("Deepest!\n");
(gdb) 
```
**advance**命令是“断续运行(**continue**)到这个临时断点”的简略表示。

## 跳到代码中的任意位置 

**jump**命令和**continue**命令完全类似，除了需要一个跳转地址值作为参数。（关于位置值的更多信息，请参与上面的“断点”节。）

如果你想在跳转目的地暂停，先在那里设置一个断点。

## 在运行时修改变量及其值

你可以使用**set variable**命令及一个赋值表达式，它能使你在运行时修改一个变量的值。你也可以用**set**后接带括号的赋值表达式的简写方式：

```shell
Breakpoint 1, main () at hello.c:15
15		int i = 10;
(gdb) print i
$1 = -1208234304
(gdb) set (i = 20)
(gdb) print i
$2 = 20
(gdb) set variable i = 40
(gdb) print i
$3 = 40
(gdb) 
```
这个命令，加个**jump**命令，能使你在不重启程序的情况下重复运行某带代码 。

## 硬件监测点

硬件监测点是一种特殊断点，它当表示值的值改变时触发。
你通常只是想知道变量值何时改变了（写入值），对此你可以用**watch**命令：

```shell
Breakpoint 1, main () at hello.c:5
5		int i = 1;
(gdb) watch i
Hardware watchpoint 2: i
(gdb) continue
Continuing.
Hardware watchpoint 2: i

Old value = -1208361280
New value = 2
main () at hello.c:7
7		while (i < 100) {
(gdb) continue
Continuing.
Hardware watchpoint 2: i

Old value = 2
New value = 3
main () at hello.c:7
7		while (i < 100) {
(gdb)
```
注意**watch**的参数是一个表达式，因此你可以将变量值放进去，或者更复杂些像**\*(p+5)**或**a[15]**。
我甚至试了像`i > 10`这样的表示表达式，但是得到了不同的结果。

你可以用**info break**或**info watch**获取监测点列表，并用**delete**命令和序号来删除。

最后，你可以用**rwatch**命令来检测变量的读操作，使用**awatch**来检测变量的读或写操作。

## 关联到正在运行的进程

假设你的程序已经在运行了，然后你想中断并调试它，首先你需要知道进程ID(PID)，它是个数字。（勇冠Unix **ps**命令获取。）
之后你可以用**attach**命令及PID来关联（并中断）正在运行的程序。

要实现这些，你只需按无参数方式启动**gdb**。

在下面的完整例子中，你会发现一些事情。
我先关联到正在运行的程序，然后它告诉我它正处于某个较深的函数调用中，函数名叫`__nanosleep_nocancel()`，这不会感到很意外，因为我在代码中调用了**sleep()**。实际上，运行**backtrace**命令就准确地显示了这个调用堆栈。因此我调用几个**finish**来返回到**main()**。

```shell
$ gdb
GNU gdb 6.8
Copyright (C) 2008 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-slackware-linux".
(gdb) attach 3490
Attaching to process 3490
Reading symbols from /home/beej/hello...done.
Reading symbols from /lib/libsafe.so.2...done.
Loaded symbols for /lib/libsafe.so.2
Reading symbols from /lib/libc.so.6...done.
Loaded symbols for /lib/libc.so.6
Reading symbols from /lib/libdl.so.2...done.
Loaded symbols for /lib/libdl.so.2
Reading symbols from /lib/ld-linux.so.2...done.
Loaded symbols for /lib/ld-linux.so.2
0xb7eab21b in __nanosleep_nocancel () from /lib/libc.so.6
(gdb) backtrace 
#0  0xb7eab21b in __nanosleep_nocancel () from /lib/libc.so.6
#1  0xb7eab05f in sleep () from /lib/libc.so.6
#2  0x080483ab in main () at hello.c:10
(gdb) finish
Run till exit from #0  0xb7eab21b in __nanosleep_nocancel ()
   from /lib/libc.so.6
0xb7eab05f in sleep () from /lib/libc.so.6
(gdb) finish
Run till exit from #0  0xb7eab05f in sleep () from /lib/libc.so.6
0x080483ab in main () at hello.c:10
10			sleep(1);
(gdb) list
5	{
6		int i = 1;
7	
8		while (i < 60) {
9			i++;
10			sleep(1);
11		}
12	
13		return 0;
14	}
(gdb) print i
$1 = 19
(gdb) quit
The program is running.  Quit anyway (and detach it)? (y or n) y
Detaching from program: /home/beej/hello, process 3490
```

注意到当我返回到**main()**后，我打印了`i`的值，它的值是19--这是因为这时程序已经运行了19秒，而`i`值每秒递增1。

一旦我们退出调试器并断开与程序的关联，程序会折回去然后正常运行。

结合上面的**set variable**，你能做很多事情！

## 利用Coredump进行事后分析

比方说你创建并运行一个程序，然后因为某种原因它的核心转储了：

```shell
$ cc -g -o foo foo.c
$ ./foo
Segmentation fault (core dumped)
```

这表明已经生成了一个叫"core"的核心转储文件（内容是崩溃时的内存快照）。
如果你没有得到一个核心转储文件（也就是说，它只提示“Segmentation fault"然后没有产生核心转储文件），
那么很可能是你的ulimit值设置的太低了；尝试下在shell提示符上输入**ulimit -c unlimited**。

你可以在启动**gdb**时用**-c**选项来指定一个核心转储文件：

```shell
$ gdb -tui -c core foo
```

如果在TUI模式下，一屏幕的信息会映入眼帘，告诉你程序退出的原因（"signal 11, Segmentation fault"），然后出错行会高亮显示。（在普通终端模式下，出错行就被打印出来。）

在这个例子中，我输出引起问题的变量信息。实际上它的值是`NULL`：

![coredump.png](http://beej.us/guide/bggdb/coredump.png)

即便你没有全部源码，获取到程序崩溃时的调用堆栈信息通常也是有用的。

## 窗口功能

在TUI模式下，使用**info win**命令你能获取当前所有窗口的列表。你可以用**focus**（或**fs**）命令来调整窗口的焦点获取
。**focus**要么用窗口外，或者"prev"或"next"做为参数。有效的窗口名是"SRC"（源代码窗口），"CMD"（命令窗口），
"REGS"（寄存器窗口），以及"ASM"（汇编窗口）。如何使用其它几个窗口请参考下面的章节。

注意到当SRC窗口获取焦点时，方向键将移动源代码，但是当CMD窗口获取焦点时，方向键将在命令历史中选择上一条和下一条命令。（在SRC窗口中移动单行和单页的命令分别是`+`、`-`、`<`和`>`。）

```shell
(gdb) info win
        SRC     (36 lines)  <has focus>
        CMD     (18 lines)
(gdb) fs next
Focus set to CMD window.
(gdb) info win
        SRC     (36 lines)
        CMD     (18 lines)  <has focus>
(gdb) fs SRC
Focus set to SRC window.
(gdb)
(Window names are case in-sensitive.)
```

**winheight**（或**wh**）命令用于设置指定窗口的调试，但是我运气太差，它好像不起作用。（译注：在`GNU gdb (Ubuntu 7.11-0ubuntu1) 7.11`上测试时，该命令可用）

## 显示寄存器和汇编代码

在TUI模式下，**layout**命令控制你能看到哪些窗口。另外，**tui reg**允许控制寄存器窗口，然后在窗口还没有打开时会将它打开。

命令有：

The commands are:
<table style="table-layout:fixed;">
<tr>
    <td>layout src</td>
    <td>标准布局－源代码窗口在上面，命令窗口在下面</td>
</tr>
<tr>
    <td>layout asm</td>
    <td>类似"src"布局，除了是汇编窗口在上面</td>
</tr>
<tr>
    <td>layout split</td>
    <td>三个窗口：源代码窗口在上，汇编窗口在中间，命令窗口在底部。</td>
</tr>
<tr>
    <td>layout reg</td>
    <td>在源代码窗口长汇编窗口上面打开寄存器窗口</td>
</tr>
<tr>
    <td>tui reg general</td>
    <td>显示通用寄存器</td>
</tr>
<tr>
    <td>tui reg float</td>
    <td>显示浮点数寄存器</td>
</tr>
<tr>
    <td>tui reg system</td>
    <td>显示"system" 寄存器</td>
</tr>
<tr>
    <td>tui reg next</td>
    <td>显示下页的寄存器－这很重要，因为可能很多页不属于"通用”、"float"或"system"的寄存器。</td>
</tr>
</table>

这里有个漂亮的截图，以便激起你的兴趣，它将源代码和汇编代码显示在“拆分”模式下：

![gdbwinss](http://beej.us/guide/bggdb/gdbwinss.png)

Intel机器上的汇编代码有两种风格：Intel和AT&T。你可以用**set disassembly-flavor**来设置在反汇编窗口中显示哪一种。
有效值是"intel"和"att"。如果你已经打开了汇编窗口，你需要关闭再重新打开。(例如，先**layout src**然后再**layout split**。）

要在普通终端模式下显示寄存器，对于整型寄存器用**info registers**，或者用**info all-registers**显示所有寄存器。

## 写一个前端软件

你在想，“哇，太酷了，但是我可以为它写个杀手级的前端软件，让它更好用！我要怎么做呢？”

GDB支持所谓的“机器界面解析器”，或者叫GDB/MI。在**gdb**命令行上使用**--interpreter**选项可以选择这个解析器。

基本上你是先开启**gdb**然后与它进行命令与结果的交互（可能使用管道）。非常直接了当。

参考[GDB文档](http://sourceware.org/gdb/current/onlinedocs/gdb_26.html#SEC263)来获取更多细节。
