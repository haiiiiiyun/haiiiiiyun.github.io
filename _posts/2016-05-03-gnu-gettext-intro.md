---
title: GNU gettext工具简介
date: 2016-05-03 10:41
categories: Programming Translation
tags: Programming Utility
---

# 一、简介
支持多语言的程序，在编写时，通常源代码中的交互语句首先还是用英文编写，然后才为交互语句添加多语言支持机制。程序在运行过程时，再根据用户环境变量设置，选择合适的语言版本，显示给用户。

[GNU gettext](https://www.gnu.org/software/gettext/) 为程序的国际化i18n和本地化l10n提供了很好的支持。

用GNU gettext实现多语言支持的一般步骤如下：

1. 在程序源代码中添加gettext的相关声明信息及本地化运行环境检测代码;
1. 为需要翻译的交互语句设置标记;
1. 使用gettext工具提取源代码中的交互语句，生成pot(portable object template)文件;
1. 使用msginit工具将pot文件转化成一个特定语言版本的po(portable object)文件; 或者使用msgmerge将更新了的pot文件与旧的po文件合并生成新的po文件;
1. 编辑po文件（可使用poedit等工具)，将交互语句逐条翻译;
1. 使用msgfmt工具将po文件转化成mo(machine object)文件。

![GNU gettext]({{ site.url }}/assets/images/gnu-gettext.png)

# 二、PO文件格式

[PO文件](https://www.gnu.org/savannah-checkouts/gnu/gettext/manual/html_node/PO-Files.html)， 也就是portable object文件，是可编辑的文本文件。通常，`xgettext`工具从源文件中提取待翻译语句后，默认生成的就是po文件，但是，我们通常将xgettext工具生成的文件保存为pot(portable object template)文件(通过`xgettext`工具的`-o`参数)，再用msginit从.pot文件生成特定语言版本的.po文件。

每个.po文件都由一个或多个翻译单元(entry)组成，各翻译单元之前由空行分隔。每个翻译单元内，包含一个待翻译语句和相对应的翻译版本。

.po文件中的翻译单元(entry)的语义格式如下：

```
white-space
#  translator-comments
#. extracted-comments
#: reference…
#, flag…
#| msgid previous-untranslated-string
msgid untranslated-string
msgstr translated-string
```

1. 先用空行分隔每一个翻译单元;
2. 由`#`开头的每一行都是注释行;

  1). `#`后紧接着空格符的注释内容，是翻译者添加的注释;
  2). `#`后紧接着`.`的注释内容，是`xgettext`从源代码中提取出的注释内容（通过`xgettext --add-comments`选项);
  3). `#`后紧接着`:`的注释是待翻译语句在源代码中的位置信息;
  4). `#`后紧接着`,`的注释是msgfmt程序专用的flag;
  5). `#`后紧接着`|`的注释是这条待翻译语句之前的相关翻译信息;
3. msgid 行是从源代码中提取出的待翻译语句;
4. msgstr 行是对应的翻译版本。

一个简单的翻译单元如下：

```

#: lib/error.c:116
msgid "Unknown system error"
msgstr "Error desconegut del sistema"
```

# 三、例子

以下操作针对C语言程序为例:

## 1. 在源程序中导入gettext声明，并设置触发gettext操作的运行环境设置

```C
#include <libintl.h>

int main (int argc, char *argv[])
{
...
setlocale (LC_ALL, "");
bindtextdomain (PACKAGE, LOCALEDIR);
textdomain (PACKAGE);
...
}
```

## 2. 在源代码中标记待翻译的交互语句

测试用的`hello.c`源代码：

```C
#include <libintl.h>
#include <stdio.h>

int main( void )
{
    /* triggering gettext declaration */
    setlocale( LC_ALL, "zh_CN" );
    bindtextdomain( PACKAGE, LOCALDIR );
    textdomain( PACKAGE );

    /* say hello here */
    printf( gettext( "Hello." ) );

    /* say hello again */
    printf( gettext( "Hello world!" ) );
}
```

## 3、用xgettext提取源代码中的待翻译语句，并生成pot文件

