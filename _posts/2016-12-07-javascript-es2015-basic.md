---
title: Javascript ES2015（ES6）新语法、新特性
date: 2016-12-07
writing-time: 2016-12-07 10:25
categories: programming Javascript
tags: Programming Javascript ES2015 ES6
---

# 概述

Javascript ES2015，即 ECMAScript 标准 ECMAScript 6 (简称 ES6) 是 2015 年 6 月正式发布的新标准。

由于大多数浏览器中的 Javascript 引擎还没有完全支持 ES2015 中的新特性，一般需要 [Babel](http://babeljs.io/) 等编译器将 ES6 代码转换成 ES5 标准的代码。


# 安装 Babel

先安装 NodeJS，在 Ubuntu 16.04 上安装当前稳定版本 v6.x:

```bash
$ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
$ sudo apt-get install -y nodejs
```

详细参考 [nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions)

再安装 Babel CLI 和 preset:

```bash
$ npm install --save-dev babel-cli babel-preset-latest
```

# ES2015 的新语法新特性

## const, const 和块级作用哉

const 用于定义常量，但在 ES6 之前的标准中，并没有原生实现，故在降级编译时，会使用 var 实现，并进行引用检查：

```javascript
// foo.js
const foo = 'bar'

foo = 'newvalue'
```

```bash
$ babel foo.js
...
SyntaxError: test.js: Line 3: "foo" is read-only
  1 | const foo = 'bar'
  2 |
> 3 | foo = 'newvalue'
...
```

参考：[https://facebook.github.io/react-native/docs/getting-started.html](https://facebook.github.io/react-native/docs/getting-started.html)
