---
title: 在github上创建文档翻译项目，并与readthedocs、transifex整合的方法
date: 2016-05-06 14:03
categories: translation
tags: Django github readthedocs transifex translation
---

# 一、概述

本文以创建Django最新LTS版本的文档简体中文翻译项目为例，描述了在github.com上创建文档翻译项目，并与readthedocs.org和transifex.com整合的方法。

操作流程主要分为三部分：

1. 在[github.com](https://github.com/)上创建一个文档翻译项目
2. 与[transifex.com](https://www.transifex.com/)整合
3. 与[readthedocs.org](https://readthedocs.org/)整合，将翻译内容发布到readthedocs.org网站

# 二、流程

## I. 需要安装的程序

1. `python2x`
2. `sphinx>=1.4.1`, 安装方法 `pip install sphinx`, [sphinx](http://www.sphinx-doc.org/)是一个文档编写工具，支持reST标识语言。
3. `sphinx_intl>=0.9.9`, 安装方法`pip install sphinx_intl`, [sphinx_intl](https://pypi.python.org/pypi/sphinx-intl)是sphinx文档的翻译助手工具。
4. `transifex_client>=0.11`, 安装方法`pip install transifex_client`, 安装后会有一个tx可执行文件，这是[transifex.com](https://www.transifex.com/)网站的客户端工具。
5. `urllib3>=1.15.1`, 这是`transifex_client`的依赖包，在ubuntu14.04上，必须用`pip install urllib3 -U`升级到最新版本后，tx执行时才不出错。

## II. 在github.com上创建Django LTS docs简体中文翻译项目

当前最新的Django LTS版本是v1.8.13 。

### 在github上建立项目，名称为`DjangoLTS-docs-zh_CN`

因原始文档从django项目里获取，故将django项目作为本项目的submodule，并放在django-lts目录中。

```
Django-docs-zh_CN > git submodule add "git@github.com:django/django.git" django-lts
Django-docs-zh_CN > git submodule init
Django-docs-zh_CN > git submodule update
```

由于submodule只是指向一个特定的commit, 所以为使submodule指向最新的LTS版本(v1.8.13)，使用以下方法： 参考[Git submodules: Specify a branch/tag](http://stackoverflow.com/questions/1777854/git-submodules-specify-a-branch-tag)。

```
Django-docs-zh_CN > cd django-lts
django-lts > git checkout 1.8.13
django-lts > cd ..
Django-docs-zh_CN > git add django-lts
Django-docs-zh_CN > git commit -m "moved django to v1.8.13"
Django-docs-zh_CN > git push
```

将django LTS下的docs目录复制到本项目中:

```
Django-docs-zh_CN > cp -R django-lts/docs ./docs

```
 docs目录是一个Sphinx文档工程，里面包含`conf.py`配置文件。
修改`conf.py`里的配置项：`locale_dirs = ['locale/']`(一般默认就是该值)。

提取docs目录下的翻译项，生成pot文件。

```
Django-docs-zh_CN > cd docs
docs > make gettext
```
运行后，在`docs/_build/locale/`目录下生成了多个.pot文档。

## III. 与transifex.com整合

在transifex.com上创建一个项目，名称为`djangolts-docs-zh_cn`。

运行`Django-docs-zh_CN > tx init`, 初始化transifex客户端，运行
后在项目的根目录下生成`.tx`目录，`.tx/config`文件内保存翻译项目的相关信息，在用户主目录下生成`.transifexrc`文件，用于存放用户名等认证信息。

设置翻译文件：

```
Django-docs-zh_CN > mkdir -p docs/locale/zh_CN/LC_MESSAGES/
Django-docs-zh_CN > tx set --auto-local -r djangolts-docs-zh_cn.index "docs/locale/<lang>/LC_MESSAGES/index.po" --source-language=en --source-file "docs/_build/locale/index.pot" -t PO --execute
```

命令各选项含义为：

+ `-r djangolts-docs-zh_cn.index "docs/locale/<lang>/LC_MESSAGES/index.po"`: `<project_id>:<resource_id> "po_file_path"`, 指定该资源文件翻译后的存放地。
+ `--source-language=en`，指该资源原文档是用英文写的。
+ `--source-file "docs/_build/locale/index.pot"`，指该资源原文件的存放地。
+ `-t PO`, 指该资源的文件为PO文件

命令运行后在`.tx/config`文件中生成如下配置内容：

```
[djangolts-docs-zh_cn.index]
file_filter = docs/locale/<lang>/LC_MESSAGES/index.po
source_file = docs/_build/locale/index.pot
source_lang = en
type = PO
```
运行以上类似的命令，为`source_file = docs/_build/locale/`下的其它10个文件生成类似的配置内容,文件有：
`glossary.pot, contents.pot, faq.pot, howto.pot, internals.pot, intro.pot, misc.pot, ref.pot, releases.pot, topics.pot`

其中的glossary.pot文件，由于`glossary`不能用做资源的资源id, 故将资源id修改为`the_glossary`。

tx的操作和git类似， 查看tx状态： `tx status`， 你可以看到一共添加了多少个资源。

上传资源：`tx push -s`

在transifex.com上翻译后，将翻译内容下载回来：`tx pull -l zh_CN`,
运行后，在`docs/locale/zh_CN/LC_MESSAGES/`下生成相应的po文件。

测试简体中文版本的文档：

```
Django-docs-zh_CN > cd docs
Django-docs-zh_CN > make -e SPHINXOPTS="-D language='zh_CN'" html
```

运行后，在`docs/_build/`目录下生成简体中文版本的文档。

## IV. 与readthedocs.org整合

由于项目的结构符合readthedocs.org的要求，只需要在readthedocs.org上`Import a Project`，并指定git库地址为项目地址即可。
然后在github的项目配置页面，设置Webhook与readthedocs关联，之后项目每次提交后，自动在readthedocs.org上重新构建。
