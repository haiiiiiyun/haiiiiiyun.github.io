---
title: Python 2 标准库示例：2.1 collections-容器数据类型
date: 2017-05-25
writing-time: 2017-05-25 21:44
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture collections
---


Python 内置了许多标准的数据结构，如 *list*, *tuple*, *dict*, *set* 等。同时，标准库还提供了额外的数据结构，我们可以基于它们创建所需的新数据结构。

*collections* 模块中实现了一些容器数据结构。例如，*Deque* 是一个双端队列，可以从任意端进行添加删除操作。*defaultdict* 当在 *key* 缺失时会返回一个默认值，而 *OrderedDict* 会保留元素加入时的次序。*namedtuple* 扩展了普通的 *tuple*，每个成员元素都对应有一个属性名，可用于引用。

处理大数据时，*array* 会比 *list* 高效。因此 *array* 初始化时会被限制为存储单个数据类型。

序列排序是数据处理的重要组成部分。*heapq* 中的函数在处理元素时会同时保留排序次序。*bisect* 也可以用来构建排序序列，它使用二分查询法。

虽然使用 *list* 的 *insert()* 和 *pop()* 可模拟实现队列，但是 *list* 是非线程安全的。可实现线程间的有序交互，要使用 *Queue* 模块。*multiprocessing* 模块中的 *Queue* 支持多进程，使用它可将多线程程序较容易地转为多进程。

*struct* 可用于对二进制文件内容或数据流进行解码。

在内存管理方面，对于图和树等高度互连的数据结构，可使用 *weakref* 来维护引用，以方便垃圾回收器工作。*copy* 函数可用来复制数据结构及其内容，而 *deepcopy* 可进行递归复制。

# collections

**目的**: 容器数据类型。

**Python 版本**: 2.4+

## Counter

*Counter* 容器会记录相同值出现的户数，它类同于其它语言中的 *bag* 或 *multiset* 等数据结构。

### 初始化

支持 3 种形式的初始化。

1. 接收一个序列。
2. 接收一个字典，key 为元素，值为元素出现的次数。
3. 使用关键字参数传入


```python
import collections

print collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
print collections.Counter({'a':2, 'b':3, 'c':1})
print collections.Counter(a=2, b=3, c=1)
```

    Counter({'b': 3, 'a': 2, 'c': 1})
    Counter({'b': 3, 'a': 2, 'c': 1})
    Counter({'b': 3, 'a': 2, 'c': 1})


也可以先创建一个空的 *Counter*，再通过 *update()* 函数添加数据（接收的参数和初始化时类似，也有 3 种形式）。


```python
import collections

c = collections.Counter()
print 'Initial: ', c

c.update('abcdaab')
print 'Sequence:', c

c.update({'a': 1, 'd': 5}) # 非替换，而是增加
print 'Dict:', c
```

    Initial:  Counter()
    Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})
    Dict: Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})


## 访问元素的次数信息

可使用类似字典的接口进行访问。


```python
import collections

c = collections.Counter('abcdaab')

for letter in 'abcde':
    print '%s : %d' % (letter, c[letter])
```

    a : 3
    b : 2
    c : 1
    d : 1
    e : 0


上例中可见，*Counter* 对于未知（未设置）元素不会抛出 *KeyError*，它会将未知元素的次数设置为 0。

*elements()* 方法返回一个迭代器，该迭代器将生产出 *Counter* 中所有次数大小 0 次的已知（已设置）元素，元素次数为多次时，则也生产出多个相同的元素。生产出的元素序列是未定义的。


```python
import collections

c = collections.Counter('extremely')
c['z'] = 0  # 操作后 z 将为已知（已设置元素）
print c
print list(c.elements())
```

    Counter({'e': 3, 'm': 1, 'l': 1, 'r': 1, 't': 1, 'y': 1, 'x': 1, 'z': 0})
    ['e', 'e', 'e', 'm', 'l', 'r', 't', 'y', 'x']


*most_common([ret_count])* 将返回 *ret_count* 个次数最多的元素及其次数。


```python
import collections

c = collections.Counter()
with open('/usr/share/dict/words', 'rt') as f:
    for line in f:
        c.update(line.rstrip().lower())
        
print 'Most common:'
for letter, count in c.most_common(3):
    print '%s: %7d' % (letter, count)
```

    Most common:
    s:   90113
    e:   88833
    i:   66986


## 算术运算

*Counter* 实例支持算术和集运算。


```python
import collections

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')

print 'C1:', c1
print 'C2:', c2

print '\nCombined counts:'
print c1 + c2

print '\nSubtraction:'
print c1 - c2

print '\nIntersection (taking positive minimums):'
print c1 & c2

print '\nUnion (taking maximums):'
print c1 | c2
```

    C1: Counter({'b': 3, 'a': 2, 'c': 1})
    C2: Counter({'a': 2, 'b': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})
    
    Combined counts:
    Counter({'a': 4, 'b': 4, 'c': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})
    
    Subtraction:
    Counter({'b': 2, 'c': 1})
    
    Intersection (taking positive minimums):
    Counter({'a': 2, 'b': 1})
    
    Union (taking maximums):
    Counter({'b': 3, 'a': 2, 'c': 1, 'e': 1, 'h': 1, 'l': 1, 'p': 1, 't': 1})


