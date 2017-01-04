---
title: 数据结构与算法--ADT
date: 2017-01-04
writing-time: 2017-01-04 09:21
categories: Computer&nbsp;Science
tags: Programming 《Data&nbsp;Structures&nbsp;and&nbsp;Algorithms&nbsp;Using&nbsp;Python》 Data&nbsp;Structure Algorithms Python
---

计算机科学的基石是对算法的研究。

算法是为解决某个问题而给出的一组清晰明确的指令步骤序列，并且这些指令能在有限的时间内执行完。

算法的实现是指将指令步骤序列转化成计算机能够执行的计算机程序。而这个转化过程就叫计算机编程。


# 简介

数据项在计算机中以二进制数的序列形式保存。同时计算机能存储和处理不同类似的数据，因此这些看似非常相似的序列都有不同的含义。为区分不同的数据类型，术语 **type** 通常用来指代一个数据集合，而术语 **data type** 指代一种给定的 **type** 以及可作用于该给定 **type** 的数据集合上的一组操作。

编程语言通常都一些一些内置的数据类型，这些内置提供的数据类型即为 **primitives**，它们分为两种：

+ simple data types: 这种数据类型不能再细分成更小的部分，例子有 Integeger 和 real 数据类型。
+ complex data types: 它们由多个 simple data type 或 complex data type 的组件构成，在 Python 中的例子有 object, string, list, dict 等。


## 抽象

计算机科学中有两种常见的抽象：

+ procedural(functiona) abstraction: 过程抽象，指使用一个函数或方法而忽略它的具体是如何实现的。
+ data abstraction: 数据抽象，指数据类型的属性（值和操作方法）与数据类型的具体实现分离。


通常，复杂问题的抽象是分层进行的，更高层级在前一层之上添加更加的抽象。以在计算机上的整数表示及执行算术运算为例：

1. 最低层是硬件层，只有很少的抽象，它用二进制来表示这些值，用逻辑电路来执行这些算术运算，该层由硬件设计师负责实现。
2. 再高一层的抽象通过汇编语言提供，它能操作二进制数据和针对低层硬件的指令，该层由编译器作者和汇编程序员使用，他们将算术运算转化成多条汇编指令。
3. 更高一层由高级编程语言的 primitive data type 实现，如整型。在这一层，我们可以用熟悉的表达式来运算了，如 `x=a+b-5`。

## ADT

ADT (abstract data type) 是由用户定义的数据类型，它指定了一组数据值的集体以及一组可在这些数据值上运行的操作。ADT 的定义与它的具体实现无关，因此我们可以只关注如何使用它，而无需关注它的具体实现。

ADT 可被看作为一个黑盒子。用户程序与 ADT 实例的交互是通过调用定义在 ADT 接口上的操作进行的。这些操作集可分为 4 类：

+ Constructors: 创建和初始化 ADT 的实例
+ Accessors: 返回实例中的数据，而进行修改
+ Mutators: 修改 ADT 实例的内容
+ Iterators: 按序列处理单个数据组件


## 数据结构

ADT 将定义与实现进行了分离。我们自定义的 ADT 必须要有一个实现，而实现 ADT 时我们所做出的选择会影响实现的功能和效率。

数据结构可以通过以下两方面来描述：

1. 它们如何存储和组织单个数据元素
2. 提供哪些操作来存取和处理其上的数据

有很多常用的数据结构，如数组，链表，堆栈，队列，树等。所有的数据结构都会存储一组数据值，但在如何组织单个数据项和提供哪些操作来处理数据集上有区别。实现 ADT 时，需要根据具体问题来选择具体的数据结构。例如，实现打印队列最好选择 queue 数据结构，而 B-Tree 适合数据库索引。


## 常用术语定义

- collection: 集合，指一组数据值，单个数据值之间没有隐含的组织关系。
- container: 容器，指存储和组织一个集合的数据结构或 ADT。集合中的单个数据值称为容器的元素 (**element**)，当容器中没有元素时，称容器为空 (**empty**)。Python 中的容器例子有： string, tuple, list, dict, set。
- sequence: 序列，是一种容器，该容器的元素按线性排列，并且每个元素能通过其位置访问（即通过下标访问）。Python 中的序列例子： string, tuple, list。
- sorted sequence: 有序序列，元素的位置基于每个元素的前后元素的某种预定关系确定的。


