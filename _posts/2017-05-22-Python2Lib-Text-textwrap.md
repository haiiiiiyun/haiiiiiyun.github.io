---
title: Python 2 标准库示例：1.2 textwrap-格式化文本段
date: 2017-05-22
writing-time: 2017-05-22 15:47
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python textwrap
---

**目的**: 通过调整段落中的断行符的位置来格式化文本。

**Python 版本**: 2.5+

*textwrap* 模块提供了对段落的折行和填充功能。

## 填充段落

*fill()* 函数以一个文本段作为一个输入，输出一个格式化文本段。


```python
sample_text = '''
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired.  It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    '''

import textwrap

print 'No dedent:\n'
print textwrap.fill(sample_text, width=50)
```

    No dedent:
    
         The textwrap module can be used to format
    text for output in     situations where pretty-
    printing is desired.  It offers     programmatic
    functionality similar to the paragraph wrapping
    or filling features found in many text editors.


上例中，文本段的宽度限制为了 50，并默认进行左对齐。由于没有进行取消缩进操作，原文本中每行行首的缩进字符都会在结果中保留。

## 删除已有的缩进

*dedent()* 函数会删除源文本中各行行首的 **共有** 缩进部分，但会保留多出的缩进符，比如：

```
 Line one.
   Line two.
 Line three.
```

会变成：

```
Line one.
  Line two.
Line three.
```


```python
import textwrap

dedented_text = textwrap.dedent(sample_text)
print 'Dedented:\n'
print dedented_text
```

    Dedented:
    
    
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired.  It offers
    programmatic functionality similar to the paragraph wrapping
    or filling features found in many text editors.
    


## 组合 dedent 和 fill


```python
import textwrap

dedented_text = textwrap.dedent(sample_text).strip()
for width in [45, 70]:
    print '%d Columns:\n' % width
    print textwrap.fill(dedented_text, width=width)
    print
```

    45 Columns:
    
    The textwrap module can be used to format
    text for output in situations where pretty-
    printing is desired.  It offers programmatic
    functionality similar to the paragraph
    wrapping or filling features found in many
    text editors.
    
    70 Columns:
    
    The textwrap module can be used to format text for output in
    situations where pretty-printing is desired.  It offers programmatic
    functionality similar to the paragraph wrapping or filling features
    found in many text editors.
    


## 悬挂式缩进

首行的缩进和其它行的缩进可以独立控制，从而可以实现悬挂式缩进。其中的缩进符也可以是非空白符。


```python
import textwrap

dedented_text = textwrap.dedent(sample_text).strip()
print textwrap.fill(dedented_text,
                   initial_indent='',
                   subsequent_indent=' '*4,
                   width=50,
                   )
```

    The textwrap module can be used to format text for
        output in situations where pretty-printing is
        desired.  It offers programmatic functionality
        similar to the paragraph wrapping or filling
        features found in many text editors.


## 其它资料

+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master    /1.2textwrap.ipynb) 

## 参考

+ [The Python Standard Library By Example: 1.2 textwrap-Formatting Text Paragraphs](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
