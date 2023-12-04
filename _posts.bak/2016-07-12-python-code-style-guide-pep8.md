---
title: Python 代码风格指南 PEP8 摘要
date: 2016-07-12
writing-time: 2016-07-08 14:57--2016-12 13:10
categories: programming
tags: python programming
---

# 一、代码布局

## 缩进
每层缩进使用 4 个空格

### 断行风格

1. 断行首字母与括号开启符垂直对齐

```
# 这是正确的例子：
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

2. 悬挂缩进，首行不能有参数; 后面还有其它代码部分时，断行要添加一层缩进，使其与其它代码部分能区别开来

```
# 这是正确的例子，额外添加了一层缩进：
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

```
# 这是错误的例子，悬挂缩进，后面还有其它代码时，需要添加一层额外的缩进加以区别：
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

```
# 这是正确的例子，悬挂缩进方式应该有一层缩进
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

```
# 这是错误的例子，悬挂方式首行不能有参数：
foo = long_function_name(var_one, var_two,
    var_three, var_four)
```

### if 条件断行

`if (` 刚好有 4 个字条，相当于一层缩进。

对于 if 条件断行，以下几种风格都可以：

1. 没有额外的缩进

```
if (this_is_one_thing and
    that_is_another_thing):
    do_something()
```

2. 添加注释加以区分

```
# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
if (this_is_one_thing and
    that_is_another_thing):
    # Since both conditions are true, we can frobnicate.
    do_something()
```

3. 添加额外的缩进加以区分

```
# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```

### 多行的括号

1. 括号结束符与最后行的首字符对齐，如：

```
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]

result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```

2. 括号结束符与首行的首字符对齐, 如：

```
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```


## Tab 符还是空格

用空格

## 每行最长长度

1. 所有行都不超过 80 个字符：
    * 限制编辑器窗口的宽度，使能并排同时打开多个文件。
    * 设置编辑器宽度（ set width to 80），来避免 wrapping

2. 对于较少结构限制的长文本（如 docstring 或注释），行长应限制为 72 个字符。

3. 如果团队成员都同意使用长行，则可以将行长增加到不超过 100 个字符，但是 docstring 和注释还必须为 72 个字符。

4. 有括号的长行可以用 implicit continuation 来断行，其它的可以用 `\` 来断行，如：

```
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

## 操作符要和操作数在一起

```
# 推荐的正确的风格，这样很容易将操作符与操作数匹配：
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

```
# 这种风格现成已不推荐使用了：
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```


## 空行分隔

1. 模块中最顶层的函数和类定义都要用两行空行分隔
2. 类中的方法定义用单行分隔
3. 要把一组相关的函数分组，可以用一些额外的空行
4. 函数中的逻辑区块可以加空行来分隔


## 源文件的编码

1. Python 核心库文件的编码都必须用 UTF-8（Python 2 是 ASCII)。
2. 使用默认的编码时（Python 3: UTF-8，Python 2: ASCII)，不能使用编码声明
3. 标准库中，只有测试、作者名才能使用非默认的编码，其它情况下的非 ASCII 字符用 \\x, \\u, \\u, \\N 表示法表示。

## Import

1. 每行 import 只导入一个包：

```
# 正确:
import os
import sys
```

```
# 错误：
import sys, os
```

```
# 正确：同一包中的内容可以在同一行导入
from subprocess import Popen, PIPE
```

2. **import** 语句要在文件的前面，在模块注释及 docstring 之后，在模块全局变量和常数定义之前。

3. **import** 分组及导入顺序，每个分组之间用一行空行分隔
    1). 标准库
    2). 相关第三方库
    3). 本地应用/库的特殊导入

4. 推荐使用绝对导入，如：

```
import mypkg.sibling
from mypkg import sibling
from mypkg.sibling import example
```

5. 在复杂的包布局中，也可以用显式的相对导入，如：

```
from . import sibling
from .sibling import example
```

6. 从一个模块中导入一个类时，要显示拼写出类名，如：

```
from myclass import MyClass
from foo.bar.yourclass import YourClass
```

如果与本地名称冲突，可以先导入模块：

```
import myclass
import foo.bar.yourclass
```

然后使用：`"myclass.MyClass"` 和 `"foo.bar.yourclass.YourClass"`。

7. 应该避免使用 `from <module> import *`


## 模块级的特殊名称（如__all__)的位置：

必须在模块的 docstring 或注释之后，但在任何的 **import** 语句之前。`from __future__` 比较特殊，Python 强制该语句必须在 docstring 或注释之后，因此风格如下：

```
"""This is the example module.

This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

# 字符引号

1. 单引号和双引号的功能是等同的。
2. 对于多行字符串，应该用双引号字符形式的三引号"""，以便与 PEP257 中的 docstring 规范兼容

# 表达式和语句中的空格

1. `()`、`[]`、`{}` 等括号内不要有多余的空格，如：

```
# 正确：
spam(ham[1], {eggs: 2})
```

```
# 错误：
spam( ham[ 1 ], { eggs: 2 } )
```

2. `,`、`;`、`:` 之前不要有空格，如：

