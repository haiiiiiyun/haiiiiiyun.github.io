---
title: Python 2 标准库示例：2.3 heapq-堆排序算法
date: 2017-05-27
writing-time: 2017-05-27 11:05
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture heapq
---


**目的**: 实现了一个适用于 Python 列表的最小堆排序算法。

**Python 版本**: 2.3+

*heap* 是一个树型数据结构，它的子结点与父结点之前都有排序关系。*二叉堆 binary heap* 可用一个列表或数据来表示，其第 N 层的子元素的存储位置为 `2*n+1` 和 `2*n+2`(基于 0 的索引）。

最大堆 *max-heap* 确保父结点值总是大于或等于它的所有子结点值，而最小堆 *min-heap* 确保了父结点值总是小于或等于它的所有子结点值。 *heapq* 模块实现了二叉 *min-heap*。

测试数据和堆显示函数如下：


```python
import math
from cStringIO import StringIO

DATA = [19, 9, 4, 10, 11]

def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i+1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2**row
        col_width = int(math.floor((total_width*1.0) / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print output.getvalue()
    print '-' * total_width
    print
    return
```

# 创建

创建堆有两种基本方法： 

1. *heappush()* : 将元素逐个添加个堆中。
2. *heapify()*：将现有的列表堆化。


```python
import heapq
import copy

print 'From heappush:'

heap = []
print 'data: ', DATA
print

for n in DATA:
    print 'add %3d:' % n
    heapq.heappush(heap, n)
    show_tree(heap)
    
    
print 'From heapify:'
print 'data: ', DATA
data = copy.copy(DATA)
heapq.heapify(data)
print 'heapified: '
show_tree(data)
```

    From heappush:
    data:  [19, 9, 4, 10, 11]
    
    add  19:
    
                     19                 
    ------------------------------------
    
    add   9:
    
                     9                  
            19        
    ------------------------------------
    
    add   4:
    
                     4                  
            19                9         
    ------------------------------------
    
    add  10:
    
                     4                  
            10                9         
        19   
    ------------------------------------
    
    add  11:
    
                     4                  
            10                9         
        19       11   
    ------------------------------------
    
    From heapify:
    data:  [19, 9, 4, 10, 11]
    heapified: 
    
                     4                  
            9                 19        
        10       11   
    ------------------------------------
    


# 访问堆内容

一旦堆组织好后，可用 *heappop* 移除并返回最小值的元素。


```python
import heapq
import copy

data = copy.copy(DATA)
print 'data: ', data
heapq.heapify(data)
print 'heapified:'
show_tree(data)
print

for i in xrange(2):
    smallest = heapq.heappop(data)
    print 'pop %3d:' % smallest
    show_tree(data)
```

    data:  [19, 9, 4, 10, 11]
    heapified:
    
                     4                  
            9                 19        
        10       11   
    ------------------------------------
    
    
    pop   4:
    
                     9                  
            10                19        
        11   
    ------------------------------------
    
    pop   9:
    
                     10                 
            11                19        
    ------------------------------------
    


*heapreplace()* 实现移除并返回最小值元素，并插入一个新元素。


```python
import heapq
import copy

data = copy.copy(DATA)
heapq.heapify(data)
print 'start:'
show_tree(data)

for n in [0, 13]:
    smallest = heapq.heapreplace(data, n)
    print 'replace %2d with %2d:' % (smallest, n)
    show_tree(data)
```

    start:
    
                     4                  
            9                 19        
        10       11   
    ------------------------------------
    
    replace  4 with  0:
    
                     0                  
            9                 19        
        10       11   
    ------------------------------------
    
    replace  0 with 13:
    
                     9                  
            10                19        
        13       11   
    ------------------------------------
    


# 从列表中获取最大或最小值

*heapq* 中的 *nlargest()* 和 *nsmallest()* 函数返回列表（不需要事先堆化）的 n 个最大值或最小值。它们仅当 n 值相对较小时才效率高。


```python
import heapq
import copy

data = copy.copy(DATA)

print 'all:', data
print '3 largest:', heapq.nlargest(3, data)
print 'from sort:', list(reversed(sorted(data)[-3:]))
print '3 smallest:', heapq.nsmallest(3, data)
print 'from sort:', sorted(data)[:3]
```

    all: [19, 9, 4, 10, 11]
    3 largest: [19, 11, 10]
    from sort: [19, 11, 10]
    3 smallest: [4, 9, 10]
    from sort: [4, 9, 10]


# 更多资源

+ [heapq](https://docs.python.org/2.7/library/heapq.html?highlight=heapq#module-heapq) The standard library documentation for this module.
+ [Heap (data structure)](http://en.wikipedia.org/wiki/Heap_(data_structure)) Wikipedia article that provides a general description of heap data structures.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.3.heapq.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.3 heapq-Heap Sort Algorithm](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
