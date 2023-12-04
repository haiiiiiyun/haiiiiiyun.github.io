---
title: Python 2 标准库示例：3.1 functools-处理函数的工具
date: 2017-06-02
writing-time: 2017-06-01
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture functools
---


*functools* 模块中包含有创建函数装饰器、进行切面编程和支持除传统面向对象方法的代码重用的工具。它还包含一个类装饰器，用来实现富比较 API (rich comparison API)。

*itertools* 模块包含有能创建和使用 *iterator* 和 *generator* 的函数。

*operator* 模块消除了对许多琐碎 lambda 函数的使用需求。

*contextlib* 使得资源管理更加容易可靠，并通常与 *with* 语句一起使用。

# functools

**目的**: 用来操作其它函数的函数。

**Python 版本**: 2.5+

*functools* 模块提供了对函数及其它可调用对象进行适配或扩展的工具。


# 装饰器

*partial* 类用来封装一个可调用对象，并设置好一些默认参数值。其结果也是一个可调用对象，能和源可调用对象一样使用。并且有着相同的参数。可用 *partial* 来替代 *lambda*，以为函数提供默认参数。

*partial* 实现了对源可调用对象的一些参数的 “固化”，使得新返回的可调用对象易用。

## partial 对象

*partial* 对象有 *func*, *args*, *keywords* 等属性。


```python
import functools

def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print ' called myfunc with:', (a, b)
    return

def show_details(name, f, is_partial=False):
    """Show details of a callable object."""
    print '%s:' % name
    print ' object:', f
    if not is_partial:
        print ' __name__:', f.__name__
    if is_partial:
        print ' func:', f.func
        print ' args:', f.args
        print ' keywords:', f.keywords
    return

show_details('myfunc', myfunc)
myfunc('a', 3)
print

# set a different default value for 'b', but require
# the caller to provide 'a'.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print

# set default values for both 'a' and 'b'.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print

print 'Insufficient arguments:'  # raise exception
p1()
```

    myfunc:
     object: <function myfunc at 0xb50775a4>
     __name__: myfunc
     called myfunc with: ('a', 3)
    
    partial with named default:
     object: <functools.partial object at 0xb46d36bc>
     func: <function myfunc at 0xb50775a4>
     args: ()
     keywords: {'b': 4}
     called myfunc with: ('passing a', 4)
     called myfunc with: ('override b', 5)
    
    partial with defaults:
     object: <functools.partial object at 0xb46d334c>
     func: <function myfunc at 0xb50775a4>
     args: ('default a',)
     keywords: {'b': 99}
     called myfunc with: ('default a', 99)
     called myfunc with: ('default a', 'override b')
    
    Insufficient arguments:



    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-1-3ac09c0db9b8> in <module>()
         38 
         39 print 'Insufficient arguments:'  # raise exception
    ---> 40 p1()
    

    TypeError: myfunc() takes at least 1 argument (1 given)


## 获取函数的属性

*partial* 对象默认没有 *__name__* 或 *__doc__*，从而使得调试被装饰函数很困难。使用 *update_wrapper()* 将从源函数对象中的属性复制或添加到 *partial* 对象上。即 *update_wrapper()* 能使装饰对象看起来和被封装对象一样。


```python
import functools

def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print ' called myfunc with:', (a, b)
    return

def show_details(name, f):
    """Show details of a callable object."""
    print '%s:' % name
    print ' object:', f
    try:
        print ' __name__:', f.__name__
    except AttributeError:
        print ' (no __name__)'
    print ' __doc__:', repr(f.__doc__)
    print
    return

show_details('myfunc', myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print 'Updating wrapper:'
print ' assign attributes defined in functools.WRAPPER_ASSIGNMENTS:', \
        functools.WRAPPER_ASSIGNMENTS
print ' update attributes defined in functools.WRAPPER_UPDATES:', \
        functools.WRAPPER_UPDATES
print

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)
```

    myfunc:
     object: <function myfunc at 0xb46b510c>
     __name__: myfunc
     __doc__ 'Docstring for myfunc().'
    
    raw wrapper:
     object: <functools.partial object at 0xb46d343c>
     __name__:  (no __name__)
     __doc__ 'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'
    
    Updating wrapper:
     assign attributes defined in functools.WRAPPER_ASSIGNMENTS: ('__module__', '__name__', '__doc__')
     update attributes defined in functools.WRAPPER_UPDATES: ('__dict__',)
    
    updated wrapper:
     object: <functools.partial object at 0xb46d343c>
     __name__: myfunc
     __doc__ 'Docstring for myfunc().'
    


