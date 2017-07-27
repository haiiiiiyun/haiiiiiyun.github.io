---
title: Python 2 标准库示例：5.1 decimal-定点和浮点数学
date: 2017-07-27
writing-time: 2017-07-27
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture decimal
---


**目的**: 使用定点或浮点数进行十进制运算。

**Python 版本**: 2.4+。

*decimal* 模块为十进制浮点数运算提供了支持。相比 *float* 数据类型有如下优势：

+ **decimal** 是基于浮点模型的， 但设计时以人为本， 实现的浮点运算以普通人熟悉的方式进行，而不是程序员的 IEEE 浮点数的样子。
+ decimal 数可以精确表示。而像 1.1 或 2.2 等浮点数却不能用二进制浮点数精确表示。
+ 精度在运算中也会保留，因此， Decimal 数运算 `0.1+0.1+0.1-0.3` 的结果会是 0，但在二进制浮点数运算中， 结果会是 5.5511151231257827e-017。
+ decimal 模块引入了有效位的概念，因此 `1.30+1.20` 的值是 2.50， 末尾的 0 会被保留用来表明有效位，类似的，相乘时两个乘数的有效位也会被保留，例如 `1.3*1.2` 为 `1.56`，`1.30*1.20` 为 `1.5600`。
+ 与基于硬件实现的二进制浮点数不同， decimal 模块的精度（默认是 28 位）是可定制的。
+ 内置的 float 类型只导出了部分的浮点数功能，而 decimal 模块实现了浮点数的所有功能，程序员可以完全控制舍入(rounding), 信号量处理（signal handling）等。

该模块的设计基于 3 个概念：十进制数，运算上下文和信号。

## 十进制数

十进制数值用 `Decimal` 类的实例表示。




```python
import decimal

fmt = '{0:<25} {1:<25}'
print fmt.format('Input', 'Output')
print fmt.format('-' * 25, '-' * 25)

# 1. 没有参数时实例化返回 Decimal('0')
print fmt.format('', decimal.Decimal())

# 2. 用整数作为参数来实例化
print fmt.format(5, decimal.Decimal(5))

# 3. 用字符串作为参数来实例化
print fmt.format('3.14', decimal.Decimal('3.14'))

# 4. 从 v2.6+ 开始，字符串前后允许有空白字符
print fmt.format('  -3.14  ', decimal.Decimal('  -3.14  '))

# 5. 从 v2.7+ 开始，允许直接舍入 float 值进行实例化，参数的二进制浮点值将无损转换到十进制值，
# 无法精确表示的二进制浮点数，转换后会舍入。
print fmt.format(1.1, decimal.Decimal(1.1))

# 6. 之前的版本，要先将 float 转换成字符串再传处， 或者通过 Decimal.from_float() 进行
f = 1.1
print fmt.format(repr(f), decimal.Decimal(str(f)))
print fmt.format('%.23g' %f, str(decimal.Decimal.from_float(f))[:25])

# 7. 通过舍入 tuple (sign, (digit1, digit2, ...), exponent) 来实例化， 其中 sign 为 0 时表示正数， 1 时为负数，
#    (digit1, digit2, ...) 表示出现的数字，而 exponent 是个整数的指数
print fmt.format((1, (3, 1, 4), -2), decimal.Decimal((1, (3, 1, 4), -2)))
```

    Input                     Output                   
    ------------------------- -------------------------
                              0                        
    5                         5                        
    3.14                      3.14                     
      -3.14                   -3.14                    
    1.1                       1.100000000000000088817841970012523233890533447265625
    1.1                       1.1                      
    1.1000000000000000888178  1.10000000000000008881784
    (1, (3, 1, 4), -2)        -3.14                    


基于 tuple 的表示不便于用来实例化，但可用来导出 Decimal 值的无损精度表示，也可用 tuple 的形式在网络上传输，或保存在数据库中。

## 运算

Decimal 实例的运算与内置的数字类型的运算相似。


```python
import decimal

a = decimal.Decimal('5.1')
b = decimal.Decimal('3.14')
c = 4
d = 3.14

print 'a=', repr(a)
print 'b=', repr(b)
print 'c=', repr(c)
print 'd=', repr(d)
print

print 'a+b=', a+b
print 'a-b=', a-b
print 'a*b=', a*b
print 'a/b=', a/b
print

print 'a+c=', a+c
print 'a-c=', a-c
print 'a*c=', a*c
print 'a/c=', a/c

print 'a+d=', 
try:
    print a+d
except TypeError, e:
    print e
```

    a= Decimal('5.1')
    b= Decimal('3.14')
    c= 4
    d= 3.14
    
    a+b= 8.24
    a-b= 1.96
    a*b= 16.014
    a/b= 1.624203821656050955414012739
    
    a+c= 9.1
    a-c= 1.1
    a*c= 20.4
    a/c= 1.275
    a+d= unsupported operand type(s) for +: 'Decimal' and 'float'


