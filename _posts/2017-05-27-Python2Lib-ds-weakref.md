---
title: Python 2 标准库示例：2.7 weakref-非持久对象引用
date: 2017-05-27
writing-time: 2017-05-27 16:16
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture weakref
---


**目的**: 引用 "昂贵" 的对象，但允许在没有其它 *nonweak* 引用时进行垃圾回收。

**Python 版本**: 2.1+

*weakref* 模块支持弱引用。普通引用会增加对象的引用计数，从而阻止了垃圾回收。而弱引用不会阻止垃圾回收，适用于有环路引用的情况。

# 引用

对对象的弱引用通过 *ref* 类来管理。要取回源对象，调用引用对象即可。


```python
import weakref

class ExpensiveObject(object):
    def __del__(self):
        print '(Deleting %s)' % self
        
obj = ExpensiveObject()
r = weakref.ref(obj)

print 'obj:', obj
print 'ref:', r
print 'r():', r()

print 'deleting obj'
del obj
print 'r():', r()
```

    obj: <__main__.ExpensiveObject object at 0xb503aa4c>
    ref: <weakref at 0xb503c43c; to 'ExpensiveObject' at 0xb503aa4c>
    r(): <__main__.ExpensiveObject object at 0xb503aa4c>
    deleting obj
    (Deleting <__main__.ExpensiveObject object at 0xb503aa4c>)
    r(): None


上例中，当被引用对象删除后，调用引用对象返回 *None*。

# 引用回调函数

*ref* 类的构造函数接收一个可选的可调用函数参数，它在被引用对象删除时调用。


```python
import weakref

class ExpensiveObject(object):
    def __del__(self):
        print '(Deleting %s)' % self
        
def callback(reference):
    """Invoked when referenced object is deleted"""
    print 'calling callback(', reference, ')'
    
obj = ExpensiveObject()
r = weakref.ref(obj, callback)

print 'obj:', obj
print 'ref:', r
print 'r():', r()

print 'deleting obj'
del obj
print 'r():', r()
```

    obj: <__main__.ExpensiveObject object at 0xb503ae2c>
    ref: <weakref at 0xb503c9b4; to 'ExpensiveObject' at 0xb503ae2c>
    r(): <__main__.ExpensiveObject object at 0xb503ae2c>
    deleting obj
    calling callback( <weakref at 0xb503c9b4; dead> )
    (Deleting <__main__.ExpensiveObject object at 0xb503ae2c>)
    r(): None


# 代理

使用代理通常比使用弱引用更加便捷。使用代理就跟使用源对象一样，因此使用方无需区别使用的是一个代理还是一个实际对象。


```python
import weakref

class ExpensiveObject(object):
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print '(Deleting %s)' % self
        
obj = ExpensiveObject('My Obj')
r = weakref.ref(obj)
p = weakref.proxy(obj)

print 'via obj:', obj.name
print 'via ref:', r().name
print 'via proxy:', p.name
del obj
print 'via proxy:', p.name
```

    (Deleting <__main__.ExpensiveObject object at 0xb503ad0c>)
    via obj: My Obj
    via ref: My Obj
    via proxy: My Obj
    (Deleting <__main__.ExpensiveObject object at 0xb46eec8c>)
    via proxy:


    ---------------------------------------------------------------------------

    ReferenceError                            Traceback (most recent call last)

    <ipython-input-6-f171937a2b7c> in <module>()
         15 print 'via proxy:', p.name
         16 del obj
    ---> 17 print 'via proxy:', p.name
    

    ReferenceError: weakly-referenced object no longer exists


上例中，当删除被引用对象后，访问代理将抛出 `ReferenceError`。


# 环引用 

图结构包含有环引用，下例中分别用普通对象和代理（弱引用）来演示区别。例子中的图结点都只支持一个出口。


