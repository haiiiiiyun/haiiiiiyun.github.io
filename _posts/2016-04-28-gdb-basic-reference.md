---
title: GDB日常调试基本命令列表
date: 2016-04-28 14:25
categories: Programming
tags: Programming
---

![GDB小鱼](/assets/images/GDB-archer.jpg)

[GDB](https://sourceware.org/gdb/) 是GUN项目里的调试器软件，支持Ada, C, C++, Objective-C, Pascal等语言。

<table style="table-layout:fixed;">
<caption style=" font-weight: bold; font-size: 120%; ">GDB日常调试基本命令</caption>
<tr>
    <th style="width:170px;">命令</th><th style="width:150px;">示例</th><th>解释</th>
</tr>
<tr>
    <td>help &lt;GDB命令名&gt;</td>
    <td>(gdb) help set</td>
    <td>GDB帮助命令，若未指定参数，刚分类列表所有GDB命令</td>
</tr>
<tr>
    <td>file &lt;文件名&gt;</td>
    <td>(gdb) file hello</td>
    <td>加载被调试的程序文件。编译时一般通过加*-g*参数将源代码信息编译到需调试的程序中，以方便GDB调试, 如`gcc hello.c -o hello -g`</td>
</tr>
<tr>
    <td>set args &lt;参数设置&gt;</td>
    <td>(gdb) set args &lt;infile.txt</td>
    <td>设置被调试程序的执行参数，如`set args &lt;infile.txt`重定向infile.txt为标准输入文件。</td>
</tr>
<tr>
    <td>set var &lt;变量值设置&gt;</td>
    <td>(gdb) set var i=10</td>
    <td>设置变量值</td>
</tr>
<tr>
    <td>b &lt;行号&gt;<br/>b &lt;函数名&gt;</td>
    <td>(gdb) b 29 <br/>(gdb) b my_func </td>
    <td>b是breakpoint的简写，表示设置断点，可以是某一行或函数的第一行。</td>
</tr>
<tr>
    <td>d [编号]</td>
    <td>(gdb) d 1</td>
    <td>删除编号指定的断点，不指定编号则删除所有断点，d(elete breakpoint)</td>
</tr>
<tr>
    <td>s</td>
    <td>(gdb) s</td>
    <td>执行下一行代码，如果是函数调用，则进入该函数，相当于s(tep Into)</td>
</tr>
<tr>
    <td>n</td>
    <td>(gdb) n</td>
    <td>执行下一行代码，如果是函数调用，不进入该函数，相当于Step Over, n(next)</td>
</tr>
<tr>
    <td>p &lt;变量名&gt;<br/> p[/输出格式] &lt;变量名&gt;</td>
    <td>(gdb) p i<br/>(gdb) p/c i</td>
    <td>`p i`将变量i以十进制数字输出<br/>`p/c i`将变量i以字符格式输出。<br/>支持的格式有x(十六进制)，d(十进制),u(十六进制无符号整型)<br/>o(八进制),t (二进制),c(字符),f(浮点数)</td>
</tr>
<tr>
    <td>q</td>
    <td>(gdb) q</td>
    <td>退出GDB调试</td>
</tr>
</table>
