---
title: Config mirror for ruby gems
date: 2024-03-01
tags: ruby mirrors
categoris: Programming
---

## Add a source and remove the default source

```bash
$ gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/ --remove https://rubygems.org/
$ gem sources -l
```

Or edit `~/.gemrc`, add the following to `sources` section:

https://mirrors.tuna.tsinghua.edu.cn/rubygems/

see https://mirrors.tuna.tsinghua.edu.cn/help/rubygems/

## Add mirror for bundle

```bash
$ bundle config mirror.https://rubygems.org https://gems.ruby-china.com
$ bundle config mirror.https://gems.ruby-china.org https://gems.ruby-china.com
```