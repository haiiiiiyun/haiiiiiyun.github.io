---
title: Underscore.js 中适用于数组的函数
date: 2017-03-21
writing-time: 2017-03-21 21:06--22:00
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。

所有数组函数都能应用于 *arguments* 对象。


* first: `_.first(array, [n])`, 别名: head, take

  > 返回数组的首个元素。
  > 如何有传入 n，则返回前 n 个元素。

  ```javascript
  _.first([5, 4, 3, 2, 1]); // 5
  ```

* initial: `_.initial(array, [n])`

  > 返回除最后一个元素外的所有数组元素。
  > 如何有传入 n，则返回除最后 n 个元素外的所有数组元素。
  > 该函数在 arguments 对象上很有用。

  ```javascript
  _.initial([5, 4, 3, 2, 1]); //[5, 4, 3, 2]
  ```

* last: `_.last(array, [n])`

  > 类似 first, 但返回末尾元素。

  ```javascript
  _.last([5, 4, 3, 2, 1]); // 1
  ```

* rest: `_.rest(array, [index])`, 别名: tail, drop

  > 返回数组中从 index 位置开始的剩余元素。
  > 没有传入 index 时，默认为 1，即从第 2 个元素开始。

  ```javascript
  _.rest([5, 4, 3, 2, 1]); //[4, 3, 2, 1]
  ```

* compact: `_.compact(array)`

  > 返回数组的一个复本，复本中去除所有的假值，
  > 假值有 false, null, 0, "", undefined, NaN 等

  ```javascript
  _.compact([0, 1, false, 2, '', 3]);//[1, 2, 3]
  ```

* flatten: `_.flatten(array, [shallow])`

  > 平整化嵌套数组（嵌套深度可任意深）。
  > 如何传入 shallow，则只平整一层。

  ```javascript
  _.flatten([1, [2], [3, [[4]]]]);//[1, 2, 3, 4]

  _.flatten([1, [2], [3, [[4]]]], true);//[1, 2, 3, [[4]]]
  ```

* without: `_.without(array, *values)`

  > 返回数组的一个复本，并去除所有 values 中指定的值

  ```javascript
  _.without([1, 2, 1, 0, 3, 1, 4], 0, 1); //[2, 3, 4]
  ```

* union: `_.union(*arrays)`

  > 返回数组的并集，相同元素按出现顺序显示。

  ```javascript
  _.union([1, 2, 3], [101, 2, 1, 10], [2,1]);//[1, 2, 3, 101, 10]
  ```

* intersection: `_.intersection(*arrays)`

  > 返回数组的交集。

  ```javascript
  _.intersection([1,2,3],[101,2,1,10],[2,1]);//[1,2]
  ```

* difference: `_.difference(array, *others)`

  > 类似 without，返回在 array 中，但不在其它
  > 数组中的元素（差集）

  ```javascript
  _.difference([1,2,3,4,5], [5,2,10]);//[1,3,4]
  ```

* uniq: `_.uniq(array, [isSorted], [iteratee])`, 别名: unique

  > 根据 array 返回一个其中没有重复元素的复本，
  > 使用 === 来测试对象的相等性，
  > 有重复时，只保留最前面的元素。
  > 如何已知数组是排序了的，传入 isSorted 为 true，
  > 从而加速运行。
  > 如何元素的唯一性需要通过变换计算，则传入 iteratee

  ```javascript
  _.uniq([1,2,1,4,1,3]); //[1,2,4,3]
  ```

* zip: `_.zip(*arrays)`

  > 将各数组中相同位置的值合并。适合于矩阵操作。

  ```javascript
  _.zip(['moe', 'larry', 'curly'],
        [30, 40, 50],
        [true, false, false]
); //[
   // ["moe", 30, true],
   // ["larry", 40, false],
   // ["curly", 50, false]
   //]
  ```

* unzip: `_.unzip(array)`

  > 正好与 zip 相反

  ```javascript
  _.unzip([
    ["moe", 30, true],
    ["larry", 40, false],
    ["curly", 50, false]
  ]); // [
      //   ['moe', 'larry', 'curly'],
      //   [30, 40, 50],
      //   [true, false, false]
      // ]
  ```

* object: `_.object(list, [values])`

  > 将数组转成对象。
  > 即可以传入 [键, 值] 对的数组，
  > 也可以传入一个键数组和一个值数组。
  > 当出现重复键时，使用最后那个值。

  ```javascript
  _.object(['moe', 'larry', 'curly'],
    [30, 40, 50]); //{moe:30, larry:40, curly:50}

  _.object([
             ['moe', 30],
             ['larry', 40],
             ['curly', 50]
           ]); //{moe:30, larry:40, curly:50}
  ```

* indexOf: `_.indexOf(array, value, [isSorted])`

  > 返回数组中 value 的索引值，未找到时返回 -1。
  > 如果已知数组已经排序了，则传入 isSorted 值 true，
  > 从而使用二分法搜索算法加快运行。

  ```javascript
  _.indexOf([1, 2, 3], 2); //1
  ```

* lastIndexOf: `_.lastIndexOf(array, value, [fromIndex])`

  > 返回数组中 value 最后出现的索引值，未找到返回 -1。
  > 传入 fromIndex 表示从该位置开始搜索。

  ```javascript
  _.lastIndexOf([1,2,3,1,2,3],2); //4
  ```

* sortedIndex: `_.sortedIndex(list, value, [iteratee], [context])`

  > 使用二分搜索算法来决定 value 应插入 list 中的位置，
  > 从而保持 list 的有序性。
  > 如何提供了 iteratee，它将用来计算 list 中每个元素及
  > value 的排序因子。
  > iteratee 也可以是字符串，表示参与排序的元素的属性名（如 length)

  ```javascript
  _.sortedIndex([10,20,30,40,50],35); //3
    var stooges = [{name: 'moe', age: 40},
        {name: 'curly', age: 60}];
  _.sortedIndex(stooges, {name: 'larry', age: 50}, 'age'); //1
  ```

* findIndex: `_.findIndex(array, predicate, [context])`

  > 类似 indexOf，返回第一个通过 predicate 测试的位置索引，
  > 未找到返回 -1

  ```javascript
  _.findIndex([4,6,8,12], isPrime); // -1

  _.findIndex([4,6,7,12], isPrime); // 2
  ```

* findLastIndex: `_.findLastIndex(array, predicate, [context])`

  > 类似 findIndex，只不过按逆序遍历数组。

  ```javascript
  var users = [{'id': 1, 'name': 'Bob', 'last': 'Brown'},
     {'id': 2, 'name': 'Ted', 'last': 'White'},
     {'id': 3, 'name': 'Frank', 'last': 'James'},
     {'id': 4, 'name': 'Ted', 'last': 'Jones'}];

  _.findLastIndex(users, { name: 'Ted' });// 3
  ```

* range: `_.range([start], stop, [step])`

  > 该函数用于创建整数列表，一般用于 each 和 map 循环。
  > 和 Python 中的 range 函数类似。

  ```javascript
  _.range(5); //[0,1,2,3,4]
  _.range(1, 5); //[1,1,2,3,4]
  _.range(0, 20, 5); //[0, 5, 10, 15]
  _.range(0, -5, -1);//[0,-1,-2,-3,-4]
  _.range(0);//[]
  ```

# 参考 

+ [Underscorejs.org](http://underscorejs.org/)
