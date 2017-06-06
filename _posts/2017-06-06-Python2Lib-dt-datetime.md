---
title: Python 2 标准库示例：4.2 datetime-日期与时间值的处理
date: 2017-06-06
writing-time: 2017-06-05
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture datetime
---


**目的**: 该模块提供了与日期和时间解析、格式化和算术运算相关的函数和类。

**Python 版本**: 2.3+。

*datetime* 模块的实现专注于对日期和时间组件属性的抽取，以进行输出的格式化和处理。

共有两种种类的日期和时间对象：*naive* 和 *aware*。

*aware* 种类的对象含有时区、夏令时等时间调整量信息。而 *naive* 种类的对象没有这些信息，因此，它是表示一个 UTC 时间、本地时间也是某个时区的时间，解释完全在于程序。

如果需要 *aware* 种类的对象，*datetime* 和 *time* 对象都有一个可选的属性 *tzinfo*，可用来设置为一个抽象类 *tzinfo* 的某子类的一个实例。*tzinfo* 对象含有至 UTC 时间的偏移量、时区名、是否有夏令时等信息。要注意的是，*datetime* 模块中没有提供 *tzinfo* 的具体类。[pytz](http://pytz.sourceforge.net/) 库提供了一些时区实现细节。


# 时间

时间由 *time* 类表示。*time* 实例具有 *hour*, *minute*, *second*, *microsecond* 及时区信息等属性。


```python
import datetime

t = datetime.time(1, 2, 3)
print t
print 'hour:', t.hour
print 'minute:', t.minute
print 'second:', t.second
print 'microsecond:', t.microsecond
print 'tzinfo:', t.tzinfo
```

    01:02:03
    hour: 1
    minute: 2
    second: 3
    microsecond: 0
    tzinfo: None


*time* 类中还有表示一天中有效时间区间的常量。


```python
import datetime

print 'Earliest:', datetime.time.min
print 'Latest:', datetime.time.max
print 'Resolution:', datetime.time.resolution
```

    Earliest: 00:00:00
    Latest: 23:59:59.999999
    Resolution: 0:00:00.000001


可见，时间的最小精度是 1 微秒。因此当将浮点值传给 *microsecond* 参数时，Python 2.7 中会出现 *TypeError*，而之前的版本中会出现 *DeprecationWarning* 并自动转成一个整数。


```python
import datetime

for m in [1, 0, 0.1, 0.6]:
    try:
        print '%02.1f:' % m, datetime.time(0, 0, 0, microsecond=m)
    except TypeError, err:
        print 'Error:', err
```

    1.0: 00:00:00.000001
    0.0: 00:00:00
    0.1: Error: integer argument expected, got float
    0.6: Error: integer argument expected, got float


# 日期

日期值由 *date* 类表示。其实例中有 *year*, *month*, *day* 等属性。可用 *today()* 获取当前的日期。


```python
import datetime

today = datetime.date.today()
print today
print 'ctime:', today.ctime()
tt = today.timetuple()  # to struct_time
print 'tuple:'
print ' tm_year:', tt.tm_year
print ' tm_mon:', tt.tm_mon
print ' tm_mday:', tt.tm_mday
print ' tm_hour:', tt.tm_hour
print ' tm_min:', tt.tm_min
print ' tm_sec:', tt.tm_sec
print ' tm_wday:', tt.tm_wday
print ' tm_yday:', tt.tm_yday
print ' tm_isdst:', tt.tm_isdst
print 'ordinal:', today.toordinal()  # (year=1, month=1, day=1) -> 1
print 'year:', today.year
print 'month:', today.month
print 'day:', today.day
```

    2017-06-05
    ctime: Mon Jun  5 00:00:00 2017
    tuple:
     tm_year: 2017
     tm_mon: 6
     tm_mday: 5
     tm_hour: 0
     tm_min: 0
     tm_sec: 0
     tm_wday: 0
     tm_yday: 156
     tm_isdst: -1
    ordinal: 736485
    year: 2017
    month: 6
    day: 5


也可以从时间戳或序号值（ordinal 值，其中 1 年 1 月 1 日的序号值为 1）。


```python
import datetime
import time

o = 736485
print 'o:', o
print 'fromordinal(o):', datetime.date.fromordinal(o)

t = time.time()
print 't:', t
print 'fromtimestamp(t):', datetime.date.fromtimestamp(t)
```

    o: 736485
    fromordinal(o): 2017-06-05
    t: 1496673680.68
    fromtimestamp(t): 2017-06-05


类似 *time*，*date* 也是最大值，最小值等常量。


```python
import datetime

print 'Earliest:', datetime.date.min
print 'Latest:', datetime.date.max
print 'Resolution:', datetime.date.resolution
```

    Earliest: 0001-01-01
    Latest: 9999-12-31
    Resolution: 1 day, 0:00:00


通过替换现存 *date* 对象的组件也可创建一个新的 *date* 实例。


```python
import datetime

d1 = datetime.date(2016, 6, 5)
print 'd1:', d1.ctime()
d2 = d1.replace(year=2017)
print 'd2:', d2.ctime()
```

    d1: Sun Jun  5 00:00:00 2016
    d2: Mon Jun  5 00:00:00 2017


# timedelta

*datetime* 对象间的偏移动量用 *timedelta* 对象表示。*timedelta* 值在内部都归整为 *days*, *seconds*, *microseconds* 三个整数存储，即通过 weeks, hours, minutes 等参数传入的值也都会转换合并到上面的 3 个变量中存储。

归整化后，*timedelta* 值的表示就会唯一，同时，各变量的值区间为：

+ 0 <= microseconds < 1000000
+ 0 <= seconds < 3600*24 (the number of seconds in one day)
+ -999999999 <= days <= 999999999


```python
import datetime

print 'microseconds:', datetime.timedelta(microseconds=1)
print 'milliseconds:', datetime.timedelta(milliseconds=1)
print 'seconds:', datetime.timedelta(seconds=1)
print 'minutes:', datetime.timedelta(minutes=1)
print "hours:", datetime.timedelta(hours=1)
print 'days:', datetime.timedelta(days=1)
print 'weeks:', datetime.timedelta(weeks=1)
```

    microseconds: 0:00:00.000001
    milliseconds: 0:00:00.001000
    seconds: 0:00:01
    minutes: 0:01:00
    hours: 1:00:00
    days: 1 day, 0:00:00
    weeks: 7 days, 0:00:00


*total_seconds()* 返回 *timedelta* 实例的总秒数（浮点数）：


```python
import datetime

for delta in [datetime.timedelta(microseconds=1),
            datetime.timedelta(milliseconds=1),
            datetime.timedelta(seconds=1),
            datetime.timedelta(minutes=1),
            datetime.timedelta(hours=1),
            datetime.timedelta(days=1),
            datetime.timedelta(weeks=1),
            ]:
    print '%15s = %s seconds' % (delta, delta.total_seconds())
```

     0:00:00.000001 = 1e-06 seconds
     0:00:00.001000 = 0.001 seconds
            0:00:01 = 1.0 seconds
            0:01:00 = 60.0 seconds
            1:00:00 = 3600.0 seconds
     1 day, 0:00:00 = 86400.0 seconds
    7 days, 0:00:00 = 604800.0 seconds


# 日期的算术运算


```python
import datetime

today = datetime.date.today()
print 'today:', today

one_day = datetime.timedelta(days=1)
print 'one day:', one_day

yesterday = today - one_day
print 'yesterday:', yesterday

tomorrow = today + one_day
print 'tomorrow:', tomorrow

print
print 'tomorrow - yesterday:', tomorrow - yesterday
print 'yesterday - tomorrow:', yesterday - tomorrow
```

    today: 2017-06-05
    one day: 1 day, 0:00:00
    yesterday: 2017-06-04
    tomorrow: 2017-06-06
    
    tomorrow - yesterday: 2 days, 0:00:00
    yesterday - tomorrow: -2 days, 0:00:00


# 比较

*date* 和 *time* 值都可以进行比较。


```python
import datetime
import time

print 'Times:'
t1 = datetime.time(12, 55, 0)
print ' t1:', t1
t2 = datetime.time(13, 5, 0)
print ' t2:', t2
print ' t1 < t2', t1 < t2

print '\nDates:'
d1 = datetime.date.today()
print ' d1:', d1
d2 = datetime.date.today() + datetime.timedelta(days=1)
print ' d2:', d2
print ' d1 > d2:', d1 > d2
```

    Times:
     t1: 12:55:00
     t2: 13:05:00
     t1 < t2 True
    
    Dates:
     d1: 2017-06-05
     d2: 2017-06-06
     d1 > d2: False


# 组合日期和时间

*datetime* 类组合了 *date* 和 *time* 的值，因而包含了它们两个的所有属性。 有以下几个创建 *datetime* 实例的便捷方法。


```python
import datetime

# 有可选 tzinfo 参数，没有提供时返回本地的时间，此时同 today()
print 'now:', datetime.datetime.now()

# 返回本地的时间
print 'today:', datetime.datetime.today()

# 返回 UTC 时间
print 'UTC now:', datetime.datetime.utcnow()
print

fields = ['year', 'month', 'day',
         'hour', 'minute', 'second', 'microsecond',
         ]

d = datetime.datetime.now()
for attr in fields:
    print '%15s: %s' % (attr, getattr(d, attr))
```

    now: 2017-06-05 23:13:24.028225
    today: 2017-06-05 23:13:24.029239
    UTC now: 2017-06-05 15:13:24.029494
    
               year: 2017
              month: 6
                day: 5
               hour: 23
             minute: 13
             second: 24
        microsecond: 29915


和 *date* 类似，*datetime* 也可以通过 *fromordinal()* 和 *fromtimestamp()* 创建实例。同时，通过 *combine* 可以将 *date* 和 *time* 值合并成一个 *datetime*。


```python
import datetime

t = datetime.time(1, 2, 3)
print 't:', t

d = datetime.date.today()
print 'd:', d

dt = datetime.datetime.combine(d, t)
print 'dt:', dt
```

    t: 01:02:03
    d: 2017-06-05
    dt: 2017-06-05 01:02:03


# 格式化和解析

*datetime* 对象默认使用 ISO-8601 格式（`YYYY-MM-DDTHH:MM:SS.mmmmmm`）输出字符串表示。可使用 *strftime()* 进行其它格式化输出。用 *strptime()* 可将格式化字符串转换回 *datetime* 对象。详细的格式化指令见: [datetime 的官方文档](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)。


```python
import datetime

format = "%Y-%m-%d %H:%M:%S"

today = datetime.datetime.today()
print 'ISO:', today

s = today.strftime(format)
print 'strftime:', s

d = datetime.datetime.strptime(s, format)
print 'strptime:', d.strftime(format)
```

    ISO: 2017-06-05 23:23:43.133657
    strftime: 2017-06-05 23:23:43
    strptime: 2017-06-05 23:23:43


# 更多资源

+ [datetime](https://docs.python.org/2/library/datetime.html) The standard library documentation for this module.
+ [dateutil](http://labix.org/python-dateutil) dateutil from Labix extends the datetime module with additional features.
+ [WikiPedia: Proleptic Gregorian calendar](http://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar) A description of the Gregorian calendar system.
+ [pytz](http://pytz.sourceforge.net/) World Time Zone database.
+ [ISO 8601](http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/date_and_time_format.htm) The standard for numeric representation of dates and time.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/4.2datetime.ipynb) 


# 参考

+ [The Python Standard Library By Example: 4.2 Datetime-Date and Time value Manipulation](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
