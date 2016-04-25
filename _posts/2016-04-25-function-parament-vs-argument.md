---
title: 函数parameter与argument的区别
date: 2016-04-25 10:40
categories: Programming
tags: Programming C
---

写注释时经常会混淆parameter和argument的用法，特记录下。

Parameter是定义函数参数时的形参，而Argument是调用函数时的实参。

```c
int my_func(int par1, int par2)
{
    /* fun block */
}

int main()
{
    int ret, arg1_val, arg2_val;
    arg1_val = 1;
    arg2_val = 3;
    ret = my_func( arg1_val, arg2_val );
}
```

例如以上的C语言例子中，**my_func**函数定义中的**par1**, **par2**是**parameter**(形参), 而函数调用**ret = my_func( arg1_val, arg2_val )**中的**arg1_val**和**arg1_val**是**argument**(实参)。
