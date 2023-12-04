---
title: Python 2 标准库示例：5.3 random-伪随机数生成器
date: 2017-08-16
writing-time: 2017-08-16
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture random
---


**目的**: 实现了几种类型的伪随机数生成器。

**Python 版本**: 1.4+。

*random* 模块基于多种不同的分布实现了伪随机数生成器。几乎所有的模块函数都基于 *random()* 函数，该函数使用均匀分布创建一个在区间 [0.0, 1.0) 之间的一个随机浮点数。

模块函数实际上都是绑定于一个隐含的 *random.Random* 的类实例。我们也可以创建独立的 *random.Random* 实现，以获取独立的生成器状态信息。例如在多线程编程中，可为每个线程创建一个单独的 *random.Random* 实例。 

## 生成随机数

*random()* 函数从一个生成器生成的序列中返回下一个随机浮点数，返回值在 [0.0, 1.0) 之间。


```python
import random

for i in xrange(5):
    print '%04.3f' % random.random(),
print
```

    0.999 0.106 0.006 0.846 0.101


使用 *uniform(min, max)* 函数可以生成在 [min, max) 之间的浮点数，该函数的返回值也是基于 *random()* 的返回值进行调整取得。


```python
import random

for i in xrange(5):
    print '%04.3f' % random.uniform(1, 100),
print
```

    85.481 89.581 34.903 56.218 20.251


## 随机种子 seeding

每次调用 *random()* 都将从一个既定序列中返回下一个随机数，该序列很长，即要过很久才会重复。*random()* 函数的返回值在序列中的起点位置可由一个初始值决定。即可通过 *random.seed(hashable_obj)* 来初始化伪随机生成器，从而使得该生成器生成一个预期的随机数序列。

*seed()* 的参数值可为任意可 Hash 的对象，默认是使用与系统平台相关的随机源，如果没有则使用当前时间。


```python
import random

random.seed(1) # 初始化后，每次运行下面的随机数函数都返回相同的随机数。

print 'First time:'
for i in xrange(5):
    print '%04.3f' % random.random(),
print

random.seed(1) # 初始化后，每次运行下面的随机数函数都返回相同的随机数。
print 'Second time:'
for i in xrange(5):
    print '%04.3f' % random.random(),
print
```

    First time:
    0.134 0.847 0.764 0.255 0.495
    Second time:
    0.134 0.847 0.764 0.255 0.495


## 保存状态及恢复

使用 *seed()* 可初始化伪随机数序列中的初始位置，而 *random()* 在伪随机数序列中的当前位置（状态），可通过 *getstate()* 和 *setstate()* 进行获取和设置。


```python
import random
import os
import cPickle as pickle

if os.path.exists('state.dat'):
    # Restore the previously saved state
    print 'Found state.dat, initializing random module'
    with open('state.dat', 'rb') as f:
        state = pickle.load(f)
    random.setstate(state)
else:
    # Use a well-know start state
    print 'No state.dat, seeding'
    random.seed(1)
    
# Produce random values
for i in xrange(5):
    print '%04.3f' % random.random(),
print

# Save state for next time
with open('state.dat', 'wb') as f:
    pickle.dump(random.getstate(), f)
    
# Produce more random values
print '\nAfter saving state:'
for i in xrange(5):
    print '%04.3f' % random.random(),
print
```

    Found state.dat, initializing random module
    0.449 0.652 0.789 0.094 0.028
    
    After saving state:
    0.836 0.433 0.762 0.002 0.445


## 随机整数


```python
import random

# randint(min, max) 随机返回 [min, max] 间的一个整数
print '[1, 100]',
for i in xrange(3):
    print random.randint(1, 100),
print
    
print '[-5, 5]:',
for i in xrange(3):
    print random.randint(-5, 5),
print

# randrange(start, end, step) 随机挑选 range(start, end, step) 序列中的一个整数
print 'range(0, 101, 5):',
for i in xrange(3):
    print random.randrange(0, 101, 5),
print
```

    [1, 100] 46 29 3
    [-5, 5]: 4 1 2
    range(0, 101, 5): 15 100 90


## 在一个序列中随机挑选

*choice()* 可在一个序列中进行随机选择。


```python
import random

# 模拟抛硬币，统计正反面出现的次数
outcomes = { 'heads': 0, 'tails': 0 }
sides = outcomes.keys()

for i in range(10000):
    outcomes[ random.choice(sides) ] += 1
    
print 'Heads:', outcomes['heads']
print 'Tails:', outcomes['tails']
```

    Heads: 4983
    Tails: 5017


## 洗牌

将一个序列想象成一副牌，*shuffle()* 实现洗牌功能。