## 其它可调用对象

*partial* 可作用于任何可调用对象，不只函数上。


```python
import functools

class MyClass(object):
    """Domonstration class for functools"""
    
    def method1(self, a, b=2):
        """Docstring for method1()."""
        print ' called method1 with:', (self, a, b)
        return
    
    def method2(self, c, d=5):
        """Docstring for method2."""
        print ' called method2 with:', (self, c, d)
        return
    
    # first arg self='wrapped c
    wrapped_method2 = functools.partial(method2, 'wrapped c')
    functools.update_wrapper(wrapped_method2, method2)
    
    def __call__(self, e, f=6):
        """Docstring for MyClass.__call__"""
        print ' called object with:', (self, e, f)
        return
    
def show_details(name, f):
    """Show details of a callable object."""
    print '%s:' % name
    print ' object:', f
    print ' __name__:',
    try:
        print f.__name__
    except AttributeError:
        print '(no __name__)'
    print ' __doc__:', repr(f.__doc__)
    print
    return

o = MyClass()

show_details('method1 straight', o.method1)
o.method1('no default for a', b=3)
print

p1 = functools.partial(o.method1, b=4)
functools.update_wrapper(p1, o.method1)
show_details('method1 wrapper', p1)
p1('a goes here')
print

show_details('method2', o.method2)
o.method2('no default for c', d=6)
print

show_details('wrapped method2', o.wrapped_method2)
o.wrapped_method2('no default for c', d=6)
print

show_details('instance', o)
o('no default for e')
print

p2 = functools.partial(o, f=7)
show_details('instance wrapper', p2)
p2('e goes here')
```

    method1 straight:
     object: <bound method MyClass.method1 of <__main__.MyClass object at 0xb46a0ecc>>
     __name__: method1
     __doc__: 'Docstring for method1().'
    
     called method1 with: (<__main__.MyClass object at 0xb46a0ecc>, 'no default for a', 3)
    
    method1 wrapper:
     object: <functools.partial object at 0xb3cc4194>
     __name__: method1
     __doc__: 'Docstring for method1().'
    
     called method1 with: (<__main__.MyClass object at 0xb46a0ecc>, 'a goes here', 4)
    
    method2:
     object: <bound method MyClass.method2 of <__main__.MyClass object at 0xb46a0ecc>>
     __name__: method2
     __doc__: 'Docstring for method2.'
    
     called method2 with: (<__main__.MyClass object at 0xb46a0ecc>, 'no default for c', 6)
    
    wrapped method2:
     object: <functools.partial object at 0xb3cc4054>
     __name__: method2
     __doc__: 'Docstring for method2.'
    
     called method2 with: ('wrapped c', 'no default for c', 6)
    
    instance:
     object: <__main__.MyClass object at 0xb46a0ecc>
     __name__: (no __name__)
     __doc__: 'Domonstration class for functools'
    
     called object with: (<__main__.MyClass object at 0xb46a0ecc>, 'no default for e', 6)
    
    instance wrapper:
     object: <functools.partial object at 0xb3cc4e3c>
     __name__: (no __name__)
     __doc__: 'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'
    
     called object with: (<__main__.MyClass object at 0xb46a0ecc>, 'e goes here', 7)


## 为装饰器函数获取函数属性

