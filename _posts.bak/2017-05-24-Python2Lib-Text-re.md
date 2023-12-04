---
title: Python 2 标准库示例：1.3 re-正则表达式
date: 2017-05-24
writing-time: 2017-05-24 11:09
categories: Programming
tags: Programming 《The&nbsp;Python&nbsp;Standard&nbsp;Library&nbsp;by&nbsp;Example》 Python re regexp
---


**目的**: 通过形式化模式在文本中查询和修改文本。

**Python 版本**: 1.5+

*正则表达式* 是用形式化语法描述的文本匹配模式。模式会被解析为一组指令，这些指令在之后执行时会将一个字符串作为输入，并产出一个匹配子集或一个源字符串的修改版本。

Python 的 *re* 模块使用 Perl 的正则表达式语法，并进行了一些扩展。

## 在文本中查找模式

*search()* 函数接受一个 *pattern* 和一个需在其中查找的文本为输入，当找到匹配模式时，返回 *Match* 对象，未找到时返回 *None*。

每个 *Match* 对象都包含有匹配的信息，如源输入的字符串 *match.string*，使用的正则表达式 *match.re.pattern*，匹配的模式在源输入字符串中的位置等 *match.start(), match.end()*。


```python
import re

pattern = 'this'
text = 'Does this text math the pattern?'

match = re.search(pattern, text)

s = match.start()
e = match.end()

print 'Found "%s"\n in "%s"\n from %d to %d ("%s)' % \
    (match.re.pattern, match.string, s, e, text[s:e])
```

    Found "this"
     in "Does this text math the pattern?"
     from 5 to 9 ("this)


## 编译表达式

*re* 中模块级的函数都需要有一个正则表达式字符串作为输入参数，但是对于常用的表达式，预先将其编译会更高效。*compile()* 函数将正则表达式字符串编译成 *RegexObject*。


```python
import re

# Precompile the patterns
regexes = [re.compile(p)
          for p in ['this', 'that']
          ]
text = 'Does this text match the pattern?'

print 'Text: %r\n' % text

for regex in regexes:
    print 'Seeking "%s" ->' % regex.pattern,
    
    if regex.search(text):
        print 'match!'
    else:
        print 'no match'
```

    Text: 'Does this text match the pattern?'
    
    Seeking "this" -> match!
    Seeking "that" -> no match


模块级的函数为用到的所有正则表达式维护一个预编译版本的缓存，但是缓存大小有限。

直接使用预编译表达式有 2 个优点：

+ 避免了缓存查询的开销
+ 预编译过程发生在模块加载时，因此将编译工作被前推到了应用启动时。

## 多重匹配 

*findall()* 函数返回所有非重叠的匹配子字符串。


```python
import re

text = 'abbaaabbbbaaaaa'

pattern = 'ab'

for matched_substr in re.findall(pattern, text):
    print 'Found "%s"' % matched_substr
```

    Found "ab"
    Found "ab"


*finditer()* 类似 *findall()*，但它返回 *Match* 实例的迭代器。


```python
import re

text = 'abbaaabbbbaaaaa'

pattern = 'ab'

for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print 'Found "%s" at %d:%d' % (text[s:e], s, e)
```

    Found "ab" at 0:2
    Found "ab" at 5:7


## 模式语法


```python
import re

def test_patterns(text, patterns=[]):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    """
    # Look for each pattern in the text and print the results
    for pattern, desc in patterns:
        print 'Pattern %r (%s)\n' % (pattern, desc)
        print '  %r' % text
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = '.' * (s+n_backslashes)
            print '  %s%r' % (prefix, substr)
        print
    return

test_patterns('abbaaabbbbaaaaa',
    [('ab', "'a' followed by 'b'"),
    ])
```

    Pattern 'ab' ('a' followed by 'b')
    
      'abbaaabbbbaaaaa'
      'ab'
      .....'ab'
    


### 重复匹配


```python
test_patterns(
    'abbaabbba',
    [ ('ab*', 'a followed by zero or more b'),
    ('ab+', 'a followed by one or more b'),
    ('ab?', 'a followed by zero or one b'),
    ('ab{3}', 'a followed by three b'),
    ('ab{2,3}', 'a followed by two to three b'),
    ])
```

    Pattern 'ab*' (a followed by zero or more b)
    
      'abbaabbba'
      'abb'
      ...'a'
      ....'abbb'
      ........'a'
    
    Pattern 'ab+' (a followed by one or more b)
    
      'abbaabbba'
      'abb'
      ....'abbb'
    
    Pattern 'ab?' (a followed by zero or one b)
    
      'abbaabbba'
      'ab'
      ...'a'
      ....'ab'
      ........'a'
    
    Pattern 'ab{3}' (a followed by three b)
    
      'abbaabbba'
      ....'abbb'
    
    Pattern 'ab{2,3}' (a followed by two to three b)
    
      'abbaabbba'
      'abb'
      ....'abbb'
    


通常，当处理重复指令时， *re* 会尽可以消耗（匹配使用完）多的输入源。这即所谓的 *贪婪* 行为，它会导致更少的匹配数量，或每个匹配时包含有更多的内容。*贪婪* 行为可以通过在重复指令后加 `?` 来关闭。


```python
test_patterns(
    'abbaabbba',
    [ ('ab*?', 'a followed by zero or more b'),
    ('ab+?', 'a followed by one or more b'),
    ('ab??', 'a followed by zero or one b'),
    ('ab{3}?', 'a followed by three b'),
    ('ab{2,3}?', 'a followed by two to three b'),
    ])
```

    Pattern 'ab*?' (a followed by zero or more b)
    
      'abbaabbba'
      'a'
      ...'a'
      ....'a'
      ........'a'
    
    Pattern 'ab+?' (a followed by one or more b)
    
      'abbaabbba'
      'ab'
      ....'ab'
    
    Pattern 'ab??' (a followed by zero or one b)
    
      'abbaabbba'
      'a'
      ...'a'
      ....'a'
      ........'a'
    
    Pattern 'ab{3}?' (a followed by three b)
    
      'abbaabbba'
      ....'abbb'
    
    Pattern 'ab{2,3}?' (a followed by two to three b)
    
      'abbaabbba'
      'abb'
      ....'abb'
    


### 字符集


```python
test_patterns(
    'abbaabbba',
    [ ('[ab]', 'either a or b'),
        ('a[ab]+', 'a followed by 1 or more a or b'),
        ('a[ab]+?', 'a followed by 1 or more a or b, not greedy'),
    ])
```

    Pattern '[ab]' (either a or b)
    
      'abbaabbba'
      'a'
      .'b'
      ..'b'
      ...'a'
      ....'a'
      .....'b'
      ......'b'
      .......'b'
      ........'a'
    
    Pattern 'a[ab]+' (a followed by 1 or more a or b)
    
      'abbaabbba'
      'abbaabbba'
    
    Pattern 'a[ab]+?' (a followed by 1 or more a or b, not greedy)
    
      'abbaabbba'
      'ab'
      ...'aa'
    


使用 `^` 可以排除字符集中的字符。


```python
test_patterns(
    'This is some text -- with punctuation.',
    [ ('[^-. ]+', 'sequences without -, ., or space'),
    ])
```

    Pattern '[^-. ]+' (sequences without -, ., or space)
    
      'This is some text -- with punctuation.'
      'This'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'
    


使用字符区间。


```python
test_patterns(
    'This is some text -- with punctuation.',
    [ ('[a-z]+', 'sequences of lowercase letters'),
    ('[A-Z]+', 'sequences of uppercase letters'),
    ('[a-zA-Z]+', 'sequences of lowercase or uppercase letters'),
    ('[A-Z][a-z]+', 'one uppercase followed by lowercase'),
    ])
```

    Pattern '[a-z]+' (sequences of lowercase letters)
    
      'This is some text -- with punctuation.'
      .'his'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'
    
    Pattern '[A-Z]+' (sequences of uppercase letters)
    
      'This is some text -- with punctuation.'
      'T'
    
    Pattern '[a-zA-Z]+' (sequences of lowercase or uppercase letters)
    
      'This is some text -- with punctuation.'
      'This'
      .....'is'
      ........'some'
      .............'text'
      .....................'with'
      ..........................'punctuation'
    
    Pattern '[A-Z][a-z]+' (one uppercase followed by lowercase)
    
      'This is some text -- with punctuation.'
      'This'
    


`.` 可匹配任何单个字符。


```python
test_patterns(
    'abbaabbba',
    [ ('a.', 'a followed by any one character'),
    ('b.', 'b followed by any one character'),
    ('a.*b', 'a followed by anything, ending in b'),
    ('a.*?b', 'a followed by anything, ending in b'),
    ])
```

    Pattern 'a.' (a followed by any one character)
    
      'abbaabbba'
      'ab'
      ...'aa'
    
    Pattern 'b.' (b followed by any one character)
    
      'abbaabbba'
      .'bb'
      .....'bb'
      .......'ba'
    
    Pattern 'a.*b' (a followed by anything, ending in b)
    
      'abbaabbba'
      'abbaabbb'
    
    Pattern 'a.*?b' (a followed by anything, ending in b)
    
      'abbaabbba'
      'ab'
      ...'aab'
    


### 转义码

这些都是可被 *re* 模块识别的预定义的字符集。

+ `\d`: 匹配一个数字
+ `\D`: 匹配一个非数字字符
+ `\s`: 匹配一个空白符（tab, 空格，换行等）
+ `\S`: 匹配一个非空白符
+ `\w`: 匹配一个字母或数字
+ `\W`: 匹配一个非字母又非数字的字符


```python
test_patterns(
    'A prime #1 example!',
    [ (r'\d+', 'sequence of digits'),
    (r'\D+', 'sequence of nondigits'),
    (r'\s+', 'sequence of whitespace'),
    (r'\S+', 'sequence of nonwhitespace'),
    (r'\w+', 'alphanumeric characters'),
    (r'\W+', 'nonalphanumeric'),
    ])
```

    Pattern '\\d+' (sequence of digits)
    
      'A prime #1 example!'
      .........'1'
    
    Pattern '\\D+' (sequence of nondigits)
    
      'A prime #1 example!'
      'A prime #'
      ..........' example!'
    
    Pattern '\\s+' (sequence of whitespace)
    
      'A prime #1 example!'
      .' '
      .......' '
      ..........' '
    
    Pattern '\\S+' (sequence of nonwhitespace)
    
      'A prime #1 example!'
      'A'
      ..'prime'
      ........'#1'
      ...........'example!'
    
    Pattern '\\w+' (alphanumeric characters)
    
      'A prime #1 example!'
      'A'
      ..'prime'
      .........'1'
      ...........'example'
    
    Pattern '\\W+' (nonalphanumeric)
    
      'A prime #1 example!'
      .' '
      .......' #'
      ..........' '
      ..................'!'
    


要匹配正则表达式语法中的字符中，要进行转义。


```python
test_patterns(
    r'\d+ \D+ \s+',
    [ (r'\\.\+', 'escape code'),
    ])
```

    Pattern '\\\\.\\+' (escape code)
    
      '\\d+ \\D+ \\s+'
      '\\d+'
      .....'\\D+'
      ..........'\\s+'
    


### 锚点

用来指定匹配项出现的位置。

+ `^`: 行首或字符串首
+ `$`: 行末或字符串末
+ `\A`: 字符串首
+ `\Z`: 字符串末
+ `\b`: 字前或字后的空字符串
+ `\B`: 非字前或字后的空字符串


```python
test_patterns(
    'This is some text -- with punctuation.',
    [ (r'^\w+', 'word at start of string'),
    (r'\A\w+', 'word at start of string'),
    (r'\w+\S*$', 'word near end of string, skip punctuation'),
    (r'\w+\S*\Z', 'word near end of string, skip punctuation'),
    (r'\w*t\w*', 'word containing t'),
    (r'\bt\w+', 't at start of word'),
    (r'\w+t\b', 't at end of word'),
    (r'\Bt\B', 't, not start or end of word'),
    ])
```

    Pattern '^\\w+' (word at start of string)
    
      'This is some text -- with punctuation.'
      'This'
    
    Pattern '\\A\\w+' (word at start of string)
    
      'This is some text -- with punctuation.'
      'This'
    
    Pattern '\\w+\\S*$' (word near end of string, skip punctuation)
    
      'This is some text -- with punctuation.'
      ..........................'punctuation.'
    
    Pattern '\\w+\\S*\\Z' (word near end of string, skip punctuation)
    
      'This is some text -- with punctuation.'
      ..........................'punctuation.'
    
    Pattern '\\w*t\\w*' (word containing t)
    
      'This is some text -- with punctuation.'
      .............'text'
      .....................'with'
      ..........................'punctuation'
    
    Pattern '\\bt\\w+' (t at start of word)
    
      'This is some text -- with punctuation.'
      .............'text'
    
    Pattern '\\w+t\\b' (t at end of word)
    
      'This is some text -- with punctuation.'
      .............'text'
    
    Pattern '\\Bt\\B' (t, not start or end of word)
    
      'This is some text -- with punctuation.'
      .......................'t'
      ..............................'t'
      .................................'t'
    


## 查询限定

*match()* 总是从源字符串的开头开始匹配。


```python
import re

text = 'This is some text -- with punctuation.'
pattern = 'is'

print 'Text :', text
print 'Pattern:', pattern

m = re.match(pattern, text)
print 'Match :', m
s = re.search(pattern, text)
print 'Search :', s
```

    Text : This is some text -- with punctuation.
    Pattern: is
    Match : None
    Search : <_sre.SRE_Match object at 0xb1c5b8e0>


预编译正则表达式对象的 *search()* 方法可接收可选的 *start* 和 *end* 位置参数，用以限定进行查询的源字符串。


```python
import re

text = 'This is some text -- with punctuation.'
pattern = re.compile(r'\b\w*is\w*\b')

print 'Text:', text
print

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()
    print '  %2d : %2d = "%s"' % (s, e-1, text[s:e])
    #Move forward in text for the next search
    pos = e
```

    Text: This is some text -- with punctuation.
    
       0 :  3 = "This"
       5 :  6 = "is"


## 匹配分组

分组 *group* 通过在模式中定义 `()` 实现。任何一个正则表达式都可以作为一个分组嵌套入更大的表达式中。重复修饰符可以作用于分组上。


```python
test_patterns(
    'abbaaabbbbaaaaa',
    [ ('a(ab)', 'a followed by literal ab'),
    ('a(a*b*)', 'a followed by 0-n a and 0-n b'),
    ('a(ab)*', 'a followed by 0-n ab'),
    ('a(ab)+', 'a followed by 1-n ab'),
    ])
```

    Pattern 'a(ab)' (a followed by literal ab)
    
      'abbaaabbbbaaaaa'
      ....'aab'
    
    Pattern 'a(a*b*)' (a followed by 0-n a and 0-n b)
    
      'abbaaabbbbaaaaa'
      'abb'
      ...'aaabbbb'
      ..........'aaaaa'
    
    Pattern 'a(ab)*' (a followed by 0-n ab)
    
      'abbaaabbbbaaaaa'
      'a'
      ...'a'
      ....'aab'
      ..........'a'
      ...........'a'
      ............'a'
      .............'a'
      ..............'a'
    
    Pattern 'a(ab)+' (a followed by 1-n ab)
    
      'abbaaabbbbaaaaa'
      ....'aab'
    


*Match* 对象上的 *groups()* 方法，可用于访问模式中被每个分组匹配的子串，其返回是一个字符串元组，元组中的字符串是模式中分组按顺匹配的字符串。


```python
import re

text = 'This is some text -- with punctuation.'

print text
print

patterns = [
    (r'^(\w+)', 'word at start of string'),
    (r'(\w+)\S*$', 'word at end, with optional punctuation'),
    (r'(\bt\w+)\W+(\w+)', 'word starting with t, another word'),
    (r'(\w+t)\b', 'word ending with t'),
]

for pattern, desc in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print 'Pattern %r (%s)\n' % (pattern, desc)
    print '  ', match.groups()
    print
```

    This is some text -- with punctuation.
    
    Pattern '^(\\w+)' (word at start of string)
    
       ('This',)
    
    Pattern '(\\w+)\\S*$' (word at end, with optional punctuation)
    
       ('punctuation',)
    
    Pattern '(\\bt\\w+)\\W+(\\w+)' (word starting with t, another word)
    
       ('text', 'with')
    
    Pattern '(\\w+t)\\b' (word ending with t)
    
       ('text',)
    


*Match.group()* 可用来获取某个分组的匹配子串，其中 *group(0)* 表示由整个表达式匹配的字符串，而 *group(1)* 等其它调用则返回子分组的匹配字符串。


```python
import re

text = 'This is some text -- with punctuation.'

print 'Input text:', text

#word starting with t, then another word
regex = re.compile(r'(\bt\w+)\W+(\w+)')
print 'Pattern:', regex.pattern

match = regex.search(text)
print 'Entire match:', match.group(0)
print 'Word starting with "t":', match.group(1)
print 'Word after "t" word:', match.group(2)
```

    Input text: This is some text -- with punctuation.
    Pattern: (\bt\w+)\W+(\w+)
    Entire match: text -- with
    Word starting with "t": text
    Word after "t" word: with


Python 扩展了分组语法，添加了 *命名分组 named group*，格式为 `(?P<name>pattern)`。命名分组方便了对命名的引用。这时，可用 *groupdict()* 获取字典形式的分组匹配信息，该字典将分组名映射到了匹配的子串上。


```python
import re

text = 'This is some text -- with punctuation.'

print text
print

for pattern in [r'^(?P<first_word>\w+)',
                r'(?P<last_world>\w+)\S*$',
                r'(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)',
                r'(?P<ends_with_t>\w+t)\b',
                ]:
    regex = re.compile(pattern)
    match = regex.search(text)
    print 'Matching "%s"' % pattern
    print '  ', match.groups()
    print '  ', match.groupdict()
    print
```

    This is some text -- with punctuation.
    
    Matching "^(?P<first_word>\w+)"
       ('This',)
       {'first_word': 'This'}
    
    Matching "(?P<last_world>\w+)\S*$"
       ('punctuation',)
       {'last_world': 'punctuation'}
    
    Matching "(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)"
       ('text', 'with')
       {'other_word': 'with', 't_word': 'text'}
    
    Matching "(?P<ends_with_t>\w+t)\b"
       ('text',)
       {'ends_with_t': 'text'}
    


下面是 *test_patterns()* 的更新版本，添加了命名分组的信息。


```python
import re

def test_patterns(text, patterns=[]):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout.
    """
    # Look for each pattern in the text and print the results
    for pattern, desc in patterns:
        print 'Pattern %r (%s)\n' % (pattern, desc)
        print '  %r' % text
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = ' '*s
            print '  %s%r%s ' % (prefix, text[s:e], ' '*(len(text)-e)),
            print match.groups()
            if match.groupdict():
                print '%s%s' % (' ' * (len(text)-s), match.groupdict())
        print
    return
    
```

由于分组本身是一个正则表达式，因此也可以嵌套入分组。


```python
test_patterns(
    'abbaabbba',
    [ (r'a((a*)(b*))', 'a followed by 0-n a and 0-n b'),
    ])
```

    Pattern 'a((a*)(b*))' (a followed by 0-n a and 0-n b)
    
      'abbaabbba'
      'abb'        ('bb', '', 'bb')
         'aabbb'   ('abbb', 'a', 'bbb')
              'a'  ('', '', '')
    


分组通过 `|` 可用于指定替代模式。


```python
test_patterns(
    'abbaabbba',
    [ (r'a((a+)|(b+))', 'a then seq. of a or seq. of b'),
      (r'a((a|b)+)', 'a then seq. of [ab]'),
    ])
```

    Pattern 'a((a+)|(b+))' (a then seq. of a or seq. of b)
    
      'abbaabbba'
      'abb'        ('bb', None, 'bb')
         'aa'      ('a', 'a', None)
    
    Pattern 'a((a|b)+)' (a then seq. of [ab])
    
      'abbaabbba'
      'abbaabbba'  ('bbaabbba', 'a')
    


上例中可见，当替代分组没有匹配时，*groups()* 的返回的元组中会为其保留为 None 值。

使用 `(?:pattern)` 可定义 *noncapturing* 分组，即该分组的匹配项不会在 *groups()* 调用中返回。


```python
test_patterns(
    'abbaabbba',
    [ (r'a((a+)|(b+))', 'capturing form'),
      (r'a((?:a+)|(?:b+))', 'noncapturing'),
    ])
```

    Pattern 'a((a+)|(b+))' (capturing form)
    
      'abbaabbba'
      'abb'        ('bb', None, 'bb')
         'aa'      ('a', 'a', None)
    
    Pattern 'a((?:a+)|(?:b+))' (noncapturing)
    
      'abbaabbba'
      'abb'        ('bb',)
         'aa'      ('a',)
    


## 查询选项

匹配引擎处理表达式的过程可以通过查询选项来修改，多个选项可以通过位或操作来组合，并传给 *compile()*, *search()* 和 *match()* 等函数。

### 大小写无关匹配 IGNORECASE


```python
import re

text = 'This is some text -- with punctuation.'
pattern = r'\bT\w+'
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print 'Text:\n  %r' % text
print 'Pattern:\n  %s' % pattern
print 'Case-sensitive:'
for match in with_case.findall(text):
    print '  %r' % match
print 'Case-insensitive:'
for match in without_case.findall(text):
    print '  %r' % match
```

    Text:
      'This is some text -- with punctuation.'
    Pattern:
      \bT\w+
    Case-sensitive:
      'This'
    Case-insensitive:
      'This'
      'text'


### 多行输入

*MULTILINE* 选项控制对锚点指令的解析，当开启 *MULTILINE* 模式时，`^` 和 `$` 针对的都是行（以 `\n` 进行分行），未开启时，针对的则是整个字符串。


```python
import re

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print 'Text:\n %r' % text
print 'Pattern:\n %s' % pattern
print 'Single Line:'
for match in single_line.findall(text):
    print '  %r' % (match,)
print 'Multiline:'
for match in multiline.findall(text):
    print '  %r' % (match,)
```

    Text:
     'This is some text -- with punctuation.\nA second line.'
    Pattern:
     (^\w+)|(\w+\S*$)
    Single Line:
      ('This', '')
      ('', 'line.')
    Multiline:
      ('This', '')
      ('', 'punctuation.')
      ('A', '')
      ('', 'line.')


`.` 默认不能匹配换行符，只有当 *DOTALL* 选项开启时才匹配。


```python
import re

text = 'This is some text -- with punctuation.\nA second line.'
pattern = r'.+'
no_newlines  = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print 'Text:\n %r' % text
print 'Pattern:\n %s' % pattern
print 'No newlines:'
for match in no_newlines.findall(text):
    print '  %r' % match
print 'Dotall:'
for match in dotall.findall(text):
    print '  %r' % match
```

    Text:
     'This is some text -- with punctuation.\nA second line.'
    Pattern:
     .+
    No newlines:
      'This is some text -- with punctuation.'
      'A second line.'
    Dotall:
      'This is some text -- with punctuation.\nA second line.'


### Unicode

在 Python 2 中，*str* 对象使用 ASCII，正则表达式处理器默认模式和输入文本都是 ASCII，并且之前定义的转义字符集如 `\w` 等也都是针对 ASCII 的。

要想在 Python 2 中进行 Unicode 匹配，需要使用 *UNICODE* 选项。


```python
import re
import codecs
import sys

# set standard output encoding to UTF-8.
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

text = u'Français złoty Österreich'
pattern = ur'\w+'
ascii_pattern = re.compile(pattern)
unicode_pattern = re.compile(pattern, re.UNICODE)

print 'Text :', text
print 'Pattern :', pattern
print 'ASCII :', u', '.join(ascii_pattern.findall(text))
print 'Unicode :', u', '.join(unicode_pattern.findall(text))
```

    Text : Français złoty Österreich
    Pattern : \w+
    ASCII : Fran, ais, z, oty, sterreich
    Unicode : Français, złoty, Österreich


上例中可看到，未开启 *UNICODE* 选项时，`\w` 不能匹配 Unicode 字符，当开启时，则由正则表达式引擎自行查询 Unicode 数据库，来决定 `\W` 等预定义字符集的包含字符范围。

当然，在 Python 3 时，由于所有的字符串都是 Unicode 的，故不再需要该选项了。


### 冗长表达式语法

冗长模式下，表达式中可以有注释，并忽略每行前后的空白符。

下面的例子中一个用的普通（压缩）模式，一个使用冗长模式，用于验证 *.com, .org, .edu* 三种域名中的电子邮件地址的有效性。


```python
import re

address = re.compile('[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)',
                    re.UNICODE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print '%-30s  %s' % (candidate, 'Matches' if match else 'No match')
```

    first.last@example.com          Matches
    first.last+category@gmail.com   Matches
    valid-address@mail.example.com  Matches
    not-valid@example.foo           No match


下面是对应的冗长模式的例子。


```python
import re

address = re.compile(
    '''
    [\w\d.+-]+    # username
    @
    ([\w\d.]+\.)+ # domain name prefix
    (com|org|edu) # TODO: support more top-level domains
    ''',
    re.UNICODE | re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print '%-30s  %s' % (candidate, 'Matches' if match else 'No match')
```

    first.last@example.com          Matches
    first.last+category@gmail.com   Matches
    valid-address@mail.example.com  Matches
    not-valid@example.foo           No match


下面的版本中加入了命名分组信息。


```python
import re

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
        ([\w.,]+\s+)*[\w.,]+)
        \s*
        # Email addresses are wrapped in angle
        # brackets: < > but only if a name is
        # found, so keep the start bracket in this group.
        <
    )? # the entire name is optional
    
    # The address itself: username@domain.tld
    (?P<email>
        [\w\d.+-]+  # username
        @
        ([\w\d.]+\.)+ # domain name prefix
        (com|org|edu) # limit the allowed top-level domains
    )
    
    >? # optional closing angle bracket
    ''',
    re.UNICODE | re.VERBOSE
)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'First Last',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
    u'<first.last@example.com>',
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Name:', match.groupdict()['name']
        print ' Email:', match.groupdict()['email']
    else:
        print ' No match'
```

    Candidate: first.last@example.com
     Name: None
     Email: first.last@example.com
    Candidate: first.last+category@gmail.com
     Name: None
     Email: first.last+category@gmail.com
    Candidate: valid-address@mail.example.com
     Name: None
     Email: valid-address@mail.example.com
    Candidate: not-valid@example.foo
     No match
    Candidate: First Last <first.last@example.com>
     Name: First Last
     Email: first.last@example.com
    Candidate: No Brackets first.last@example.com
     Name: None
     Email: first.last@example.com
    Candidate: First Last
     No match
    Candidate: First Middle Last <first.last@example.com>
     Name: First Middle Last
     Email: first.last@example.com
    Candidate: First M. Last <first.last@example.com>
     Name: First M. Last
     Email: first.last@example.com
    Candidate: <first.last@example.com>
     Name: None
     Email: first.last@example.com


### 将控制选项嵌入到正则表达式中

控制选项不只能用在 *compile()* 时使用，也可以直接加入到表达式中。由于这些控制选项是作为于整个表达式的，故要放在加在表达式的最前面，如开启大小写无关模式，在表达式前加 `(?i)`。

控制选项常量名与对应的缩写如下：

+ `IGNORECASE`: `i`
+ `MULTILINE`: `m`
+ `DOTALL`: `s`
+ `UNICODE`: `u`
+ `VERBOSE`: `v`

多个选项也可以组合，如 `(?imu)`。

下面是一个例子。


```python
import re

text = 'This is some text -- with punctuation.'
pattern = r'(?i)\bT\w+'
regex = re.compile(pattern)

print 'Text: ', text
print 'Pattern: ', pattern
print 'Matches: ', regex.findall(text)
```

    Text:  This is some text -- with punctuation.
    Pattern:  (?i)\bT\w+
    Matches:  ['This', 'text']


## 向前或向后条件判定

这些判定并不消耗输入源，即判定处理后并不移动输入源的当前位置。向前肯定式判定 *positive look-ahead assertion* 使用 `(?=pattern)`。

下面的例子中，判定电子邮件地址是否包围在平衡的尖括号中，或者没有包围在括号中。


```python
import re

address = re.compile(
    '''
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    ((?P<name>
        ([\w.,]+\s+)*[\w.,]+
     )
     \s+
    ) # name is no longer optional
    
    # LOOKAHEAD
    # Email addresses are wrapped in angle brackets, but only
    # if they are both present or neither is.
    (?=(<.*>$)  # remainder wrapped in angle brackets
        |
        ([^<].*[^>]$)  # remainder *not* wrappped in angle brackets
    )
    
    <? # optional opening angle bracket
    
    # The address itself: username@domain.tld
    (?P<email>
        [\w\d.+-]+  # username
        @
        ([\w\d.]+\.)+  # domain name prefix
        (com|org|edu)  # limit the allowed top-level domains
    )
    
    >? # optioanl closing angle bracket
    ''',
    re.UNICODE | re.VERBOSE
)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Name:', match.groupdict()['name']
        print ' Email:', match.groupdict()['email']
    else:
        print ' No match'
```

    Candidate: First Last <first.last@example.com>
     Name: First Last
     Email: first.last@example.com
    Candidate: No Brackets first.last@example.com
     Name: No Brackets
     Email: first.last@example.com
    Candidate: Open Bracket <first.last@example.com
     No match
    Candidate: Close Bracket first.last@example.com>
     No match


向前否定性判定使用 `(?!pattern)`。下例实现了过滤 noreply 邮件地址。


```python
import re

address = re.compile(
    '''
    ^
    # An address: username@domain.tld
    
    # Ignore noreply address
    (?!noreply@.*$)
    
    [\w\d.+-]+  # username
    @
    ([\w\d.]+\.)+  # domain name prefix
    (com|org|edu)  # limit the allowed top-level domains
    
    $
    ''',
    re.UNICODE | re.VERBOSE
)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com’'
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Match:', candidate[match.start(): match.end()]
    else:
        print ' No match'
```

    Candidate: first.last@example.com
     Match: first.last@example.com
    Candidate: noreply@example.com’
     No match


上例也可以用向后否定式判定实现，使用 `(?<!pattern>)` 语法。


```python
import re

address = re.compile(
    '''
    ^
    # An address: username@domain.tld
    
    [\w\d.+-]+  # username
    
    # Ignore noreply address
    (?<!noreply)
    
    
    @
    ([\w\d.]+\.)+  # domain name prefix
    (com|org|edu)  # limit the allowed top-level domains
    
    $
    ''',
    re.UNICODE | re.VERBOSE
)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com’'
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Match:', candidate[match.start(): match.end()]
    else:
        print ' No match'
```

    Candidate: first.last@example.com
     Match: first.last@example.com
    Candidate: noreply@example.com’
     No match


向后判定和向前判定有些不同，它使用的模式 `pattern` 必须是固定长度的，如果模式中有重复指令，重复数也必须是固定的。

肯定式向后判定使用 `(?<=pattern)`，下例中实现了查找 Twitter 名。


```python
import re

twitter = re.compile(
    '''
    # A twitter handler: @username
    (?<=@)
    ([\w\d_]+)  # username
    ''',
    re.UNICODE | re.VERBOSE
)

text = '''This text includes two Twitter handles.
    One for @ThePSF, and one for the author, @doughellmann.
    '''

print text
for match in twitter.findall(text):
    print 'Handler:', match
```

    This text includes two Twitter handles.
        One for @ThePSF, and one for the author, @doughellmann.
        
    Handler: ThePSF
    Handler: doughellmann


## 表达式中的自引用

对分组的引用可用 `\num` 语法，但是 `\123` 等 3 位数的会被正则表达式解析成为八进制数，故这种引用最多能对 1--99 共 99 个分组进行引用。


```python
import re

address = re.compile(
    r'''
    # The regular name
    (\w+)  # first name
    \s+
    (([\w.])+\s+)?  # optional middle name or initial
    (\w+)   # last anme
    
    \s+
    
    <
    
    # The address: first_name.last_name@domain.tld
    (?P<email>
        \1  # first name
        \.
        \4  # last name
        @
        ([\w\d.]+\.)+  # domain name prefix
        (com|org|edu)  # limit the allowed top-level domains
    )
    
    >
    ''',
    re.UNICODE | re.VERBOSE | re.IGNORECASE )

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Match name :', match.group(1), match.group(4)
        print ' Match email:', match.group(5)
    else:
        print ' No match'
```

    Candidate: First Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com
    Candidate: Different Name <first.last@example.com>
     No match
    Candidate: First Middle Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com
    Candidate: First M. Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com


基于分组编号进行引用，当分组改变时，进行要更新引用号。使用命名分组及引用可以避免这种不便。


```python
import re

address = re.compile(
    '''
    # The regular name
    (?P<first_name>\w+)
    \s+
    (([\w.]+)\s+)?  # optional middle name or initial
    (?P<last_name>\w+)
    
    \s+
    
    <
    
    # The address: first_name.last_name@domain.tld
    (?P<email>
        (?P=first_name)
        \.
        (?P=last_name)
        @
        ([\w\d.]+\.)+  # domain name prefix
        (com|org|edu)  # limit the allowed top-level domains
    )
    
    >
    ''',
    re.UNICODE | re.VERBOSE | re.IGNORECASE )

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Match name :', match.groupdict()['first_name'],
        print match.groupdict()['last_name']
        print ' Match email:', match.groupdict()['email']
    else:
        print ' No match'
```

    Candidate: First Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com
    Candidate: Different Name <first.last@example.com>
     No match
    Candidate: First Middle Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com
    Candidate: First M. Last <first.last@example.com>
     Match name : First Last
     Match email: first.last@example.com


反向引用也可用在基于之前分组的匹配情况，选择不同的模式。语法为 `(?(id)yes-expression|no-expression)`，这里的 *id* 是分组的名字或编号，*yes-expression* 是当分组有值时选择的表达式。

下例的模式中，邮件地址要求：当出现名字时，地址必须由尖括号包围，当没有出现名字时，地址本身不能被尖括号包围。


```python
import re

address = re.compile(
    '''
    ^
    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    (?P<name>
        ([\w.]+\s+)*[\w.]+
    )?
    \s*
    
    # Email addresses are wrapped in angle brackets, but
    # only if a name is found.
    (?(name)
        # remainder wrapped in angle brackets because
        # there is a name
        (?P<brackets>(?=(<.*>$)))
        |
        # remainder does not include angle brackets without name
        (?=([^<].*[^>]$))
    )
    
    # Only look for a bracket if the look-ahead assertion
    # found both of them
    (?(brackets)<|\s*)
    
    # The address itself: username@domain.tld
    (?P<email>
        [\w\d.+-]  # username
        @
        ([\w\d.]+\.)+  # domain name prefix
        (com|org|edu)  # limit the allowed top-level domains
    )
    
    # Only look for a bracket if the look-ahead assertion
    # found both of them
    (?(brackets)<|\s*)
    
    $
    ''',
    re.UNICODE | re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
    u'no.brackets@example.com',
]

for candidate in candidates:
    print 'Candidate:', candidate
    match = address.search(candidate)
    if match:
        print ' Match name :', match.groupdict()['name']
        print ' Match email:', match.groupdict()['email']
    else:
        print ' No match'
```

    Candidate: First Last <first.last@example.com>
     No match
    Candidate: No Brackets first.last@example.com
     No match
    Candidate: Open Bracket <first.last@example.com
     No match
    Candidate: Close Bracket first.last@example.com>
     No match
    Candidate: no.brackets@example.com
     No match


## 通过模式修改字符串

使用 *sub()* 对所有匹配的部分进行替换，替换的内容可以通过反向引用使用匹配的分组内容。


```python
import re

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.sub(r'<b>\1</b>', text)
```

    Text: Make this **bold**. This **too**.
    Bold: Make this <b>bold</b>. This <b>too</b>.


当使用命名分组时，替换内容中用 `\g<name>` 进行引用。`\g<name>` 语法也适用于编号分组的情况，如 `\g<1>`。


```python
import re

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}', re.UNICODE)

text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.sub(r'<b>\g<bold_text></b>', text)
```

    Text: Make this **bold**. This **too**.
    Bold: Make this <b>bold</b>. This <b>too</b>.


*subn()* 和 *sub()* 类似，但它除了返回修改后的字符串外，还返回一个替换次数，因此返回是一个元组 *(modified_string, count)*。


## 用模式进行分隔

*str.split()* 的分隔符只能是一个简单的字符串值。当在需要分离出段落（一般由 2+ 个换行符表示）时，*str.split()* 并不太适用。

下例中先用 *findall()* 进行段落分离。


```python
import re

text = '''Paragraph one
on two lines.


Paragraph two.


Paragraph three.'''

for num, para in enumerate(re.findall(r'(.+?)\n{2,}',
                                     text,
                                     flags=re.DOTALL)
                          ):
    print num, repr(para)
    print
```

    0 'Paragraph one\non two lines.'
    
    1 'Paragraph two.'
    


上例中没有匹配最后一个段落，可以进行扩展，或者直接使用 *re.split()*，它自动对边缘条件进行了处理。


```python
import re

text = '''Paragraph one
on two lines.


Paragraph two.


Paragraph three.'''

print 'With findall:'
for num, para in enumerate(re.findall(r'(.+?)(\n{2,}|$)',
                                     text,
                                     flags=re.DOTALL)
                          ):
    print num, repr(para)
    print
    
print
print 'With re.split:'
for num, para in enumerate(re.split(r'\n{2,}', text)):
    print num, repr(para)
    print
```

    With findall:
    0 ('Paragraph one\non two lines.', '\n\n\n')
    
    1 ('Paragraph two.', '\n\n\n')
    
    2 ('Paragraph three.', '')
    
    
    With re.split:
    0 'Paragraph one\non two lines.'
    
    1 'Paragraph two.'
    
    2 'Paragraph three.'
    


当 *re.split()* 使用的分隔模式中使用括号定义分组时，其使用更像 *str.partition()*，它即返回分隔符，也返回其它部分。


```python
import re

text = '''Paragraph one
on two lines.


Paragraph two.


Paragraph three.'''

print 'With re.split:'
for num, para in enumerate(re.split(r'(\n{2,})', text)):
    print num, repr(para)
    print
```

    With re.split:
    0 'Paragraph one\non two lines.'
    
    1 '\n\n\n'
    
    2 'Paragraph two.'
    
    3 '\n\n\n'
    
    4 'Paragraph three.'
    


## 更多资源

+ [Regular Expression HOWTO](http://docs.python.org/howto/regex.html) Andrew Kuchling's introduction to regular expressions for Python developers.
+ [Kodos,  The Python Regular Expression Debugger](http://kodos.sourceforge.net/) An interactive tool for testing regular expressions, created by Phil Schwartz.
+ [Regular expression](http://en.wikipedia.org/wiki/Regular_expressions) Wikipedia article that provides a general introduction to regular expression concepts and techniques.
+ locale (page 909): 当使用 Unicode 时，使用 `locale` 模块进行语言设置。
+ [unicodedata](docs.python.org/library/unicodedata.html) Programmatic access to the Unicode character property database.
+ [本文对应的 Jupyter notebook](https://github.com/haiiiiiyun/ThePythonStandardLibraryByExample-ipynb/blob/master/1.3re.ipynb) 

## 参考

+ [The Python Standard Library By Example: 1.3 re-Regular Expressions](https://www.amazon.com/Python-Standard-Library-Example/dp/0321767349)