Decimal 数可与整数相互运算，但是浮点数必须先转换为 Decimal 实例后才能相互运算。

除了基本运算外，Decimal 实例还有获取基于 10 或自然数的 log 值的函数，如：


```python
import decimal

print 'decimal.Decimal(100).log10()=', decimal.Decimal(100).log10()
print 'decimal.Decimal(100).ln()=', decimal.Decimal(100).ln()
```

    decimal.Decimal(100).log10()= 2
    decimal.Decimal(100).ln()= 4.605170185988091368035982909


## 特殊值

Decimal 可表示一些特殊值，如正负无穷大， NaN，和 0 等。


```python
import decimal

for value in ['Infinity', 'NaN', '0']:
    print decimal.Decimal(value), decimal.Decimal('-' + value)
print

# 与无穷大的运算结果都为无穷大
print 'Infinity + 1:', (decimal.Decimal('Infinity') + 1)
print '-Infinity + 1:', (decimal.Decimal('-Infinity') +1)

# 与 NaN 的比较结果都是 False
print decimal.Decimal('NaN') == decimal.Decimal('Infinity')
print decimal.Decimal('NaN') != decimal.Decimal(1)
```

    Infinity -Infinity
    NaN -NaN
    0 -0
    
    Infinity + 1: Infinity
    -Infinity + 1: -Infinity
    False
    True


## 上下文 Context

上面的所有例子都使用了 decimal 模块的模块行为。不过通过 *context*，可以定制精度、舍入、错误处理等设置。*context* 可应用于一个线程中或者某代码段中的所有 Decimal 实例。

### 当前上下文

获取当前的全局上下文使用 *getcontext()*。


```python
import decimal
import pprint

context = decimal.getcontext()

# 允许的最大和最小指数值（整数）
print 'Emax =', context.Emax
print 'Emin =', context.Emin

# capitals 域的值为 0 或 1 (默认值).
# 值为 1 时，指数打印输出时用 E 表示，否则用小写 e 表示，如 Decimal('6.02e+23').
print 'capitals =', context.capitals

# 精度
print 'prec =', context.prec

# 舍入
print 'rounding =', context.rounding

print 'flags ='
pprint.pprint(context.flags)

print 'traps ='
pprint.pprint(context.traps)
```

    Emax = 999999999
    Emin = -999999999
    capitals = 1
    prec = 28
    rounding = ROUND_HALF_EVEN
    flags =
    {<class 'decimal.Clamped'>: 0,
     <class 'decimal.InvalidOperation'>: 0,
     <class 'decimal.DivisionByZero'>: 0,
     <class 'decimal.Inexact'>: 1,
     <class 'decimal.Rounded'>: 1,
     <class 'decimal.Subnormal'>: 0,
     <class 'decimal.Overflow'>: 0,
     <class 'decimal.Underflow'>: 0}
    traps =
    {<class 'decimal.Clamped'>: 0,
     <class 'decimal.InvalidOperation'>: 1,
     <class 'decimal.DivisionByZero'>: 1,
     <class 'decimal.Inexact'>: 0,
     <class 'decimal.Rounded'>: 0,
     <class 'decimal.Subnormal'>: 0,
     <class 'decimal.Overflow'>: 1,
     <class 'decimal.Underflow'>: 0}


### 精度

上下文中的 `prec` 属性控制运算时生成的新值的精度（即非零有效数字）。明确实例化的值不受此控制。


```python
import decimal

d = decimal.Decimal('0.123456')
for i in range(4):
    decimal.getcontext().prec = i
    print i, ':', d, d * 1
```

    0 : 0.123456 0
    1 : 0.123456 0.1
    2 : 0.123456 0.12
    3 : 0.123456 0.123


### 舍入

由于存在精度限制，故有舍入。下面是支持的舍入方式。