```python
import gc
from pprint import pprint
import weakref

class Graph(object):
    def __init__(self, name):
        self.name = name
        self.other = None
        
    def set_next(self, other):
        print '%s.set_next(%r)' % (self.name, other)
        self.other = other
        
    def all_nodes(self):
        "Generate the nodes in the graph sequence."
        yield self
        n = self.other
        while n and n.name != self.name:
            yield n
            n = n.other
        if n is self:
            yield n
        return
    
    def __str__(self):
        return '->'.join(n.name for n in self.all_nodes())
    
    def __repr__(self):
        return '<%s at 0x%x name=%s>' % (self.__class__.__name__,
                                         id(self), self.name)
    
    def __del__(self):
        print '(Deleting %s)' % self.name
        self.set_next(None)
        
def collect_and_show_garbage():
    "Show what garbage is present."
    print 'Collecting...'
    # run garbage collection, return num of unreachable objects
    n = gc.collect() 
    print 'Unreachable objects:', n
    print 'Garbage:', 
    pprint(gc.garbage)
    
def demo(graph_factory):
    print 'Set up graph:'
    one = graph_factory('one')
    two = graph_factory('two')
    three = graph_factory('three')
    one.set_next(two)
    two.set_next(three)
    three.set_next(one)
    
    print 
    print 'Graph:'
    print str(one)
    collect_and_show_garbage()
    
    print
    three = None
    two = None
    print 'After 2 references removed:'
    print str(one)
    collect_and_show_garbage()
    
    print
    print 'Removing last reference:'
    one = None
    collect_and_show_garbage()
    
    
# __main__
# DEBUG_LEAK causes gc to print info about
# objects that cannot be seen
gc.set_debug(gc.DEBUG_LEAK)

print 'Setting up the cycle'
print
demo(Graph)

print
print 'Breaking the cycle and cleaning up garbage'
print
gc.garbage[0].set_next(None)
while gc.garbage:
    del gc.garbage[0]
print
collect_and_show_garbage()
```


```python
Setting up the cycle

Set up graph:
one.set_next(<Graph at 0xb71ef9ec name=two>)
two.set_next(<Graph at 0xb71efa0c name=three>)
three.set_next(<Graph at 0xb71ef9cc name=one>)

Graph:
one->two->three->one
Collecting...
Unreachable objects: 0
Garbage:[]

After 2 references removed:
one->two->three->one
Collecting...
Unreachable objects: 0
Garbage:[]

Removing last reference:
Collecting...
gc: uncollectable <Graph 0xb71ef9cc>
gc: uncollectable <Graph 0xb71ef9ec>
gc: uncollectable <Graph 0xb71efa0c>
gc: uncollectable <dict 0xb71f935c>
gc: uncollectable <dict 0xb71f93e4>
gc: uncollectable <dict 0xb71f92d4>
Unreachable objects: 6
Garbage:[<Graph at 0xb71ef9cc name=one>,
 <Graph at 0xb71ef9ec name=two>,
 <Graph at 0xb71efa0c name=three>,
 {'name': 'one', 'other': <Graph at 0xb71ef9ec name=two>},
 {'name': 'two', 'other': <Graph at 0xb71efa0c name=three>},
 {'name': 'three', 'other': <Graph at 0xb71ef9cc name=one>}]

Breaking the cycle and cleaning up garbage

one.set_next(None)
(Deleting two)
two.set_next(None)
(Deleting three)
three.set_next(None)
(Deleting one)
one.set_next(None)

Collecting...
Unreachable objects: 0
Garbage:[]
```

下例中创建一个更智能的 *WeakGraph*，它通过使用代理避免了出现环引用。


```python
import gc
from pprint import pprint
import weakref

class WeakGraph(Graph):
    def set_next(self, other):
        if other is not None:
            # see if we should replace the reference
            # to other with a weakref
            if self in other.all_nodes():
                other = weakref.proxy(other)
        super(WeakGraph, self).set_next(other)
        return

# __main__
# DEBUG_LEAK causes gc to print info about
# objects that cannot be seen
gc.set_debug(gc.DEBUG_LEAK)

demo(Graph)
```


```python
Set up graph:
one.set_next(<WeakGraph at 0xb7212aec name=two>)
two.set_next(<WeakGraph at 0xb7212b0c name=three>)
three.set_next(<weakproxy at 0xb7213414 to WeakGraph at 0xb7212acc>)

Graph:
one->two->three
Collecting...
Unreachable objects: 0
Garbage:[]

After 2 references removed:
one->two->three
Collecting...
Unreachable objects: 0
Garbage:[]

Removing last reference:
(Deleting one)
one.set_next(None)
(Deleting two)
two.set_next(None)
(Deleting three)
three.set_next(None)
Collecting...
Unreachable objects: 0
Garbage:[]
```

