---
title: 数据结构与算法--Array
date: 2017-01-11
writing-time: 2017-01-11 11:28--2017-01-16 11:31
categories: Computer&nbsp;Science
tags: Programming 《Data&nbsp;Structures&nbsp;and&nbsp;Algorithms&nbsp;Using&nbsp;Python》 Data&nbsp;Structure Algorithms Python
---

# Array ADT

一维数组是连续元素的集合，其中的每个元素都可以通过唯一的整数下标来存取。数组的大小在创建后不能修改。

ADT 定义：

+ Array(size): 创建一个长度为 size 的一维数组，并且将每个元素初始化成 None
+ length(): 返回数组中的元素个数
+ getitem(index): 返回指定下标的元素
+ setitem(index, value): 修改数组中 index 位置的元素值
+ clearing(value): 将数组中的所有元素值重置成 value
+ iterator(): 返回迭代器


# Array 的实现

## ctypes 模块

Python 中的许多数据类型及类实际上都是基于低层 C 语言中的相关类型实现的。Python 标准库中的 **ctypes** 模块可用来访问 C 语言中的各种类型及 C 类库中的功能。使用 **ctypes** 提供的大多数功能都要求理解一些 C 语言知识。

类似 Python 实现 string, list, tuple 和 dict，我们通过 **ctypes** 创建一个数组，其中的元素都是 Python 对象引用：

```python
import ctypes

ArrayType = ctypes.py_object * 5
slots = ArrayType()
```

这个数组必须先初始化后才能访问，不然会抛出异常，如 `slots[0]` 会抛出异常，初始化如下：

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
    for i in range( size ):
        yield elements[i]
```

# Python List

Python List 也是通过低层的 C 语言类型实现的，它是一个可修改的序列容器，其大小可以随着元素的添加和删除自动改变。

## 创建一个 Python List

```python
pyList = [4, 12, 2, 34, 17]
```

以上代码将调用 `list()` 构造器，构造器将创建一个数组结构用来存储列表中的元素。实际上初始创建的数组大小会大于所需的容量，这样便于以后的扩展操作。

用于存储列表元素的数组实际上是刚才创建的数组中的一个子数组 *subarray*。`len(lst)` 返回该子数组的长度，而整个数组的长度为 `capacity`。 用数组实现的 Python List 的抽象和物理视图如下：

![用数组实现的 Python List 的抽象和禅理视图](/assets/images/datastructsusingpython/listUsingArrayView.png)

## 追加元素 append

当数组容量足够时，新元素将追加到数组中，并且 list 的 `length` 域也相应增加。

当数组満时，List 会进行自动扩展，即：

1. 新建一个更大容量的数组
2. 将原数组的元素全部复制到新建的数组
3. 将新建的数组设置为 List 的数据结构
4. 销毁旧的数组

新建数组的大小是根据原数组的大小确定的，比如说，新数组的大小定为原数组大小的 2 倍 。 扩展后再在数组后追加元素。

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


下面的实现采用了数组的数组方法，将二维数组中的每一行存储在一维数组中，然后再创建一个数组，用来保存行数组（即该数组是数组的数组）。Array2D 的抽象和物理存储视图如下：


![Array2D 的抽象和物理存储视图](/assets/images/datastructsusingpython/array2dView.png)

有些语言的实现中，可以存取每个行，从而对每个元素的访问使用 `x[r][c]` 进行。为了隐藏实现细节，我们的实现不暴露行数组，从而对每个元素的访问使用 `x[r,c]` 进行。

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

矩阵是标量值的集合，这些值以行和列的形式组织成一个固定大小的矩形网格中。

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

实现如下：

```python
from array import Array2D

