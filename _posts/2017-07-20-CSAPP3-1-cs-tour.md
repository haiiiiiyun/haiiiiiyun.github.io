---
title: CSAPP3: 1 计算机系统漫游
date: 2017-07-20
writing-time: 2017-07-12
categories: Programming CSAPP3
tags: Programming 《深入理解计算机系统》
---

## 信息就是位 + 上下文

## Amdahl 定律

当对系统的某部分加速时，某对整个系统的性能影响取决于该部分的重要性和加速程度。如果系统原来的运行时间为 $T_{old}$，提速部分运行时间所占比例为 $\alpha$，该部分的提速比例为 $k$，则该部分原来运行所需时间为 $\alpha T_{old}$，而提速后所需时间为 $(\alpha T_{old})/k$。因此，提速后的总运行时间为 $$T_{new} = (1-\alpha)T_{old} + (\alpha T_{old})/k = T_{old}[(1-\alpha) + \alpha/k]$$
由此，计算加速比为 $$S=T_{old}/T_{new} = \frac{1}{(1-\alpha)+\alpha/k}$$

因此，当 $\alpha=0.6$ (60%)，加速因子$k=3$ 时， 加速比 $S=1/[0.4+0.6/3]=1.67$ 倍。可见，虽然对系统的一个主要部分做出了重大改进，但是整体系统的加速比还是很小。

Amdahl 定律的主要观点是：要想显著加速整个系统，必须提升全系统中相当大部分的速度。


当对某部分的加速因子 $k$ 走向于 $\infty$ 时，即运行时间可忽略不计时，整个系统的加速比为 $$S\infty = \frac {1}{(1-\alpha)}$$

此时，当 $\alpha=0.6$ 时，加速比 $=1/(1-0.6)=2.5$。可见，即使 60% 部分的系统做了最大改善，整体上也只能提速 2.5 倍。

## 参考

+ [Jupter 中输入数字公式例子](http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Typesetting%20Equations.html)
+ [在Jupyter Notebook里面写Python代码和数学公式](http://blog.csdn.net/winnerineast/article/details/52274556)
+ [MathJax 支持的 Latex 符号总结](http://blog.csdn.net/liyuanbhu/article/details/50636416)
+ [深入理解计算机系统](https://www.amazon.cn/dp/B01N03IQK4/ ) The standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/csapp-v3-ipynb/blob/master/1_tour_of_cs.ipynb) 
