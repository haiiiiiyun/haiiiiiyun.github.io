---
title: Python 2 标准库示例：3.2 itertools-迭代函数
date: 2017-06-02
writing-time: 2017-06-01
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture itertools
---


**目的**: 实现了一组用于处理序列数据集的函数。

**Python 版本**: 2.3+。


*itertools* 中这些函数都是受 Clojure, Haskell 等函数式编程语言的一些功能特性启发的。

基于迭代的代码，使用的是 "lazy" 处理模式，有更好的内存使用性能。


# 合并和拆分迭代器

*chain()* 函数将参数中的多个迭代器合并成一个迭代器使用。


```python
from itertools import *

for i in chain([1, 2, 3,], ['a', 'b', 'c']):
    print i,
print
```

    1 2 3 a b c


*izip()* 返回的迭代器，其元素是收集至参数中每个迭代器中相同位置的元素，组成的一个元组。它和内置函数 *zip()* 很类似。


```python
from itertools import *

for i in izip([1, 2, 3], ['a', 'b', 'c', 'd']):
    print i
```

    (1, 'a')
    (2, 'b')
    (3, 'c')


*islice()* 返回的迭代器，其元素是基于索引从输入迭代器中选择出来的。它原理和列表的分片操作类似，也接受相同的 3 个参数： start, stop, step。


```python
from itertools import *

print 'Stop at 5:'
# itertools.count() --> [0, 1, 2,...]
for i in islice(count(), 5):  # xrange(5)
    print i,
print '\n'

print 'Star at 5, stop at 10:'
for i in islice(count(), 5, 10): # xrange(5, 10)
    print i,
print '\n'
```

    Stop at 5:
    0 1 2 3 4 
    
    Star at 5, stop at 10:
    5 6 7 8 9 
    


*tee()* 会基于单个的源输入序列，返回多个（默认 2 个）独立的迭代器。其语义和 UNIX 的 *tee* 命令类似，*tee* 命令会将输入中读取的值同时写入一个命名文件及标准输出上。


```python
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)

print 'i1:', list(i1)
print 'i2:', list(i2)
```

    i1: [0, 1, 2, 3, 4]
    i2: [0, 1, 2, 3, 4]


*tee()* 返回的新迭代器与源迭代器共享输入数据，因此，源迭代器中消耗了的数据，新迭代器都不会再出现。


```python
from itertools import *

r = islice(count(), 5)
i1, i2 = tee(r)

print 'r:',
for i in r:
    print i,
    if i > 1:
        break
print

print 'i1:', list(i1)
print 'i2:', list(i2)
```

    r: 0 1 2
    i1: [3, 4]
    i2: [3, 4]


# 转换输入值

*imap()* 函数返回的迭代器，其序列值是对输入迭代器中的每个值调用某个映射函数进行映射后得到。它和内置的 *map()* 函数类似，只不过当某个输入迭代器消耗完后即中止（而不是通过填充 None 以处理完全部输入源）。


```python
from itertools import *

print 'Doubles:'
for i in imap(lambda x:2*x, xrange(5)):
    print i
    
print 'Multiples:'
for i in imap(lambda x,y:(x, y, x*y), xrange(5), xrange(5, 10)):
    print '%d * %d = %d' % i
```

    Doubles:
    0
    2
    4
    6
    8
    Multiples:
    0 * 5 = 0
    1 * 6 = 6
    2 * 7 = 14
    3 * 8 = 24
    4 * 9 = 36


*starmap()* 和 *imap()* 类似，但它不是从多个输入迭代器中获取值构建出一个元组 tuple，而是从单个输入迭代器中抽取出元素，使用 `*` 语法分拆出多个值，以给映射函数使用。


```python
from itertools import *

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
for i in starmap(lambda x,y:(x, y, x*y), values):
    print '%d * %d = %d' % i
```

    0 * 5 = 0
    1 * 6 = 6
    2 * 7 = 14
    3 * 8 = 24
    4 * 9 = 36


# 创造新值

*count()* 函数返回一个能产生无限整数序列的迭代器，序列首元素值可由第 1 个参数指定（默认值为 0）。其参数和 *xrange()* 的类似。


```python
from itertools import *

for i in izip(count(1), ['a', 'b', 'c']):
    print i
```

    (1, 'a')
    (2, 'b')
    (3, 'c')


*cycle()* 返回的迭代器会重复产生参数中的内容。


```python
from itertools import *

for i, item in izip(xrange(7), cycle(['a', 'b', 'c'])):
    print (i, item)
```

    (0, 'a')
    (1, 'b')
    (2, 'c')
    (3, 'a')
    (4, 'b')
    (5, 'c')
    (6, 'a')


*repeat()* 返回的迭代器会重复相同的值，重复次数可由参数 *times* 指定。


```python
from itertools import *

for i in repeat('over-and-over', 5):
    print i
```

    over-and-over
    over-and-over
    over-and-over
    over-and-over
    over-and-over


*repeat()* 组合 *izip()* 或 *imap()* 会很有用。下面是一个计数器组合常量的例子：