# Date  ADT

一个 *date* 表示公历 (proleptic Gregorian calendar) 中的一天。公历中的每一天为 西元前 4713 年的 12 月 24 日。

ADT 定义的操作有：

+ Date(year, month, day): 创建一个 Date 实例并初始化成公历中的一天。西元前 1 年及之前的日期中的年部分用负数表示。
+ year(): 返回该公历日期的年。
+ month(): 返回该公历日期的月。
+ day(): 返回该公历日期的日。
+ monthName(): 返回该公历日期的月份名。
+ dayOfWeek(): 返回星期数，值为 [0-6]，0 表示星期一，6 表示星期日。
+ numDays(otherDate): 返回这两个日期间所差距的天数，是一个正整数。
+ isLeapYear(): 布尔值，检测该日期是否在一个闰年中。
+ advanceBy(days): 如果参数是正数，则返回的日期将增加这么多天，如果负数则减少，有必要的话，该日期将近似到西元前 4714 年的 12 月 24 日。
+ comparable(otherDate): 实现逻辑运算，如 &lt;, &lt;=, &gt;, &gt;=, ==, !==。
+ toString(): 返回 `yyyy-mm-dd` 形式的字符串表示。


## 实现 Date

### Date 的表示

一般可以用两种方式来保存对象中的 date 数据:

+ 一种是将 year, month, day 分开单独存储，这种方式，易于存取每个日期部分，但是难于实现日期的比较等操作。
+ 另一种是只用一个整数开保存一个 Julian day，即该日期至西元前 4713 年 12 月 24 日的偏离天数。这种方式易于实现日期间的比较等操作。


以下的实现采用第二种存储方式。

### 构造 Date

将公历日期转化成 Julian day 值的公式为：

```
T = (M - 14) / 12
jday = D - 32075 + (1461 * (Y + 4800 + T) / 4) +
                    (367 * (M - 2 - T * 12) / 12) -
                    (3 * ((Y + 4900 + T) / 100) / 4)
```

### 实现代码

