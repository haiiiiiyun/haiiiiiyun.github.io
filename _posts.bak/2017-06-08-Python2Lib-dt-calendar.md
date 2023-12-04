---
title: Python 2 标准库示例：4.3 calendar-处理日期值
date: 2017-06-08
writing-time: 2017-06-08
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture calendar
---


**目的**: 该模块实现了一些处理日期的类，用来管理年、月、周等值。

**Python 版本**: 1.4+， 并在 2.5 时有更新。

*calendar* 模块定义了 *Calendar*，封装了日历计算相关的方法。另外，子类 *TextCalendar* 和 *HTMLCalendar* 可进行格式化输出。这些类默认将周一设置为每周的第一天（欧洲习惯），但可在初始化时通过传入参数修改（0 是 周一，..., 6 是周日，也可用模块中的常量指定，如 *calendar.MONDAY*）。

# Calendar 实例的方法


```python
import calendar

c = calendar.Calendar()

import calendar

c = calendar.Calendar()

# 按序输出一周中的每天的整数值，第一天值和 firstweekday 同
print '\niterweekdays():'
for d in c.iterweekdays(): 
    print d
    
# 返回某月 [1,12] 中的所有天 (datetime.date 对象), 为补全
#  整周，会包含之前月和之后月的某些天
print '\nitermonthdates(2017, 6):'
for d in c.itermonthdates(2017,6):
    print d
    
# 类似 itermonthdates()，但只返回整数表示的第几天，[0-31], 其中 0 表示为补全整周包含的
# 临近月中的天
print '\nitermonthdays(2017, 6):'
for d in c.itermonthdays(2017, 6):
    print d
    
# 类似 iermonhdays()，但返回中包含整数表示的第几天及周几的数据
print '\nitermonthdays2(2017, 6):'
for d in c.itermonthdays2(2017, 6):
    print d
    
# 日历数据都是按周组织的，
# 故返回周数据列表，
# 其中周数据是一个包含 7 个 datetime.date 对象的列表
print '\nmonthdatescalendar(2017, 6):'
for index, week in enumerate(c.monthdatescalendar(2017, 6)):
    print ' week', index+1, ':', week
    
# monthdayscalendar(), monthdays2calendar() 都和 monthdatescalenar()
# 类似，只不过前者返回的周数据中的元素是天数，而后者返回的周数据中的元素是 (天数,周几)

#yeardatescalendar(year[, width])
# 返回 width(默认 3) 个月为一组的组列表，组中的每个月数据和 monthdatescalendar()
# 返回的相同。
#而 yeardayscalendar(), yeardays2calendar() 也类似。
width = 3
print '\nyeardatescalendar(2017, ', width, '):'
for index, month_rows in enumerate(c.yeardatescalendar(2017, 3)):
    print ' row', index+1, ':'
    for index2, month in enumerate(month_rows):
        print '  month', index2+1, ':', month
```

    
    iterweekdays():
    0
    1
    2
    3
    4
    5
    6
    
    itermonthdates(2017, 6):
    2017-05-29
    2017-05-30
    2017-05-31
    2017-06-01
    2017-06-02
    2017-06-03
    2017-06-04
    2017-06-05
    2017-06-06
    2017-06-07
    2017-06-08
    2017-06-09
    2017-06-10
    2017-06-11
    2017-06-12
    2017-06-13
    2017-06-14
    2017-06-15
    2017-06-16
    2017-06-17
    2017-06-18
    2017-06-19
    2017-06-20
    2017-06-21
    2017-06-22
    2017-06-23
    2017-06-24
    2017-06-25
    2017-06-26
    2017-06-27
    2017-06-28
    2017-06-29
    2017-06-30
    2017-07-01
    2017-07-02
    
    itermonthdays(2017, 6):
    0
    0
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    0
    0
    
    itermonthdays2(2017, 6):
    (0, 0)
    (0, 1)
    (0, 2)
    (1, 3)
    (2, 4)
    (3, 5)
    (4, 6)
    (5, 0)
    (6, 1)
    (7, 2)
    (8, 3)
    (9, 4)
    (10, 5)
    (11, 6)
    (12, 0)
    (13, 1)
    (14, 2)
    (15, 3)
    (16, 4)
    (17, 5)
    (18, 6)
    (19, 0)
    (20, 1)
    (21, 2)
    (22, 3)
    (23, 4)
    (24, 5)
    (25, 6)
    (26, 0)
    (27, 1)
    (28, 2)
    (29, 3)
    (30, 4)
    (0, 5)
    (0, 6)
    
    monthdatescalendar(2017, 6):
     week 1 : [datetime.date(2017, 5, 29), datetime.date(2017, 5, 30), datetime.date(2017, 5, 31), datetime.date(2017, 6, 1), datetime.date(2017, 6, 2), datetime.date(2017, 6, 3), datetime.date(2017, 6, 4)]
     week 2 : [datetime.date(2017, 6, 5), datetime.date(2017, 6, 6), datetime.date(2017, 6, 7), datetime.date(2017, 6, 8), datetime.date(2017, 6, 9), datetime.date(2017, 6, 10), datetime.date(2017, 6, 11)]
     week 3 : [datetime.date(2017, 6, 12), datetime.date(2017, 6, 13), datetime.date(2017, 6, 14), datetime.date(2017, 6, 15), datetime.date(2017, 6, 16), datetime.date(2017, 6, 17), datetime.date(2017, 6, 18)]
     week 4 : [datetime.date(2017, 6, 19), datetime.date(2017, 6, 20), datetime.date(2017, 6, 21), datetime.date(2017, 6, 22), datetime.date(2017, 6, 23), datetime.date(2017, 6, 24), datetime.date(2017, 6, 25)]
     week 5 : [datetime.date(2017, 6, 26), datetime.date(2017, 6, 27), datetime.date(2017, 6, 28), datetime.date(2017, 6, 29), datetime.date(2017, 6, 30), datetime.date(2017, 7, 1), datetime.date(2017, 7, 2)]
    
    yeardatescalendar(2017,  3 ):
     row 1 :
      month 1 : [[datetime.date(2016, 12, 26), datetime.date(2016, 12, 27), datetime.date(2016, 12, 28), datetime.date(2016, 12, 29), datetime.date(2016, 12, 30), datetime.date(2016, 12, 31), datetime.date(2017, 1, 1)], [datetime.date(2017, 1, 2), datetime.date(2017, 1, 3), datetime.date(2017, 1, 4), datetime.date(2017, 1, 5), datetime.date(2017, 1, 6), datetime.date(2017, 1, 7), datetime.date(2017, 1, 8)], [datetime.date(2017, 1, 9), datetime.date(2017, 1, 10), datetime.date(2017, 1, 11), datetime.date(2017, 1, 12), datetime.date(2017, 1, 13), datetime.date(2017, 1, 14), datetime.date(2017, 1, 15)], [datetime.date(2017, 1, 16), datetime.date(2017, 1, 17), datetime.date(2017, 1, 18), datetime.date(2017, 1, 19), datetime.date(2017, 1, 20), datetime.date(2017, 1, 21), datetime.date(2017, 1, 22)], [datetime.date(2017, 1, 23), datetime.date(2017, 1, 24), datetime.date(2017, 1, 25), datetime.date(2017, 1, 26), datetime.date(2017, 1, 27), datetime.date(2017, 1, 28), datetime.date(2017, 1, 29)], [datetime.date(2017, 1, 30), datetime.date(2017, 1, 31), datetime.date(2017, 2, 1), datetime.date(2017, 2, 2), datetime.date(2017, 2, 3), datetime.date(2017, 2, 4), datetime.date(2017, 2, 5)]]
      month 2 : [[datetime.date(2017, 1, 30), datetime.date(2017, 1, 31), datetime.date(2017, 2, 1), datetime.date(2017, 2, 2), datetime.date(2017, 2, 3), datetime.date(2017, 2, 4), datetime.date(2017, 2, 5)], [datetime.date(2017, 2, 6), datetime.date(2017, 2, 7), datetime.date(2017, 2, 8), datetime.date(2017, 2, 9), datetime.date(2017, 2, 10), datetime.date(2017, 2, 11), datetime.date(2017, 2, 12)], [datetime.date(2017, 2, 13), datetime.date(2017, 2, 14), datetime.date(2017, 2, 15), datetime.date(2017, 2, 16), datetime.date(2017, 2, 17), datetime.date(2017, 2, 18), datetime.date(2017, 2, 19)], [datetime.date(2017, 2, 20), datetime.date(2017, 2, 21), datetime.date(2017, 2, 22), datetime.date(2017, 2, 23), datetime.date(2017, 2, 24), datetime.date(2017, 2, 25), datetime.date(2017, 2, 26)], [datetime.date(2017, 2, 27), datetime.date(2017, 2, 28), datetime.date(2017, 3, 1), datetime.date(2017, 3, 2), datetime.date(2017, 3, 3), datetime.date(2017, 3, 4), datetime.date(2017, 3, 5)]]
      month 3 : [[datetime.date(2017, 2, 27), datetime.date(2017, 2, 28), datetime.date(2017, 3, 1), datetime.date(2017, 3, 2), datetime.date(2017, 3, 3), datetime.date(2017, 3, 4), datetime.date(2017, 3, 5)], [datetime.date(2017, 3, 6), datetime.date(2017, 3, 7), datetime.date(2017, 3, 8), datetime.date(2017, 3, 9), datetime.date(2017, 3, 10), datetime.date(2017, 3, 11), datetime.date(2017, 3, 12)], [datetime.date(2017, 3, 13), datetime.date(2017, 3, 14), datetime.date(2017, 3, 15), datetime.date(2017, 3, 16), datetime.date(2017, 3, 17), datetime.date(2017, 3, 18), datetime.date(2017, 3, 19)], [datetime.date(2017, 3, 20), datetime.date(2017, 3, 21), datetime.date(2017, 3, 22), datetime.date(2017, 3, 23), datetime.date(2017, 3, 24), datetime.date(2017, 3, 25), datetime.date(2017, 3, 26)], [datetime.date(2017, 3, 27), datetime.date(2017, 3, 28), datetime.date(2017, 3, 29), datetime.date(2017, 3, 30), datetime.date(2017, 3, 31), datetime.date(2017, 4, 1), datetime.date(2017, 4, 2)]]
     row 2 :
      month 1 : [[datetime.date(2017, 3, 27), datetime.date(2017, 3, 28), datetime.date(2017, 3, 29), datetime.date(2017, 3, 30), datetime.date(2017, 3, 31), datetime.date(2017, 4, 1), datetime.date(2017, 4, 2)], [datetime.date(2017, 4, 3), datetime.date(2017, 4, 4), datetime.date(2017, 4, 5), datetime.date(2017, 4, 6), datetime.date(2017, 4, 7), datetime.date(2017, 4, 8), datetime.date(2017, 4, 9)], [datetime.date(2017, 4, 10), datetime.date(2017, 4, 11), datetime.date(2017, 4, 12), datetime.date(2017, 4, 13), datetime.date(2017, 4, 14), datetime.date(2017, 4, 15), datetime.date(2017, 4, 16)], [datetime.date(2017, 4, 17), datetime.date(2017, 4, 18), datetime.date(2017, 4, 19), datetime.date(2017, 4, 20), datetime.date(2017, 4, 21), datetime.date(2017, 4, 22), datetime.date(2017, 4, 23)], [datetime.date(2017, 4, 24), datetime.date(2017, 4, 25), datetime.date(2017, 4, 26), datetime.date(2017, 4, 27), datetime.date(2017, 4, 28), datetime.date(2017, 4, 29), datetime.date(2017, 4, 30)]]
      month 2 : [[datetime.date(2017, 5, 1), datetime.date(2017, 5, 2), datetime.date(2017, 5, 3), datetime.date(2017, 5, 4), datetime.date(2017, 5, 5), datetime.date(2017, 5, 6), datetime.date(2017, 5, 7)], [datetime.date(2017, 5, 8), datetime.date(2017, 5, 9), datetime.date(2017, 5, 10), datetime.date(2017, 5, 11), datetime.date(2017, 5, 12), datetime.date(2017, 5, 13), datetime.date(2017, 5, 14)], [datetime.date(2017, 5, 15), datetime.date(2017, 5, 16), datetime.date(2017, 5, 17), datetime.date(2017, 5, 18), datetime.date(2017, 5, 19), datetime.date(2017, 5, 20), datetime.date(2017, 5, 21)], [datetime.date(2017, 5, 22), datetime.date(2017, 5, 23), datetime.date(2017, 5, 24), datetime.date(2017, 5, 25), datetime.date(2017, 5, 26), datetime.date(2017, 5, 27), datetime.date(2017, 5, 28)], [datetime.date(2017, 5, 29), datetime.date(2017, 5, 30), datetime.date(2017, 5, 31), datetime.date(2017, 6, 1), datetime.date(2017, 6, 2), datetime.date(2017, 6, 3), datetime.date(2017, 6, 4)]]
      month 3 : [[datetime.date(2017, 5, 29), datetime.date(2017, 5, 30), datetime.date(2017, 5, 31), datetime.date(2017, 6, 1), datetime.date(2017, 6, 2), datetime.date(2017, 6, 3), datetime.date(2017, 6, 4)], [datetime.date(2017, 6, 5), datetime.date(2017, 6, 6), datetime.date(2017, 6, 7), datetime.date(2017, 6, 8), datetime.date(2017, 6, 9), datetime.date(2017, 6, 10), datetime.date(2017, 6, 11)], [datetime.date(2017, 6, 12), datetime.date(2017, 6, 13), datetime.date(2017, 6, 14), datetime.date(2017, 6, 15), datetime.date(2017, 6, 16), datetime.date(2017, 6, 17), datetime.date(2017, 6, 18)], [datetime.date(2017, 6, 19), datetime.date(2017, 6, 20), datetime.date(2017, 6, 21), datetime.date(2017, 6, 22), datetime.date(2017, 6, 23), datetime.date(2017, 6, 24), datetime.date(2017, 6, 25)], [datetime.date(2017, 6, 26), datetime.date(2017, 6, 27), datetime.date(2017, 6, 28), datetime.date(2017, 6, 29), datetime.date(2017, 6, 30), datetime.date(2017, 7, 1), datetime.date(2017, 7, 2)]]
     row 3 :
      month 1 : [[datetime.date(2017, 6, 26), datetime.date(2017, 6, 27), datetime.date(2017, 6, 28), datetime.date(2017, 6, 29), datetime.date(2017, 6, 30), datetime.date(2017, 7, 1), datetime.date(2017, 7, 2)], [datetime.date(2017, 7, 3), datetime.date(2017, 7, 4), datetime.date(2017, 7, 5), datetime.date(2017, 7, 6), datetime.date(2017, 7, 7), datetime.date(2017, 7, 8), datetime.date(2017, 7, 9)], [datetime.date(2017, 7, 10), datetime.date(2017, 7, 11), datetime.date(2017, 7, 12), datetime.date(2017, 7, 13), datetime.date(2017, 7, 14), datetime.date(2017, 7, 15), datetime.date(2017, 7, 16)], [datetime.date(2017, 7, 17), datetime.date(2017, 7, 18), datetime.date(2017, 7, 19), datetime.date(2017, 7, 20), datetime.date(2017, 7, 21), datetime.date(2017, 7, 22), datetime.date(2017, 7, 23)], [datetime.date(2017, 7, 24), datetime.date(2017, 7, 25), datetime.date(2017, 7, 26), datetime.date(2017, 7, 27), datetime.date(2017, 7, 28), datetime.date(2017, 7, 29), datetime.date(2017, 7, 30)], [datetime.date(2017, 7, 31), datetime.date(2017, 8, 1), datetime.date(2017, 8, 2), datetime.date(2017, 8, 3), datetime.date(2017, 8, 4), datetime.date(2017, 8, 5), datetime.date(2017, 8, 6)]]
      month 2 : [[datetime.date(2017, 7, 31), datetime.date(2017, 8, 1), datetime.date(2017, 8, 2), datetime.date(2017, 8, 3), datetime.date(2017, 8, 4), datetime.date(2017, 8, 5), datetime.date(2017, 8, 6)], [datetime.date(2017, 8, 7), datetime.date(2017, 8, 8), datetime.date(2017, 8, 9), datetime.date(2017, 8, 10), datetime.date(2017, 8, 11), datetime.date(2017, 8, 12), datetime.date(2017, 8, 13)], [datetime.date(2017, 8, 14), datetime.date(2017, 8, 15), datetime.date(2017, 8, 16), datetime.date(2017, 8, 17), datetime.date(2017, 8, 18), datetime.date(2017, 8, 19), datetime.date(2017, 8, 20)], [datetime.date(2017, 8, 21), datetime.date(2017, 8, 22), datetime.date(2017, 8, 23), datetime.date(2017, 8, 24), datetime.date(2017, 8, 25), datetime.date(2017, 8, 26), datetime.date(2017, 8, 27)], [datetime.date(2017, 8, 28), datetime.date(2017, 8, 29), datetime.date(2017, 8, 30), datetime.date(2017, 8, 31), datetime.date(2017, 9, 1), datetime.date(2017, 9, 2), datetime.date(2017, 9, 3)]]
      month 3 : [[datetime.date(2017, 8, 28), datetime.date(2017, 8, 29), datetime.date(2017, 8, 30), datetime.date(2017, 8, 31), datetime.date(2017, 9, 1), datetime.date(2017, 9, 2), datetime.date(2017, 9, 3)], [datetime.date(2017, 9, 4), datetime.date(2017, 9, 5), datetime.date(2017, 9, 6), datetime.date(2017, 9, 7), datetime.date(2017, 9, 8), datetime.date(2017, 9, 9), datetime.date(2017, 9, 10)], [datetime.date(2017, 9, 11), datetime.date(2017, 9, 12), datetime.date(2017, 9, 13), datetime.date(2017, 9, 14), datetime.date(2017, 9, 15), datetime.date(2017, 9, 16), datetime.date(2017, 9, 17)], [datetime.date(2017, 9, 18), datetime.date(2017, 9, 19), datetime.date(2017, 9, 20), datetime.date(2017, 9, 21), datetime.date(2017, 9, 22), datetime.date(2017, 9, 23), datetime.date(2017, 9, 24)], [datetime.date(2017, 9, 25), datetime.date(2017, 9, 26), datetime.date(2017, 9, 27), datetime.date(2017, 9, 28), datetime.date(2017, 9, 29), datetime.date(2017, 9, 30), datetime.date(2017, 10, 1)]]
     row 4 :
      month 1 : [[datetime.date(2017, 9, 25), datetime.date(2017, 9, 26), datetime.date(2017, 9, 27), datetime.date(2017, 9, 28), datetime.date(2017, 9, 29), datetime.date(2017, 9, 30), datetime.date(2017, 10, 1)], [datetime.date(2017, 10, 2), datetime.date(2017, 10, 3), datetime.date(2017, 10, 4), datetime.date(2017, 10, 5), datetime.date(2017, 10, 6), datetime.date(2017, 10, 7), datetime.date(2017, 10, 8)], [datetime.date(2017, 10, 9), datetime.date(2017, 10, 10), datetime.date(2017, 10, 11), datetime.date(2017, 10, 12), datetime.date(2017, 10, 13), datetime.date(2017, 10, 14), datetime.date(2017, 10, 15)], [datetime.date(2017, 10, 16), datetime.date(2017, 10, 17), datetime.date(2017, 10, 18), datetime.date(2017, 10, 19), datetime.date(2017, 10, 20), datetime.date(2017, 10, 21), datetime.date(2017, 10, 22)], [datetime.date(2017, 10, 23), datetime.date(2017, 10, 24), datetime.date(2017, 10, 25), datetime.date(2017, 10, 26), datetime.date(2017, 10, 27), datetime.date(2017, 10, 28), datetime.date(2017, 10, 29)], [datetime.date(2017, 10, 30), datetime.date(2017, 10, 31), datetime.date(2017, 11, 1), datetime.date(2017, 11, 2), datetime.date(2017, 11, 3), datetime.date(2017, 11, 4), datetime.date(2017, 11, 5)]]
      month 2 : [[datetime.date(2017, 10, 30), datetime.date(2017, 10, 31), datetime.date(2017, 11, 1), datetime.date(2017, 11, 2), datetime.date(2017, 11, 3), datetime.date(2017, 11, 4), datetime.date(2017, 11, 5)], [datetime.date(2017, 11, 6), datetime.date(2017, 11, 7), datetime.date(2017, 11, 8), datetime.date(2017, 11, 9), datetime.date(2017, 11, 10), datetime.date(2017, 11, 11), datetime.date(2017, 11, 12)], [datetime.date(2017, 11, 13), datetime.date(2017, 11, 14), datetime.date(2017, 11, 15), datetime.date(2017, 11, 16), datetime.date(2017, 11, 17), datetime.date(2017, 11, 18), datetime.date(2017, 11, 19)], [datetime.date(2017, 11, 20), datetime.date(2017, 11, 21), datetime.date(2017, 11, 22), datetime.date(2017, 11, 23), datetime.date(2017, 11, 24), datetime.date(2017, 11, 25), datetime.date(2017, 11, 26)], [datetime.date(2017, 11, 27), datetime.date(2017, 11, 28), datetime.date(2017, 11, 29), datetime.date(2017, 11, 30), datetime.date(2017, 12, 1), datetime.date(2017, 12, 2), datetime.date(2017, 12, 3)]]
      month 3 : [[datetime.date(2017, 11, 27), datetime.date(2017, 11, 28), datetime.date(2017, 11, 29), datetime.date(2017, 11, 30), datetime.date(2017, 12, 1), datetime.date(2017, 12, 2), datetime.date(2017, 12, 3)], [datetime.date(2017, 12, 4), datetime.date(2017, 12, 5), datetime.date(2017, 12, 6), datetime.date(2017, 12, 7), datetime.date(2017, 12, 8), datetime.date(2017, 12, 9), datetime.date(2017, 12, 10)], [datetime.date(2017, 12, 11), datetime.date(2017, 12, 12), datetime.date(2017, 12, 13), datetime.date(2017, 12, 14), datetime.date(2017, 12, 15), datetime.date(2017, 12, 16), datetime.date(2017, 12, 17)], [datetime.date(2017, 12, 18), datetime.date(2017, 12, 19), datetime.date(2017, 12, 20), datetime.date(2017, 12, 21), datetime.date(2017, 12, 22), datetime.date(2017, 12, 23), datetime.date(2017, 12, 24)], [datetime.date(2017, 12, 25), datetime.date(2017, 12, 26), datetime.date(2017, 12, 27), datetime.date(2017, 12, 28), datetime.date(2017, 12, 29), datetime.date(2017, 12, 30), datetime.date(2017, 12, 31)]]


