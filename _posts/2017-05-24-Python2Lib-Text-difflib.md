---
title: Python 2 标准库示例：1.4 difflib-序列比较
date: 2017-05-24
writing-time: 2017-05-24 16:39
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python difflib
---


**目的**: 比较序列，特别是文本行。

**Python 版本**: 2.1+

*difflib* 模块对比较文非常有用，并包含有支持多种通用差分格式的多个报告生成函数。

本文使用的测试数据如下：


```python
text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor.  In nec mauris eget magna consequat
convallis. Nam sed sem vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
tristique enim. Donec quis lectus a justo imperdiet tempus."""

text1_lines = text1.splitlines()
print 'tex1 lines:', repr(text1_lines)

text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor. In nec mauris eget magna consequat
convallis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a
justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text2_lines = text2.splitlines()
print
print 'text2 lines:', repr(text2_lines)
```

    tex1 lines: ['Lorem ipsum dolor sit amet, consectetuer adipiscing', 'elit. Integer eu lacus accumsan arcu fermentum euismod. Donec', 'pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis', 'pharetra tortor.  In nec mauris eget magna consequat', 'convallis. Nam sed sem vitae odio pellentesque interdum. Sed', 'consequat viverra nisl. Suspendisse arcu metus, blandit quis,', 'rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy', 'molestie orci. Praesent nisi elit, fringilla ac, suscipit non,', 'tristique vel, mauris. Curabitur vel lorem id nisl porta', 'adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate', 'tristique enim. Donec quis lectus a justo imperdiet tempus.']
    
    text2 lines: ['Lorem ipsum dolor sit amet, consectetuer adipiscing', 'elit. Integer eu lacus accumsan arcu fermentum euismod. Donec', 'pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis', 'pharetra tortor. In nec mauris eget magna consequat', 'convallis. Nam cras vitae mi vitae odio pellentesque interdum. Sed', 'consequat viverra nisl. Suspendisse arcu metus, blandit quis,', 'rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy', 'molestie orci. Praesent nisi elit, fringilla ac, suscipit non,', 'tristique vel, mauris. Curabitur vel lorem id nisl porta', 'adipiscing. Duis vulputate tristique enim. Donec quis lectus a', 'justo imperdiet tempus.  Suspendisse eu lectus. In nunc.']


## 文本体的比较

*Differ* 类用于处理文本行序列，并产生可读的差异信息，或者叫修改指令。*Differ* 的默认输出同 UNIX 下的 *diff* 命令的输出类似。它包含有取自两个比较列表中的源值，包含共同部分的值，及表示修改的标识数据。

+ 带 `-` 前缀的行：表示这行出现在第一个序列中，但没有在第二个序列中
+ 带 `+` 前缀的行： 表示这行出现在第二个序列中，但没有在第一个序列中
+ 如果版本间是增量修改，则有额外的带 `?` 的新行来强调修改内容
+ 如果行没有修改，则在最左边另加一个空格，以用于对齐

*Differ.compare()* 的参数是 2 个序列值。


```python
import difflib

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print '\n'.join(diff)
```

      Lorem ipsum dolor sit amet, consectetuer adipiscing
      elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
    - pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
    + pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
    ?         +
    
    - pharetra tortor.  In nec mauris eget magna consequat
    ?                 -
    
    + pharetra tortor. In nec mauris eget magna consequat
    - convallis. Nam sed sem vitae odio pellentesque interdum. Sed
    ?                  - --
    
    + convallis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
    ?                +++ +++++   +
    
      consequat viverra nisl. Suspendisse arcu metus, blandit quis,
      rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
      molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
      tristique vel, mauris. Curabitur vel lorem id nisl porta
    - adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
    - tristique enim. Donec quis lectus a justo imperdiet tempus.
    + adipiscing. Duis vulputate tristique enim. Donec quis lectus a
    + justo imperdiet tempus.  Suspendisse eu lectus. In nunc.


*ndiff()* 方法的输出本质上与 *compare()* 的相同，但它只针对处理文本数据，并且去除了输入中的噪音数据 (noise)。

### 其它输出格式

*Differ* 类会输出所有的输入行，但是 *unified diff* 只会包含有修改的行和一些上下文行，在 Python 2.3+ 中， *unified_diff()* 输出 *unified diff* 格式。


```python
import difflib

diff = difflib.unified_diff(text1_lines,
                           text2_lines,
                           lineterm='',
                           )
print '\n'.join(list(diff))
```

    --- 
    +++ 
    @@ -1,11 +1,11 @@
     Lorem ipsum dolor sit amet, consectetuer adipiscing
     elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
    -pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
    -pharetra tortor.  In nec mauris eget magna consequat
    -convallis. Nam sed sem vitae odio pellentesque interdum. Sed
    +pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
    +pharetra tortor. In nec mauris eget magna consequat
    +convallis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
     consequat viverra nisl. Suspendisse arcu metus, blandit quis,
     rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
     molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
     tristique vel, mauris. Curabitur vel lorem id nisl porta
    -adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
    -tristique enim. Donec quis lectus a justo imperdiet tempus.
    +adipiscing. Duis vulputate tristique enim. Donec quis lectus a
    +justo imperdiet tempus.  Suspendisse eu lectus. In nunc.


