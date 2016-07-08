---
title: Python 代码风格指南 PEP8 摘要
date: 2016-07-08
writing-time: 2016-07-08 14:57
categories: programming
tags: python programming
---

# 代码布局

## 缩进
每层缩进使用 4 个空格

## 断行规则

1. 

```
# 断行开头与括号等分隔符的开始符号垂直对齐
# 这种断行方式下首行的分隔符后要包含其它参数，如 var_one, var_two
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

2.
```
# More indentation included to distinguish this from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```



> 参考文献： [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)