```python
from itertools import *

for i, s in izip(count(), repeat('over-and-over', 5)):
    print i, s
```

    0 over-and-over
    1 over-and-over
    2 over-and-over
    3 over-and-over
    4 over-and-over


下面使用 *imap()* 进行乘 2 操作的例子：


```python
from itertools import *

for i in imap(lambda x,y:(x, y, x*y), repeat(2), xrange(5)):
    print '%d * %d = %d' % i
```

    2 * 0 = 0
    2 * 1 = 2
    2 * 2 = 4
    2 * 3 = 6
    2 * 4 = 8


## 过滤

*dropwhile()* 返回的迭代器，它对输入迭代器中的每个元素逐一进行测试，丢弃所有满足测试条件的元素，直到碰到使条件测试返回值为 False 的元素，该元素及之后的所有元素作为返回迭代器中的元素。

即 *dropwhile()* 不对输入源中的每个元素进行测试，当首次使测试返回 False 后，后面的所有元素都将返回。


```python
from itertools import *

def should_drop(x):
    print 'Testing:', x
    return (x<1)

for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print 'Yielding:', i
```

    Testing: -1
    Testing: 0
    Testing: 1
    Yielding: 1
    Yielding: 2
    Yielding: -2


*dropwhile()* 的相反函数是 *takewhile()*。一旦测试返回为 False, 则后面的元素都不再处理。


```python
from itertools import *

def should_take(x):
    print 'Testing:', x
    return (x<2)

for i in takewhile(should_take, [-1, 0, 1, 2, -2]):
    print 'Yielding:', i
```

    Testing: -1
    Yielding: -1
    Testing: 0
    Yielding: 0
    Testing: 1
    Yielding: 1
    Testing: 2


*ifilter()* 与内置的 *filter()* 类似，它会对源输入中的每个元素进行测试。


```python
from itertools import *

def check_item(x):
    print 'Testing:', x
    return (x<1)

for i in ifilter(check_item, [-1, 0, 1, 2, -2]):
    print 'Yielding:', i
```

    Testing: -1
    Yielding: -1
    Testing: 0
    Yielding: 0
    Testing: 1
    Testing: 2
    Testing: -2
    Yielding: -2


*ifilterfalse()* 返回的迭代器中的元素需满足测试函数返回 False。


```python
from itertools import *

def check_item(x):
    print 'Testing:', x
    return (x<1)

for i in ifilterfalse(check_item, [-1, 0, 1, 2, -2]):
    print 'Yielding:', i
```

    Testing: -1
    Testing: 0
    Testing: 1
    Yielding: 1
    Testing: 2
    Yielding: 2
    Testing: -2


# 数据分组

*groupby()* 函数返回一个迭代器，它产生一组基于某键值组织的一个数据集。

下例演示了基于一个属性值分组。


```python
from itertools import *
import operator
import pprint

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return '(%s, %s)' % (self.x, self.y)
    
    def __cmp__(self, other):
        return cmp((self.x, self.y), (other.x, other.y))
    
# Create a dataset of Point instances
data = list(imap(Point,
                cycle(islice(count(), 3)),
                islice(count(), 7),
                )
           )
print 'Data:'
pprint.pprint(data, width=69)
print

# Try to group the unsorted data based on X values
print 'Grouped, unsorted:'
for k, g in groupby(data, operator.attrgetter('x')):
    print k, list(g)
print

# sort the data
data.sort()
print 'Sorted:'
pprint.pprint(data, width=69)
print

# Group the sorted data based on X values
print 'Grouped, sorted:'
for k, g in groupby(data, operator.attrgetter('x')):
    print k, list(g)
print
```

    Data:
    [(0, 0), (1, 1), (2, 2), (0, 3), (1, 4), (2, 5), (0, 6)]
    
    Grouped, unsorted:
    0 [(0, 0)]
    1 [(1, 1)]
    2 [(2, 2)]
    0 [(0, 3)]
    1 [(1, 4)]
    2 [(2, 5)]
    0 [(0, 6)]
    
    Sorted:
    [(0, 0), (0, 3), (0, 6), (1, 1), (1, 4), (2, 2), (2, 5)]
    
    Grouped, sorted:
    0 [(0, 0), (0, 3), (0, 6)]
    1 [(1, 1), (1, 4)]
    2 [(2, 2), (2, 5)]
    


可见，要基于某键分组，输入序列需要事先基于该键预先进行排序。

# 更多资源

+ [itertools](https://docs.python.org/2/library/itertools.html) Standard library documentation for this module.
+ [The Standard ML Basis Library](www.standardml.org/Basis/) The library for SML.
+ [Definition of Haskell and the Standard Libraries](www.haskell.org/definition/) Standard library specification for the functional language Haskell.
+ [Clojure](http://clojure.org/) Clojure is a dynamic functional language that runs on the Java Virtual Machine.
+ [tee](http://unixhelp.ed.ac.uk/CGI/man-cgi?tee) UNIX command line tool for splitting one input into multiple identical output streams.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/3.2itertools.ipynb) 


# 参考

+ [The Python Standard Library By Example: 3.2 Itertools-Iterator Functions](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