+ **ROUND_CEILING**: 向上舍入。
+ **ROUND_FLOOR**: 向下舍入。
+ **ROUND_DOWN**: 向零舍入。
+ **ROUND_HALF_DOWN**: 当最低有效位小于或等于 5 时，向零舍入；否则偏离零方向舍入。
+ **ROUND_HALF_EVEN**: 类似 **ROUND_HALF_DOWN**，但当最低有效位为 5 时，进行向偶数舍入，即此时当前一个数字是偶数时向下舍入，前一个数字是奇数是向上舍入。
+ **ROUND_HALF_UP**: 类似 **ROUND_HALF_DOWN**，但当最低有效位为 5 时，进行偏离零方向舍入。
+ **ROUND_05UP**: 如果最低有效位之前的数字是 0 或 5 时，进行偏离零方向舍入， 否则向零舍入。


```python
import decimal
 
context = decimal.getcontext()

ROUNDING_MODES = [
    'ROUND_CEILING',
    'ROUND_FLOOR',
    'ROUND_DOWN',
    'ROUND_HALF_DOWN',
    'ROUND_HALF_EVEN',
    'ROUND_HALF_UP',
    'ROUND_UP',
    'ROUND_05UP',
]


values = ['0.123', '0.125', '0.127', '-0.133', '-0.135', '-0.137']
header_fmt = '{:10} ' + ' '.join(['{:^8}'] * 6)
print header_fmt.format(' ', *values )

for rounding_mode in ROUNDING_MODES:
    print '{0:10}'.format(rounding_mode.partition('_')[-1]),
    for v in values:
        context.rounding = getattr(decimal, rounding_mode)
        context.prec = 2
        value = decimal.Decimal(v) * 1
        print '{0:^8}'.format(value),
    print
```

                0.123    0.125    0.127    -0.133   -0.135   -0.137 
    CEILING      0.13     0.13     0.13    -0.13    -0.13    -0.13  
    FLOOR        0.12     0.12     0.12    -0.14    -0.14    -0.14  
    DOWN         0.12     0.12     0.12    -0.13    -0.13    -0.13  
    HALF_DOWN    0.12     0.12     0.13    -0.13    -0.13    -0.14  
    HALF_EVEN    0.12     0.12     0.13    -0.13    -0.14    -0.14  
    HALF_UP      0.12     0.13     0.13    -0.13    -0.14    -0.14  
    UP           0.13     0.13     0.13    -0.14    -0.14    -0.14  
    05UP         0.12     0.12     0.12    -0.13    -0.13    -0.13  


### 局部上下文

v2.5+ 后可以通过 with 语句将 context 应用于代码段。


```python
import decimal

decimal.getcontext().prec = 28

print 'Default precision:', decimal.getcontext().prec
print '3.14 / 3 = ', (decimal.Decimal('3.14') / 3)

print

with decimal.localcontext() as c:
    c.prec = 2
    print 'Local precision:', c.prec
    print '3.14 / 3 = ', (decimal.Decimal('3.14') / 3)
    
print
print 'Default precision:', decimal.getcontext().prec
print '3.14 / 3 = ', (decimal.Decimal('3.14') / 3)
```

    Default precision: 28
    3.14 / 3 =  1.046666666666666666666666666
    
    Local precision: 2
    3.14 / 3 =  1.1
    
    Default precision: 28
    3.14 / 3 =  1.046666666666666666666666666


### 预生成 Context 实例

Context 实例可用来创建 Decimal 实现， 创建时会使用该 Conctext 实例中的设置信息。


```python
import decimal

# Set up a context with limited precision
c = decimal.getcontext().copy()
c.prec = 3

# Create our constant
pi = c.create_decimal('3.1415')

# The constant value is rounded off
print 'PI:', pi

# The result of using the constant uses the global context
print 'RESULT:', decimal.Decimal('2.01') * pi
```

    PI: 3.14
    RESULT: 6.3114


### 线程

**global** 的上下文，实际上是针对每个线程的， 即每个线程都有自己独立的 global default context。


```python
import decimal
import threading
from Queue import PriorityQueue

class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)
        
    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c) # set own global default context
        self.q.put( (self.prec, a * b) )
        return
    
a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')

# A PrioriyQueue will return values sorted by precision, no matter
# what order the threads finish.
q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()
    
for t in threads:
    t.join()
    
for i in range(5):
    prec, value = q.get()
    print prec, '\t', value
```

    1 	4
    2 	3.9
    3 	3.87
    4 	3.875
    5 	3.8748


# 更多资源

+ [The Python Standard Library By Example: 5.1 Decimal](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
+ [decimal](https://docs.python.org/2/library/decimal.html) The standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/5.1decimal.ipynb) 
