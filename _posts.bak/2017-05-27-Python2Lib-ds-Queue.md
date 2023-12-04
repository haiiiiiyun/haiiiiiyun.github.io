---
title: Python 2 标准库示例：2.5 Queue-实现线程安全的队列
date: 2017-05-27
writing-time: 2017-05-27 15:10
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture Queue
---


**目的**: 实现一种线程安全的队列。

**Python 版本**: 1.4+，Python 3 中模块名改为 queue

*Queue* 模块提供了 3 种队列：

1. 普通的 FIFO 队列
2. LIFO 队列，即堆栈
3. 基于 heapq 实现的优先队列 PriorityQueue

初始化队列中可传入一个 *max_size* 参数，以限制队列的最大长度，从而当队列满时，添加元素操作会堵塞。

# 基本的 FIFO 队列

使用 *put()* 添加元素，*get()* 移除并返回元素。


```python
import Queue

q = Queue.Queue()

for i in range(5):
    q.put(i)
    
while not q.empty():
    print q.get(),
print
```

    0 1 2 3 4


# LIFO 队列（堆栈）


```python
import Queue

q = Queue.LifoQueue()

for i in range(5):
    q.put(i)
    
while not q.empty():
    print q.get(),
print
```

    4 3 2 1 0


# 优先队列 PriorityQueue

基于 *heapq* 模块实现优先排序，因此最小优先值的最先处理。PriorityQueue 的元素的一般形式是元组 `(priority, task)`。


```python
import Queue
import threading

class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print 'New job:', description
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
    
q = Queue.PriorityQueue()

q.put(Job(3, 'Mid-level job'))
q.put(Job(10, 'Low-level job'))
q.put(Job(1, 'Important job'))

def process_job(q):
    while True:
        next_job = q.get()
        print 'Processing job:', next_job.description
        q.task_done()
        
workers = [threading.Thread(target=process_job, args=(q,)),
          threading.Thread(target=process_job, args=(q,)),
          ]
for w in workers:
    w.setDaemon(True)
    w.start()

# 该队列会堵塞，直到队列上的所有任何都已处理完毕。
# q.put(task) 会增加队列上的未处理任务数，
# 而消费者线程中先调用 q.get() 后再调用 q.task_done()
# 表明任务处理完毕，再减少队列上的未处理任务数。
# 当未处理任务数为 0 时，取消队列堵塞。
q.join() 

```

    New job: Mid-level job
    New job: Low-level job
    New job: Important job
    Processing job: Important job
    Processing job: Mid-level job
    Processing job: Low-level job


# 更多资源

+ [Queue](https://docs.python.org/2.7/library/queue.html?highlight=queue) Standard library documentation for this module.
+ [Queue data structures](http://en.wikipedia.org/wiki/Queue_(data_structure)) Wikipedia article explaining queues.
+ [FIFO](http://en.wikipedia.org/wiki/FIFO) Wikipedia article explaining first-in, first-out data structures.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.5Queue.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.5 Queue-Threa-Safe FIFO Implementation](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
