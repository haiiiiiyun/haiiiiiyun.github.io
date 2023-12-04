---
title: Python 2 标准库示例：2.4 bisect-使列表保持有序
date: 2017-05-27
writing-time: 2017-05-27 14:08
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture bisect
---


**目的**: 维护列表的有序性，从而无需在每次添加新元素时调用排序操作。

**Python 版本**: 1.4+

*bisect* 模块实现了基本的二分查询算法 (bisection)。在大数据情况下，使用它来构建一个有序列表比先生成一个普通列表再进行排序效率高。

# 插入元素 INsort in SORTed order

*insort()* 使用二分法查询将元素插入列表中，从而维护列表的有序性。


```python
import bisect
import random

# Use a constant seed to ensure that
# the same pseudo-random numbers
# are used each time the loop is run.
random.seed(1)

print 'New Pos Contents'
print '--- --- --------'

# Generate random numbers and
# insert them into a list in sorted order
l = []
for i in range(1, 15):
    r = random.randint(1, 100)
    pos = bisect.bisect(l, r)
    bisect.insort(l, r)
    print '%3d %3d' % (r, pos), l
```

    New Pos Contents
    --- --- --------
     14   0 [14]
     85   1 [14, 85]
     77   1 [14, 77, 85]
     26   1 [14, 26, 77, 85]
     50   2 [14, 26, 50, 77, 85]
     45   2 [14, 26, 45, 50, 77, 85]
     66   4 [14, 26, 45, 50, 66, 77, 85]
     79   6 [14, 26, 45, 50, 66, 77, 79, 85]
     10   0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
      3   0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
     84   9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
     44   4 [3, 10, 14, 26, 44, 45, 50, 66, 77, 79, 84, 85]
     77   9 [3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
      1   0 [1, 3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]


# 处理重复数据

*bisect* 模块对于重复数据有 2 种处理方法。*insort()* （是 *insort_right()* 的别名) 插入到现有值的右边，而 *insort_left()* 插入到现有值的左边。


```python
import bisect
import random

random.seed(1)

print 'New Pos Contents'
print '--- --- --------'

# Use bisect_left and insort_left.
l = []
for i in range(1, 15):
    r = random.randint(1, 100)
    pos = bisect.bisect_left(l, r)
    bisect.insort_left(l, r)
    print '%3d %3d' % (r, pos), l
```

    New Pos Contents
    --- --- --------
     14   0 [14]
     85   1 [14, 85]
     77   1 [14, 77, 85]
     26   1 [14, 26, 77, 85]
     50   2 [14, 26, 50, 77, 85]
     45   2 [14, 26, 45, 50, 77, 85]
     66   4 [14, 26, 45, 50, 66, 77, 85]
     79   6 [14, 26, 45, 50, 66, 77, 79, 85]
     10   0 [10, 14, 26, 45, 50, 66, 77, 79, 85]
      3   0 [3, 10, 14, 26, 45, 50, 66, 77, 79, 85]
     84   9 [3, 10, 14, 26, 45, 50, 66, 77, 79, 84, 85]
     44   4 [3, 10, 14, 26, 44, 45, 50, 66, 77, 79, 84, 85]
     77   8 [3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]
      1   0 [1, 3, 10, 14, 26, 44, 45, 50, 66, 77, 77, 79, 84, 85]


# 用于查询

模块中提供的函数适用于构建一个有序列表，或者进行元素插入操作。但是不太适合进行查询操作。

下面的几个函数基于 *bisect* 模块中的现有函数，方便了查询操作。


```python
import bisect

def index(a, x):
    'Locate the leftmost value exactly equaly to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect.bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError
    
def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError
    
def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect.bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
    
def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
```

# 更多资源

+ [bisect](https://docs.python.org/2.7/library/bisect.html?highlight=bisect#module-bisect) The standard library documentation for this module.
+ [Insertion Sort](http://en.wikipedia.org/wiki/Insertion_sort) Wikipedia article that provides a description of the insertion sort algorithm.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.4bisect.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.4 Bisect-Maintain Lists in Sorted Order](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