*functools.wraps()* 会调用 *update_wrapper()* 函数，实现将被装饰函数的属性复制到装饰函数上。


```python
import functools

def show_details(name, f):
    """Show details of a callable object."""
    print '%s:' % name
    print ' object:', f
    print ' __name__:',
    try:
        print f.__name__
    except AttributeError:
        print '(no __name__)'
    print ' __doc__:', repr(f.__doc__)
    print
    return

def simple_decorator(f):
    @functools.wraps(f)
    def decorated(a='decorated defaults', b=1):
        print ' decorated:', (a, b)
        print ' ',
        f(a, b=b)
        return
    return decorated

def myfunc(a, b=2):
    "myfunc() is not complicated"
    print ' myfunc:', (a, b)
    return

# The raw function
show_details('myfunc', myfunc)
myfunc('unwrapped, default b')
myfunc('unwrapped, passing b', 3)
print

# Wrap explicitly
wrapped_myfunc = simple_decorator(myfunc)
show_details('wrapped_myfunc', wrapped_myfunc)
wrapped_myfunc()
wrapped_myfunc('args to wrapped', 4)
print

# Wrap with decorator syntax
@simple_decorator
def decorated_myfunc(a, b):
    myfunc(a, b)
    return

show_details('decorated_myfunc', decorated_myfunc)
decorated_myfunc()
decorated_myfunc('args to decorated', 4)
```

    myfunc:
     object: <function myfunc at 0xb46b50d4>
     __name__: myfunc
     __doc__: 'myfunc() is not complicated'
    
     myfunc: ('unwrapped, default b', 2)
     myfunc: ('unwrapped, passing b', 3)
    
    wrapped_myfunc:
     object: <function myfunc at 0xb46b5ed4>
     __name__: myfunc
     __doc__: 'myfunc() is not complicated'
    
     decorated: ('decorated defaults', 1)
       myfunc: ('decorated defaults', 1)
     decorated: ('args to wrapped', 4)
       myfunc: ('args to wrapped', 4)
    
    decorated_myfunc:
     object: <function decorated_myfunc at 0xb46b59cc>
     __name__: decorated_myfunc
     __doc__: None
    
     decorated: ('decorated defaults', 1)
       myfunc: ('decorated defaults', 1)
     decorated: ('args to decorated', 4)
       myfunc: ('args to decorated', 4)


# 比较

在 Python 2 中，类通过定义 `__cmp__()` 方法来实现比较。Python 2.1 引入了富比较 API (*__lt__()*, *__le__()*, *__eq__()*, *__ne__()*, *__ge__()*, *__gt__()*)，可针对特定的比较操作进行专门的实现。Python 3 中 *__cmp__()* 已过时，只使用这些富比较 API，因此 *functools* 提供了使 Python 2 类与 Python 3 的新比较需求兼容的工具。

## 富比较 (rich comparison)

富比较 API 较多，对于只需支持简单比较操作的类， *total_ordering()* 类装饰器会基于已实现的比较方法，自动补全其它方法。


```python
import functools
import inspect
from pprint import pprint

@functools.total_ordering
class MyObject(object):
    def __init__(self, val):
        self.val = val
        
    def __eq__(self, other):
        print ' testing __eq__(%s, %s)' % (self.val, other.val)
        return self.val == other.val
    
    def __gt__(self, other):
        print ' testing __gt__(%s, %s)' % (self.val, other.val)
        return self.val > other.val
    
print 'Methods:\n'
pprint(inspect.getmembers(MyObject, inspect.ismethod))

a = MyObject(1)
b = MyObject(2)

print '\nComparisons:'
for expr in ['a<b', 'a<=b', 'a==b', 'a>=b', 'a>b']:
    print '\n%-6s:' % expr
    result = eval(expr)
    print ' result of %s: %s' % (expr, result)
```

    Methods:
    
    [('__eq__', <unbound method MyObject.__eq__>),
     ('__ge__', <unbound method MyObject.__ge__>),
     ('__gt__', <unbound method MyObject.__gt__>),
     ('__init__', <unbound method MyObject.__init__>),
     ('__le__', <unbound method MyObject.__le__>),
     ('__lt__', <unbound method MyObject.__lt__>)]
    
    Comparisons:
    
    a<b   :
     testing __gt__(1, 2)
     testing __eq__(1, 2)
     result of a<b: True
    
    a<=b  :
     testing __gt__(1, 2)
     result of a<=b: True
    
    a==b  :
     testing __eq__(1, 2)
     result of a==b: False
    
    a>=b  :
     testing __gt__(1, 2)
     testing __eq__(1, 2)
     result of a>=b: False
    
    a>b   :
     testing __gt__(1, 2)
     result of a>b: False