class Matrix:
    def __init__( self, nrow, ncols ):
        self._theGrid = Array2D( nrow, ncols )
        self._theGrid.clear( 0 )

    def numRows( self ):
        return self._theGrid.numRows()

    def numCols( self ):
        return self._theGrid.numCols()

    def __getitem__( self, xy ):
        return self._theGrid[ xy[0], xy[1] ]

    def __setitem__( self, xy, scalar ):
        self._theGrid[ xy[0], xy[1] ] = scalar

    def scaleBy( self, scalar ):
        for r in xrange( self.numRows() ):
            for c in xrange( self.numCols() ):
                self[r, c] *= scalar

    def transpose( self ):
        newMatrix = Matrix( self.numCols(), self.numRows() )
        for r in xrange( self.numRows() ):
            for c in xrange( self.numCols() ):
                newMatrix[c, r] = self[r, c]
        return newMatrix

    def add( self, rhsMatrix ):
        assert rhsMatrix.numRows() == self.numRows() and \
            rhsMatrix.numCols() == self.numCols(), \
            "Matrix sizes not compatible for the add operation."

        newMatrix = Matrix( self.numRows(), self.numCols() )
        for r in xrange( self.numRows() ):
            for c in xrange( self.numCols() ):
                newMatrix[r, c] = self[r, c] + rhsMatrix[r, c]

        return newMatrix

    def subtract( self, rhsMatrix ):
        assert rhsMatrix.numRows() == self.numRows() and \
            rhsMatrix.numCols() == self.numCols(), \
            "Matrix sizes not compatible for the add operation."

        newMatrix = Matrix( self.numRows(), self.numCols() )
        for r in xrange( self.numRows() ):
            for c in xrange( self.numCols() ):
                newMatrix[r, c] = self[r, c] - rhsMatrix[r, c]

        return newMatrix

    def multiple( self, rhsMatrix ):
        assert self.numCols() == rhsMatrix.numRows(), \
            "Matrix sizes not compatible for the multiple operation."

        newMatrix = Matrix( self.numRows(), rhsMatrix.numCols() )

        for r in xrange( self.numRows() ):
            for rhsC in xrange ( rhsMatrix.numCols() ):
                tmp = 0
                for c in xrange( self.numCols() ):
                    tmp += self[r, c] * rhsMatrix[c, r]
                newMatrix[r, rhsC] = tmp

        return newMatrix
```

# 应用： 游戏人生

*The game of Life* 是由英国数学家 John H. Conway 发明的，它能模拟生物群落的兴衰更替。该游戏可用来观察一个复杂的系统或模式如何能从一组简单的规则演化而来。

## 游戏规则

该游戏使用一个不限大小的矩形网格，其中的每个单元格要么是空的，要么被一个有机体占据。被占据的单元格被视作是活的，而空的单元格被视作是死的。游戏的每次演进，都会基于当前的单元格布局，创造新的“一代”。下一代中的每个单元格状态是根据以下规则确定的：

1. 若某单元格是活的，并且有 2 或 3 个活的邻居，那么它在下一代也保持活。每个单元格有 8 个邻居。
2. 若某单元格是活的，但它没有活的邻居，或只有一个活邻居，它在下一代会死于孤立。
3. 一个活单元格，若有 4 个或更多个活邻居，它在下一代会死于人口过剩。
4. 一个死单元格，当且仅当只有 3 个活邻居时，会在下一代重生。


用户先初始化配置，即指定哪些单元格是活的，然后运用以上的规则，生成下一代。可以看到，一些系统可能最终会消亡，而有些最终会进化成 “稳定” 状态。例如：

![游戏人员稳定状态1](/assets/images/datastructsusingpython/gamelife_stable1.png)

![游戏人员稳定状态2](/assets/images/datastructsusingpython/gamelife_stable2.png)


## 设计方案

一个网格 *life grid* 用来表示和存储游戏区。网格包含一组矩形单元格，并分成有限大小的行和列。

+ LifeGrid(nrows, ncols): 创建一个新的游戏网格。所有单元格设置为空（死）。
+ numRows(): 返回网格行数。
+ numCols(): 返回网格列数。
+ configure(coordList): 配置网格以进行下一代的演化。参数是一个 (row, col) 的序列，每一个元组表示该位置的单元格是活的。
+ clearCell(row, col): 设置单元格为空（死）。
+ setCell(row, col): 设置单元格为活。
+ isLiveCell(row, col): 返回一个布尔值，表示某个单元格是否包含一个活的有机体。
+ numLiveNeighbors(row, col): 返回某个单元格的所有活邻居个数。对于边缘的单元格，落在边缘外的邻居都认为是死的。


## 实现

使用一个二维数组来表示网格。每个单元格的状态使用 0 和 1 表示，0 表示死，1 表示活。这样在统计单元格的活邻居总数时，只需要将邻居的状态相加即可。实现时网格的大小是限定的，如果大小超出了，在运行过程中可以重新创建一个新的网格。


```python
# life.py
from array import Array2D

