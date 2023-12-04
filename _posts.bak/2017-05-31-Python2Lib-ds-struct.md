---
title: Python 2 标准库示例：2.6 struct-二进制数据结构
date: 2017-05-31
writing-time: 2017-05-27 15:10--2017-05-31 11:08
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python Data&nbsp;Sturcture struct
---


**目的**: 字节字符串与二进制数据之间的转换。

**Python 版本**: 1.4+

*struct* 模块实现了 Python 数值与用字节字符串表示的 C struct 数据间的转换。

可以采用 *struct* 模块级的函数进行转换工作，也可以先创建一个 *Struct* 类实例，用其方法进行操作。

存储格式指示串和正则表达式类似，也会进行预编译。


# 打包与解包

*struct* 通过 *pack()* 将 Python 数值打包成字节字符串，用 *unpack()* 将字节中解包回 Python 数值。

下面的例子中，存储格式指示串指明了： 1 个整数，1 个 2 字符的字符串，1 个浮点数。


```python
import struct
import binascii

values = (1, 'ab', 2.7)
s = struct.Struct('I 2s f')
packed_data = s.pack(*values)

print 'Original values:', values
print 'Format string:', s.format
print 'Uses:', s.size, 'bytes' # s.size = struct.calcsize(s.format)
print 'Packed values:', binascii.hexlify(packed_data)
```

    Original values: (1, 'ab', 2.7)
    Format string: I 2s f
    Uses: 12 bytes
    Packed values: 0100000061620000cdcc2c40


使用 *unpack()* 进行解包。


```python
import struct
import binascii

packed_data = binascii.unhexlify('0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print 'Unpacked values:', unpacked_data
```

    Unpacked values: (1, 'ab', 2.700000047683716)


注意到上面 *unpack()* 回来后浮点数值的变化。


# 格式字符串

格式字符串是一种用于指定封包解包数据存储布局的一种机制。它由格式字符组成，而格式字符指定封包解包数据的类型。同时，还包含一些特殊字符，用来控制字节序、大小和对齐。

## 字节序、大小和对齐

C 类型默认使用本机的本地格式和字节序表示，并会使用填充字节来保持对齐。

格式字符串的第 1 个字符可用来表示封包数据的字节序、大小和对齐，和字符的意义如下：

字符 | 字节序              | 大小     | 对齐
-----|
`@`  | native              | native   | native
`=`  | native              | standard | none
`<`  | little-endian       | standard | none
`>`  | big-endian          | standard | none
`!`  | network(big-endian) | standard | none

如果第 1 个字符不是上表中的字符，则默认即为 `@`。

下面是一个例子。


```python
import struct
import binascii

values = (1, 'ab', 2.7)
print 'Original values:', values
endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print
    print 'Format string:', s.format, 'for', name
    print 'Uses:', s.size, 'bytes'
    print 'Packed Value:', binascii.hexlify(packed_data)
    print 'Unpacked Value:', s.unpack(packed_data)
```

    Original values: (1, 'ab', 2.7)
    
    Format string: @ I 2s f for native, native
    Uses: 12 bytes
    Packed Value: 0100000061620000cdcc2c40
    Unpacked Value: (1, 'ab', 2.700000047683716)
    
    Format string: = I 2s f for native, standard
    Uses: 10 bytes
    Packed Value: 010000006162cdcc2c40
    Unpacked Value: (1, 'ab', 2.700000047683716)
    
    Format string: < I 2s f for little-endian
    Uses: 10 bytes
    Packed Value: 010000006162cdcc2c40
    Unpacked Value: (1, 'ab', 2.700000047683716)
    
    Format string: > I 2s f for big-endian
    Uses: 10 bytes
    Packed Value: 000000016162402ccccd
    Unpacked Value: (1, 'ab', 2.700000047683716)
    
    Format string: ! I 2s f for network
    Uses: 10 bytes
    Packed Value: 000000016162402ccccd
    Unpacked Value: (1, 'ab', 2.700000047683716)


## 格式字符

C 与 Python 值之间的转换关系通过格式字符指定。下表中的 **标准大小** 列表示封包数据用标准大小是的字节数（即格式字符串首字符为 `<`, `>`, `!`, `=` 时）。

下面是格式字符表。

格式 | C 类型             | Python 类型       | 标准大小
-----|
x    | 填充字节           | 无值              |
c    | char               | 长度为 1 的字符串 | 1
b    | signed char        | integer           | 1
B    | unsigned char      | integer           | 1
?    | \_Bool             | bool              | 1
h    | short              | integer           | 2
H    | unsigned short     | integer           | 2
i    | int                | integer           | 4
I    | unsigned int       | integer           | 4
l    | long               | integer           | 4
L    | unsigned long      | integer           | 4
q    | long long          | integer           | 8
Q    | unsigned long long | integer           | 8
f    | float              | float             | 4
d    | double             | float             | 8
s    | char[]             | string            |
p    | char[]             | string            |
P    | void *             | integer           |


每个格式字符前都可加表示重复次数的数字（之间不能有空白符），比如 `4h` 表示 `hhhh`。而格式字符间的空白符都会被忽略。

对于 `s` 来说，前面的数字表示字符串的大小，而不像其它格式字符那样表示重复次数。因此 `10s` 表示一个 10 字节的字符串，而 `10c` 表示 10 个字符。


# 缓冲区

二进制封包数据一般用于提高性能，如用于和扩展模块的数据交互。在这些情况下，可为 `Struct` 对象预先分配一个缓冲区来进一步优化。*pack_into()* 和 *unpack_from()* 方法支持对缓冲区操作。


```python
import struct
import binascii

s = struct.Struct('I 2s f')
values = (1, 'ab', 2.7)
print 'Original:', values

print
print 'ctypes string buffer'

import ctypes
b = ctypes.create_string_buffer(s.size)
print 'Before:', binascii.hexlify(b.raw)
s.pack_into(b, 0, *values)
print 'After:', binascii.hexlify(b.raw)
print 'Unpacked:', s.unpack_from(b, 0)

print
print 'array'

import array
a = array.array('c', '\0' * s.size)
print 'Before:', binascii.hexlify(a)
s.pack_into(a, 0, *values)
print 'After:', binascii.hexlify(a)
print 'Unpacked:', s.unpack_from(a, 0)
```

    Original: (1, 'ab', 2.7)
    
    ctypes string buffer
    Before: 000000000000000000000000
    After: 0100000061620000cdcc2c40
    Unpacked: (1, 'ab', 2.700000047683716)
    
    array
    Before: 000000000000000000000000
    After: 0100000061620000cdcc2c40
    Unpacked: (1, 'ab', 2.700000047683716)


# 更多资源

+ [struct](https://docs.python.org/2/library/struct.html) The standard library documentation for this module.
+ [binascii](http://docs.python.org/2/library/binascii.html) The binascii module, for producing ASCII representations of binary data.
+ [Endianness](http://en.wikipedia.org/wiki/Endianness) Wikipedia article that provides an explanation of byte order and endianness in encoding.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/2.6struct.ipynb) 


# 参考

+ [The Python Standard Library By Example: 2.6 Struct-Binary Data Structures](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
