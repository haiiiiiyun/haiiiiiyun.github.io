---
title: 软件随想录--编程建议
date: 2016-10-27
writing-time: 2016-10-27 15:48--2016-10-28 17:00
categories: programming
tags: Programming 《软件随想录》
---

# 循证式日程规划

软件开发者并不喜欢做日程规划，总想避开。原因：

+ 做起来比较麻烦
+ 不相信日程规划是可行的


应使用循证式日程规划（Evidence-Based Scheduling, EBS）。

如果日程规划是以 “天” 为单位，就是没用的，必须将日程规划先分解成一些非常小的任务，这些任务能够在以 “小时” 为单位的时间段内完成。但任何任务所需的时间都不能超过 16 小时。

这实际上迫使你想清楚自己要干什么。如果没有仔细想过你要做什么，没有在细节上想清楚详细的工作步骤，就在日程规划上为一个大型任务（如 “完成 Ajax 照片编辑器”）分配 3 个星期，那么其实你不知道它究竟要花费多少时间。

将任务所需的时间控制在 16 小时内，就迫使你好好去规划任务的每个细节，细分每个步骤。


## 追踪时间的用途

保留好工作时间记录单，使每项任务用的时间长度留下可追踪的痕迹。以后就可参考这些数据，估计新任务的时间。


## 对未来情况进行模拟

使用蒙特卡洛方法 (Monte Carlo method)，模拟未来各种可能的结果。可以假设未来存在 100 种可能发生的情况，每一种情况发生的可能性是百分之一，这样就能画出一张图，里面是项目在任意一个日期完成的概率分布。

为了计算任意一名程序员在未来任意一种情况下的实际完成时间，就用每个任务的估计用时去除这个程序员历史数据中完成速率的一个随机选择的值。对 100 种可能发生的情况，重复做这样的计算，这样就能估计出在任意一个日期完成项目的概率。

## 积极管理你的项目

将要实现的功能划分为不同的优先级，这样就很容易看出砍掉那些低优先级的功能会让完成日期提前多少。

## 范围渐变 (scope creep)

scope creep 是项目管理中的一个专门名称，指在开发过程中涉及以前没有考虑到的问题，导致项目的范围越来越大。

在理想情况下，在规划时应为以下的情况预留一段缓冲期：

+ 新的功能设想
+ 对手的新动向
+ 整合中出现的问题
+ 解决各种错误
+ 易用性测试
+ Beta 版测试


## 几条经验

+ 只有一线的程序员才能提出完成日期的估计值，管理层制定的定然不准
+ 一发现错误就立即修正，将用时算入原始的任务用时中
+ 防止管理层向程序员施加压力，要求加快开发速度
+ 一份日程规划就是一个装满木块的盒子。如果你有一堆木块，无法将它们装入盒子，你就只有两个选择，要么找一个大点的盒子（增加规划期），要么拿掉几块木块（删除功能）


日程规划一个最大好处是能迫使你删去不重要的功能，集中精力先完成重要的功能。

# 关于战略问题

## 低速 CPU 和小容量内存的环境

由于硬件发展遵循摩尔定律，所以不必太在意软件的效率问题和内存占用，只要把最酷的功能做出来，然后等着硬件升级就可以了。

CPU、内存、带宽都会越来越便宜，将大量精力投入优化工作，不会带来长期的竞争优势。从长远的观点来看，那些不关心效率、不关心程序是否臃肿、一个劲往软件中加入高级功能的程序员最终将拥有更好的产品。

## 跨平台的编程语言

实现跨平台（跨浏览器）的策略应该像 C 语言一样，它能将程序编译成不同平台、不同系统可能理解的 “本地码”（各种不同的 JavaScript 和 DOM 也是本地码），至于怎么编译，那是编译器的事情了。

## 完善的互动性和用户界面标准

Lotus 1-2-3 和 WordPerfect 在 20 世纪 80 年代占主导地位，但是它们没有统一的界面标准，各自为战，数据甚至无法在相互之间进行复制粘贴。后来出现了 Windows，它上面的 Office 软件功能强大，用户界面与 Windows 操作系统协调一致，程序间可以相互交互，但是程序对机器的性能要求很高，因此一开始没有引起人员的注意。随着机器性能的提升，Office 软件由于其完善的互动性和统一的用户界面，成为了占主导地位的软件，而 Lotus 和 WordPerfect 退出了历史舞台。