由于 *WeakGraph* 使用代理来引用已出现的对象，从而避免了出现环引用，垃圾回收机制可回收删除的对象。

# 缓存对象

*ref* 和 *proxy* 类都是 *低层的*。它们可用于维护对单个对象的引用。而 *WeakKeyDictionary* 和 *WeakValueDictionary* 提供了操作多个对象的 API。

*WeakValueDictionary* 继承至 *dict*，但它对其值对象使用了弱引用，允许当其它代码没有使用它们时，可进行垃圾回收。而 *WeakKeyDictionary* 则对其键使用了弱引用。


```python
import gc
from pprint import pprint
import weakref

gc.set_debug(gc.DEBUG_LEAK)

class ExpensiveObject(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return 'ExpensiveObject (%s)' % self.name
    
    def __del__(self):
        print ' (Deleting %s)' % self
        

def demo(cache_factory):
    # hold objects so any weak references
    # are not removed immediately
    all_refs = {}
    # create the cache using the factory
    print 'cache type:', cache_factory
    cache = cache_factory()
    for name in ['one', 'two', 'three']:
        o = ExpensiveObject(name)
        cache[name] = o
        all_refs[name] = o
        del o # decref
        
    print ' all_refs = ',
    pprint(all_refs)
    print '\n Before, cache contains:', cache.keys()
    for name, value in cache.items():
        print ' %s = %s' % (name, value)
        del value # decref
        
    # Remove all refs to the objects except the cache
    print '\n Cleanup:'
    del all_refs
    gc.collect()
    
    print '\n After, cache contains:', cache.keys()
    for name, value in cache.items():
        print ' %s = %s' % (name, value)
    print ' demo returning'
    return

demo(dict)
print

demo(weakref.WeakValueDictionary)
```


```python
cache type: <type 'dict'>
 all_refs = {'one': ExpensiveObject (one),
 'three': ExpensiveObject (three),
 'two': ExpensiveObject (two)}

 Before, cache contains: ['three', 'two', 'one']
 three = ExpensiveObject (three)
 two = ExpensiveObject (two)
 one = ExpensiveObject (one)

 Cleanup:

 After, cache contains: ['three', 'two', 'one']
 three = ExpensiveObject (three)
 two = ExpensiveObject (two)
 one = ExpensiveObject (one)
 demo returning
 (Deleting ExpensiveObject (three))
 (Deleting ExpensiveObject (two))
 (Deleting ExpensiveObject (one))

cache type: weakref.WeakValueDictionary
 all_refs = {'one': ExpensiveObject (one),
 'three': ExpensiveObject (three),
 'two': ExpensiveObject (two)}

 Before, cache contains: ['three', 'two', 'one']
 three = ExpensiveObject (three)
 two = ExpensiveObject (two)
 one = ExpensiveObject (one)

 Cleanup:
 (Deleting ExpensiveObject (three))
 (Deleting ExpensiveObject (two))
 (Deleting ExpensiveObject (one))

 After, cache contains: []
 demo returning
```

上例中，当值为垃圾回收后，*WeakValueDictionary* 中对应的整个元素都被删除。

要注意的是，由于 *WeakValueDictionary* 是基于 *dict* 的，因此在遍历时不能修改其大小。

使用时，一般使用 *WeakValueDictionary* 和 *WeakKeyDictionary* 即可，而 *ref*, *proxy* 等被看作低层接口，用于实现高级功能。

# 是否可弱引用

一些内置类型，如 *list*, *dict* 等不直接直接被弱引用，但他们的子类可以。


```python
class Dict(dict):
    pass

obj = Dict(red=1, green=2, blue=3) # 该对象可被弱引用
```

而 Cpython 中的 *tuple*, *long* 等即使其子类也不支持被弱引用。

# 更多资源

+ [weakref](https://docs.python.org/2/library/weakref.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.6weakref.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.7 Weakref-Impermanent References to Objects](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
