---
title: Python 2 标准库示例：3.4 contextlib-上下文管理工具
date: 2017-06-04
writing-time: 2017-06-04
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture contextlib
---


**目的**: 创建和使用上下文管理器的工具。

**Python 版本**: 2.5+。

*contextlib* 模块结合 *with* 语句使用上下文管理器。由于 *with* 语句在 Python 2.6 中引入，若要在 Python 2.5 中使用，则需要从 `__future__` 中导入。


# Context Manager API

一个 *context manager* 负责一个代码段中的一个资源，它在当进入代码段时创建，并在退出代码段时被清除。例如，文件对象支持 *context manager API*，从而确保了如下的代码段中，当完成读写操作后，文件会被自动关闭。


```python
with open('/tmp/pymotw.txt', 'wt') as f:
    f.write('contents go here')
# file is automatically closed
```

上下文管理器对象通过 *with* 语句启用，主要有 2 个方法。`__enter()__` 方法在执行流进入 *with* 的代码段时运行，它返回的一个对象会在当前上下文中使用。当执行流离开代码段时，会调用 `__exit__()` 来清理使用的资源。


```python
class Context(object):
    def __init__(self):
        print '__init__()'
        
    def __enter__(self):
        print '__enter__()'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit__()'
        
with Context():
    print 'Doing work in the context'
```

    __init__()
    __enter__()
    Doing work in the context
    __exit__()


`__enter__()` 方法返回的对象，可通过 *with* 语句的 *as* 从句关联到一个变量，如下。


```python
class WithinContext(object):
    def __init__(self, context):
        print 'WithinContext.__init__(%s)' % context
        
    def do_something(self):
        print 'WithinContext.do_something()'
        
    def __del__(self):
        print 'WithinContext.__del__'
        
class Context(object):
    def __init__(self):
        print 'Context.__init__()'
        
    def __enter__(self):
        print 'Context.__enter__()'
        return WithinContext(self)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'Context.__exit__()'
        
with Context() as c:
    c.do_something()
```

    Context.__init__()
    Context.__enter__()
    WithinContext.__init__(<__main__.Context object at 0x7fdbc327cfd0>)
    WithinContext.do_something()
    Context.__exit__()


如果 *with* 代码段中抛出异常， 则 `__exit__()` 方法的参数会接收到异常的详细信息。


```python
class Context(object):
    def __init__(self, handle_error):
        print '__init__(%s)' % handle_error
        self.handle_error = handle_error
        
    def __enter__(self):
        print '__enter__()'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print '__exit__()'
        print ' exc_type=', exc_type
        print ' exc_val=', exc_val
        print ' exc_tb=', exc_tb
        return self.handle_error
    
with Context(True):
    raise RuntimeError('error message handled')
    
print

with Context(False):
    raise RuntimeError('error message propagated')
```

    __init__(True)
    __enter__()
    __exit__()
     exc_type= <type 'exceptions.RuntimeError'>
     exc_val= error message handled
     exc_tb= <traceback object at 0x7fdbadeeab00>
    
    __init__(False)
    __enter__()
    __exit__()
     exc_type= <type 'exceptions.RuntimeError'>
     exc_val= error message propagated
     exc_tb= <traceback object at 0x7fdbadeeac68>



    ---------------------------------------------------------------------------

    RuntimeError                              Traceback (most recent call last)

    <ipython-input-5-45d0ff46304f> in <module>()
         21 
         22 with Context(False):
    ---> 23     raise RuntimeError('error message propagated')
    

    RuntimeError: error message propagated


`__exit__()` 返回 `True` 表示已处理了异常，不向上传递异常，而返回 `False` 表示会向上传递异常。

# 用 generator 实现上下文管理器

定义上下文管理器的传统方法是实现 `__enter__()` 和 `__exit__()`。但也可以通过 *contextmanager()* 装饰器将一个 *generator* 函数直接转变成一个上下文管理器。


```python
import contextlib

@contextlib.contextmanager
def make_context():
    print ' entering'            # __enter__
    try:
        yield {}                 # return from __enter__
    except RuntimeError, err:    
        print ' Error:', err     # like __exit__ return True, not to propagate.
    finally:
        print ' exiting'         # __exit__
        
print 'Normal:'
with make_context() as value:
    print ' inside with statement:', value
    
print '\nHandled error:'
with make_context() as value:
    raise RuntimeError('showing example of handling an error')
    
print '\nUnhandled error:'
with make_context() as value:
    raise ValueError('this exception is not handled')
```

    Normal:
     entering
     inside with statement: {}
     exiting
    
    Handled error:
     entering
     Error: showing example of handling an error
     exiting
    
    Unhandled error:
     entering
     exiting



    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-7-ee829d1776a7> in <module>()
         21 print '\nUnhandled error:'
         22 with make_context() as value:
    ---> 23     raise ValueError('this exception is not handled')
    

    ValueError: this exception is not handled


*generator* 中 *yield* 前的代码用来初始化上下文管理器，并只 *yield* 一次，*yield* 出的值相当于 `__enter__` 的返回值。`try, except` 中提及的异常会被处理，不会向上传递，即等同 `__exit__` 返回 True。

# 嵌套上下文

使用 *nested()* 可在一个 *with* 语句中使用嵌套的上下文。


```python
import contextlib

@contextlib.contextmanager
def make_context(name):
    print 'entering:', name
    yield name
    print 'exiting:', name
    
with contextlib.nested(make_context('A'),
                      make_context('B')) as (A, B):
    print 'inside with statement:', A, B
```

    entering: A
    entering: B
    inside with statement: A B
    exiting: B
    exiting: A


    /usr/local/lib/python2.7/dist-packages/ipykernel_launcher.py:10: DeprecationWarning: With-statements now directly support multiple context managers
      # Remove the CWD from sys.path while we load stuff.


上例中，注意到进入上下文的顺序和离开的正好相反。在 Python 2.7 中， *nested()* 已过时，因为 *with* 现已直接支持嵌套，如下：


```python
import contextlib

@contextlib.contextmanager
def make_context(name):
    print 'entering:', name
    yield name
    print 'exiting:', name
    
with make_context('A') as A, make_context('B') as B:
    print 'inside with statement:', A, B
```

    entering: A
    entering: B
    inside with statement: A B
    exiting: B
    exiting: A


# 关闭打开的句柄

*file* 类支持 *context manager API*，但有些旧的类如 `urllib.urlopen()` 返回的对象，都是用 `close()` 方法关闭，但不支持 *context manager API*。

可以使用 *closing()* 为这些对象创建一个上下文，确保退出时会调用 `close()`。


```python
import contextlib

class Door(object):
    def __init__(self):
        print ' __init__()'
        
    def close(self):
        print ' close()'
        
print 'Normal Example:'
with contextlib.closing(Door()) as door:
    print ' inside with statement'
    
print '\nError handling example:'
try:
    with contextlib.closing(Door()) as door:
        print ' rasing from inside with statement'
        raise RuntimeError('error message')
except Exception, err:
    print ' Had an error:', err
```

    Normal Example:
     __init__()
     inside with statement
     close()
    
    Error handling example:
     __init__()
     rasing from inside with statement
     close()
     Had an error: error message


# 更多资源

+ [contextlib](https://docs.python.org/2/library/contextlib.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/3.4contextlib.ipynb) 


# 参考

+ [The Python Standard Library By Example: 3.4 Contextlib-Context Manager Utilities](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
