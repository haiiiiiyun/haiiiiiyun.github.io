---
title: Python 2 标准库示例：2.2 array-固定类型的序列
date: 2017-05-27
writing-time: 2017-05-25 21:44--2017-05-27 10:06
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture array
---

**目的**: 高效管理固定类型的数字型数据。

**Python 版本**: 1.4+

*array* 模块中定义了一个类似于 *list* 的序列数据结构，但是它包含的所有成员类型都必须是相同的，且是基本类型，即值为字符值、整数值或浮点数值等。

存储的成员类型在创建 *array* 实例时就需通过 *type code* 指定。支持的 *type code* 及对应的类型如下：

Type code | C 类型             | Python 类型  | 最少字节数 | 备注
----------|
'c'       | char               | character    | 1          |
'b'       | signed char        | int          | 1          |
'B'       | unsigned char      | int          | 1          |
'u'       | PY_UNICODE         | Unicode char | 2          | 即 wchar_t，Py 3.3 中已过时，将在 Py4.0 中删除
'h'       | signed short       | int          | 2          |
'H'       | unsigned short     | int          | 2          |
'i'       | signed int         | int          | 2          |
'I'       | unsigned int       | int          | 2          |
'l'       | signed long        | int          | 4          |
'L'       | unsigned long      | int          | 4          |
'f'       | float              | float        | 4          |
'd'       | double             | float        | 8          |


成员值的具体表示形式由低层的 C 语言实现决定，实际表示的字节个数可通过 *itemsize* 属性获得。


# 初始化

第一个参数通过 *type code* 指定存储的类型，第二个参数可选，是一个可迭代的初始序列。


```python
import array
import binascii

s = 'This is the array.'
a = array.array('c', s)

print 'As string:', s
print 'As array:', a
print 'As hex:', binascii.hexlify(a)
```

    As string: This is the array.
    As array: array('c', 'This is the array.')
    As hex: 54686973206973207468652061727261792e


# 对 array 的操作

操作和普通 Python list 类似。


```python
import array
import pprint

a = array.array('i', xrange(3))
print 'Initial: ', a

a.extend(xrange(3))
print 'Extended:', a

print 'slice:', a[2:5]

print 'Iterator:'
print list(enumerate(a))
```

    Initial:  array('i', [0, 1, 2])
    Extended: array('i', [0, 1, 2, 0, 1, 2])
    slice: array('i', [2, 0, 1])
    Iterator:
    [(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]


# 与文件的操作

*array* 的内容可通过内置方法写入到文件中，或从文件中读出。

下列中先将 *array* 内容写入到文件中，再根据读出的文件内容构建新的 *array*。


```python
import array
import binascii
import tempfile

a = array.array('i', xrange(5))
print 'A1:', a

# Write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile()
a.tofile(output.file) # must pass an *actual* file object
output.flush()

# Read the raw data
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print 'Raw Contents:', binascii.hexlify(raw_data)
    
    # Read the data into a array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print 'A2:', a2
```

    A1: array('i', [0, 1, 2, 3, 4])
    Raw Contents: 0000000001000000020000000300000004000000
    A2: array('i', [0, 1, 2, 3, 4])


# 切换字节序

*array* 的 *byteswap()* 进行字节序切换，它用 C 语言实现。


```python
import array
import binascii

def to_hex(a):
    chars_per_item = a.itemsize * 2 # 2 hex digits
    hex_version = binascii.hexlify(a)
    num_chunks = len(hex_version) / chars_per_item
    for i in xrange(num_chunks):
        start = i*chars_per_item
        end = start + chars_per_item
        yield hex_version[start:end]
        
a1 = array.array('i', xrange(5))
a2 = array.array('i', xrange(5))
a2.byteswap()

fmt = '%10s %10s %10s %10s'
print fmt % ('A1 hex', 'A1', 'A2 hex', 'A2')
print fmt % (('-'*10, ) * 4)
for values in zip(to_hex(a1), a1, to_hex(a2), a2): # zip(seq1, seq2,..) -> [(seq1[0], seq2[0],..), (seq1[1], seq2[1],..),..]
    print fmt % values
```

        A1 hex         A1     A2 hex         A2
    ---------- ---------- ---------- ----------
      00000000          0   00000000          0
      01000000          1   00000001   16777216
      02000000          2   00000002   33554432
      03000000          3   00000003   50331648
      04000000          4   00000004   67108864


# 更多资源

+ array(https://docs.python.org/2.7/library/array.html?highlight=array#module-array) The standard library documentation for this module.
+ [Numerical Python](www.scipy.org) NumPy is a Python library for working with large
data sets efficiently.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.1.collections.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.2 Array-Sequence of Fixed-Type Data](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
