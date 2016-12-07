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
$ sudo npm install -g --save-dev babel-cli babel-preset-latest babel-preset-es2015
```

然后，在项目的根目录下创建一个 .babelrc 文件，内容为：

```json
{
    "presets": [
        "es2015"
    ]
}
```

这样 Babel 就能将 ES6 文件编译成 ES5 标准的文件了。

# ES2015 的新语法新特性

## const, const 和块级作用域

const 用于定义常量。

```javascript
// foo.js
const foo = 'bar';

foo = "newvalue";
```

由于 ES6 之前没有原生实现，编码后用 var 来实现，并进行引用检查：

```bash
$ babel foo.js

SyntaxError: foo.js: "foo" is read-only
  1 | const foo = 'bar'
  2 | 
> 3 | foo = 'newvalue'
    | ^
  4 | 
  5 | console.log(foo)
  6 | 
```


Es6 之前的 JavaScrip 没有块级作用域，变量都用 var 声明，都是全局使用域。因此很容易出现下面的错误。

```html
<button>一</button>
<button>二</button>
<button>三</button>
<button>四</button>

<div id="output"></div>

<script>
  var buttons = document.querySelectorAll('button');
  var output = document.querySelector('#output');

  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
      output.innerText = buttons[i].innerText;
    })
  }
</script>
```

基于以上的代码，当点击任何一个按钮时，会出现 **Uncaught TypeError: Cannot read property 'innerText' of undefined** 错误。这是因为用 `var` 声明的 i 变量没有块作用域，故在回调函数中对 i 的引用值全部都是 `for` 循环结束时的 i 值（即值为 buttons.length）。

在 ES6 中，只需将 `var` 改为 `let`，使变量具有块作用域，即可解决以上的问题：

```javascript
  // let.js
  var buttons = document.querySelectorAll('button');
  var output = document.querySelector('#output');

  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function() {
      output.innerText = buttons[i].innerText;
    })
  }
```

```bash
$ babel let.js 

'use strict';

var buttons = document.querySelectorAll('button');
var output = document.querySelector('#output');

var _loop = function _loop(i) {
  buttons[i].addEventListener('click', function () {
    output.innerText = buttons[i].innerText;
  });
};

for (var i = 0; i < buttons.length; i++) {
  _loop(i);
}
```

可以看到，编译后使用闭包来避免了之前的问题。


## 箭头函数 Arrow Function

箭头函数就是使用 `=>` 进行定义的函数，属性匿名函数 lambda 一类。它有以下几种语法：

```javascrit

foo => foo + ' world' // means return foo + ' world'

(foo, bar) => foo + bar // means return foo + bar

foo => {
    return foo + ' world'
}

(foo, bar) => {
    return foo + bar
}
```

箭头函数特别适合用于回调函数定义，如：

```javascript
// arrow.js
let names = ['Will', 'Jack', 'Peter', 'Steve', 'John', 'Hugo', 'Mike'];

let newSet = names
    .map((name, index) => { //转化成格式为 {id:id, name:name} 的对象组
        return {
            id: index,
            name: name
        }
    })
    .filter(man => man.id % 2 == 0) // 去除 id 值为奇数的对象
    .map(man => [man.name]) // 将对象组中的对象格式 {id:id, name:name} 变换成 [name]
    .reduce((a, b) => a.concat(b)) // 合并

    console.log(newSet) // 输出 ['Will', 'Peter', 'John', 'Mike']
```

### 箭头函数的上下文

箭头函数中的上下文(即 this) 绑定为定义该箭头函数所在的作用域的上下文，并且这种绑定是强制而且不可修改的。

例如：

```javascript

let obj = {
    hello: 'world',
    foo() {
        let bar = () => {
            return this.hello;
        }
        return bar;
    }
}

window.hello = 'ES6';
window.bar = obj.foo();
window.bar(); // 输出 'world'
```

上面的 obj.foo 等价于：

```javascript
foo() {
    let bar = (function() {
        return this.hello;
    }).bind(this);

    return bar;
}
```

箭头函数具有的这种特性，使得它作为回调函数时能方便地使用上下文中的变量，如：

```javascript
let DataCenter = {
    baseURL: 'http://example.com/api/data/',
    search(query) {
        fetch(`${this.baseURL}/search?query=${query}`)
        .then(res => {
            return fetch(`${this.baseURL}/....`);
        })
    }
}
```

箭头函数绑定的上下文是强制的，无法通过 applay 或 call 方法改变，例如：

```javascript
// bind.js
let a = {
    init() {
        this.bar = () => this.dam;
    },
    dam: 'hei',
    foo() {
        return this.dam;
    }
}

let b = {
    dam: 'ha'
}

a.init();

console.log(a.foo()); // => hei
console.log(a.foo.bind(b).call(a)); // => ha, 普通函数可改变上下文
console.log(a.bar.call(b)); // => hei, 箭头函数不可改变上下文
```

以上例子可以直接用 babel 运行：

```bash
$ babel-node bind.js
```
