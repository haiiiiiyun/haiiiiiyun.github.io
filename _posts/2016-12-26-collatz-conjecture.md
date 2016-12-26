---
title: Collatz 猜想，即 3n+1 问题
date: 2016-12-26
writing-time: 2016-12-26 15:37
categories: Tools
tags: Python Collatz&nbsp;Conjecture
---

Collatz 猜想，即著名的 "3n+1" 数学问题。它假设一个接受一个正整数 n 为参数的函数，当参数 n 是偶数时，函数将返回 n/2;当 参数 n 为奇数时，函数将返回 3n+ 1。

![Collatz 猜想](/assets/images/collatz-conjecture.jpg)

Collatz 猜想声称：对于任何一个正整数，只要经过足够多次的以上变换，最终会得到值 1。

```python
def collatz(n):
    ret = [n,]
    while n != 1:
        if n%2 == 0:
            n /= 2
        else:
            n = 3*n+1
        ret.append(n)
    return ret
```

# 参考文献

+ [CsForAll: Functional Programming](https://www.cs.hmc.edu/csforall/FunctionalProgramming/functionalprogramming.html)
+ [Collatz猜想](https://www.douban.com/note/297211518/)