```
# 正确：
if x == 4: print x, y; x, y = y, x
```

```
# 错误：
if x == 4 : print x , y ; x , y = y , x
```

3. 在 slice 语句中的 `:`实际上是一个二元操作符，因此其两侧的空格数必须相同; 但当无 slice 参数时，两侧的空格可以都省略，如：

```
# 以下是正确的风格：
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
ham[lower + offset : upper + offset]
```

```
# 以下是错误的风格：
ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : upper]
ham[ : upper]
```

4. 函数调用的 `()` 及索引的 `[]` 前不要加空格，如：

```
# 正确风格：
spam(1)
dct['key'] = lst[index]
```

```
# 错误风格：
spam (1)
dct ['key'] = lst [index]
```

5. 不要在赋值语句中加入额外的空格来对齐，如：

```
# 正确的风格：
x = 1
y = 2
long_variable = 3
```

```
# 错误的风格:
x             = 1
y             = 2
long_variable = 3
```


## 其它推荐风格

1. 任何行的行尾都不要有空白符。
2. 在二元操作符两侧一般都要加一个空格，一般的二元操作符如：
    * 赋值: `=`, `+=`, `-=`
    * 比较：`==`, `<`, `>`, `!=`, `<>`, `<=`, `>=`, `in`, `not in`, `is`, `is not`
    * 布尔操作： `and`, `or`, `not`
3. 在分优先级的表达式中，在最低优先级的操作符两侧加一个空格，但至多只能加一个空格，如：

```
# 正确的风格：
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)
```

```
# 错误的风格：
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```

4. 在关键字参数和默认参数值中的 `=` 两侧不要加空格，如：

```
# 正确的风格：
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```

```
错误的风格：
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

5. 函数注解中的 `:` 前不要加空格，这符合 `:` 的常规风格，但是 `->` 两侧要加空格，如：

```
# 正确的风格：
def munge(input: AnyStr): ...
def munge() -> AnyStr: ...
```

```
# 错误的风格：
def munge(input:AnyStr): ...
def munge()->PosInt: ...
```

6. 参数注解中，如果注解的参数有默认值，指定默认值的 `=` 两侧要加空格，如：

```
# 正确的风格：
def munge(sep: AnyStr = None): ...
def munge(input: AnyStr, sep: AnyStr = None, limit=1000): ...
```

```
# 错误的风格：
def munge(input: AnyStr=None): ...
def munge(input: AnyStr, limit = 1000): ...
```

7. 不要将多条语句组合在一行中，如：

```
# 正确的风格：
if foo == 'blah':
    do_blah_thing()
do_one()
do_two()
do_three()
```

```
# 错误风格：
if foo == 'blah': do_blah_thing()
do_one(); do_two(); do_three()
```

```
# 如果 if/for/while 体很小，组合在一行有时还是可以接受的，
# 但是不推荐，如：
if foo == 'blah': do_blah_thing()
for x in lst: total += x
while t < 10: t = delay()
```

```
# 但是在有多段语句时，绝对不能这样，如：
if foo == 'blah': do_blah_thing()
else: do_non_blah_thing()

try: something()
finally: cleanup()

do_one(); do_two(); do_three(long, argument,
                             list, like, this)

if foo == 'blah': one(); two(); three()
```

# 注释

1. 注释内容必须要和代码同步！
2. 注释应该是完整的语句，首字母一般大写，一般要有句号。
3. 注释很短时句号可以省略。
4. 块注释一般由多个段落组成。
5. You should use two spaces after a sentence-ending period??
6. 用英文写注释

## 块注释
1. 每行用 `#` 及一个空格开始，如 `# `
2. 段落用一个只有 `#` 的行分隔

## 行内注释
注释与语句内容至少用两个空格分开，注释用 `#` 加一个空格开始

```
# 不要像下面这样，注释内容没有必要
x = x + 1                 # Increment x
```

```
# 但是有时，如下面的注释会很有用
x = x + 1                 # Compensate for border
```

## 文档字符串

1. 公开的模块、函数、类及方法都应该有文档字符串，而非公开的方法可以用注释来代替，且注释放置在 `def` 行之后。
2. 多行的文档字符串，结束符要自成一行，如：

```
"""Return a foobang

Optional plotz says to frobnicate the bizbaz first.
"""
```

3. 单行的文档字符串，结束符和内容放在同一行

# 命名

1. 没有推荐的风格，但是别人要能从你的代码中看出你用的是什么风格，常用的风格如下：

* b 单个小写字母

* B 单个大写字母

* lowercase

* lower_case_with_underscores

* UPPERCASE

* UPPER_CASE_WITH_UNDERSCORES

* CapitalizedWords, 这种风格中，对于缩写词应全部用大写，如 `HTTTPServerError` 比 `HttpServerError` 好

* mixedCase

* Capitalized_Words_With_Underscores，这个太丑，不要用这种！

* `st_mode`、`st_mtime` 等前缀，一般是系统接口返回，如果自己写的代码不推荐用这种

* _single_leading_underscore : 弱 “内部使用” 指示器，这种对象用 `from M import *` 不会被导入 

