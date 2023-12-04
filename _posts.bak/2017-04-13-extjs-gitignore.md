---
title: ExtJS 项目的 gitignore
date: 2017-04-13
writing-time: 2017-04-13 15:39--15:44
categories: Programming
tags: Programming Sencha ExtJS Javascript Git 《Ext&nbsp;JS&nbsp;Application&nbsp;Development&nbsp;Blueprints》
---


```ini
# sample gitignore for extjs project
# The build directory can be recreated by developers using Sencha
# Cmd – it should be excluded from the repo
build/

# Changes every time a build is run
bootstrap.js
bootstrap.css

# Temporary files created when compiling .scss files
.sass-cache/

# Some team members may use Sencha architect – exclude so they
# keep their custom settings
.architect

# It's possible to create reusable packages using Sencha Cmd
# but depending on your preference you might want to exclude this
# directory.
packages/
```


# 参考 

+ [Chapter1: In safe hands](https://www.amazon.com/Ext-JS-Application-Development-Blueprints/dp/1784395307/)
