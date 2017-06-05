---
title: Python 2 标准库示例：4.1 time-时钟时间
date: 2017-06-05
writing-time: 2017-06-04
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture time
---


不像 *int*, *float* 等，Python 没有本地的日期或时间类型，但包含有 3 个模块用于处理与日期和时间相关的值。

+ *time* 模块导出底层 C 函数库中时间相关的函数，包括获取时钟时间和处理器运行时间的函数，基本的解析和格式化工具等。
+ *datetime* 模块为日期、时间及其组合支持更高级的接口。该模块中的类还支持算术操作、比较、时区配置等。
+ *calendar* 模块为年、月、周等创建格式化表示。

**目的**: 提供处理时钟时间的函数。

**Python 版本**: 1.4+

*time* 模块与低层的 C 实现关联，因此一些细节会特定于平台。


# 术语

## 纪元 epoch

指开始的时间点，在 Unix 中，指 1970-01-01 00:00:00。可通过 *time.gmtime(0)* 获取。本模块中的函数不能处理纪元前或纪元很久后的时间。表示的时间范围由低层的 C 实现决定，Unix 中最大表示时间是 2038 年。

## UTC，GMT

即世界标准时间 Coordinated Universal Time，缩写为 UTC 不是误写，是英文与法文折中的结果。之前叫作格林尼治标准时间（Greenwich Mean Time, GMT）。

## DST

DST 是 Daylight Saving Time 的缩写, 即夏令时间（日光节省时间）。由于夏天日出早，白天长，一些地方人为规定将时间提前 1 小时，从而使人们早睡早起，节约能源。实行夏令时的地方，处理时间时要偏移 1 个小时。DST 的规则由各地方规定，且可能每年变化，只能通过查询 C 库中包含的一个表格来了解。

## struct_time

*gmtime()*, *localtime()*, *strptime()* 返回的都是 *struct_time* 类型的时间值，这是一个具有 *named tuple* 接口的对象，各项可通过索引和属性名访问。

索引 | 属性名   | 值
-----|
0    | tm_year  | 例如 2017
1    | tm_mon   | [1, 12]
2    | tm_mday  | [1, 31]
3    | tm_hour  | [0, 23]
4    | tm_min   | [0, 59]
5    | tm_sec   | [0, 61]
6    | tm_wday  | [0, 6], 0 指周一
7    | tm_yday  | [1, 366]
8    | tm_isdst | 0, 1, -1

其中 *tm_sec* 最多有 61 秒，这是由于闰秒(leap second)的存在导致的。由于地球自转不均，会使世界时（民用时）和原子时有偏差，故要人为规定在某些时间调整世界标准间约为 1 秒。

而 *asctime()*, *mktime()*, *strftime()* 接受的参数也是 *struct_time* 对象。

自纪元以前的浮点秒数值与 *struct_time* 对象间的转换如下：

From                      | To                        | Use
--------------------------|
seconds since epoch       | struct_time in UTC        | gmtime()
seconds since epoch       | struct_time in local time | localtime()
struct_time in UTC        | seconds since epoch       | calendar.timegm()
struct_time in local time | seconds since epoch       | mktime


# 挂钟时间


*time* 模块中的一个核心函数是 *time()*，它返回一个浮点值，表示从纪元时间到当前的秒数。


```python
import time

print 'The time is:', time.time()
```

    The time is: 1496577423.91