* single_trailing_underscore_ : 可以用来和 Python 关键词进行区分，如 `Tkinter.Toplevel(master, class_='ClassName')`

* __double_leading_underscore : 命名一个类属性时，可以进行命名矫正，例如 `class FooBar` 内的 `__boo` 会变成 `_FooBar__boo`

* __double_leading_and_trailing_underscore__ : "magic" 对象，不要自己发明这种对象


## 命名传统
1. 不用单个 `l`, `O`, `I` 等这样的单个字符来命名，它们与数字不好区分
2. 包名和模块名：全部用小写，必要时可用 `_`，但不推荐，C/C++ 的扩展模块，如果其对应有 Python 版本，那么 C/C++ 扩展模块名前加 `_`
3. 类名：用 `CapWords` 风格
4. 异常名：用 `CapWords` 风格，一般应该有 `Error` 后缀
5. 全局变量名：能用 `from M import *` 导入的变量全部放在 `__all__` 中，或者全局变量用 `_` 做前缀
6. 函数名：应该用全部用小写，单词间可以用 `_` 分隔，如 `my_func`，不推荐用 `mixedCase` 风格
7. 函数和方法的参数：实例方法的第一个参数用 `self`, 类方法的第一个参数用 `cls`，如果参数与关键字冲突，在参数名后加 `_` 后缀，如 `class_`
8. 实例变量和方法： 用小写字符和 `_`, 非公开的实例变量和方法用一个 `_` 做前缀; 避免与子类中的名字冲突，类的变量可用两个 `_` 作前缀，例如 `class FooBar` 内的 `__boo` 会变成只能通过 `FooBar._FooBar__boo` 访问
9. 常数：全部大写，可用 `_` 分隔，如 `MAX_OVERFLOW`、`TOTAL`

# 推荐的编程方式

1. 字符串连接不要用 `a += b` 或者 `a = a + b`, 用 `''.join()`, 后者性能更好。
2. 和单子如 None 的比较用 `is` 和 `is not`，不要用 `==`，如果你想判断 `if x is not None`, 不要缩写成 `if x`
3. 使用 `if foo is not None`，而不是 `if not foo is None`，前者更加易读
4. 如果要实现序列比较操作的话，应将 6 个操作（`__eq__ , __ne__ , __lt__ , __le__ , __gt__ , __ge__`）全部实现，可以借助 `functools.total_ordering()` 修饰器来减少工作量
5. 将函数保存在一个变量中应该用 `def f(x): return 2*x`， 而非 `f = lambda x: 2*x`，后者不利于调试
6. 自定义的异常类应该继承至 `Exception` 类，而非 `BaseException` 类。
7. Python 2 中抛出异常用 `raise ValueError('message')`，而非 `raise ValueRoor, 'message'`
8. 尽可以的指明异常名，如：

```
try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None
```

避免使用无异常名的 `except:` 语句，它会捕获全部的异常（如 Ctrl C）。
9. 将异常绑定到名字的方法：

```
try:
    process_data()
except Exception as exc:
    raise DataProcessingFailedError(str(exc))
```

10. `try:` 中的语句要尽量减少，如：

```
# 正确的写法：
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

```
# 错误的写法
try:
    # Too broad!
    return handle_value(collection[key])
except KeyError:
    # Will also catch KeyError raised by handle_value()
    return key_not_found(key)
```

11. 如果资源只适用于某个代码段内，使用 `with` 或 `try/finally` 来确保能进行清理工作
12. 上下文管理器应用通过一个单独的函数或方法来激活，如：

```
# 正确的做法：
with conn.begin_transaction():
    do_stuff_in_transaction(conn)
```

```
# 错误的做法：
with conn:
    do_stuff_in_transaction(conn)
```

13. `return` 语句应该一致，如：

```
# 正确的做法：

def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

def bar(x):
    if x < 0:
        return None
    return math.sqrt(x)
```

```
# 错误的做法：

def foo(x):
    if x >= 0:
        return math.sqrt(x)

def bar(x):
    if x < 0:
        return
    return math.sqrt(x)
```

14. 使用字符串的方法，而不是用 string 模块中的方法

15. 使用 `''.startswith()` 和 `''.endswidth()` 而不用 slicing 来检查前缀和后缀：

```
# 正确：
if foo.startswith('bar'):
```

```
# 错误：
if foo[:3] == 'bar':
```

16. 判断对象的类型用 `isinstance` 而不直接 type 比较，如：

```
# 正确：
if isinstance(obj, int):
```

```
# 错误:
if type(obj) is type(1):
```

17. 对序列是否空的判断不用 len，如：

```
# 正确：
if not seq:
if seq:
```

```
# 错误：
if len(seq):
if not len(seq):
```

18. 布尔值的比较：

```
# 正确：
if greeting:
```

```
# 不要这样:
if greeting == True:
```

```
# 这样更不行：
if greeting is True:
```

# 检测工具

使用 [Flake8](https://flake8.readthedocs.io/en/latest/) 来检查代码质量。

> 参考文献： [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)