上面的 *lineterm* 参数值告诉 *unified_diff()* 不要在返回结果的行中添加换行符，因为输入都没有带换行符。这个输出格式和 SVN 等版本控制工具的输出类似。

使用 *context_diff()* 也可产生类似的可读输出。

## 垃圾（噪音）数据

所有能产生差异序列的函数都接受 2 个参数（值为一个函数），用于判断哪些行是垃圾行，因而需要忽略，判断行中的哪些字符是垃圾是垃圾字符，因而也需要忽略。这些参数一般用来忽略文件中的标签和空白符的修改情况。


```python
# This example is adapted from the source for difflib.py

from difflib import SequenceMatcher

def show_results(s):
    i, j, k = s.find_longest_match(0, 5, 0, 9)
    print ' i = %d' % i
    print ' j = %d' % j
    print ' k = %d' % k
    print ' A[i:i+k] = %r' % A[i:i+k]
    print ' B[j:j+k] = %r' % B[j:j+k]
    
A = " abcd"
B = "abcd abcd"

print 'A = %r' % A
print 'B = %r' % B

print '\nWithout junk detection:'
show_results(SequenceMatcher(None, A, B))

print '\nTreat spaces as junk:'
show_results(SequenceMatcher(lambda x: x==" ", A, B))
```

    A = ' abcd'
    B = 'abcd abcd'
    
    Without junk detection:
     i = 0
     j = 4
     k = 5
     A[i:i+k] = ' abcd'
     B[j:j+k] = ' abcd'
    
    Treat spaces as junk:
     i = 1
     j = 0
     k = 4
     A[i:i+k] = 'abcd'
     B[j:j+k] = 'abcd'


*Differ* 类默认没有显式设置忽略任何行或字符，但它依赖 *SequenceMatcher* 来检测噪音。*ndiff()* 默认忽略空格和制表符。

## 比较任意类型

*SequenceMatcher* 类对两个任意类型的序列进行比较，只需序列值可 *hashable*。它使用的算法能在去除噪音的基础上，识别出最长的连续匹配块。


```python
import difflib

s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]

print 'Initial data:'
print 's1 =', s1
print 's2 =', s2
print 's1 == s2:', s1==s2
print

matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
    if tag == 'delete':
        print 'Remove %s from positions [%d:%d]' % \
            (s1[i1:i2], i1, i2)
        del s1[i1:i2]
    elif tag == 'equal':
        print 's1[%d:%d] and s2[%d:%d] are the same' % \
            (i1, i2, j1, j2)
    elif tag == 'insert':
        print 'Insert %s from s2[%d:%d] into s1 at %d' % \
            (s2[j1:j2], j1, j2, i1)
        s1[i1:i2] = s2[j1:j2]
    elif tag == 'replace':
        print 'Replace %s from s1[%d:%d] with %s from s2[%d:%d]' % (
            s1[i1:i2], i1, i2, s2[j1:j2], j1, j2)
        s1[i1:i2] = s2[j1:j2]
        
    print ' s1 =', s1
print 's1 == s2:', s1==s2
```

     Initial data:
    s1 = [1, 2, 3, 5, 6, 4]
    s2 = [2, 3, 5, 4, 6, 1]
    s1 == s2: False
    
    Replace [4] from s1[5:6] with [1] from s2[5:6]
     s1 = [1, 2, 3, 5, 6, 1]
    s1[4:5] and s2[4:5] are the same
     s1 = [1, 2, 3, 5, 6, 1]
    Insert [4] from s2[3:4] into s1 at 4
     s1 = [1, 2, 3, 5, 4, 6, 1]
    s1[1:4] and s2[0:3] are the same
     s1 = [1, 2, 3, 5, 4, 6, 1]
    Remove [1] from positions [0:1]
     s1 = [2, 3, 5, 4, 6, 1]
    s1 == s2: True


*SequenceMatcher.get_opcodes()* 方法返回将源列出转变成新列表的指令序列。上例中，先将指令序列反序，再执行修改指令，这能确保添加和删除操作上指令中使用到列表索引还能正确引用。

## 更多资源

+ [difflib](https://docs.python.org/3/library/difflib.html) The standard library documentation for this module.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/1.4difflib.ipynb) 

## 参考

+ [The Python Standard Library By Example: 1.4 difflib-Compare Sequences](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
