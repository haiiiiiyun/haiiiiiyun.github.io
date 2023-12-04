---
title: Python 2 标准库示例：2.8 copy-复制对象
date: 2017-06-01
writing-time: 2017-05-31 16:16
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture copy
---


**目的**: 提供影子复制和深度复制函数。

**Python 版本**: 1.4+。


*copy* 模块包含 2 个函数， *copy()* 和 *deepcopy()*，用于复制现有对象。


# 影子复制 (shallow copy)

使用 *copy()* 复制出来的是一个新的容器，但其内容都是对源对象内容的引用。


```python
import copy

class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
a = MyClass('a')
my_list = [a]
dup = copy.copy(my_list)

print 'my_list:', my_list
print 'dup:', dup
print 'dup is my_list:', dup is my_list
print 'dup == my_list:', dup == my_list
print 'dup[0] is my_list[0]:', dup[0] is my_list[0]
print 'dup[0] == my_list[0]:', dup[0] == my_list[0]
```

    my_list: [<__main__.MyClass instance at 0xb46d85cc>]
    dup: [<__main__.MyClass instance at 0xb46d85cc>]
    dup is my_list: False
    dup == my_list: True
    dup[0] is my_list[0]: True
    dup[0] == my_list[0]: True


# 深度复制 (deep copy)

使用 *deepcopy()* 复制出来的也是一个新的容器，并且其内容也复制至源对象的内容。


```python
import copy

class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
a = MyClass('a')
my_list = [a]
dup = copy.deepcopy(my_list)

print 'my_list:', my_list
print 'dup:', dup
print 'dup is my_list:', dup is my_list
print 'dup == my_list:', dup == my_list
print 'dup[0] is my_list[0]:', dup[0] is my_list[0]
print 'dup[0] == my_list[0]:', dup[0] == my_list[0]
```

    my_list: [<__main__.MyClass instance at 0xb46d87ac>]
    dup: [<__main__.MyClass instance at 0xb46d878c>]
    dup is my_list: False
    dup == my_list: True
    dup[0] is my_list[0]: False
    dup[0] == my_list[0]: True


# 定制复制的行为

可通过 *__copy__()* 和 *__deepcopy__()* 进行复制行为定制。

+ `__copy__()`: 没有参数，需返回一个影子复制对象。
+ `__deepcopy__()`: 参数是一个备忘录字典 (memo dict)，需返回一个深度复制对象。备忘录字典用于控制递归。


```python
import copy

class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
    def __copy__(self):
        print '__copy__()'
        return MyClass(self.name)
    
    def __deepcopy__(self, memo):
        print '__deepcopy__(%s)' % str(memo)
        return MyClass(copy.deepcopy(self.name, memo))
    
a = MyClass('a')
sc = copy.copy(a)
dc = copy.deepcopy(a)
```

    __copy__()
    __deepcopy__({})


# 深度复制中的递归

为避免复制递归型数据结构时出现的问题，*deepcopy()* 通过一个列表对象来跟踪已复制的对象。


```python
import copy
import pprint

class Graph:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections
        
    def add_connection(self, other):
        self.connections.append(other)
        
    def __repr__(self):
        return 'Graph(name=%s, id=%s)' % (self.name, id(self))
    
    def __deepcopy__(self, memo):
        print '\nCalling __deepcopy__ for %r' % self
        if self in memo:
            existing = memo.get(self)
            print ' Already copied to %r' % existing
            return existing
        print ' Memo dict:'
        pprint.pprint(memo, indent=4, width=40)
        dup = Graph(copy.deepcopy(self.name, memo), [])
        print ' Coping to new object %s' % dup
        memo[self] = dup
        for c in self.connections:
            dup.add_connection(copy.deepcopy(c, memo))
        return dup
    
root = Graph('root', [])
a = Graph('a', [root])
b = Graph('b', [a, root])
root.add_connection(a)
root.add_connection(b)

dup = copy.deepcopy(root)
```

    
    Calling __deepcopy__ for Graph(name=root, id=3027163916)
     Memo dict:
    {   }
     Coping to new object Graph(name=root, id=3027077196)
    
    Calling __deepcopy__ for Graph(name=a, id=3027163852)
     Memo dict:
    {   Graph(name=root, id=3027163916): Graph(name=root, id=3027077196),
        3027166316L: ['root'],
        3072195296L: 'root'}
     Coping to new object Graph(name=a, id=3027164012)
    
    Calling __deepcopy__ for Graph(name=root, id=3027163916)
     Already copied to Graph(name=root, id=3027077196)
    
    Calling __deepcopy__ for Graph(name=b, id=3027163404)
     Memo dict:
    {   Graph(name=a, id=3027163852): Graph(name=a, id=3027164012),
        Graph(name=root, id=3027163916): Graph(name=root, id=3027077196),
        3027163852L: Graph(name=a, id=3027164012),
        3027163916L: Graph(name=root, id=3027077196),
        3027166316L: [   'root',
                         'a',
                         Graph(name=root, id=3027163916),
                         Graph(name=a, id=3027163852)],
        3072195296L: 'root',
        3075206920L: 'a'}
     Coping to new object Graph(name=b, id=3027164108)


上面的有向图的例子中，通过备忘录字典避免了递归复制。

# 更多资源

+ [copy](https://docs.python.org/2/library/copy.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.7copy.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.8 Copy-Duplicate Objects](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