```python
import random

cards = list(range(10))
random.shuffle(cards)
print cards

random.shuffle(cards)
print cards
```

    [6, 2, 1, 3, 0, 8, 4, 9, 7, 5]
    [3, 5, 1, 4, 2, 6, 7, 0, 8, 9]


## 取样

*sample()* 在不对输入序列进行任何改动的情况下，取抽取出 n 个样本。


```python
import random

with open('/usr/share/dict/words', 'rt') as f:
    words = f.readlines()
words = [w.rstrip() for w in words]

for w in random.sample(words, 5):
    print w
```

    Salton's
    mushrooming
    immunology
    racketed
    hundred's


## 多个随机生成器并行

以上介绍的模块级的函数，实际上都作用在 random 模块内置的一个 Random 实例上的。显式创建多个 Random 实例，在这个实例上的随机数生成过程互不干扰。


```python
import random
import time

print 'Default initialization:\n'
r1 = random.Random()
r2 = random.Random()

for i in xrange(3):
    print '%04.3f %04.3f' % (r1.random(), r2.random())
    
print '\nSame seed:\n'
seed = time.time()
r1 = random.Random(seed)
r2 = random.Random(seed)

for i in xrange(3):
    print '%04.3f %04.3f' % (r1.random(), r2.random())
```

    Default initialization:
    
    0.930 0.448
    0.944 0.743
    0.872 0.949
    
    Same seed:
    
    0.760 0.760
    0.577 0.577
    0.559 0.559


如果系统本身对随机数生成支持不好，可能会使用当前时间作为默认种子，从而上面代码的第一部分也可能会输出相同的随机值。

要想确保生成器产生不同的值，可使用 *jumpahead(delta)* 对初始状态进行偏移，偏移量 delta 是一个非负整数，生成器内部状态会基于这个 delta 值进行偏移，但并不是进行简单的递增该值。


```python
import random

r1 = random.Random()
r2 = random.Random()

# Force r2 to a different part of the random period than r1.
r2.setstate(r1.getstate())
r2.jumpahead(1024)

for i in xrange(3):
    print '%04.3f %04.3f' % (r1.random(), r2.random())
```

    0.914 0.925
    0.930 0.333
    0.768 0.021


## SystemRandom

一些操作系统本身会提供一个随机数生成器，这个生成器具有具有更随机，更强大的功能。random 模块通过 SystemRandom 类对其进行封装。SystemRandom 和 Random 类的 API 是相同的，只不过它是通过 *os.urandom()* 来产生随机数的。


```python
import random
import time

print 'Default initialization:\n'
r1 = random.SystemRandom()
r2 = random.SystemRandom()

for i in xrange(3):
    print '%04.3f %04.3f' % (r1.random(), r2.random())
    
print '\nSame seed:\n'
seed = time.time()
r1 = random.SystemRandom(seed)
r2 = random.SystemRandom(seed)

for i in xrange(3):
    print '%04.3f %04.3f' % (r1.random(), r2.random())
```

    Default initialization:
    
    0.595 0.363
    0.668 0.468
    0.819 0.891
    
    Same seed:
    
    0.794 0.695
    0.138 0.481
    0.900 0.211


由于 SystemRandom 中的随机数是来自系统本身的，而不是基于软件状态产生，因此是不可重复的（即使初始化时 seed 相同也不能产生相同的随机数）。实际上，seed() 和 setstate() 在 SystemRandom 上都是无效的。

## 非均匀分布

*random()* 是基于均匀分布算法实现的。 random 模块也实现了基于其它分布实现的随机数生成器。

### 正态分布 normal distribution

正态分布也叫高斯分布，曲线形如钟。*random.normalvariate()* 和 *random.gauss()*（速度较快）能生成基于正态分布的随机值。*random.lognormalvariate()* 生成的随机值，其对数值是符合正态分布的。

### 近似分布 approximation distribution

对于小样本环境，用三角分布 triangular distribution 用来表示近似分布，对应函数是 *random.triangular()*。

### 指数分布 exponential distribution

*expovariate()* 和 *paretovariate()*。


# 更多资源

+ [The Python Standard Library By Example: 5.3 ](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
+ [random](https://docs.python.org/2/library/random.html) The standard library documentation for this module.
+ [Mersenne Twister](http://en.wikipedia.org/wiki/Mersenne_twister) Wikipedia article about the pseudorandom generator algorithm used by Python.
+ [Uniform distribution](http://en.wikipedia.org/wiki/Uniform_distribution_(continuous) Wikipedia article about continuous uniform distributions in statistics.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/5.3random.ipynb) 
