---
title: Python 2 标准库示例：1.1 String-文本常量和模板
date: 2017-05-22
writing-time: 2017-05-22 14:42
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python string
---

# Python 2 标准库示例: 1.1 String-文本常量和模板

Python 2.0 之前，通常使用 *string* 模块中的函数来处理文本（已过时），没有使用 *string* 对象的方法。

Python 2.4 及之后的程序可能会使用 *string.Template* 来参数化字符串，即将动态数值插入到文本中。

*textwrap* 模块中的工具用于格式化文本段，如限制文本宽度，添加缩进，插入换行以实现折行功能等。

*string* 对象支持内置的相等和排序比较操作，除此之外，标准库中还包含 2 个与文本值比较相关的模块。*re* 是一个完整的正则表达式库，用 C 实现。它适于在大数据集中进行子串查询和模式匹配。

*difflib* 模块能计算出两个文本序列间的实际不同处，如新增、删除、修改等各部分。我们可以利用 *difflib* 中的比较函数的输出，来反映文本随时间的修改情况。

## string--文本常量和模板 

**目的**: 包含用于处理文本的常量和类。
**Python 版本**: 1.4+

自 2.0 开始，之前在 *string* 模块中实现的函数都迁移到了 *str* 和 *unicode* 对象中，作为方法呈现。*string* 模块的相应函数已经过时，会到 Python 3.0 时删除。

*string* 模块中还保留一些有用的常量和类，用于处理 *string* 和 *unicode* 对象。

###  函数

*capwords()* 和 *maketrans()* 这两个函数没有从 *string* 中移除。

*capwords()* 函数将字符串中每个字的首字母大写。


```python
import string

s = 'The quick brown fox jumped over the lazy dog.'

print s
print string.capwords(s)
```

    The quick brown fox jumped over the lazy dog.
    The Quick Brown Fox Jumped Over The Lazy Dog.


其作用等于：先调用 *split()*，再将每个字的首字母变大写，然后调用 *join()* 组合回文本。

*maketrans()* 函数会先创建一个转换表，然后 *translate()* 方法会通过查询该转换表，将一个字符转换成另一个字符。这种方式比多次调用 *replace()* 便捷。


```python
import string

leet = string.maketrans('abegiloprstz', '463611092572')

s = 'The quick brown fox jumped over the lazy dog.'

print s
print s.translate(leet)
```

    The quick brown fox jumped over the lazy dog.
    Th3 qu1ck 620wn f0x jum93d 0v32 7h3 142y d06.


上面例子中，e->3, i->1,b->6,...

###  模板

文本模板在 Python 2.4 (PEP 292) 时引入。使用 *string.Template* 时，变量标识前加 \$，如 \$var，必要时，也可加 {}，以与周围文本区分，如 \${var}。


```python
import string

values = {'var': 'foo'}

t = string.Template("""
Variable: $var
Escape: $$
Variable in text: ${var}iable
""")

print 'TEMPLATE:', t.substitute(values)

s = """
Variable: %(var)s
Escape: %%
Variable in text: %(var)ssiable
"""

print 'INTERPOLATION: ', s % values
```

    TEMPLATE: 
    Variable: foo
    Escape: $
    Variable in text: fooiable
    
    INTERPOLATION:  
    Variable: foo
    Escape: %
    Variable in text: foosiable



上面的例子中，触发字符(`$` 和 `%`) 都通过重复两次实现转义。

模板和字符串标准修改间的一个关键不同是：模板的参数不考虑类型，它们的值都会预先转化成字符串后，再插入结果中。并且没有格式化选项，比如无法控制浮点数值的小数表示个数。

但是，模板的一个好处是，使用 *safe_substitute()* 方法时，如果没有为模板提供足够的参数值，也不会抛出异常，缺少值的变量表达式会在结果中原样保留。


```python
import string

values = {'var': 'foo'}

t = string.Template("$var is here but $missing is not provided")

try:
    print 'substitute(): ', t.substitute(values)
except KeyError, err:
    print 'ERROR:', str(err)

print 'safe_substitute(): ', t.safe_substitute(values)
```

    substitute():  ERROR: 'missing'
    safe_substitute():  foo is here but $missing is not provided


### 1.1.3  高级模板

*string.Template* 类通过正则表达式来查找变量名，因此可以通过修改类属性 *delimiter* 和 *idpattern* 来修改。


```python
import string

class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'

values = {'with_underscore': 'replaced',
         'notunderscored': 'not replaced',
         }

t = MyTemplate('''
    Delimiter: %%
    Replaced: %with_underscore
    Ignored: %notunderscored
    ''')

print 'Modified ID pattern:'
print t.safe_substitute(values)
```

    Modified ID pattern:
    
        Delimiter: %
        Replaced: replaced
        Ignored: %notunderscored



上例中，模板的分隔符修改为了 %, 变量名通过 idpattern 限制为了必须包含有下划线字符。

对于更复杂的情况，可以重载 *pattern* 类属性实现。提供的 *pattern* 这个正则表达式必须包含 4 个命名组，来匹配获取：转义的分隔符，命名变量，带花括号版本的变量名，及任何无效的分隔符模式。


```python
import string

t = string.Template('$var')
print t.pattern.pattern
```

    
        \$(?:
          (?P<escaped>\$) |   # Escape sequence of two delimiters
          (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
          {(?P<braced>[_a-z][_a-z0-9]*)}   |   # delimiter and a braced identifier
          (?P<invalid>)              # Other ill-formed delimiter exprs
        )



*t.pattern* 是已编译版本的正则表达式，源字符串版本是 *t.pattern.pattern*。

下面的例子中定义了一个新的 *pattern*，以使用 *\{\{var\}\}* 这种变量语法。


```python
{% raw %}
import re
import string

class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
      (?P<escaped>\{\{)|
      (?P<named>[_a-z][_a-z0-9]*)\}\}|
      (?P<braced>[_a-z][_a-z0-9]*)\}\}|
      (?P<invalid>)
    )
    '''

t = MyTemplate('''
{{{{
{{var}}
''')

print 'MATCHES:', t.pattern.findall(t.template)
print 'SUBSTITUTED:', t.safe_substitute(var='replacement')
{% endraw %}
```

{% raw %}
    MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
    SUBSTITUTED: 
    {{
    replacement
{% endraw %}



# 更多资源

+ [string 标准库文档](https://docs.python.org/2.7/library/string.html?highlight=string#module-string)
+ [PEP 292](www.python.org/dev/peps/pep-0292)
+ [1337](https://en.wikipedia.org/wiki/Leet), "Leetspeak"，另一种字母表
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/1.1string.ipynb)

# 参考

+ [The Python Standard Library By Example: 1.1 String-Text Constants and Templates](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
