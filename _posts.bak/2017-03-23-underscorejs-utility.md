---
title: Underscore.js 中的工具函数
date: 2017-03-23
writing-time: 2017-03-23 08:24--09:50
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。


* noConflict: `_.noConflict()`

  > 将 `_` 返还给原主，并返回 `Underscore` 对象引用。

  ```javascript
  var underscore = _.noConflict()
  ```


* identity: `_.identity(value)`

  > 返回原样的传入参数，即数学函数 f(x)=x。
  > 能作为 Underscore 的默认 iteratee 函数。

  ```javascript
  var stooge = {name: 'moe'};
  stooge === _.identity(stooge); // true
  ```

* constant: `_.constant(value)`

  > 返回一个函数。
  > 该函数返回原样的 _.constant 函数的参数。

  ```javascript
  var stooge = {name: 'moe'};
  stooge === _.constant(stooge)(); // true
  ```

* noop: `_.noop()`

  > 不管传入什么参数，都返回 undefined。
  > 一般用于默认的回调参数。


* times: `_.times(n, iteratee, [context])`

  > 调用该 iteratee 函数 n 次。
  > 每次调用 iteratee 时传入一个 index 参数。
  > 将每次调用的返回值组成一个数组返回。

  ```javascript
  // 本例使用 underscore 面向对象语法
  _(3).times(function(index){
    return index+1;
  }); //[1,2,3]
  ```

* random: `_.random(min, max)`

  > 返回 [min, max] 之间的一个整数随机数。
  > 如果只传入一个参数，则另一个参数默认为 0

  ```javascript
  _.random(0, 100); // 42
  ```

* mixin: `_.mixin(obj)`

  > 使用自定义的函数扩展 Underscore 功能。
  > 传入 {name: function} 型的定义体。

  ```javascript
  _.mixin({
    capitalize: function(str){
        return str.charAt(0).toUpperCase();
    }
  });
  // 本例使用 underscore 面向对象语法
  _("fabio").capitalize(); //"Fabio"
  ```

* iteratee: `_.iteratee(value, [context])`

  > 创建一个可作用于集合中每个元素的回调函数。
  > 针对一些常用的回调用例，_.iteratee 支持
  > 一些简写方式，基于 `value` 的类型，_.iteratee
  > 将返回:

  ```javascript
  // 无参数
  _.iteratee(); // _.identity()

  // 函数参数
  _.iteratee(function(n) {
    return n * 2; 
  }); // function(n){ return n*2; }

  // 对象参数
  _.iteratee({firstName: 'Chelsea'});
  //=> _.matcher({firstName: 'Chelsea'})

  //其它参数
  _.iteratee('firstName');
  //=> _.property('firstName');
  ```
  > 下面的这些 Underscore 函数都是通过 _.iteratee 变换来的：
  > countBy, every, filter, find, findIndex, findKey, 
  > findLastIndex, groupBy, indexBy, map, mapObject,
  > max, min, partition, reject, some, sortBy, 
  > sortedIndex, uniq


* uniqueId: `_.uniqueId([prefix])`

  > 为客户端数据模型和 DOM 元素产生
  > 一个全局的唯一 ID。
  > 如果有 prefix 传入，会添加在 ID 前。

  ```javascript
  _.uniqueId('contact_'); // 'contact_104'
  ```

* escape: `_.escape(str)`

  > 转义 HTML 的特殊字符，替换 `&, <, >, ", '` 等字符。

  ```javascript
  _.escape('Curly, Larry & Moe'); // 'Curly, Larry &amp; Moe'
  ```

* unescape: `_.unescape(str)`

  > 和 escape 相反。

  ```javascript
  _.unescape('Curly, Larry &amp; Moe'); //'Curly, Larry & Moe'
  ```

* result: `_.result(obj, property, [defaultVal])`

  > 如果 property 是一个函数，返回值是该函数以 obj 为上下文
  > 运行的返回值，如果是属性则直接返回属性值。
  > 如果属性不存在或为 undefined，则返回 defaultVal，
  > 如果 defaultVal 是一个函数，则返回 defaultVal 的调用返回值。

  ```javascript
  var obj = {cheese: 'crumpets', 
            stuff: function(){ return 'nonsense'; }
  };
  _.result(obj, 'cheese'); //'crumpets'
  _.result(obj, 'stuff'); // 'nonsense'
  _.result(obj, 'meat', 'ham'); // 'ham'
  ```

* now: `_.now()`

  > 返回当前时间的整数值，并尽可能用速度最快的方法实现该功能。
  > 实现计时/动画时很有用。

  ```javascript
  _now(); //1392066795351
  ```

* template: `_.template(templateString, [settings])`

  > 将 JavaScript 模板编译成函数，并在呈现时运行。
  > 在基于 JSON 数据源呈现复杂 HTML 段时很有用。
  > 模板函数即能解析在 {% raw %}<%= ... %>{% endraw %} 间的值，也能运行在
  > {% raw %}<% ... %>{% endraw %} 间的任意 JavaScript 代码。
  > 如果要想将值插入后进行转义，用 {% raw %}<%- ... %>{% endraw %}。
  > 在运行模板函数时，传入包含模板变量值的一个对象。
  > settings 参数是一个 {name:value} 型的对象，包含
  > 用来覆盖 _.templateSettings 的一些设置项。

  ```javascript
  {% raw %}
  var compiled = _.template("hello: <%= name %>");
  compiled({name: 'moe'}); // 'hello: moe'

  var template = _.template("<b><%- value %></b>");
  template({value: '<script>'});
  //=> "<b>&lt;script&gt;</b>"
  {% endraw %}
  ```

  > 也可以在 JavaScript 代码中使用 print：

  ```javascript
  {% raw %}
  var compiled = _.template("<% print('Hello ' + epithet); %>");
  compiled({epithet: "stooge"}); // Hello stooge
  {% endraw %}
  ```

  > 也可以修改模板使用的默认变量嵌入符。
  > 例如替换为 [Mustache.js](https://github.com/janl/mustache.js) 风格：

  ```javascript
  _.templateSettings = {
    // 定义正则表达式来匹配嵌入位置，Mustache.js 风格
    interpolate: /\{\{(.+?)\}\}/g
  };

  var template = _.template("Hello {{ name }}!");
  template({name: "Mustache"}); //"Hello Mustache!"
  ```

  > 预编译过的模板在运行出错时可提供行号和堆栈，
  > 有利于调试。模板的 source 属性可查看模板的源码：

  ```html
  {% raw %}
  <script>
    JST.project = <%= _.template(jstText).source %>;
  </script>
  {% endraw %}
  ```

* # 参考 

+ [Underscorejs.org](http://underscorejs.org/)
