---
title: 回来符与换行符的区别以实现终端中的进度小转轮
date: 2016-09-25
writing-time: 2016-09-25 14:24
categories: Python
tags: Python
---

回车符 `\r`，表示将当前输出位置移到本行的行首。

换行符 `\n`，表示将当前输出位置移到下一行。

实现终端中的进度小转轮的 Python 代码：

```python
while True:
    for i in ["/", "-", "|", "\\", "|"]:
        print "\r%s" % i,
```
