---
title: Python 2 标准库示例：2.9 pprint-美化数据结构输出
date: 2017-06-01
writing-time: 2017-05-31 16:16--2017-06-01 08:53
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture pprint
---


**目的**: 美化数据结构输出。

**Python 版本**: 1.4+。


*pprint* 中的格式化器产生的数据结构表示，能被解析器正常解析，并且也非常易读。其输出会尽可以放在同一行上，当有跨行时则会添加适当的缩进。

下面是使用的测试数据。


```python
data = [ (1, { 'a':'A', 'b':'B', 'c':'C', 'd':'D' }),
    (2, { 'e':'E', 'f':'F', 'g':'G', 'h':'H',
        'i':'I', 'j':'J', 'k':'K', 'l':'L',
        }),
]
```

# 输出

使用该模板的最简单方法是使用 *pprint()* 函数，它将内容输出到作为参数传入的数据源中（默认为 *sys.stdout*)。


```python
from pprint import pprint

print 'print:'
print data
print
print 'pprint:'
pprint(data)
```

    print:
    [(1, {'a': 'A', 'c': 'C', 'b': 'B', 'd': 'D'}), (2, {'e': 'E', 'g': 'G', 'f': 'F', 'i': 'I', 'h': 'H', 'k': 'K', 'j': 'J', 'l': 'L'})]
    
    pprint:
    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
     (2,
      {'e': 'E',
       'f': 'F',
       'g': 'G',
       'h': 'H',
       'i': 'I',
       'j': 'J',
       'k': 'K',
       'l': 'L'})]


# 格式化

使用 *pformat()* 不进行输出，只返回一个字符串表示。


```python
import logging
from pprint import pformat

logging.basicConfig(level=logging.DEBUG,
                   format='%(levelname)-8s %(message)s',
                   )
logging.debug('Logging pformatted data')
formatted = pformat(data)
for line in formatted.splitlines():
    logging.debug(line.rstrip())
```

    DEBUG    Logging pformatted data
    DEBUG    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
    DEBUG     (2,
    DEBUG      {'e': 'E',
    DEBUG       'f': 'F',
    DEBUG       'g': 'G',
    DEBUG       'h': 'H',
    DEBUG       'i': 'I',
    DEBUG       'j': 'J',
    DEBUG       'k': 'K',
    DEBUG       'l': 'L'})]


# 与其它类兼容

*pprint()* 使用 *PrettyPrinter* 类来格式化，并兼容所有定义了 *__repr__* 的类


```python
from pprint import pprint

class Node(object):
    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]
        
    def __repr__(self):
        return ('Node(' + repr(self.name) + ',' +
               repr(self.contents) + ')'
               )
    
trees = [ Node('Node-1'),
            Node('Node-2', [ Node('Node-2-1')]),
            Node('Node-3', [ Node('Node3-1')]),
        ]
pprint(trees)
```

    [Node('Node-1',[]),
     Node('Node-2',[Node('Node-2-1',[])]),
     Node('Node-3',[Node('Node3-1',[])])]


# 递归

递归数据结构使用 `<Recursion on typename with id=number>` 这种形式的引用来表示。


```python
from pprint import pprint

local_data = ['a', 'b', 1, 2]
local_data.append(local_data)

print 'id(local_data) =>', id(local_data)
pprint(local_data)
```

    id(local_data) => 3028745740
    ['a', 'b', 1, 2, <Recursion on list with id=3028745740>]


# 限制嵌套输出的层级


```python
from pprint import pprint

pprint(data, depth=1)
```

    [(...), (...)]


# 控制输出宽度

格式化后默认的输出宽度是 80 字符，可用 *width* 参数调整。当调整后的宽度太小，折行后出现语法错误，将不会进行折行。


```python
from pprint import pprint

for width in [80, 5]:
    print 'Width = ', width
    pprint(data, width=width)
    print
```

    Width =  80
    [(1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
     (2,
      {'e': 'E',
       'f': 'F',
       'g': 'G',
       'h': 'H',
       'i': 'I',
       'j': 'J',
       'k': 'K',
       'l': 'L'})]
    
    Width =  5
    [(1,
      {'a': 'A',
       'b': 'B',
       'c': 'C',
       'd': 'D'}),
     (2,
      {'e': 'E',
       'f': 'F',
       'g': 'G',
       'h': 'H',
       'i': 'I',
       'j': 'J',
       'k': 'K',
       'l': 'L'})]
    


# 更多资源

+ [pprint](https://docs.python.org/2/library/pprint.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.9pprint.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.9 Pprint-Pretty-Print Data Structures](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
