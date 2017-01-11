---
title: 数据结构与算法--Array
date: 2017-01-11
writing-time: 2017-01-11 11:28
categories: Computer&nbsp;Science
tags: Programming 《Data&nbsp;Structures&nbsp;and&nbsp;Algorithms&nbsp;Using&nbsp;Python》 Data&nbsp;Structure Algorithms Python
---

# Array ADT

一维数组是连续元素的集合，其中的每个元素都可以通过唯一的整数下标来存取。数组的大小在创建后不能修改。

ADT 定义：

+ Array(size): 创建一个长度为 size 的一组数组，并且将每个元素初始化成 None
+ length(): 返回数组中的元素个数
+ getitem(index): 返回指定下标中的元素
+ setitem(index, value): 修改数组中 index 位置的元素值
+ clearing(value): 将数组中的所有元素值重置成 value
+ iterator(): 返回迭代器


# Array 的实现

## ctypes 模块

Python 中的许多数据类型和类实际上是用低层 C 语言中的相关类型实现的。Python 标准库中的 **ctypes** 模块可用来访问 C 语言中的各种类型及 C 类库中的功能。使用 **ctypes** 提供的大多数功能都要求理解一些 C 语言知识。

类似 Python 实现 string, list, tuple 和 dict，我们通过 **ctypes** 创建一个数组，其中的元素都是 Python 对象引用：

```python
import ctypes

ArrayType = ctypes.py_object * 5
slots = ArrayType()
```

这个数组必须先初始化后才能访问，不然访问元素，如 `slots[0]` 会抛出异常，初始化如下：

```python
for i in range(5):
    slots[i] = None
```

Array 的实现如下：

```python
import ctypes

class Array:
    def __init__( self, size ):
        assert size > 0, "Array size must be > 0"
        self._size = size
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        self.clear( None )

    def __len__( self ):
        return self._size

    def __getitem__( self, index ):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements[ index ]

    def __setitem__( self, index, val ):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        self._elements[ index ] = val

    def clear( self, val ):
        for i in xrange( self._size ):
            self._elements[ i ] = val

    def __iter__( self ):
        return _ArrayGenerator( self._elements, self._size )

def _ArrayGenerator( elements, size ):
    for i in xrange( size ):
        yield elements[i]
```

# Python List

Python List 也是通过低层的 C 语言类型实现的，它是一个可修改的序列容器，其大小可以随着元素的添加和删除自动改变。

## 创建一个 Python List

```python
pyList = [4, 12, 2, 34, 17]
```

以上代码将调用 `list()` 构造器，构造器将创建一个数组结构用来存储列表中的元素。实际上初始创建的数组大小会大于所需的容量，这样便于以后的扩展操作。因此，用于存储列表元素的数组实际上是刚才创建的数组中的一个子数组 *subarray*。`len(lst)` 返回该子数组的长度，而整个数组的长度为 `capacity`。 用数组实现的 Python List 的抽象和物理视图如下：

![用数组实现的 Python List 的抽象和禅理视图](/assets/images/datastructsusingpython/listUsingArrayView.png)

## 追加元素 append

当数组容量足够时，新元素将追加到数组中，并且 list 的 `length` 域也相应增加。

当数组満时，List 会进行自动扩展，即：

1. 新建一个更大容量的数组
2. 将原数组的元素全部复制到新建的数组
3. 将新建的数组设置为 List 的数据结构
4. 销毁旧的数组

新建数组的大小是根据原数组的大小确定的，比如说，新数组的大小定为原数组的大小的 2 倍 。 扩展后再在数组后追加元素。

## 扩充列表 extend

比如：

```python
pyListA = [34, 12]
pyListB = [4, 6, 31, 9]
pyListA.extend(pyListB)
```

当 pyListA 中的数组容量不够时，List 会自动进行如 append 进行的类似数组扩展操作。

## 插入 insert

比如：

```python
pyList.insert(3, 79)
```

当位置 3 已经有元素时，位置 3 及其后面的所有元素都将后移一个位置，并在位置 3 插入新元素。当数组容器不够，会进行和上面相似的数组扩展操作。

## 删除 pop

比如：

