---
title: 软件随想录--设计的作用
date: 2016-10-27
writing-time: 2016-10-27 09:42--14:35
categories: programming
tags: Programming 《软件随想录》
---

# 字体平滑、反锯齿和次像素渲染(subpixel rendering)

苹果字体算法的指导思想： 尽可能多地保持原始设计的样子，即使有损屏幕显示的清晰性，也在所不惜。这种方法的好处是屏幕上看到的与印刷出来的样子很接近，缺点是屏幕显示时有时会模糊。

微软字体算法的指导思想：字体的形状一定要适应像素的限制，要保证屏幕显示不模糊、容易辨识，即使字体的形状因此背离原始设计，也在所不惜。这种方法的好处是有利于屏读，缺点是屏幕上看到的与印刷出来的可能差别较大。

苹果将艺术性置于实用性之上，而微软选择实用主义。但在向用户调查哪种更好时，人们总是认为自己熟悉的是最好的。这种现象到处都是，不管是字体应用或平面设计，还是选购银器（人们会挑选小时候用过的样式）。除非受过专门训练，明确知道自己想要什么，否则人们挑中的就是自己最熟悉的。

# 寸土必争

> Dave Winter: 创建一个有使用价值的软件，你必须时时刻刻都在奋斗，每一次的修补，每一个功能，每一处小小的改进，你都在奋斗，目的只是为了再多创造一点空间，可以再多吸引一个用户加入。没有捷径可走。你需要一点运气，但是这不取决于你是否幸运。你之所以会有好运气，那是你寸土必争。(www.scripting.com/2002/01/12.html)

商业软件，是一种寸土必争的游戏。每天前进一小步，将它做得比昨天好一点点。在改正了一个又一个的小细节后，当磨光、定型、擦亮、修饰产品的每个小边角后，就会有神奇的事情发生，最后拿出来的是一件真正优秀的产品。

在你的软件中，即使是看门人的小屋都铺着大理石的地板，配有实心的橡木门和桃花心木的壁板，这个时候，你意识到这是一款优秀软件。


# 大构想的陷阱

有些项目不停地转动轮子，转啊转，但是却一步也没有前进。原因是项目的设想太宏伟了，而细节的设计上不没有跟上。

如果软件设计用形容词描述产品（“刻产品将酷毙了”），而没有提及细节（如 “它的标题栏将是 XXX 颜色，所有的图标将带有一点反光，好像被放在三角钢琴上一样”），那么就很难成功。


# 别给用户太多选择

你给用户的选择越多，他们就越难选择，就会感到越不开心。

> 《出版者周刊》对 Barry Schwartz 《The Paradox of Choice: Why More Is Less》的书评中写到： 大量令人眼花缭乱的选择在我们的大脑中泛滥成灾，令人精疲力竭。太多的选择最终限制了我们的自由，而不是解放了我们。太多的选择实际上损害了我们内心的幸福感。

# 易用性是不够的

一个应用如果具备确实非常重要的功能，而且用户真地非常需要这个功能，那么即使这个程序难用得令人感到可悲，它仍然会大受欢迎。相反，如果一个应用程序，被做成是世界上最容易使用的，但它对任何人都毫无用处，那么它照样完蛋。

但是，在其他条件相同的情况下，易用性设计就是决定性的。

对于充当人与人之间中介的软件，做好易用性设计后，还必须做好社会化界面设计。例如，对于一个论坛系统，如果想限制用户发广告，不应该在用户发广告后提示错误信息，而应该假装成功发布了广告，这样即不冒犯用户，也避免他用其它方式继续尝试发布。

良好的社会化界面设计能创造更多的价值。



> 参考文献： 

+ 《软件随想录》2009 邮电，作者 Joel Spolsky，翻译阮一峰: 设计的作用
