---
title: Beej的GDB快速指南
date: 2016-05-14 20:14
writing-time: 2016-05-14 20:14--2016-05-14 23:00, 2016-05-15 15:37 2016-05-15 17:24
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

For this, you can just start gdb with no arguments.

In the following complete run, you'll notice a few things. First I attach to the running process, and it tells me it's in some function deep down called __nanosleep_nocancel(), which isn't too surprising since I called sleep() in my code. Indeed, asking for a backtrace shows exactly this call stack. So I say finish a couple times to get back up to main().

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
Notice that when I get back to main(), I print the value of i and it's 19—because in this case the program has been running for 19 seconds, and i gets incremented once per second.

Once we've quit the debugger and detached from the program, the program returns to running normally.

Mix this with set variable, above, and you've got some power!

Using Coredumps for Postmortem Analysis
Let's say you build and run a program, and it dumps core on you for some reason or another:

$ cc -g -o foo foo.c
$ ./foo
Segmentation fault (core dumped)
This means that a core file (with a memory snapshot from the time of the crash) has been created with the name "core". If you're not getting a core file (that is, it only says "Segmentation fault" and no core file is created), you might have your ulimit set too low; try typing ulimit -c unlimited at your shell prompt.

You can fire up gdb with the -c option to specify a core file:

$ gdb -tui -c core foo
And, if in TUI mode, you'll be greeted with a screen of information, telling you why the program exited ("signal 11, Segmentation fault"), and the highlight will be on the offending line. (In dumb terminal mode, the offending line is printed out.)

In this example, I print the variable that's causing the problem. Indeed it is NULL:


Even if you don't have all the source code, it's often useful to get a backtrace from the point the program crashed.

Window Functions
In TUI mode, you can get a list of existing windows with the info win command. You can then change which window has focus with the focus (or fs) command. focus takes either a window name, or "prev" or "next" as an argument. Valid window names are "SRC" (source window), "CMD" (command window), "REGS" (registers window), and "ASM" (assembly window). See the next section for how to use these other windows.

Note that when the SRC window has focus, the arrow keys will move the source code, but when the CMD window has focus, the arrow keys will select the previous and next commands in the command history. (For the record, the commands to move the SRC window single lines and single pages are +, -, <, and >.)

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

The winheight (or wh) command sets the height of a particular window, but I've had bad luck with this working well.

Display Registers and Assembly
In TUI mode, the layout command controls which windows you see. Additionally, the tui reg allows control of the register window, and will open it if it's not already open.

The commands are:
layout src	Standard layout—source on top, command window on the bottom
layout asm	Just like the "src" layout, except it's an assembly window on top
layout split	Three windows: source on top, assembly in the middle, and command at the bottom
layout reg	Opens the register window on top of either source or assembly, whichever was opened last
tui reg general	Show the general registers
tui reg float	Show the floating point registers
tui reg system	Show the "system" registers
tui reg next	Show the next page of registers—this is important because there might be pages of registers that aren't in the "general", "float", or "system" sets
Here's a nifty screenshot to whet your appetite, showing source and assembly in "split" mode:


Assembly code comes in two flavors on Intel machines: Intel and AT&T. You can set which one appears in the disassembly window with set disassembly-flavor. Valid values are "intel" and "att". If you already have the assembly window open, you'll have to close it and reopen it (layout src followed by layout split, for example.)

To display registers in dumb terminal mode, type info registers for the integer registers, or info all-registers for everything.

Writing a Front-End
You're thinking, "Wow, this is pretty cool, but I could write a killer front-end for this thing that worked so much better! How do I do it?"

GDB supports what it calls the "machine interface interpreter", or GDB/MI. The interpreter is selected on the gdb command line with the --interpreter switch.

Basically you'll launch gdb and read commands and results to and from it (probably using pipes). Pretty straightforward.

See the GDB documentation for all the details.