class LifeGrid:
    DEAD_CELL = 0
    LIVE_CELL = 1

    def __init__( self, nrows, ncols ):
        self._grid = Array2D( nrows, ncols )
        self.configure( list() )

    def numRows( self ):
        return self._grid.numRows()

    def numCols( self ):
        return self._grid.numCols()

    def configure( self, coordList ):
        for i in range( self.numRows() ):
            for j in range( self.numCols() ):
                self.clearCell(i, j)

        for coord in coordList:
            self.setCell( coord[0], coord[1] )

    def isLiveCell( self, row, col ):
        return self._grid[ row, col ] == LifeGrid.LIVE_CELL

    def clearCell( self, row, col ):
        self._grid[ row, col ] = LifeGrid.DEAD_CELL

    def setCell( self, row, col ):
        self._grid[ row, col ] = LifeGrid.LIVE_CELL

    def numLiveNeighbors( self, row, col ):
        nrows = self.numRows()
        ncols = self.numCols()

        liveNum = 0
        for i in range( row-1, row+2 ):
            for j in range( col-1, col+2 ):
               if ( 0 <= i < nrows ) and ( 0 <= j < ncols ):
                   liveNum += self._grid[i, j]
        liveNum -= self._grid[ row, col ]

        return liveNum
```

```python
from life import LifeGrid

# Define the initial configuration of live cells.
INIT_CONFIG = [ (0, 0), (0, 1), (1, 0), (1, 2), (3, 2), (3, 4), (5, 4), (5, 6), (7, 6), (7, 8), (9, 8), (9, 10), (11, 10), (11, 12), (12, 11), (12, 12)]

# Indicate the number of generations
#NUM_GENS = 8

def main():
    GRID_WIDTH = int( raw_input( "Grid width:" ) )
    GRID_HEIGHT = int( raw_input( "Grid height:" ) )
    NUM_GENS = int( raw_input( "Nbr of generations to evolve:" ) )
    grid = LifeGrid( GRID_WIDTH, GRID_HEIGHT )
    grid.configure( INIT_CONFIG )

    # Play the game.
    draw( grid )
    for i in range( NUM_GENS ):
        evolve( grid )
        draw( grid )

def evolve( grid ):
    liveCells = list()

    for i in range( grid.numRows() ):
        for j in range( grid.numCols() ):
            neighbors = grid.numLiveNeighbors( i, j )

            # 1. If a cell is alive and has either two or three live neighbors, the cell remains alive in the next generation. 
            # The neighbors are the eight cells immediately surrounding a cell: vertically, horizontally, and diagonally.  
            # 2. A living cell that has no live neighbors or a single live neighbor dies from isolation in the next generation.
            # 3. A living cell that has four or more live neighbors dies from overpopulation in the next generation.
            # 4. A dead cell with exactly three live neighbors results in a birth and becomes alive in the next generation.
            # All other dead cells remain dead in the next generation.

            if (neighbors == 2 and grid.isLiveCell( i, j )) or \
                (neighbors == 3):
                    liveCells.append( (i, j) )

    grid.configure( liveCells )

def draw( grid ):
    print
    for i in range( grid.numRows() ):
        for j in range( grid.numCols() ):
            if grid.isLiveCell( i, j):
                print '@',
            else:
                print '.',
        print

main()
```

> 参考： 

+ [Data Structures and Algorithms Using Python: Arrays](https://www.amazon.com/Data-Structures-Algorithms-Using-Python/dp/0470618299/)
