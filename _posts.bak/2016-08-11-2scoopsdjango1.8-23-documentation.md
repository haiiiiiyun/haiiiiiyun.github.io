---
title: Django 文档
date: 2016-08-11
writing-time: 2016-08-11 13:32--14:12
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

相关包： 将 Sphinx 安装在系统级上，使其能应用于所有的 Django 项目。

# 使用 reStructuredText 来写 Python 文档

RST 的格式文档： [restructured text specification](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html)

下面是 RST 的最基本的命令：

```restructured

章节头
==============

**强调 (bold/strong)**

*斜体*

简单的链接: http://django.2scoops.org
引用链接: `Two Scoops of Django`_

.. _Two Scoops of Django: https://django.2scoops.org

子章节头
-----------------

#) 一个编号列表项

#) 第二个编号列表项

* 第一个符号列表项

* 第二个符号列表项

  * 缩进的符号列表项

  * 注意回车和缩进

普通代码块::

    def like():
        print("I like Ice Cream")

    for i in range(10):
        like()


Python 高亮的代码块 （需要 pygments ）:

code-block:: python

    # You need to "pip install pygments" to make this work.

    for i in range(10):
        like()

JavaScript 高亮的代码块:

code-block:: javascript

    console.log("Don't use alert()")
```

# 使用 Sphinx 从 reStructuredText 中提取文档

Sphinx 工具能根据 **.rst** 文件内容输出包含 HTML、LaTeX、man 页和文本文件等格式的文档。

参考： [sphinx-doc](http://sphinx-doc.org)。

每周至少对 Sphinx 文档进行一次构建，从而避免过多的交叉引用或有效格式破坏了 SPhinx 的构建过程。

# Django 项目应包含哪些文档

以下是每个项目都应包含的最基本的文档：

文件或目录            | 理由                                                   | 备注
----------------------|--------------------------------------------------------|
README.rst            | 每个 Python 项目都应在根目录下有一个 README.rst 文件。 | 至少要有一段关于项目的描述。而且还要链接到 docs/ 目录下的安装指令。
docs/                 | 项目文档应该放在一个统一的位置。这个是 Python 的标准位置|
docs/deployment.rst   | 该文档能使你节省很多时间                               | 一步步说明如何安装/升到到生产环境，即使这些操作已通过 Chef,Fabric 或 Makefile 来完成了。
docs/installation.rst | 它对新人或你需要在新的机器上安装时很有用               | 一步步说明如何安装设置一个项目
docs/architecture.rst | 有助于理解项目是怎样发展至今的                         | 这是你对项目的预想。描述可长可短，有助于你保持项目初心

# 使用 Markdown

Markdown 在技术书编写中用的较多，但在 Python 和 Django 社区中用的较少。

使用 Markdown 要注意：

+ PyPI 只认 reStructuredText 格式的 long_description
+ 多数 Python 和 Django 开发者会先查找 reStructuredText 格式的文档


## 使用 Pandoc 将 README.md 转成 README.rst

可以在项目的 **setup.py** 中，增加：

```python
# setup.py
import subprocess
import sys

if sys.argv[-1] == 'md2rst':
    subprocess.call('pandoc README.md -o README.rst', shell=True)
```

之后运行 `python setup.py md2rst` 就能转换了，然后可以将 README.rst 上传到 PyPI。


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
