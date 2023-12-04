---
title: Python 2 标准库示例：3.3 operator-内置操作符的函数接口
date: 2017-06-03
writing-time: 2017-06-04
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture operator
---


**目的**: 实现了内置操作符的函数接口。

**Python 版本**: 1.4+。


*operator* 模块定义了对应算术及比较等内置操作的相应函数，如 *operator.add(x,y)* 对应 *x+y* 等。函数名字即与类中对应的特殊方法名相同，如 *operator.__add__* 对应类中的 *__add__()* 方法，为方便起见，也提供了无下划线的版本，即 *operator.add* 和 *operator.__add__* 等同。


# 逻辑操作

布尔值操作的相关函数。


```python
from operator import *

a = 1
b = 5

print 'a=', a
print 'b=', b
print

print 'not_(a):', not_(a)
print 'truth(a):', truth(a)
print 'is_(a, b):', is_(a, b)
print 'is_not(a, b):', is_not(a, b)
```

    a= 1
    b= 5
    
    not_(a): False
    truth(a): True
    is_(a, b): False
    is_not(a, b): True


# 比较操作符

支持所有的富比较操作符。


```python
from operator import *

a = 1
b = 5.0

print 'a=', a
print 'b=', b
for func in (lt, le, eq, ne, ge, gt):
    print 'operator.%s(a, b):' % func.__name__, func(a, b)
```

    a= 1
    b= 5.0
    operator.lt(a, b): True
    operator.le(a, b): True
    operator.eq(a, b): False
    operator.ne(a, b): True
    operator.ge(a, b): False
    operator.gt(a, b): False


# 算术操作符


```python
from operator import *

a = -1
b = 5.0
c = 2
d = 6

print 'a=', a
print 'b=', b
print 'c=', c
print 'd=', d

print '\nPositive/Negative:'
print 'abs(a):', abs(a)   # |a|
print 'neg(a):', neg(a)   # -a
print 'neg(b):', neg(b)  
print 'pos(a):', pos(a)  # +a
print 'pos(b):', pos(b)

print '\nArithmetric:'
print 'add(a, b):', add(a, b)
print 'div(a, b):', div(a, b)
print 'div(d, c):', div(d, c)
print 'floordiv(a, b):', floordiv(a, b)  # integer division, = a // b
print 'floordiv(d, c):', floordiv(d, c)
print 'truediv(a, b):', truediv(a, b)    # floating-point division
print 'truediv(d, c):', truediv(d, c)
print 'mod(a, b):', mod(a, b)
print 'mul(a, b):', mul(a, b)
print 'pow(c, d):', pow(c, d)
print 'sub(b, a):', sub(b, a)

print '\nBitwise:'
print 'and_(c, d):', and_(c, d)
print 'invert(c):', invert(c)
print 'lshift(c, d):', lshift(c, d)
print 'or_(c, d):', or_(c, d)
print 'rshift(d, c):', rshift(d, c)
print 'xor(c, d):', xor(c, d)

```

    a= -1
    b= 5.0
    c= 2
    d= 6
    
    Positive/Negative:
    abs(a): 1
    neg(a): 1
    neg(b): -5.0
    pos(a): -1
    pos(b): 5.0
    
    Arithmetric:
    add(a, b): 4.0
    div(a, b): -0.2
    div(d, c): 3
    floordiv(a, b): -1.0
    floordiv(d, c): 3
    truediv(a, b): -0.2
    truediv(d, c): 3.0
    mod(a, b): 4.0
    mul(a, b): -5.0
    pow(c, d): 64
    sub(b, a): 6.0
    
    Bitwise:
    and_(c, d): 2
    invert(c): -3
    lshift(c, d): 128
    or_(c, d): 6
    rshift(d, c): 1
    xor(c, d): 4


# 序列操作符

用于序列的操作符分为 4 组：构建序列的、查询元素的、存取内容的、删除元素的。


```python
from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print 'a=', a
print 'b=', b

print '\nConstructive:'
print ' concat(a, b):', concat(a, b)
print ' mul(a, 3):', mul(a, 3)

print '\nSearching:'
print ' contains(a, 1):', contains(a, 1)
print ' contains(b, "d"):', contains(b, "d")
print ' countOf(a, 1):', countOf(a, 1)
print ' countOf(b, "d"):', countOf(b, "d")
print ' indexOf(a, 5):', indexOf(a, 1)

print '\nAccess Items:'
print ' getitem(b, 1):', getitem(b, 1)
print ' getslice(a, 1, 3):', getslice(a, 1, 3)
print ' setitem(b, 1, "d"):', setitem(b, 1, "d"),
print ', after b=', b
print ' setslice(a, 1, 3, [4, 5]):', setslice(a, 1, 3, [4, 5]),
print ', after a=', a

print '\nDestructive:'
print ' delitem(b, 1):', delitem(b, 1), 
print ', after b=', b
print ' delslice(a, 1, 3):', delslice(a, 1, 3),
print ', after a=', a
```

    a= [1, 2, 3]
    b= ['a', 'b', 'c']
    
    Constructive:
     concat(a, b): [1, 2, 3, 'a', 'b', 'c']
     mul(a, 3): [1, 2, 3, 1, 2, 3, 1, 2, 3]
    
    Searching:
     contains(a, 1): True
     contains(b, "d"): False
     countOf(a, 1): 1
     countOf(b, "d"): 0
     indexOf(a, 5): 0
    
    Access Items:
     getitem(b, 1): b
     getslice(a, 1, 3): [2, 3]
     setitem(b, 1, "d"): None , after b= ['a', 'd', 'c']
     setslice(a, 1, 3, [4, 5]): None , after a= [1, 4, 5]
    
    Destructive:
     delitem(b, 1): None , after b= ['a', 'c']
     delslice(a, 1, 3): None , after a= [1]


