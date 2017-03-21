---
title: Underscore 中的集合函数
date: 2017-03-21
writing-time: 2017-03-21 15:01
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量的函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行了修改。

# 安装

Node.js : `npm install underscore`
Meteor.js: `meteor add underscore`
Require.js: `require(["underscore"], ...`
Bower: `bower install underscore`
Component: `component install jashkenas/underscore`

# 集合函数（数组或对象）

* each:  `_.each(list, iteratee, [context])`, 别名: forEach

  > 遍历列表中的元素，将每个元素传入 iteratee 函数。如何有传入 context,
  > 则将 iteratee 上下文绑定到 context 对象。每次调用 iteratee 都有 3
  > 个参数 (element, index, list)。如果 list 是一个 JavaScript 对象，iteratee
  > 的参数都为 (value, key, list)

  ```javascript
  _.each([1, 2, 3], alert); // 按序 alert 每个数字
  _.each({one: 1, two: 2, three: 3}, alert); // 按序 alert 每个数字
  ```

  > 注意：集合函数可用于数组，对象和数组型的对象如 arguments, NodeList 等。
  > each 循环是不能中断的，要中断用 _.find。

* map: `_.map(list, iteratee, [context])`, 别名: collect

  > 遍历列表中的元素，将每个元素传入 iteratee 函数。如何有传入 context,
  > 则将 iteratee 上下文绑定到 context 对象。每次调用 iteratee 都有 3
  > 个参数 (element, index, list)。如果 list 是一个 JavaScript 对象，iteratee
  > 的参数都为 (value, key, list)

  ```javascript
  _.each([1, 2, 3], alert); // 按序 alert 每个数字
  _.each({one: 1, two: 2, three: 3}, alert); // 按序 alert 每个数字
  ```

  > 注意：集合函数可用于数组，对象和数组型的对象如 arguments, NodeList 等。
  > each 循环是不能中断的，要中断用 _.find。






# 参考 

+ [Underscorejs.org](http://underscorejs.org/)