# calendar 模块级函数


```python
import calendar

# 返回周标题头，参数值表示显示的周几的字符限制
# 例如，n=1 时，周一为 M, n=2 为 Mo, n=3 时为 Mon
print '\nweekheader(2):'
print calendar.weekheader(2)
print '\nweekheader(3):'
print calendar.weekheader(3)

# 本地化的周几名字列表
print '\nday_name:'
print list(calendar.day_name)
# 本地化的周几的缩写名字列表
print '\nday_abbr:'
print list(calendar.day_abbr)

# 本地化的月名列表
print '\nmonth_name:'
print list(calendar.month_name)
# 本地化的月缩写名列表
print '\nmonth_abbr:'
print list(calendar.month_abbr)
```

    
    weekheader(2):
    Mo Tu We Th Fr Sa Su
    
    weekheader(3):
    Mon Tue Wed Thu Fri Sat Sun
    
    day_name:
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    day_abbr:
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    month_name:
    ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    month_abbr:
    ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']



# 格式化的例子

*prmonth()* (print month) 函数格式化输出某年某月的日历信息。


```python
import calendar

c = calendar.TextCalendar(calendar.MONDAY)
c.prmonth(2017, 6)
```

         June 2017
    Mo Tu We Th Fr Sa Su
              1  2  3  4
     5  6  7  8  9 10 11
    12 13 14 15 16 17 18
    19 20 21 22 23 24 25
    26 27 28 29 30


使用 *HTMLCalendar* 的 *formatmonth()* 可产生一个类似效果的表格（HTML 文本），用 HTML 标签组成，并且每个单元格设置了对应星期几的一个 CSS 类。

# 更多资源

+ [calendar](https://docs.python.org/2/library/calendar.html) The standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/4.3calendar.ipynb) 


# 参考

+ [The Python Standard Library By Example: 4.3 Calendar](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
