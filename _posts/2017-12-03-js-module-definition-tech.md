---
title: JS 模块化规范简介
date: 2017-12-03
writing-time: 2017-12-02
categories: programming
tags: JS javascript CommonJS AMD CMD require.js
---

# CommonJS

CommonJS 致力于定义使 JS 能进行通用应用编程 API，并最终实现一个类似于 Python 的标准库。使用 CommonJS API 编写的程序，可以在各种环境中（如客户端和服务端）运行。

## CommonJS 模块化规范

模块系统有一个全局方法 `require()`，用来加载模块，例如：

```javascript
var math = require('math');

math.add(40, 2); // 42
```
require() 方法是同步的，不适合在浏览器中运用。

模块中有一个 `exports` 对象变量，模块中要导出的 API 只能通过加到 `exports` 实现。

模块中有一个 `module` 对象变量，`module.id` 属性用来设置该模块名，而 `require(module.id)` 将该模块中的 `exports` 对象。

例如：

```javascript
//math.js
exports.add = function(){
    var sum = 0, i = 0, args = arguments, l = args.length;
    while (i <l) {
        sum += args[i++];
    }
    return sum;
};

//increment.js
var add = require('math').add;
exports.increment = function(val) {
    return add(val, 1);
};

//program.js
var inc = require('increment').increment;
var a = 1;
inc(a); //2
module.id == "program";
```

NodeJS 的模块系统，就是基于 CommonJS 规范实现的，CommonJS 模块规范适合服务端编程。

# AMD

AMD 即 "Asynchronous Module Definition"，异步模块定义。它采用异步方式加载模块，适合在浏览器端编程。

AMD 也用 `require()` 加载模块：

```javascript
require([module1, module2, ...], callback);
```

所有依赖的模块都写在列表中，依赖这些模块的代码则放在 callback 回调函数中。例如：

```javascript
require(['math', function(math){
    math.add(40, 2); //42
});
```

AMD 是 [require.js](http://requirejs.org/) 定义的规范。

## AMD 模块

AMD 模块用 `define()` 函数定义，如果定义的模块不依赖其它模块，则如：

```javascript
//math.js
define(function(){
    
    var add = function(x, y){
        return x + y;
    };

    return {
        add: add
    };
});
```

如果定义的模块要依赖其它模块，则如：

```javascript
define(['mylib'], function(mylib) {

    function foo() {
        mylib.dosomething();
    }

    return {
        foo: foo
    };
});
```

AMD 规范也可以定义与 CommonJS 规范兼容的模块，定义如：

```javascript
define(function(require, exports, module){

    var mylib = require('./mylib');

    exports.foo = function() {
        mylib.dosomething();
    }
});
```

## require.js 加载模块

require.js 用于对 JS 文件进行模块化管理。先到 [官网](http://requirejs.org/) 下载最新版本到本地 `js` 目录，加载到页面中：

```html
<script src="js/require.js" defer async="true"></script>
```

async 表示异步加载，IE 不支持该属性，只支持 defer。

下一步加载主模块：

```html
<script src="js/require.js" data-main="js/main"></script>
```

`data-main` 属性用于指定主模块，主模块就是入口代码，指定后，require.js 将先加载 main.js。

主模块的写法，例如主模块依赖 jquery, underscore, backbone 三个模块：

```javascript
//main.js
require(['jquery', 'underscore', 'backbone'], function($, underscore, Backbone) {
    // do something
});
```

上例的写法中，都假定这三个依赖模块与主模块放在同一目录下，且文件名为 jquery.js, underscore.js, backbone.js。可以用 `require.config()` 定制加载行为。写在主模块的开头：

```javascript
require.config({
    paths: {
        "jquery": "js/lib/jquery.min",
        "underscore": "js/lib/underscore.min",
        "backbone": "js/lib/backbone.min"
    }
});
```

也可以直接改变其路径：

```javascript
require.config({
    baseUrl: "js/lib",
    paths: {
        "jquery": "jquery.min",
        "underscore": "underscore.min",
        "backbone": "backbone.min"
    }
});
```

也可指定外部 URL：

```javascript
require.config({
    paths: {
        "jquery": "https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min"
    }
});
```

当加载非 AMD 规范的模块时，要在加载前，用 `require.config()` 定义模块的特征。例如 underscore 和 backbone 都没有采用 AMD 规范：

```javascript
require.config({
    shim: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    }
});
```

即通过 `shim` 属性定义每个模块的 exports 值及依赖性。


# CMD

CMD 是 SeaJS 的模块定义规范，也是异步加载模块，并且与 CommonJS 规范保持了兼容性。

AMD 事先就要声明依赖的模块，例如：

```javascript
define(['lib1', 'lib2'], function(lib1, lib2){
});
```

而 CMD 无需事先声明依赖，如：

```javascript
define(function(require, exports, module){
    var lib1 = require('./lib1');
    //...

    if(condition) {
        var lib2 = require('./lib2');
        //...
    }
});
```


# 参考

+ http://www.commonjs.org/
+ [CommonJS Modules/1.1](http://wiki.commonjs.org/wiki/Modules/1.1)
+ [Javascript模块化编程（二）：AMD规范](http://www.ruanyifeng.com/blog/2012/10/asynchronous_module_definition.html)
+ [CommonJS，AMD，CMD区别](http://zccst.iteye.com/blog/2215317)
+ [Javascript模块化编程（三）：require.js的用法](http://www.ruanyifeng.com/blog/2012/11/require_js.html)
+ http://requirejs.org/
