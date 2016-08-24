---
title: YAML 基础知识
date: 2016-08-24
writing-time: 2016-08-24 12:54
categories: programming
tags: YAML
---

YAML 即 Yet Another Markup Language 的缩写，它是一种数据序列化语言。它的语法参数了 C, Java, Perl, Python, Ruby, RFC0822(MAIL), RFC1866(HTML), RFC2045(MIME), RFC2396(URI), XML, SAX, SOAP 和 JSON 等。

它是 JSON 格式的严格超集，因此里面可以写 JSON 的格式及 Javascript 的一些类型，如 true, null 等。

和 Python 类似，它大量使用换行和缩进来作为语法表示，但与 Python 有所不同的是，YAML 中禁止使用制表符。

```yaml
# YAML 中的注释就像本行这样

################
# 标量类型     #
################

# 我们的根对象（将在整个文档中延续）将是一个映射，
# 它等同于其它语言中的一个字典、哈希对象等。
key: value
another_key: Another value goes here.
a_number_value: 100
# 如果要用数量 1 作为值，需要将它括在引号中。
# 不然 YAML 解析器会假定它是一个布尔值 true。
scientific_notation: 1e+12
boolean: true
null_value: null
key with spaces: value
# 需要注意字符串不要求括在引号中。但是，当然也可以括起来。
however: "A string, enclosed in quotes."
"Keys can be quoted too.": "Useful if you want to put a ':' in your key."

# 多行字符串即可以写成一个 '文字块 literal block' (使用管道符 |),
# 也可以写成一个 '折叠块 folded block' (使用折叠符 >)。
literal_block: |
    This entire block of text will be the value of the 'literal_block' key,
    with line breaks being preserved.

    The literal continues until de-dented, and the leading indentation is
    stripped.

        Any lines that are 'more-indented' keep the rest of their indentation -
        these lines will be indented by 4 spaces.
folded_style: >
    This entire block of text will be the value of 'folded_style', but this
    time, all newlines will be replaced with a single space.

    Blank lines, like above, are converted to a newline character.

        'More-indented' lines keep their newlines, too -
        this text will appear over two lines.

####################
# 集合类型         #
####################

# 嵌套是通过缩进来完成的。
a_nested_map:
    key: value
    another_key: Another Value
    another_nested_map:
        hello: hello

# 映射的键 key 可以不必是字符串。
0.25: a float key

# 键也可以很复杂，比如可以是多行的对象
# 我们使用 ? 后跟一个空格来表示一个复杂键的开始。
? |
    This is a key
    that has multiple lines
: and this is its value

# YAML 中也允许使用复杂键语法来表示序列间的映射关系。
# 但一些语言的解析器可能不支持。
# 一个例子：
? - Manchester United
  - Real Madrid
: [ 2001-01-01, 2002-02-02 ]

# 序列 (等价于列表或数组) 看起来像这样：
a_sequence:
    - Item 1
    - Item 2
    - 0.5 # 序列可以含不同类型。
    - Item 4
    - key: value
      another_key: another_value
    -
        - This is a sequence
        - inside another sequence

# 因为 YAML 是 JSON 的超集，因此也可以写 JSON 风格的映射和序列：
json_map: {"key": "value"}
json_seq: [3, 2, 1, "takeoff"]

#######################
# YAML 的其它功能     #
#######################

# YAML 还有一个方便的特性叫 '锚'，它能让你很容易在文档中实现文本复用。
# 它的语法借鉴了 C 语言中的指针及引用。
# 如下两个键会有相同的值：
anchored_content: &anchor_name This string will appear as the value of two keys.
other_anchor: *anchor_name

# 锚也可被用来复制/继承属性
base: &base
    name: Everyone has same name

foo: &foo
    <<: *base
    age: 10

bar: &bar
    <<: *base
    age: 20

# foo 和 bar 将都含有 name: Everyone has same name

# YAML 还有标签，你可以用它来显示地声明类型。
explicit_string: !!str 0.5
# 一些解析器实现了特定语言的标签，比如 Python 中的复数类型。
python_complex_number: !!python/complex 1+2j

# 我们也可以在 YAML 的复杂键中使用特定语言的标签
? !!python/tuple [5, 7]
: Fifty Seven
# 将会是 Python 中的  {(5, 7): 'Fifty Seven'}

####################
# 其余的 YAML 类型 #
####################

# 除了字符串和数字，YAML 还能理解其它标量。
# ISO 格式的日期和日期时间文本也可以被解析。
datetime: 2001-12-15T02:59:43.1Z
datetime_with_spaces: 2001-12-14 21:59:43.10 -5
date: 2002-12-14

# !!binary 标签表示一个字符串实际上是一个用 base64 编码表示的二进制 blog 对象。
gif_file: !!binary |
    R0lGODlhDAAMAIQAAP//9/X17unp5WZmZgAAAOfn515eXvPz7Y6OjuDg4J+fn5
    OTk6enp56enmlpaWNjY6Ojo4SEhP/++f/++f/++f/++f/++f/++f/++f/++f/+
    +f/++f/++f/++f/++f/++SH+Dk1hZGUgd2l0aCBHSU1QACwAAAAADAAMAAAFLC
    AgjoEwnuNAFOhpEMTRiggcz4BNJHrv/zCFcLiwMWYNG84BwwEeECcgggoBADs=

# YAML 还有一个集合类型，像这样：
set:
    ? item1
    ? item2
    ? item3

# 和 Python 类似, 集合仅是值为 null 的映射;上面的集合等价于：
set2:
    item1: null
    item2: null
    item3: null
```

> 参考文献： 
> [YAML spce 1.2](http://yaml.org/spec/1.2/spec.html) 及 [Learn X in Y minutes](https://learnxinyminutes.com/docs/yaml/)