上例中，*delslice(a, b, c)* 已在 Python 2.6 中过时，会在 Python 3 中删除，可用 *delitem(a, slice_index)* 实现。*getslice(a, b, c)* 也已在 Python 2.6 中过时，会在 Python 3 中删除，可用 *getitem(a, slice_index)* 实现。

# in-place 操作符

`+=` 等 in-place 操作符。


```python
from operator import *

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']
print 'a=', a
print 'b=', b
print 'c=', c
print 'd=', d
print

a = iadd(a, b)
print 'a=iadd(a, b)=>', a
print

c = iconcat(c, d)
print 'c=iconcat(c, d)=>', c
```

    a= -1
    b= 5.0
    c= [1, 2, 3]
    d= ['a', 'b', 'c']
    
    a=iadd(a, b)=> 4.0
    
    c=iconcat(c, d)=> [1, 2, 3, 'a', 'b', 'c']


# 属性及元素的 "Getters"

*operator* 模块中的 *getter* 都是可调用对象，它们在运行时构建，用于获取对象的属性或序列的元素。*getter* 和 *iterator* 或 *generator* 序列一起使用时很有用，例如用于 *map()*, *sorted()*, *itertools.groupby()* 等中用来获取参数的数据项。


```python
from operator import *

class MyObj(object):
    """example class for attrgetter"""
    def __init__(self, arg):
        super(MyObj, self).__init__()
        self.arg = arg
        
    def __repr__(self):
        return 'MyObj(%s)' % self.arg
    
l = [MyObj(i) for i in xrange(5)]
print 'Objects:', l

# Extract the 'arg' value from each object
g = attrgetter('arg')
vals = [g(i) for i in l]
print 'arg values:', vals

# Sort using arg
l.reverse()
print 'reversed:', l
print 'sorted:', sorted(l, key=g)
```

    Objects: [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
    arg values: [0, 1, 2, 3, 4]
    reversed: [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
    sorted: [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]


上例中，*attrgetter* 等价为 *lambda o, a='attrname': getattr(o, a)*。

而 *itemgetter* 可用于获取列表或序列的元素，等价于 *lambda o, i: o.\_\_getitem\_\_(i)*，如下例所示。


```python
from operator import *
l= [dict(val=-1*i) for i in xrange(4)]
print 'Dictionaries:', l
g = itemgetter('val')
vals = [g(i) for i in l]
print ' values:', vals
print ' sorted:', sorted(l, key=g)
print
l = [(i, i*-1) for i in xrange(4)]
print 'Tuples:', l
g = itemgetter(1)
vals = [g(i) for i in l]
print ' values:', vals
print ' sorted:', sorted(l, key=g)
```

    Dictionaries: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
     values: [0, -1, -2, -3]
     sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]
    
    Tuples: [(0, 0), (1, -1), (2, -2), (3, -3)]
     values: [0, -1, -2, -3]
     sorted: [(3, -3), (2, -2), (1, -1), (0, 0)]


*operator.methodcaller(method_name, [,args...])* 返回的函数，调用时会调用其操作数上的相应函数。

+ `f=methodcaller('method_name')` 后，调用 `f(b)` 返回 `b.method_name()`

# 自定义类与 operator 模块

*operator* 模块是基于标准的 Python 接口实现的，因此，只要自定义类实现了相应的 `__name__` 型操作方法，即可与该模块兼容。


```python
from operator import *

class MyObj(object):
    """Example for operator overloading"""
    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val
        return
    
    def __str__(self):
        return 'MyObj(%s)' % self.val
    
    def __lt__(self, other):
        """Compare for less-than"""
        print 'Testing %s < %s' % (self, other)
        return self.val < other.val
    
    def __add__(self, other):
        print 'Adding %s + %s' % (self, other)
        return MyObj(self.val + other.val)
    
a = MyObj(1)
b = MyObj(2)

print 'Comparison:'
print lt(a, b)

print '\nArithmetic:'
print add(a, b)
```

    Comparison:
    Testing MyObj(1) < MyObj(2)
    True
    
    Arithmetic:
    Adding MyObj(1) + MyObj(2)
    MyObj(3)


# 类型检查

实现了检测可调用对象，映射、数字和序列类型的函数。


```python
from operator import *

class NoType(object):
    """Supports none of the type APIs"""
    
class MultiType(object):
    """Supports multiple type APIs"""
    def __len__(self):
        return 0
    
    def __getitem(self, name):
        return 'mapping'
    
    def __int__(self):
        return 0
    
o = NoType()
t = MultiType()

for func in (isMappingType, isNumberType, isSequenceType):
    print '%s(o):' % func.__name__, func(o)
    print '%s(t):' % func.__name__, func(t)
```

    isMappingType(o): False
    isMappingType(t): False
    isNumberType(o): False
    isNumberType(t): True
    isSequenceType(o): False
    isSequenceType(t): False


但是这些检测都不是可靠的，并且这些函数都已过时，可用 *isinstance* 代替实现，如：

*operator.isCallable(obj)* 对应 *isinstance(x, collections.Callable)*，*operator.isMappingType(obj)* 对应 *isinstance(x, collections.Mapping)*，*operator.isNumberType(obj)* 对应 *isinstance(x, numbers.Number)*，*operator.isSequenceType(obj)* 对应 *isinstance(x, collections.Sequence)*。

# 更多资源

+ [operator](https://docs.python.org/2/library/operator.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/3.3operator.ipynb) 


# 参考

+ [The Python Standard Library By Example: 3.3 Operaotr-Functional Interface to Build-in Operators](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
