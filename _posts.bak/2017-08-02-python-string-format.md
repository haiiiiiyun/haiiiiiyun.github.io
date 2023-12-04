---
title: 使用 Python 字符串的 format 功能实现自定义格式化输出
date: 2017-08-02
writing-time: 2017-08-02
categories: Programming
tags: Programming Python string format
---

Python V2.6 开始，可用 `str.format()` 来实现 `%` 的格式化输出。字符串中的替换区域用 `{}` 包围，因此如果要输出这两个包围符，需进行转义，如 `{{`, `}}`。

## 基于位置的参数


```python
print '{0} is {1} years old.'.format('haiiiiiyun', 32)

# v2.7 开始可以用 {} 来省略默认的位置序号, '{} {}' 等价于 '{0} {1}'
print '{} is {} years old.'.format('haiiiiiyun', 32)
```

    haiiiiiyun is 32 years old.
    haiiiiiyun is 32 years old.
    

## 基于关键字参数

适合参数多次输出的情况


```python
print '{name} is {age} years old.'.format(name='haiiiiiyun', age=32)
```

    haiiiiiyun is 32 years old.
    

## 基于对象属性值的参数

*arg.name* 将通过 *getattr()* 来获取对象的属性值。


```python
class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age
        
haiiiiiyun = Person('haiiiiiyun', 32)

print '{p.name} is {p.age} years old.'.format(p=haiiiiiyun)
```

    haiiiiiyun is 32 years old.
    

## 基于下标的参数

*arg[index]* 将通过 *__getitem__()* 来获取参数值。


```python
haiiiiiyun = ['haiiiiiyun', 32]

print '{p[0]} is {p[1]} years old.'.format(p=haiiiiiyun)
```

    haiiiiiyun is 32 years old.
    

## 参数值切换

默认在格式化前，每个参数值都通过 *__format__()* 方法进行格式处理。现支持指定两种格式处理方式。

1. `!s` 在参数值上调用 `str()`
2. `!r` 在参数值上调用 `repr()`


```python
class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age
        
    def __str__(self):
        return '"{}"'.format(self.name)
    
    def __repr__(self):
        return '<{}>'.format(self.name)
        
haiiiiiyun = Person('haiiiiiyun', 32)

print 'str:'
print '{p!s} is {p.age} years old.'.format(p=haiiiiiyun)

print 'repr:'
print '{p!r} is {p.age} years old.'.format(p=haiiiiiyun)
```

    str:
    "haiiiiiyun" is 32 years old.
    repr:
    <haiiiiiyun> is 32 years old.
    

## 格式限定

通用格式形式为 `:[[fill]align][sign][#][0][width][,][.precision][type]`。

`align` 指定对齐方式，值有：

值  | 含义
----|
`<` | 左对齐（默认值）
`>` | 右对齐
`=` | 强制填充符接在符号值（如果有的话）后，在数字值前。该选项只对数字参数有限，用来显示如 `+000120` 的数字。
`^` | 居中

`:` 后面要带一个填充字符，默认为空格符。


```python
print "{0:-<10s} {1:->10s} {2:-^10s}".format("Name", "Arg", "Balance")
print "{0:<10s} {1:>10d} {2:^10d}".format("Haiiiiiyun", 32, 120)
```

    Name------ -------Arg -Balance--
    Haiiiiiyun         32    120    
    

`sign` 指定数字值符号的显示方式，值有：

值  | 含义
----|
`+` | 正数和负数都显示符号
`-` | 负数显示，正数不显示（默认）
空格| 表示正数前用空格占位，负数前显示符号


```python
print "{0:->10s} {1:->10s} {2:->10s} {3:->10s} {4:->10s} {5:->10s}".format("", "", "", "", "", "")
print "{0:>+10d} {1:>+10d} {2:>-10d} {3:>-10d} {4:> 10d} {5:> 10d}".format(120, -120, 120, -120, 120, -120,  )
```

    ---------- ---------- ---------- ---------- ---------- ----------
          +120       -120        120       -120        120       -120
    

`#` 只作用于整数值，表示在数字前加前缀，比如二进制数字前加 `0b`, 八进制前加 `0o`，十六进制前加 `0x`。

`,` 表示在多位整数中添加千分位。

`width` 表示数字域的最小长度。`width` 前加 `0` 表示进行 0 填充，等价于对齐方式 `=`。

`precision` 表示浮点数小数点后显示的数字个数。

`type` 指定显示的类型。字符型的有：

类型 | 含义
-----|
s   | 字符串，或直接省略不写

整数型的有：

类型 | 含义
-----|
b   | 二进制。
c   | char, 在输出前将整数转化成对应的 unicode 字符
d   | 十进制，这是默认值，可省略
o   | 八进制
x,X  | 十六进制
n   | 类似 d, 但使用本地的显示设置，如插入千分符等


浮点数型的有：

类型 | 含义
-----|
e, E | 科学计数法表示
f, F | 定点数显示，默认精度是 6
g, G | General format. g 是默认值，可省略。
n   | 类似 g, 但使用本地的显示设置，如插入千分符等
%   | 数字先乘以 100， 再用 f 格式显示，后加 %



```python
print 'Integer:'
print '{:8b} {:8c} {:8d} {:8o} {:8x}'.format(65, 65, 65, 65, 65)
print '{:#8b} {:#8c} {:#8d} {:#8o} {:#8x}'.format(65, 65, 65, 65, 65)
```

    Integer:
     1000001        A       65      101       41
    0b1000001        A       65    0o101     0x41
    

# 参考

+ [string 标准库文档](https://docs.python.org/2.7/library/string.html)
+ [飘逸的python - 增强的格式化字符串format函数](http://blog.csdn.net/handsomekang/article/details/9183303)
