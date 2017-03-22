---
title: Underscore.js 中适用于函数的函数
date: 2017-03-22
writing-time: 2017-03-22 09:22--11:05
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。


# 适用于函数对象的函数

* bind: `_.bind(func, obj, *args)`

  > 将函数 func 绑定到 obj，即在调用 func
  > 时，`this` 的值将为该 obj。
  > 如果有传入 *args，这些参数会对 func
  > 进行预填充（称为 partial application）

  ```javascript
  var func = function(greeting){
    return greeting + ': ' + this.name
  };
  func = _.bind(func, {name: 'moe'}, 'hi');
  func(); // 'hi: moe'
  ```


* bindAll: `_.bindAll(obj, *methodNames)`

  > 将 obj 上的多个方法绑定到 obj，
  > 需要绑定的方法由 *methodNames 指定，
  > 从而使这些方法的运行上下文为 obj。
  > 将这些绑定方法用于事件处理函数非常方便。

  ```javascript
  var buttonView = {
    label: 'underscore',
    onClick: function(){
      alert('clicked: ' + this.label);
    },
    onHover: function(){
      console.log('hovering: ' + this.label);
    }
  };
  _.bindAll(buttonView, 'onClick', 'onHover');
  // 当点击该按钮时，this.label 将有正确的值
  jQuery('#underscore_btn').on('click', buttonView.onClick);
  ```


* partial: `_.partial(func, *args)`

  > 将传入的 *args 预填充到 func 的参数中，
  > 而不修改其动态的 `this` 值，类似于 _.bind。
  > 可以在 *args 中传入 `_`，来指定这些
  > 参数不要进行预填充，只能在调用时提供。

  ```javascript
  var subtract = function(a,b){ return b-a; };
  sub5 = _.partial(subtract, 5);// 参数按顺序填充，这里填充了 a
  sub5(20);// 15

  subFrom20 = _.partial(subtract, _, 20);
  subFrom20(5); //15
  ```

* memoize: `_.memoize(func, [hashFunc])`

  > 缓存 func 的计算结果。
  > 常用于缓存耗时长的计算结果。
  > 如果传入 hashFunc，它将基于传入的 func 
  > 计算存储结果的 hash 值。
  > 默认的 hashFunc 将传入的 func 作为 hash 值。
  > 缓存的计算值可通过函数返回对象的 `cache` 属性获取。

  ```javascript
  var fibonacci = _memoize(function(n){
    return n < 2 ? n : fibonacci(n-1) + fibonacci(n-2);
  });

  fibonacci(2).cache; //2
  ```

* delay: `_.delay(func, wait, *args)`

  > 非常像 setTimeout，会在 wait 毫秒后运行 func。
  > 如果有 *args 传入，会在运行 func 时传给 func。

  ```javascript
  var log = _.bind(console.log, console);
  _.delay(log, 1000, 'logged later'); //在 1 秒后显示 "logged later"
  ```

* defer: `_.defer(func, *args)`

  > 对 defer 的调用会立即返回，只在当前调用堆栈清理后才运行 func，
  > 类似于使用 setTimeout，并将 wait 值设为 0。
  > 适用于func 需要进行大量更新 HTML 页面的操作，从而不阻塞当前的 UI 线程。
  > 传入的可选 *args 会在运行 func 时传给 func。

  ```javascript
  _.defer(function(){
    alert('deferred');
  }); // 在运行 alert 前就返回
  ```

* throttle: `_.throttle(func, wait, [options])`

  > 创建并返回 func 的节流版本，即当重复调用时，最多每 
  > wait 毫秒一次调用原 func 函数。
  > 适用于限速的情况。
  > 默认时，throttle 会在你第 1 次调用时立即运行 func，
  > 然后再次调用时会有 wait 毫秒的间隔限制，
  > 如果想禁止在第 1 次调用时就立即运行，传入 {leading:false}，
  > 如果想禁止刚好到(未超过) wait 毫秒时运行 func，
  > 传入 {trailing: false}

  ```javascript
  var throttled = _.throttle(updatePosition, 100);
  $(window).scroll(throttled)
  ```

* debounce: `_.debouce(func, wait, [immediate])`

  > 创建并返回 func 的去抖动版本，即在调用时
  > 会延时至 func 最后一次运行后 wait 毫秒执行。
  > 适用于那些只有停止输入后才进行的操作，例如：
  > 呈现 Markdown 评论的预览，在窗口停止调整大小
  > 后重新计算布局等。
  > 若传入 immediate 的值为 true，则第 1 次调用
  > 时就立即运行 func。
  > 适用于防止意外双击表单的提交按钮进行重复提交的情况。

  ```javascript
  var lazyLayout = _.debounce(calcLayout, 300);
  $(window).resize(lazyLayout);
  ```

* once: `_.once(func)`

  > 创建并返回 func 的只能运行一次的版本。
  > 之后的调用会直接返回第 1 次运行的结果。
  > 适用于初始化函数的情况，从而无需设置一个 flag 标识并以后检测

  ```javascript
  var init = _.once(createApplication);
  init();
  init(); // Application 只创建一次
  ```

* after: `_.after(count, func)`

  > 创建并返回 func 的一个新版本，
  > 该版本只有对该函数调用 count 次后才运行 func。
  > 适用于组合异步操作，从而确保
  > 所有的异步操作完成后再进行处理。

  ```javascript
  var renderNotes = _.after(notes.length, render);
  _.each(notes, function(note){
    note.asyncSave({success: renderNotes});
  }); //只有在所有  notes 保存后，renderNotes 才会运行一次
  ```

* before: `_.before(count, func)`

  > 创建并返回 func 的一个新版本，
  > 该版本的调用不能超过 count 次，
  > 最后一次调用结果会被缓存，
  > 并作为以后调用的结果返回。

  ```javascript
  var monthlyMeeting = _.before(3, askForRaise);
  monthlyMeeting(); // 不能超过 2 次调用
  monthlyMeeting();
  monthlyMeeting(); // 这次及以后调用结果与第 2 次的相同
  ```

* wrap: `_.wrap(func, wrapper)`

  > 将 func 封装在 wrapper 函数中。
  > wrapper 能在调用 func 之前和之后进行一些操作，
  > 如修改参数，条件执行等。

  ```javascript
  var hello = function(name){ return "hello: " + name; };
  hello = _.wrap(hello, function(func){
    return "before, " + func("moe") + ", after";
  });
  hello(); // 'before, hello: moe, after'
  ```

* negate: `_.negate(predicate)`

  > 返回 predicate 函数的否定版本。

  ```javascript
  var isFalsy = _.negate(Boolean);
  _.find([-2, -1, 0, 1, 2], isFalsy); // 0
  ```

* compose: `_.compose(*funcs)`

  > 组合函数 f(), g(), h()，产生 f(g(h()))

  ```javascript
  var greet = function(name){ return "hi: " + name; };
  var exclaim = function(statement) {
    return statement.toUpperCase() + "!";
  };
  welcome('moe'); // 'hi: MOE!'
  ```

* # 参考 

+ [Underscorejs.org](http://underscorejs.org/)