## defaultdict

内置 *dict* 的 *setdefault()* 可用来键的值，当键不存在时，返回一个默认值。

而 *defaultdict* 则在容器初始化前即要先定义初始值函数。


```python
import collections

def default_factory():
    return 'default value'

d = collections.defaultdict(default_factory, foo='bar')
print 'd:', d
print 'foo =>', d['foo']
print 'bar =>', d['bar']
```

    d: defaultdict(<function default_factory at 0x7fa008ccf398>, {'foo': 'bar'})
    foo => bar
    bar => default value


上例中，当首次访问 `d['bar']` 时，由于键不存在，会先调用 *default_factory* 来返回一个默认值，并设置该键对应该值。

当将默认值生成函数设置为 *list*, *set*, *int* 等类型时，可以完成一些聚合统计等工作。


```python
import collections

d = collections.defaultdict(list)
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]

for k, v in s:
    d[k].append(v)

print d.items()
```

    [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]


上例中，将 *default_factory* 设置为 *list*，则当首次访问键时，由于键不存在，会调用 *list()* 生成一个新列表，并且将该键值设置为该列表。之后通过 *list.append()* 操作将值添加到列表中。

这种技术比用 *dict.setdefault()* 实现的更加简单和高效， *dict.setdefault()* 版本如下：


```python
d = {}
for k, v in s:
    d.setdefault(k, []).append(v)
    
print d.items()
```

    [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]


类似地，将 *default_factory* 设置为 *set*，可创建一个 *set* 字典。


```python
import collections

d = collections.defaultdict(set)
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]

for k, v in s:
    d[k].add(v)

print d.items()
```

    [('blue', set([2, 4])), ('red', set([1])), ('yellow', set([1, 3]))]


将 *default_factory* 设置为 *int* 可使 *defaultdict* 实现计数功能，如下：


```python
import collections

s = 'mississippi'
d = collections.defaultdict(int)
for k in s:
    d[k] += 1

print d.items()
```

    [('i', 4), ('p', 2), ('s', 4), ('m', 1)]


上例中，函数 *int()* 会返回一个值为 0 的整数对象。

## deque

*deque* 是一个双端队列，支持从任意一端进行操作。


```python
import collections

d = collections.deque('abcdefg')
print 'Deque:', d
print 'Length:', len(d)
print 'Left end:', d[0]
print 'Right end:', d[-1]

d.remove('c')  # deque 类似 list
print 'remove(c):', d
```

    Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    Length: 7
    Left end: a
    Right end: g
    remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])


*deque* 是一个序列容器，也支持 *list* 的一些接口，如 *__getitem__()*，*len()*, *remove()* 等。

### 添加数据

*deque* 的两端分别称为 **left** 和 **right**（默认操作端）。


```python
import collections

# Add to the right
d1 = collections.deque()
d1.extend('abcdefg')
print 'extend: ', d1
d1.append('h')
print 'append: ', d1

# Add to the left
d2 = collections.deque()
d2.extendleft(xrange(6))
print 'extendleft: ', d2
d2.appendleft(6)
print 'appendleft: ', d2
```

    extend:  deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    append:  deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    extendleft:  deque([5, 4, 3, 2, 1, 0])
    appendleft:  deque([6, 5, 4, 3, 2, 1, 0])


*extendleft()* 和 *appendleft()* 等都在左端进行操作。

### 使用元素

*deque* 也可以从两端获取元素，使用 *pop()* 和 *popleft()*。


```python
import collections

print 'From the right:'
d = collections.deque('abcdefg')
while True:
    try:
        print d.pop(),
    except IndexError:
        break
print

print '\nFrom the left:'
d = collections.deque(xrange(6))
while True:
    try:
        print d.popleft(),
    except IndexError:
        break
print
```

    From the right:
    g f e d c b a
    
    From the left:
    0 1 2 3 4 5


*deque* 还是线程安全的，可能不同的线程同时操作。


```python
import collections
import threading
import time

candle = collections.deque(xrange(5))

def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print '%8s: %s' % (direction, next)
            time.sleep(0.1)
    print '%8s done' % direction
    return

left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()
```

        Left: 0
       Right: 4
        Left: 1
       Right: 3
        Left: 2
       Right done
        Left done


### 回转

想象将 *deque* 的两端连接，形成一个圆，即可想象其回转操作。*rotate(n)* 将所有元素向右移动 n 位，移出右端的元素回到前左端最前面，当参数 *n* 为负数时，则是向左回转。


