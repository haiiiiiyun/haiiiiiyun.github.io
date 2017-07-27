---
title: Python 2 标准库示例：5.2 fractions-有理数
date: 2017-07-27
writing-time: 2017-07-27
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture fractions
---


**目的**: 实现有理数。

**Python 版本**: 2.6+。

*Fraction* 类实现了由 *numbers.Rational* 模块中定义的有理数运算 API.

## 创建 Fraction 实例

实例化后，Fraction 实例都将数规整化成分子(numerator) 和分母(denominator) 两个整数。


```python
import fractions
import decimal

# 1. 通过指定分子(numerator) 和分母(denominator) 来实例化
print 'from (numerator, denominator):'
for n, d in [(1, 2), (2, 4), (3, 6)]:
    f = fractions.Fraction(n, d)
    print '%s/%s = %s' %(n, d, f)
    
print
print 'from string "X/Y":'
# 2. 以分数字符串的形式指定
for s in ['1/2', '  2/4 ', '-3/6']:
    f = fractions.Fraction(s)
    print '%s = %s' % (s, f)
    
print
print 'from string "X.Y":'
# 3. 字符串还可以小数的形式指定
for s in ['0.5', '1.5', '2.0']:
    f = fractions.Fraction(s)
    print '%s = %s' % (s, f)
    
print
print 'from float:'
# 4. 以浮点数指定(v2.7+), v2.7 之前要用 Fraction.from_float() 实现
for v in [0.5, 1.5, 2.0]:
    f = fractions.Fraction(v)
    print '%s = %s' % (v, f)

# 有些 float 无法精确转换成 Fraction， 会出现未期望的结果
print
print 'from float 0.1:'
# 4. 以浮点数指定(v2.7+), v2.7 之前要用 Fraction.from_float() 实现
v = 0.1
f = fractions.Fraction(v)
print '%s = %s' % (v, f)

print
print 'from decimal:'
# 5. 以 Decimal 指定(v2.7+), v2.7 之前要用 Fraction.from_decimal() 实现,
#  和 float 的情况不同，Decimal 没有浮点数的精度问题
for v in [decimal.Decimal('0.1'),
          decimal.Decimal('0.5'),
          decimal.Decimal('1.5'),
          decimal.Decimal('2.0')]:
    f = fractions.Fraction(v)
    print '%s = %s' % (v, f)
```

    from (numerator, denominator):
    1/2 = 1/2
    2/4 = 1/2
    3/6 = 1/2
    
    from string "X/Y":
    1/2 = 1/2
      2/4  = 1/2
    -3/6 = -1/2
    
    from string "X.Y":
    0.5 = 1/2
    1.5 = 3/2
    2.0 = 2
    
    from float:
    0.5 = 1/2
    1.5 = 3/2
    2.0 = 2
    
    from float 0.1:
    0.1 = 3602879701896397/36028797018963968
    
    from decimal:
    0.1 = 1/10
    0.5 = 1/2
    1.5 = 3/2
    2.0 = 2


## 运算

Fraction 实例可以在任何的数学表达式中使用。


```python
import fractions

f1 = fractions.Fraction(1, 2)
f2 = fractions.Fraction(3, 4)

print '%s + %s = %s' % (f1, f2, f1+f2)
print '%s - %s = %s' % (f1, f2, f1-f2)
print '%s * %s = %s' % (f1, f2, f1*f2)
print '%s / %s = %s' % (f1, f2, f1/f2)
```

    1/2 + 3/4 = 5/4
    1/2 - 3/4 = -1/4
    1/2 * 3/4 = 3/8
    1/2 / 3/4 = 2/3


## 近似值

可利用 Fraction 将一个浮点数转换到一个最接近的有理数值。


```python
import fractions
import math

print 'PI = ', math.pi
f_pi = fractions.Fraction(str(math.pi))
print 'No limit = ', f_pi

for i in [1, 6, 11, 60, 70, 90, 100]:
    limited = f_pi.limit_denominator(i) # 限制转换后的分母的最大值
    print '{0:8} = {1}'.format(i, limited)
```

    PI =  3.14159265359
    No limit =  314159265359/100000000000
           1 = 3
           6 = 19/6
          11 = 22/7
          60 = 179/57
          70 = 201/64
          90 = 267/85
         100 = 311/99


## 找到最大公约数

*fractions.gcd(a, b)* 可用来找到最大公约数。


```python
import fractions

# 非 0 时：
print 'gcd(15, 25) = ', fractions.gcd(15, 25)

# b 非 0 时结果取 b 的符号
print 'gcd(15, -25) = ', fractions.gcd(15, -25)

# b  0 时结果取 a 的符号
print 'gcd(-15, 0) = ', fractions.gcd(-15, 0)
```

    gcd(15, 25) =  5
    gcd(15, -25) =  -5
    gcd(-15, 0) =  -15


# 更多资源

+ [The Python Standard Library By Example: 5.2 ](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
+ [fractions](https://docs.python.org/2/library/decimal.html) The standard library documentation for this module.
+ [numbers](https://docs.python.org/2/library/decimal.html) Numberic 抽象基类.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/5.2fractions.ipynb) 