虽然返回值是浮点数，但具体精度依赖平台。浮点表示方便排序和比较操作，但不易看懂。*ctime()* (char time 缩写）可将当前值或浮点数表示的时间值格式化输出。


```python
import time

print 'The time is:', time.ctime()
latter = time.time() + 15
print '15 secs from now:', time.ctime(latter)
```

    The time is: Sun Jun  4 21:03:16 2017
    15 secs from now: Sun Jun  4 21:03:31 2017


# 处理器时钟时间

*time()* 返回挂钟时间，而 *clock()* 返回处理器时钟时间，其返回值反映了程序使用处理器的实际时间，故可用于性能测试、基准测试等。


```python
import hashlib
import time

# Data to use to calculate md5 checksums
data = 'abc'*1000

for i in range(5):
    h = hashlib.sha1()
    print time.ctime(), ': %0.3f %0.3f' % (time.time(), time.clock())
    for i in range(300000):
        h.update(data)
    cksum = h.digest()
```

    Sun Jun  4 21:08:51 2017 : 1496581731.747 0.924
    Sun Jun  4 21:08:53 2017 : 1496581733.464 2.636
    Sun Jun  4 21:08:55 2017 : 1496581735.176 4.347
    Sun Jun  4 21:08:56 2017 : 1496581736.860 6.031
    Sun Jun  4 21:08:58 2017 : 1496581738.538 7.709


当程序没有做任何事时，处理器一般不会计时。如下，*sleep()* 会交出当前线程的控制权，并等待系统再次调度它，其 *sleep* 时间没有计时在程序运行时间内。


```python
import time

for i in range(6, 1, -1):
    print '%s %0.2f %0.2f' % (time.ctime(),
                             time.time(),
                             time.clock())
    print 'Sleeping', i
    time.sleep(i)
```

    Sun Jun  4 21:11:36 2017 1496581896.07 9.41
    Sleeping 6
    Sun Jun  4 21:11:42 2017 1496581902.08 9.42
    Sleeping 5
    Sun Jun  4 21:11:47 2017 1496581907.08 9.42
    Sleeping 4
    Sun Jun  4 21:11:51 2017 1496581911.09 9.42
    Sleeping 3
    Sun Jun  4 21:11:54 2017 1496581914.09 9.43
    Sleeping 2


# 时间组件

通过 *struct_time* 定义时间的各组件部分。


```python
import time

def show_struct(s):
    print ' tm_year:', s.tm_year
    print ' tm_mon:', s.tm_mon
    print ' tm_mday:', s.tm_mday
    print ' tm_hour:', s.tm_hour
    print ' tm_min:', s.tm_min
    print ' tm_sec:', s.tm_sec
    print ' tm_wday:', s.tm_wday
    print ' tm_yday:', s.tm_yday
    print ' tm_isdst:', s.tm_isdst
    
print 'gmtime(UTC):'
show_struct(time.gmtime())
print '\nlocaltime:'
show_struct(time.localtime())
print '\nmktime:', time.mktime(time.localtime())
```

    gmtime(UTC):
     tm_year: 2017
     tm_mon: 6
     tm_mday: 4
     tm_hour: 13
     tm_min: 19
     tm_sec: 11
     tm_wday: 6
     tm_yday: 155
     tm_isdst: 0
    
    localtime:
     tm_year: 2017
     tm_mon: 6
     tm_mday: 4
     tm_hour: 21
     tm_min: 19
     tm_sec: 11
     tm_wday: 6
     tm_yday: 155
     tm_isdst: 0
    
    mktime: 1496582351.0


*gmtime()* 返回 UTC 的当前时间，*localtime()* 返回当前时区内的当前时间，返回的都是 *struct_time* 对象。而 *mktime()* 将 *struct_time* 值转换成一个浮点数时间值。

# 时区

检测当前时间的函数依赖时区设置信息。时区可由程序设置，也可使用系统默认的时间设置。修改时区设置不会修改时间值，只是修改了时间的呈现方式。

要修改时区，先设置环境变量 *TZ*，再调用 *tzset()* 即可。时区的细节很复杂，因此通常是通过指定时区名，由低层库进行具体处理。


```python
import time
import os

def show_zone_info():
    print ' TZ:', os.environ.get('TZ', '(not set)')
    print ' tzname:', time.tzname # return (name_of_local_non-DST_timezone, name_of_local-DST_timezone)
    print ' Zone: %d (%d)' % (time.timezone, # offset of the local non-DST timezone, in seconds
                             (time.timezone/3600))
    print ' DST:', time.daylight
    print ' Time:', time.ctime()
    
print 'Default:'
show_zone_info()

ZONES = [ 'GMT',
          'Europe/Amsterdam',
        ]

for zone in ZONES:
    os.environ['TZ'] = zone
    time.tzset()
    print zone, ":"
    show_zone_info()
```

    Default:
     TZ: Europe/Amsterdam
     tzname: ('CET', 'CEST')
     Zone: -3600 (-1)
     DST: 1
     Time: Sun Jun  4 15:43:05 2017
    GMT :
     TZ: GMT
     tzname: ('GMT', 'GMT')
     Zone: 0 (0)
     DST: 0
     Time: Sun Jun  4 13:43:05 2017
    Europe/Amsterdam :
     TZ: Europe/Amsterdam
     tzname: ('CET', 'CEST')
     Zone: -3600 (-1)
     DST: 1
     Time: Sun Jun  4 15:43:05 2017


# 时间的解析和格式化

*strptime()* 和 *strftime()* 在 *struct_time* 与字符串表示的时间值之间进行转换。具体的格式指令见 [time 模块的官方文档](https://docs.python.org/2/library/time.html#time.strftime)。

下例将当前时间从字符串转成 *struct_time* 实例，再转回字符串。


```python
import time

def show_struct(s):
    print ' tm_year:', s.tm_year
    print ' tm_mon:', s.tm_mon
    print ' tm_mday:', s.tm_mday
    print ' tm_hour:', s.tm_hour
    print ' tm_min:', s.tm_min
    print ' tm_sec:', s.tm_sec
    print ' tm_wday:', s.tm_wday
    print ' tm_yday:', s.tm_yday
    print ' tm_isdst:', s.tm_isdst
    
now = time.ctime()
print 'Now:', now

parsed = time.strptime(now)
print '\nParsed:'
show_struct(parsed)

print '\nFormatted:', time.strftime("%a %b %d %H:%M:%S %Y", parsed)
```

    Now: Sun Jun  4 15:50:50 2017
    
    Parsed:
     tm_year: 2017
     tm_mon: 6
     tm_mday: 4
     tm_hour: 15
     tm_min: 50
     tm_sec: 50
     tm_wday: 6
     tm_yday: 155
     tm_isdst: -1
    
    Formatted: Sun Jun 04 15:50:50 2017


输入字符串与输入不完全相同，输出中的月日期加了 0 前缀。

# 更多资源

+ [time](https://docs.python.org/2/library/time.html) Standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/4.1time.ipynb) 


# 参考

+ [The Python Standard Library By Example: 4.1 Time-Clock Time](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