```python
import collections

d = collections.deque(xrange(10))
print 'Normal: ', d

d = collections.deque(xrange(10))
d.rotate(2)
print 'Right rotation: ', d

d = collections.deque(xrange(10))
d.rotate(-2)
print 'Left rotation: ', d
```

    Normal:  deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    Right rotation:  deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
    Left rotation:  deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])


### deque Recipes

#### 1. 实现 Unix tail 功能


```python
import collections

def tail(filename, n=10):
    'Return the last n lines of a file'
    return collections.deque(open(filename), n)

for l in tail('./2.1collections.ipynb', 5):
    print l
```

      }
    
     },
    
     "nbformat": 4,
    
     "nbformat_minor": 2
    
    }
    


#### 2. 实现 deque 的分片和删除功能

可通过 *rotate()* 函数来实现。


```python
import collections

def delete_nth(d, n):
    d.rotate(-n)  # 将要删除的元素移到最左边（第一个）
    d.popleft()
    d.rotate(n)
    
d = collections.deque(xrange(5))
print 'd=', d
delete_nth(d, 2)
print 'after delete the 3th item:', d

```

    d= deque([0, 1, 2, 3, 4])
    after delete the 3th item: deque([0, 1, 3, 4])


# namedtuple

*namedtuple* 的实例没有维护一个字典，因而和 *tuple* 效率一样高。每个 *namedtuple* 类型都需要使用 *namedtuple()* 工厂函数创建，函数的第一个参数和创建的新 *namedtuple* 类型名相同，另一个参数是包含所有数据域命名的字符串。

*namedtuple* 实例中的数据域即可以像普通 *tuple* 一样通过数字索引访问，也可以通过数据域名 `obj.attr` 的形式访问。


```python
import collections

Person = collections.namedtuple('Person', 'name age gender')

print 'Type of Person:', type(Person)

bob = Person(name='Bob', age=30, gender='male')
print '\nRepresentation:', bob

jane = Person(name="Jane", age=29, gender='female')
print '\nField by name:', jane.name

print '\nFields by index:'
for p in [bob, jane]:
    print '%s is a %d year old %s' % p
```

    Type of Person: <type 'type'>
    
    Representation: Person(name='Bob', age=30, gender='male')
    
    Field by name: Jane
    
    Fields by index:
    Bob is a 30 year old male
    Jane is a 29 year old female


### 无效的数据域名

当数据域名重复，或与 Python 关键字冲突时为无效。当数据域名不可控时（如由数据库查询返回），调用 *namedtuple* 工厂函数时传入 *rename=True*，此时无效的数据域名为基于其位置自动重命名。


```python
import collections

try:
    collections.namedtuple('Person', 'name class age gender')
except ValueError, err:
    print err
    
try:
    collections.namedtuple('Person', 'name age gender age')
except ValueError, err:
    print err
    
with_class = collections.namedtuple(
    'Person', 'name class age gender',
    rename=True)
print with_class._fields

two_ages = collections.namedtuple(
    'Person', 'name age gender age',
    rename=True)
print two_ages._fields
```

    Type names and field names cannot be a keyword: 'class'
    Encountered duplicate field name: 'age'
    ('name', '_1', 'age', 'gender')
    ('name', 'age', 'gender', '_3')


# OrderedDict

*OrderedDict* 会记录内容添加时的次序，因此对其迭代产生的元素次序和添加元素时是一致的。而普通 *dict* 元素的次序是由其 hash 值决定的。


```python
import collections

print 'Regular dictionary'
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print k, v
    
print '\nOrderedDict:'
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print k, v
```

    Regular dictionary
    a A
    c C
    b B
    
    OrderedDict:
    a A
    b B
    c C


### 相等性

普通 *dict* 比较相等时只看内容，而 *OrderedDict* 比较时不仅看内容，而且还要看元素的添加次序。


```python
import collections

print 'dict:',
d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = {}
d2['c'] = 'C'
d2['a'] = 'A'
d2['b'] = 'B'

print d1 == d2

print 'OrderedDict:',
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['a'] = 'A'
d2['b'] = 'B'

print d1 == d2
```

    dict: True
    OrderedDict: False


# 更多资源

+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.1.collections.ipynb) 
+ [defaultdict examples](https://docs.python.org/2.7/library/collections.html?highlight=defaultdict#collections.defaultdict) Examples of using defaultdict from the standard library documentation.
+ [Evolution of Default Dictionaries in Python](http://jtauber.com/blog/2008/02/27/evolution_of_default_dictionaries_in_python/) Discussion from James Tauber of how defaultdict relates to other means of initializing dictionaries.
+ [Deque](http://en.wikipedia.org/wiki/Deque) Wikipedia article that provides a discussion of the deque data structure.
+ [Deque Recipes](https://docs.python.org/3/library/collections.html?highlight=deque#collections.dequel) Examples of using deques in algorithms from the standard library documentation.


# 参考

+ [The Python Standard Library By Example: 2.1 collections-Container Data Type](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