```python
# encoding: utf-8
# Filename: date.py
# Implements a proleptic Gregorian calendar date as a Julian day number.

# Interfaces: 
# + Date(year, month, day): 创建一个 Date 实例并初始化成公历中的一天。西元前 1 年及之前的日期中的年部分用负数表示。
# + year(): 返回该公历日期的年。
# + month(): 返回该公历日期的月。
# + day(): 返回该公历日期的日。
# + monthName(): 返回该公历日期的月份名。
# + dayOfWeek(): 返回星期数，值为 [0-6]，0 表示星期一，6 表示星期日。
# + numDays(otherDate): 返回这两个日期间所差距的天数，是一个正整数。
# + isLeapYear(): 布尔值，检测该日期是否在一个闰年中。
# + advanceBy(days): 如果参数是正数，则返回的日期将增加这么多天，如果负数则减少，有必要的话，该日期将近似到西元前 4714 年的 12 月 24 日。
# + comparable(otherDate): 实现逻辑运算，如 &lt;, &lt;=, &gt;, &gt;=, ==, !==。
# + toString(): 返回 `yyyy-mm-dd` 形式的字符串表示。

class Date:
    # Creates an object instance for the specified Gregorian date.
    def __init__(self, year, month, day):
        self._julianDay = 0
        assert self._isValidGregorian(year, month, day), \
                "Invalid Gregorian date."

        # Gredorian data --> julian day formula:
        # T = (M - 14) / 12
        # jday = D - 32075 + (1461 * (Y + 4800 + T) / 4) +
        #                    (367 * (M - 2 - T * 12) / 12) -
        #                    (3 * ((Y + 4900 + T) / 100) / 4)
        #
        # This first line of the equation, T = (M-14)/12, has to be changed
        # since Python's implementation of integer division is not the same
        # as mathematical definition
        tmp = 0
        if month < 3:
            tmp = -1
        self._julianDay = day - 32075 + \
                (1461 * (year + 4800 + tmp) // 4) + \
                (367 * (month -2 - tmp * 12) // 12) - \
                (3 * ((year + 4900 + tmp) // 100) // 4)

    # 一月（31天），二月（平年28天，闰年29天），三月（31天），
    # 四月（30天），五月（31 天），六月（30天），七月（31天），
    # 八月（31天），九月（30天），十月（31天），十一月（30天），
    # 十二月（31天）。

    def _isValidGregorian(self, year, month, day):
        if month > 12 or month < 1:
            return False

        if day < 1 or day > 31:
            return False

        # months_31_days = [1, 3, 5, 7, 8, 10, 12]
        months_30_days = [4, 6, 9, 11]

        if month in months_30_days and day > 30:
            return False

        if month == 2:
            if self._leapYear(year):
                if day > 29:
                    return False
            if day > 28:
                return False

        return True
    # Extracts the appropriate Gregorian date component.
    def year(self):
        return (self._toGregorian())[0] # returing Y from (Y, M, D)

    def month(self):
        return (self._toGregorian())[1] # returing M from (Y, M, D)

    def day(self):
        return (self._toGregorian())[2] # returing D from (Y, M, D)

    # Returns day of the week as an int between 0 (Mon) and 6 (Sun).
    def dayOfWeek(self):
        year, month, day = self._toGregorian()
        if month < 3:
            month = month + 12
            year = year - 1
        return ((13 * month + 3) // 5 + day + \
                year + year // 4 - year // 100 + year // 400 ) % 7

    # Returns the date as a string in Gregorian format.
    def __str__(self):
        year, month, day = self._toGregorian()
        return "%04d/%02d/%02d" % (year, month, day)

    # Returns the date as a string in Gregorian format.
    def __repr__(self):
        return str(self)

    # Logically compares the two dates.
    def __eq__(self, otherDate):
        return self._julianDay == otherDate._julianDay

    def __lt__(self, otherDate):
        return self._julianDay < otherDate._julianDay

    def __le__(self, otherDate):
        return self._julianDay <= otherDate._julianDay


    # Returns the Gregorian date as a tuple: (year, month, day).
    def _toGregorian(self):
        A = self._julianDay + 68569
        B = 4 * A // 146097
        A = A - (146097 * B + 3) // 4
        year = 4000 * (A + 1) // 1461001
        A = A - (1461 * year // 4) + 31
        month = 80 * A // 2447
        day = A - (2447 * month // 80)
        A = month // 11
        month = month + 2 - (12 * A)
        year = 100 * (B - 49) + year + A
        return year, month, day

    def monthName(self):
        months = ["Jan", "Feb", "Mar", "Apr", "may", "Jun",
                "Jul", "Aug", "Sept", "Oct", "Nov", "Dec",]
        return months[self.month()]

    def _leapYear(self, year):
        if year % 400 == 0 or \
                (year % 4 == 0 and year % 100 != 0):
                return True
        return False

    def isLeapYear(self):
        return self._leapYear(self.year)


    def numDays(self, otherDate):
        if self._julianDay > otherDate._julianDay:
            return self._julianDay - otherDate._julianDay
        else:
            return otherDate._julianDay - self._julianDay

    def advanceBy(self, days):
        self._julianDay += days
        if self._julianDay < 0:
            self._julianDay = 0
```

以上实现中，以 T=(M-14)/12 进行的变换，因为 Python 对整数除法的实现与数学定义不同。根据定义， -11/12 将为 0, 而 Python 中 -11/12.0 将为 -1。


关于逻辑比较运算，从 Python 3 开始，对于一个逻辑运算的相关运算，如 `<` 和 `>`，如果相反的运算没有实现， Python 会自动调换操作数，并调用本运算的实现。因此这里省略了一些逻辑运算的实现。


调用的例子：

```python
# Filename: checkdate.py

# Extracts a collection of birth dates from the user and determines
# if each individual is at least 32 years of age.
from date import Date

def main():
    # Date before which a person must have been born to be 32 or older.
    bornBofore = Date(1984, 5, 2)

    # Extract birth dates from the user and determine if 32 or older
    date = promptAndExtractDate()
    while date is not None:
        if date <= bornBofore:
            print("Is at least 32 years of age: ", date)
        date = promptAndExtractDate()


# Prompts for and extracts the Gregorian date components. Return a
# Date object or None when user has finished entering dates.
def promptAndExtractDate():
    print("Enter a birth date.")
    year = int(input("year (0 to quit): "))
    if year == 0:
        return None
    else:
        month = int(input("month: "))
        day = int(input("day: "))
        return Date(year, month, day)

main()
```

续 ...

> 参考： 

+ [Data Structures and Algorithms Using Python: Abstract Data Types]()