```python
pyList.pop(0) # remove the first item
pyList.pop() # remove the last item
```

删除后，如果后面还有元素，那么被删除元素后面的所有元素将前移一个位置，以便填充删除后的空位。

当然，如果删除后的数组空位过多，也会进行相对应的收缩数组操作。


## List Slice

Slice 会创建一个新的 List。


# 二维数组 two-dimensional array

它将数据组织成行和列，类似于表格。每个元素通过两个下标来存取。


## Array2D ADT

+ Array2D(nrows, ncols): 创建一个 nrows 行，ncols 列的二维数组，并初始化每个元素为 None
+ numRows(): 返回行数
+ numCols(): 返回列数
+ clear(value): 将所有元素的值设为 value
+ getitem(row, col): 通过下标法 `y=x[1,2]` 来访问元素
+ setitem(row, col, value): 设置元素值


## Array2D 的实现

通常有 2 种数据组织方法：

+ 使用一个一维数组，将行列上的每个元素位置映射到数组的相应位置
+ 使用数组的数组实现


下面的实现采用了数组的数组方法，将二维数组中的每一行存储在它自己的一维数组中，然后再创建一个数组，进来保存行（即该数组是数组的数组）。Array2D 的抽象和物理存储视图如下：


![Array2D 的抽象和物理存储视图](/assets/images/datastructsusingpython/array2dView.png)

有些语言的实现中，可以存取每个行，从而对每个元素的访问使用 `x[r][c]` 进行。为了隐藏实现现在，我们的实现不暴露行数组，从而对每个元素的访问使用 `x[r,c]` 进行。

实现如下：

```python
class Array2D:
    def __init__( self, nrows, ncols ):
        # Create a 1-D array to store an array reference for each row.
        self._theRows = Array( nrows )

        # Create the 1-D arrays for each row of the 2-D array.
        for i in range( nrows ):
            self._theRows[i] = Array( ncols )

    def numRows( self ):
        return len( self._theRows )

    def numCols( self ):
        return len( self._theRows[0] )

    # Clears the array by setting every element to the given value.
    def clear( self, val ):
        for row in range( self.numRows() ):
            self._theRows[row].clear( val )

    def __getitem__( self, xy ):
        assert len( xy ) == 2, "Invalid number of array subscripts."
        row = xy[0]
        col = xy[1]
        assert row >= 0 and row < self.numRows() and \
            col >= 0 and col < self.numCols(), "Array subscript out of range."
        the1arr = self._theRows[row]
        return the1arr[col]

    def __setitem__( self, xy, val ):
        assert len( xy ) == 2, "Invalid number of array subscripts."
        row = xy[0]
        col = xy[1]
        assert row >= 0 and row < self.numRows() and \
            col >= 0 and col < self.numCols(), "Array subscript out of range."
        the1arr = self._theRows[row]
        the1arr[col] = val
```

### 实现元素的存取

`__getitem__(self, index)` 和 `__setitem__(self, index. value)` 这两个函数定义参数中， 只有一个 index 参数，但这不会限制只能使用一个下标。当使用多个下标时，如 `y = x[i,j]`，多个下标会组合成一个 tuple 作为 index 参数传入。


# Matrix ADT

矩阵是标量值的集合，这些值以行和列的形式组织成一个固定大小的矩形网格。

+ Matrix(nrows, ncols): 创建一个 nrows 行和 ncols 列的矩阵
+ numRows(): 返回行数
+ numCols(): 返回列数
+ getitem(row, col): 返回元素
+ setitem(row, col, scalar): 设置元素值
+ scaleBy(scalar): 矩阵中的每个元素都乘该值，操作后矩阵本身将被修改
+ transpose(): 返回一个转置矩阵
+ add(rhsMatrix): 创建并返回一个新矩阵。这两个矩阵大小必须相同
+ subtract(rhsMatrix): 相减
+ multiply(rhsMatrix): 相乘。


## Matrix 的实现

一般用二维数组来实现矩阵。














> 参考： 

+ [Data Structures and Algorithms Using Python: Arrays](https://www.amazon.com/Data-Structures-Algorithms-Using-Python/dp/0470618299/)
