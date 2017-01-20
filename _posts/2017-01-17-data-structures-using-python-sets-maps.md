---
title: 数据结构与算法--Set 和 Map
date: 2017-01-17
writing-time: 2017-01-17 15:01
categories: Computer&nbsp;Science
tags: Programming 《Data&nbsp;Structures&nbsp;and&nbsp;Algorithms&nbsp;Using&nbsp;Python》 Data&nbsp;Structure Algorithms Python Set Map
---

# Set

和数学中的概念一样，集内的值是唯一的。

## Set ADT

+ Set(): 创建一个空集。
+ length(): 返回集中的元素个数。
+ contains(element): 判断某元素是否在集中。
+ add(element): 将元素加入集中，如果该元素已存在，即省略本操作。
+ remove(element): 从集中删除元素，元素不存在则抛出异常。
+ equals(setB): 判断两元素是否相等。
+ isSubsetOf(setB): 判断本集是否是集 setB 的一个子集。
+ union(setB): 返回两个集合的合集。
+ intersect(setB): 返回两个集合的交集。
+ difference(setB): 返回两个集合的相异集，即返回所有存在本集中，但不在 setB 中的元素。
+ iterator(): 返回一个迭代器用来遍历集合中的元素。 


## 基于 List 的实现

```python
# Implementation of the Set ADT container using a Python list.
class Set:
    def __init__(self, *initElements):
        self._theElements = list()

        if initElements:
            for e in initElements:
                self.add(e)

    def __len__(self):
        return len(self._theElements)

    def __contains__(self, item):
        return item in self._theElements

    def add(self, item):
        if item not in self._theElements:
            self._theElements.append(item)

    def remove(self, item):
        assert item in self, "The element must be in the set."
        self._theElements.remove(item)

    def __eq__(self, setB):
        if len(self) != len( setB ):
            return False
        else:
            return self.isSubsetOf(setB)

    def isSubsetOf(self, setB):
        for i in self._theElements:
            if i not in setB._theElements:
                return False
        return True

    def isProperSubset(self, setB):
        if len(self) >= len( setB ):
            return False
        return self.isSubsetOf(setB)

    def union(self, setB):
        newSet = Set()
        newSet._theElements.extend(self._theElements)
        for i in setB._theElements:
            if i not in self:
                newSet._theElements.append(i)

        return newSet

    def intersect(self, setB):
        newSet = Set()
        for i in self._theElements:
            if i in setB:
                newSet._theElements.append(i)

        return newSet

    def difference(self, setB):
        newSet = Set()
        for i in self._theElements:
            if i not in setB:
                newSet._theElements.append(i)

        return newSet

    __add__ = union
    __mul__ = intersect
    __sub__ = difference
    __lt__ = isSubsetOf

    def __str__(self):
        print '(',
        for e in self._theElements:
            print e, ',',
        print ')',

    def __iter__(self):
        return _SetGenerator(self._theElements)

def _SetGenerator(elements):
    for i in elements:
        yield i


if __name__ == '__main__':
    smith = Set()
    smith.add("CSCI-112")
    smith.add("MATH-121")
    smith.add("HIST-340")
    smith.add("ECON-101")

    roberts = Set()
    roberts.add("POL-101")
    roberts.add("ANTH-230")
    roberts.add("CSCI-112")
    roberts.add("ECON-101")

    if smith == roberts :
        print("Smith and Roberts are taking the same courses.")
    else :
        sameCourses = smith.intersect(roberts)
    if len(sameCourses) == 0:
        print("Smith and Roberts are not taking any of "\
            + "the same courses.")
    else :
        print("Smith and Roberts are taking some of the "\
            + "same courses:")
        for course in sameCourses :
            print(course),
```

# Map

映射是存储数据记录集的一个容器，存储的每条记录都与一个唯一 key 关联。

## Map ADT

+ Map(): 创建一个空映射。
+ length(): 返回映像中的 key/value 对个数。
+ contains(key): 判断该 key 是否在映射中
+ add(key, value); 若该键值对未存在于映射中，添加; 若已存在即更新该 key 对应的值;添加后返回 True，更新后返回 False。
+ remove(key): 删除键值对，不存在时抛出异常。
+ valueOf(key): 返回该 key 关联的数据记录。
+ iterator(): 返回迭代器用于遍历映射中的键。