类似的情况正发生在现今的 Ajax 开发中，现在不同的 Ajax 应用没有统一的库和接口，相互无法交互（如不能复制粘贴），而 Gmail 等这样的应用占主导地位。一个新的 SDK 出现了，用它开发出的应用都可以协同工作，有相同的界面。这种 SDK 使用一种性能优异的跨平台编程语言，可以直接编译成 JavaScript，只是目前它生成的代码量很大。随着浏览器功能的升级，这种 SDK 的地位最终会像 Windows API 的地位一样，而用它开发的程序也最终会替换 Gmail 等现有应用。


# 你的编程语言做得到吗

具备了 “第一类函数” 功能的编程语言，能让你更容易地完成进一步抽象代码的任务，你的代码体积将更小、更紧凑、更容易重复利用、更方便扩展。

# 让错误的代码显而易见

## 变量的命名

不安全的变量，如那些直接从用户处获取的变量以 us (unsafe) 作为前缀，而安全的变量（如已经 HTML 编码过的）用 s(safe) 作为前缀。进而函数名也采用类似的规则，返回安全变量的以 s 为前缀，如 sEncode，返回不安全变量的以 us 为前缀，如 usRequest;而操作安全变量的用 s 为后缀，如 writeS，等。

## 一些通用规则

+ 尽量将函数写得简短
+ 变量声明的位置离使用的位置越近越好
+ 不要使用宏去创建你自己的编程语言
+ 不要使用 goto
+ 不要让右括号与对应的左括号之间的距离超过一个显示屏


以上这些规则的共同点是：让一行代码相关的所有信息尽可能靠拢，缩短物理距离，这将大大增加你一眼看出程序内部是怎么回事的机会。

寻找一种代码的书写规范，让错误的代码变得容易被看出。让代码中的相关信息在显示屏上集中在一起，使你能够当场发现和改正某些种类的错误。

## 匈牙利命名法

### 正确的匈牙利命名法

也叫做 “应用型匈牙利命名法” Apps Hungarian，它用前缀表示变量的种类(kind)，这是非常有用的。

匈牙利命名法的几种使用举例：

+ us (unsafe) 前缀表示不安全的字符串， s (safe) 表示安全字符串
+ 在 Excel 源码中，用 rw 前缀指行，col 前缀指列
+ cb 前缀代表字节个数 count of bytes
+ ix 表示数组的索引值 index
+ c 表示计数器 count
+ d 表示两个数量之间的差额，如 dx


### 错误的匈牙利命名法，也叫 “系统型匈牙利命名法”

被误解的匈牙利命名法用前缀来表示变量的类型(type)，这没什么大用处。

几种使用举例：

+ l 表示长整型 long
+ ul 表示 unsigned long
+ dw 表示 double word


## 避免使用异常处理

异常处理结构破坏了代码的关联性，相关的代码会分散到不同的地方。为了了解某一行代码是否运行正常，你不得不到其它地方寻找答案，因此就不能利用人的眼睛一目了然的优势学着看出错误的代码。

基于相同的原因，也要避免使用宏。

## 推荐阅读

+ 异常处理的危害： [Raymond Chen 的 文章 Cleaner, More Elegant, and Harder to Recognize](https://blogs.msdn.microsoft.com/oldnewthing/20050114-00/?p=36693)
+ 宏的危害： [Raymond Chen 的 文章 A Rant Against Flow Control Macros]https://blogs.msdn.microsoft.com/oldnewthing/20050106-00/?p=36783)
+ Simonyi 的匈牙利命名法的原始文档: [Hungarian Notaion](https://msdn.microsoft.com/en-us/library/aa260976(VS.60).aspx)
+ Doug Klunder 介绍匈牙利命名法的文章： [Hungarian Naming Conventions](http://www.byteshift.de/msg/hungarian-notation-doug-klunder)


> 参考文献： 

+ 《软件随想录》2009 邮电，作者 Joel Spolsky，翻译阮一峰: 编程建议
