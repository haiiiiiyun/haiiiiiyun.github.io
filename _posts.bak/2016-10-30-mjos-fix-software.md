---
title: 软件随想录--修订软件
date: 2016-10-30
writing-time: 2016-10-30 14:47--16:04
categories: programming
tags: Programming 《软件随想录》
---

# 五个为什么

黑天鹅难题：黑天鹅代表外来因素，是一个超出正常预料的事件。几乎所有的互联网服务中断都来自意料之外的突发事件，属于极其小概率的非主流意外。这类事件是如此罕见，以至于常规的统计方法（如平均故障间隔时间）都失效了。

丰田公司创始人丰田佐吉的五个为什么思想：当某个地方出错的时候，你就问为什么，一遍遍地追问，直到你找到根本性的原因为止。然后，你针对根本性的原因开始着手解决问题，你要从根本上解决这个问题，不是只解决一些表面的症状。

对于服务稳定性问题，由于几乎都是由罕见意外引起的，故设置一个静态值作为目标是毫无意思的。希望通过测量某些无意义的指标来改进工作，那肯定是没用的。不过可以搭建一个博客，在上面实时记录每次的服务中断，提供完整的事后分析，找到根本性的原因，告诉顾客为了防止类似故障再次发生所采取的举措。顾客可访问该博客，从而增强信心，相信我们的服务品质正稳步提高。如果故障对顾客造成了影响，可以要求补偿。

# 确定优先顺序

不应该被采用的两种方法：

+ 你发现你开发某个功能只是因为你答应过一个顾客，这时你的大脑中就应该亮起红色警报。这会使你的开发走向　“个性化软件”　这条危险道路。面向整个市场销售的软件采用顾客　“要么接受、要么放弃”　的开发模式。“定制软件”　是一个暗无天日的世界。
+ 不要因为有些事情不得不做，你就去做。不得不做并不是一个足够好的理由。不是所有必须要做的事情都是同等重要的。不同的事情有不同的重要性，如果你想把所有事情都做完，最后只会一事无成。所以如果要想把事情做完，无论何时，你一定要想清楚什么是眼下最重要、必须马上做好的事。如果不做这件事，你就不能以最快的速度取得进展。不去理会相对不重要的事，把它们留在那里。将办公桌收拾得干干净净，可能表明你的工作效率不高。


正确的方法：

1. 拿出一叠卡片，每一张上写下一个功能。
2. 召集整个团队(这种方法只适合最多 20 人)，在开会前，要求每个人都想好自己想要实现的功能，确保大家对不同功能的含义大致上有一个非常粗略的共同理解。
3. 审查功能项，要求大家对每个功能进行投票表决，简单地表示 “赞成”　或　“反对”　即可。最后将没人赞成或赞成很少的功能去掉。
4. 将每个功能设定一个成本，用 1 到　10 表示，1 表示这个功能可以很容易实现和部署，10 表示这个功能很难实现和部署。
5. 将每个功能及其成本做成一个菜单，规定每个与会人员一个相同的总额（如 50)，要求每人进行　“点菜”。
6. 将每个人在每项功能上花掉的　“钱”　加总起来，最后用　“销售额”　除以　“费用”，以这个值排序，找出最受欢迎的功能。
7. 当然在实施过程中，可以根据实际情况调整。


> 参考文献： 

+ 《软件随想录》2009 邮电，作者 Joel Spolsky，翻译阮一峰: 修订软件