## 基于 List 的实现

两种实现方法：
    1. 分别用一个 List 存储 key，另一个 List 存储 value，并维护这两个 List 的关联性。
    2. 只用一个 List 来存储 key/value 对。

下面的实现代码使用了 方法 2：


```python
# Implementation of Map ADT using a single list.
class _MapEntry:
    def __init__(self, key, val):
        self.key = key
        self.value = val

class Map:
    def __init__(self):
        self._entryList = list()

    def __len__(self):
        return len(self._entryList)

    # Helper method used to find the index position of a category. If the
    # key is not found, None is returned.
    def _findPosition(self, key):
        for e, ndx in enumerate(self._entryList):
            if e.key == key:
                return ndx
        return None

    def __contains__(self, key):
        ndx = self._findPosition(key)
        return ndx is not None

    # Adds a new entry to the map if the key does exist. Otherwise, the
    # new value replaces the current value associated with the key.
    def add(self, key, val):
        ndx = self._findPosition(self, key)
        if ndx is not None:
            self._entryList[ndx].value = val
            return False
        else:
            self._entryList.append(_MapEntry( key, val) )
            return True

    def valueOf(self, key):
        ndx = self._findPosition(self, key)
        assert ndx is not None, "Invalid map key."
        return self._entryList[ndx].value

    def remove(self, key):
        ndx = self._findPosition(self, key)
        assert ndx is not None, "Invalid map key."
        self._entryList.pop(ndx)

    def keyArray(self):
        keys = list()
        for e in self._entryList:
            keys.append(e.key
        return keys

    def __iter__(self):
        return _MapGenerator(self._entryList)

    __setitem__ = add
    __getitem__ = valueOf

def _MapGenerator(entryList):
    for e in entryList:
        yield e
```


# 多维数组

二维数组可视为包含行和列的表格，三维数组可视为表格的堆栈。


## MultiArray ADT

多维数组是多维元素的集合。每个元素通过指定多维的下标来引用。

+ MultiArray(d1, d2, ...dn): 创建一个 n 维的数组。数组的每个维度必须大于 0。d1 是最高维的维度，而 dn 是最低维的维度。
+ dims(): 返回维数。
+ length(dim): 返回指定维的数组长度。每个维从 1 开始编号，1 表示第一维或最高维。例如，在 3 维数组中，1 表示表格的堆栈的维， 2 指表格的行，3 指列。
+ clear(value): 设置数组中的每个元素值。
+ getitem(i1, i2, ...in): 返回元素值。如 y = x[1, 2]
+ setitem(i1, i2, ...in, value): 设置元素值。如 x[1, 2] = y


## 数据的组织

### 一维数组

硬件层一般都提供对一维数组的管理。一维数组的元素都保存在一段连续的内存空间中，每个元素的索引就是该元素到数组首元素的偏移量。

大多数语言中，也是使用一维数组和操作和管理多维数组的。

### 二维数组

二维数组一般被视为表格，表格又分为行和列。有两种存储方法：

1. 行优先存储（大多数语言采用）： 每行按序存储，即首行的所有元素存储在一维数组的最前面，第 2 以后面行的所有元素接下去存储。
2. 列优先存储（如 FORTRAN）： 每列按序存储，即首列的所有元素存储在一维数组的最前面，第 2 以后面列的所有元素接下去存储。

### 多维数组

以和二给数组类似的方式进行处理。以三维数组为例，它的每个 “表” 可以用行优先或列优先的方式连续存储。当维数增加时，只需将每一维实例中的所有元素都连续存储在该维下一个实例前即可。例如，对于四维数组来说，它可被视作 box(三维数组) 的一个数组，每个 box 内的所有元素都连续存储在下一个 box 前即可。

## 索引的计算（以行优先存储）

### 大小为 m X n 的二维数组

index(i,j) = i*n + j

### 大小为 d1 X d2 X d3 的三维数组

index(i,j,k) = i*(d2*d3) + j*d3 + k











> 参考： 

+ [Data Structures and Algorithms Using Python: Sets and Maps](https://www.amazon.com/Data-Structures-Algorithms-Using-Python/dp/0470618299/)