上例中，类必须实现 *__eq__()* 及某个富比较方法，这样 *total_ordering()* 类装饰器才能补全其它的方法。

## 排序

由于旧式的比较函数已在 Python 3 中已过时，像 *sort()* 等函数中的 *cmp* 参数也已不再被支持了。

旧式的比较函数是一个接受两个参数的可调用对象，并返回一个整数，负数表示小于，0 表示相等，正数表示大小。键函数 *key function* 是一个只接受一个参数，并返回一个作为排序键的函数。

使用 *cmp_to_key()* 可将卡式的比较函数转成键函数，用于像 *sorted()*, *min()*, *max()*, *heapq.nlargest()*, *heapq.nsmallest()*, *itertools.groupby()* 等函数中。


```python
import functools

class MyObject(object):
    def __init__(self, val):
        self.val = val
    
    def __str__(self):
        return 'MyObject (%s)' % self.val
    
def compare_obj(a, b):
    "Old style comparison function."
    print 'comparing %s and %s' % (a, b)
    return cmp(a.val, b.val)

# make a key function using cmp_to_key()
get_key = functools.cmp_to_key(compare_obj)

def get_key_wrapper(o):
    "Wrapper function for get_key to allow for print statements."
    new_key = get_key(o)
    print 'key_wrapper(%s) -> %s' % (o, new_key)
    return new_key
objs = [MyObject(x) for x in xrange(5, 0, -1)]

for o in sorted(objs, key=get_key_wrapper):
#for o in sorted(objs, key=get_key):
    print o
```

    key_wrapper(MyObject (5)) -> <functools.K object at 0xb3cdf2e4>
    key_wrapper(MyObject (4)) -> <functools.K object at 0xb3cdf80c>
    key_wrapper(MyObject (3)) -> <functools.K object at 0xb3cdf2b4>
    key_wrapper(MyObject (2)) -> <functools.K object at 0xb3cdf464>
    key_wrapper(MyObject (1)) -> <functools.K object at 0xb3cdf44c>
    comparing MyObject (4) and MyObject (5)
    comparing MyObject (3) and MyObject (4)
    comparing MyObject (2) and MyObject (3)
    comparing MyObject (1) and MyObject (2)
    MyObject (1)
    MyObject (2)
    MyObject (3)
    MyObject (4)
    MyObject (5)


通常是直接 *cmp_to_key()*，但上例中进行封装只是为了输出更多信息。

上例中，*sorted()* 为序列中的每个成员调用 *get_key_wrapper()* 以获得一个键。*cmp_to_key()* 返回的是一个在 *functools* 中定义的类实例，该类会根据传入的旧式比较函数生成所有的富比较 API。

# 更多资源

+ [functools](https://docs.python.org/2/library/functools.html) Standard library documentation for this module.
+ [Rich comparison methods](https://docs.python.org/2.7/reference/datamodel.html#object.__lt__) Description of the rich comparison methods from the Python
Reference Guide.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/3.1functools.ipynb) 


# 参考

+ [The Python Standard Library By Example: 3.1 Functools-Tools for Manipulating Functions](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
