---
title: 软件随想录--经营软件公司
date: 2016-10-30
writing-time: 2016-10-28 23:47--2016-10-30 13:06
categories: programming
tags: Programming 《软件随想录》
---

# 仿生学办公室

+ 许多证据表明，良好的办公空间，尤其是单独的办公室，能够提高程序员的生产率
+ 非常漂亮的，有窗的个人办公室，会使得招募明星程序员变得容易许多
+ 这也是我办公的地方，我会长时间待在这里，远离朋友和家庭，所以这里最好条件好点


程序员办公室的设计需求和实现：

+ 个人办公室，带有可以关上的门。

宽敞、有窗户的个人办公室，而且公共的办公区（供非程序员使用）也被聪明地隐藏在墙壁之间不规则的角落中，这样一来，每个人就都有了自己的个人办公空间，一眼望去不会看到其他人。

+ 需要许多电源接口，可以将各种新颖的小玩意插入与电脑桌齐高的插座，而不用在地板上拖电线。

每张电脑桌都有 20 个电源插孔，其中 4 个是橙色的，与放在一个中央机柜中的不间断电源 UPS 相连，所以你就不需要在每一间办公室中都放一个 UPS。电源插孔都位于桌面之下的一条特殊的槽中，这条槽与桌面等长，你可以将所有的各种线缆都恰到好处地藏在这条槽中，它上面还有一个很方便的盖板，合上后完全与桌面融为一体。

+ 可以方便地转接各种数据线，装修后就再也不用在墙壁上打洞了。