```
shell: xgettext hello.c --add-comments --add-location \
        --no-wrap --copyright-holder="My Copyright Message" \
        --package-name="My Package Name" --package-version="V1.8.5"\
        --msgid-bugs-address="myemil@mail.com" -o messages.pot
```

getgext工具集使用的是0.18.3版本。

```
shell: xgettext --version
xgettext (GNU gettext-tools) 0.18.3
Copyright (C) 1995-1998, 2000-2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Written by Ulrich Drepper.
```

生成的messages.pot：

```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR My Copyright Message
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: My Package Name V1.8.5\n"
"Report-Msgid-Bugs-To: myemil@mail.com\n"
"POT-Creation-Date: 2016-05-03 14:03+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=CHARSET\n"
"Content-Transfer-Encoding: 8bit\n"

#. say hello here
#: hello.c:12
#, c-format
msgid "Hello."
msgstr ""

#. say hello again
#: hello.c:15
#, c-format
msgid "Hello world!"
msgstr ""
```

修改pot文件，编辑第一作者(FIRST AUTHOR)，翻译者(Last-Translator), 语言工作组(Language-Team)等信息。

修改后的messages.pot文件如下:

```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR My Copyright Message
# This file is distributed under the same license as the PACKAGE package.
# first-author-name <name@email.com>, 2016.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: My Package Name V1.8.5\n"
"Report-Msgid-Bugs-To: myemil@mail.com\n"
"POT-Creation-Date: 2016-05-03 14:03+0800\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: my name <name@emial.com>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#. say hello here
#: hello.c:12
#, c-format
msgid "Hello."
msgstr ""

#. say hello again
#: hello.c:15
#, c-format
msgid "Hello world!"
msgstr ""
```

## 4、 使用msginit工具将pot文件转成对应简体中文翻译的.po文件

```
shell: msginit --input=messages.pot --local=zh_CN.po
```

生成的zh_CN.po文件如下：

```
# Chinese translations for My Package Name package.
# Copyright (C) 2016 My Copyright Message
# This file is distributed under the same license as the My Package Name package.
# first-author-name <name@email.com>, 2016.
#
msgid ""
msgstr ""
"Project-Id-Version: My Package Name V1.8.5\n"
"Report-Msgid-Bugs-To: myemil@mail.com\n"
"POT-Creation-Date: 2016-05-03 14:03+0800\n"
"PO-Revision-Date: 2016-05-03 14:14+0800\n"
"Last-Translator: hy <hy@hy-hp-pro-3330-mt>\n"
"Language-Team: Chinese (simplified)\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

#. say hello here
#: hello.c:12
#, c-format
msgid "Hello."
msgstr ""

#. say hello again
#: hello.c:15
#, c-format
msgid "Hello world!"
msgstr ""
```

使用文本编辑或[POedit](https://poedit.net/)来修改.po文件，添加相应的翻译语句。

## 5、使用msgfmt工具生成mo文件。

`shell: msgfmt zh_CN.po -o zh_CN.mo`

## 6、更新与合并

当源文件更新后，通过步骤1-2-3生成新的.pot文件，假设为messages.pot。此时可使用`msgmerge`工具将原来的已翻译条目与新的.pot文件合并，生成新的.po文件。

`shell: msgmerge messages.pot zh_CN.po -o zh_CN2.po`

# 四、翻译词库

当有多个翻译好了的.po文件后，可以将所有的.po文件合并生成一个词库文件。然后用词库文件中的翻译项应用到新的.pot文件的翻译工作中。

## 1. 生成词库文件
使用`msgcat`生成一个翻译词库文件`compendium.po`:
`msgcat --use-first -o compendium.po file1.po file2.po`

## 2. 应用词库文件
将翻译词库文件应用到新的.pot文件中，并生成po文件:
`msgmerge --compendium compendium.po -o file.po /dev/null file.pot`

## 3. 更新.po文件
将所有的翻译词库文件和旧的.po文件file.po组合，生成一个临时的.po文件update.po：
msgcat --use-first -o update.po compendium1.po compendium2.po file.po

新的.pot文件与update.po合并，以更新update.po:
msgmerge update.po file.pot | msgattrib --no-obsolete > file.po