在机房中接近天花板中地方，安装了一套 [桥架系统(Snake Tray System)](http://www.snaketray.com/)，从这里开始贯穿整个办公空间，每间屋子都有。每个办公室里还有一个独立的 8 口交换机，可以把笔记本、台式机、Macbook 都插进去。

+ 办公室可以用来 “结对编程”。

办公桌设计成长条形，因此无论第一个程序员坐在哪里，他的身边总是有空间，可供第二个人再拉一把椅子过来，并排坐下。


+ 整天对着一台显示器工作就需要通过注视远方，使眼睛得到休息，所以显示器不应该靠着一整堵墙摆放。

虽然办公桌是对着墙放的，但是墙上有一个对内的窗口，可以很巧妙地看到隔壁办公室的一角，以及通过那间办公室的窗口向室外看。由于设计非常巧妙，这扇窗口并不影响到私密性。结果是每间办公室的三面墙上都有窗户，其中有两扇可以看到外部，这就符合建筑学上 “两面采光” Light on Two Sides of Every Room 的模式。

+ 办公室应该是一个窝，一个能够很愉快度过时间的地方。

配上小厨房、休息区、沙发、大电视、台球桌、电子游戏主机...


# 他山之石，不可攻玉

为什么很多软件许可证都限制客户修改源码呢？为什么不我们自己的许可证也要这样设计？

如果没有源码，出现问题就没有办法解决。因此应该把职业生涯赌在可信任、可被维护（有源码）的技术上。

同样，要使其他聪明的工程师放心地在我们自己的产品上押注，最好也开放我们的源码。

# 简化性

精简设计被过度宣传了。根据 2/8 法则，20 &#37; 的功能能满足 80 &#37; 的用户，但是每个用户的功能需求都是不一样的，难以归集到 20 &#37; 中。

事实上，最能增加用户数的做法是推出一个带有更多功能的新软件版本。

简化性应该理解为产品的易用性、设计地美学性，但绝不能理解为 “不提供大量功能” 或 “只提供一种功能，并把这种功能完美实现”。故意减少功能的产品是没有前途的。

# 揉一揉，搓一搓

如果基代码杂乱无章，绝对不要推倒重来，应该按以下规则进行重构：

+ 不添加任何新功能
+ 无论何时向源码库提交代码，都要保证程序依然能完善地运行
+ 只做些合乎逻辑的变换，几乎都是机械性的，而且能够立刻确定不会改变代码行为

如果把所有代码推倒重来，可能会犯下和以前同样的错误。

# 组织 beta 测试的十二个最高秘诀

这里所说的软件是指面向大量用户的软件。

1. 开放式的 beta 测试没用。一种情况是有太多测试者（像 Netscape），反馈了太多意见，从而无法找出有用的数据;另一种是现有的测试者根据不向你反馈使用情况，无法得到足够的数据。
2. 要想找到那些能够向你反馈意见的测试者，最好的方法是诉诸他们 “言行一致” 的心理。需要让他们自己承诺会向你发送反馈意见，或者更好的方法是，让他们自己申请参加 beta 测试。一旦采取了主动行为，比如填写了申请表，在 “我同意尽快发回反馈意见和软件故障报告” 后，许多人就会发送反馈意见。
3. 不要妄想一次完整的 beta 测试的所有步骤能在少于 8-10 周的时间内完成。
4. 不要妄想在测试中发布新版本的频率能以至于每两周一次。
5. 一次 beta 测试中计划发布的软件版本不要少于 4 个。
6. 如果在测试过程中你为软件添加了一个功能，那么哪怕这个功能非常微小，整个 8 个周期的测试也要回到起点。
7. 即使有一个申请参加 beta 测试的步骤，最后也只有五分之一的测试者会向你提交反馈意见。
8. 制定政策，所有提交反馈意见的测试者都将免费获赠一份正版软件。
9. 需要严肃测试者（即会把反馈意见写成 3 页纸发送给你的人）的最小数据约为 100 人。如果是独立开发软件，这也是你能够处理的反馈意见的最大数量。如果有一支独立的测试管理团队，那么设法分别为每个人员找到 100 个严肃测试者。
10. 根据第 7 条，如果有 3 个测试管理人员，那么需要 300 个严肃测试者，这意味着要准备 1500 份参加测试的申请表。
11. 大多数 beta 测试的参与者只会在第一次拿到这个程序的时候去试用一下，然后就丧失了兴趣。此后每次你推出新版本发送给他们，他们也不会有兴趣重新测试，除非他们每天都在使用。因此，我们需要错开不同版本的测试对象，将所有测试参与者分成四组，每次发布一个新版本，就把一个新组加入测试，这样就能保证每个版本都有第一次使用这个程序的测试者。
12. 不要混淆技术 beta 测试和市场 beta。以上讲的都是技术 beta。

# 建立优质客户服务的七个步骤

## 每件事都有两种做法

几乎所有技术支持方面的问题都有两种解决方法。一种是表面的、快速的解决方法，只求把问题解决了了事。但是只要你深入一点思考，就会发现还有另一种方法，能够防止类似的问题再次发生。

对每一个技术支持，即可修复，放入知识库，也要彻查原因，彻底解决。这有两个含义：

+ 技术支持团队必须能够与开发团队直接沟通，这很关键，这意味着不能把技术支持人员外包，他们必须与开发人员在同一个地址办公，必需有途径让问题彻底解决。
+ 每次发生问题，都寻找方法永久性解决，长此以往，所有觉见问题都会被解决。


## 建议吹掉灰尘

客户打电话抱怨键盘失灵，结果不出所料，原因是键盘没插好。但是直接问客户键盘有没有插好，他们会觉得受到了侮辱。应该换一种说法：有时候键盘接口会有灰尘，导致接触不良。你能不能拔掉键盘插头，吹掉上面的灰尘，然后再把它插回去。

很多时候，要求客户去检查某东西，都可以这样表达。

## 让客户迷上你

客户遇到问题，你帮他解决了，客户实际上变得比没有问题时还要满意。这与期望值有关。大多数人对于技术支持和客户服务的期望值来自于他们同航空公司、电话公司等的经验。

要是有客户打来电话，你要把这当作一个千载难逢的机会，一个可以培养出死心塌地的忠实客户的机会。如果你做得好，客户逢人就会唠叨你的服务是多么出色。

## 承受责备

承担错误，能承认 “这是我的错”。

## 学会说软话

客户有投诉时：

+ 对不起，这是我的错
+ 对不起，我不能收你的钱，这一顿饭算我们的
+ 真是糟糕，请告诉我事情是怎么发生的，我要确保不会再有类似事件

这些话能够使得发怒的顾客变得很高兴。

## 学会做木偶

与顾客争吵，你永远不会是赢家。

面对愤怒的顾客，你只有一条路。你要明白，顾客不是因为你这个人而生气，而是因为你的企业而生气。在顾客面前，你要假装成一个木偶，真正的你则是躲在后面操纵木偶的人。

## 贪婪让你一无所获

90 天的无条件退款保证，即使在第 91 天或 92 天或 203 天打电话来，依然能退款。在网站上发布的招聘广告，如果没有招到人，可以把钱拿回去，这意味着这里发布的广告会比别人多得多，因为顾客不会有任何损失。

这样的一种策略， Fog Creek 在 6 年左右的时间中，因接受顾客的退货而导致的成本也只占总成本的 2 &#37;。

## 为客服人员提供职业发展道路

你需要非常称职的人与顾客交谈。

> 参考文献： 

+ 《软件随想录》2009 邮电，作者 Joel Spolsky，翻译阮一峰: 经营软件公司