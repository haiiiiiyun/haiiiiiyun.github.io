---
title: Underscore.js 中适用于集合的函数
date: 2017-03-21
writing-time: 2017-03-21 15:01--20:11
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。

# 安装

+ Node.js : `npm install underscore`
+ Meteor.js: `meteor add underscore`
+ Require.js: `require(["underscore"], ...`
+ Bower: `bower install underscore`
+ Component: `component install jashkenas/underscore`

# 适用于集合（数组或对象）的函数

* each:  `_.each(list, iteratee, [context])`, 别名: forEach

  > 遍历列表中的元素，将每个元素传入 iteratee 函数。如何有传入 context,
  > 则将 iteratee 上下文绑定到 context 对象。每次调用 iteratee 都有 3
  > 个参数 (element, index, list)。如果 list 是一个 JavaScript 对象，iteratee
  > 的参数将为 (value, key, list)。
  > 注意：这些函数可用于数组，对象和类似数组的对象(ducking type)， 如 arguments 和 NodeList 等。
  > each 循环是不能中断的，要中断用 _.find。

  ```javascript
  _.each([1, 2, 3], alert); // 按序 alert 每个数字
  _.each({one: 1, two: 2, three: 3}, alert); // 按序 alert 每个数字
  ```

* map: `_.map(list, iteratee, [context])`, 别名: collect

  > 将 list 中的每次元素通过 iteratee 函数进行变换，从而生成一个
  > 新的数组。iteratee 会传入 3 个参数 (value, index/key, list)

  ```javascript
  _.map([1, 2, 3], function(num){
      return num*3; 
  }); // [3, 6, 9]

  _.map({one: 1, two: 2, three: 3}, function(num, key) {
    return num*3; 
}); // [3, 6, 9]

  _.map([[1, 2], [3, 4], _.first); // [1, 3]
  ```

* reduce: `_.reduce(list, iteratee, [memo], [context])`, 别名: inject, foldl

  > 将列表 list 归结为一个值。memo 是归结函数 iteratee 的初始状态值，
  > iteratee 每次归结后都将返回值作为下一次归结操作的状态值。
  > iteratee 会传入 4 个参数：(memo, value, index/key, list)。
  > 如果调用 reduce 时没有传入 memo，那么 list 的首个元素将作为 memo，
  > 而从第 2 个元素开始进行归结操作。

  ```javascript
  var sum = _.reduce([1, 2, 3], function(memo, num){
      return memo + num; 0;
  });// 6
  ```

* reduceRight: `_.reduceRight(list, iteratee, [memo], [context])`, 别名: foldr

  > reduce 的右序版本，foldr 在 JavaScript 中用处不是很大，
  > 但是在有 lazy evaluation 的语言中很有用

  ```javascript
  var list = [[0, 1], [2, 3], [4, 5]];
  var flat = _.reduceRight(list, function(a, b){
    return a.concat(b); 
  }, []); // [4, 5, 2, 3, 0, 1]
  ```

* find: `_._find(list, predicate, [context])`, 别名: detect

  > 遍历 list 中的每个值，一旦碰到某个能通过 predicate 函数测试（即返回值为真）的值时，
  > 就立即返回该值。如果遍历完后都未找到，则返回 undefined。
  > 该函数找到符合的元素时就会立即返回，因此有可能没有遍历完整个 list。

  ```javascript
  var even = _.find([1, 2, 3, 4, 5, 6], function(num) {
    return num % 2 == 0; 
  }); // 2
  ```

* filter: `_.filter(list, predicate, [context])`, 别名: select

  > 遍历 list 的每个值，将那些能通过 predicate 函数测试的值组成一个数组，并返回。

  ```javascript
  var even = _.find([1, 2, 3, 4, 5, 6], function(num) {
    return num % 2 == 0; 
  }); // [2, 4, 6]
  ```

* where: `_.where(list, properties)`

  > 遍历 list, 将 list 中的那些包含 properties 中的所有键值对的元素组成一个新数组并返回。

  ```javascript
  var listOfPlays = [{title: "Cymbeline", author: "Shakespeare", year: 1611},
                      {title: "The Tempest", author: "Shakespeare", year: 1611},
                      {title: "Hello world", author: "JS", year: 2017}]
  _.where(listOfPlays, {author: "Shakespeare", year: 1611}) // [
                                                            // {title: "Cymbeline", author: "Shakespeare", year: 1611},
                                                            // {title: "The Tempest", author: "Shakespeare", year: 1611} 
                                                            // ]
  ```

* findWhere: `_.findWhere(list, properties)`

  > 遍历过程和 where 一样，但是一旦找到相符元素时，就立即返回。
  > 如果没有相匹配元素，或者 list 为空，返回 undefined

  ```javascript
  var listOfPlays = [{title: "Cymbeline", author: "Shakespeare", year: 1611},
                      {title: "The Tempest", author: "Shakespeare", year: 1611},
                      {title: "Hello world", author: "JS", year: 2017}]
  _.findWhere(listOfPlays, {author: "Shakespeare", year: 1611}) // {title: "Cymbeline", author: "Shakespeare", year: 1611}
  ```

* reject: `_.reject(list, predicate, [context])`

  > 正好与 filter 相反。
  > 遍历 list 的每个值，将那些不能通过 predicate 函数测试的值组成一个数组，并返回。

  ```javascript
  var odds = _.reject([1, 2, 3, 4, 5, 6], function(num) {
    return num % 2 == 0; 
  }); // [1, 3, 5]
  ```

* every: `_.every(list, [predicate], [context])`, 别名: all

  > 只有 list 中的所有元素都通过 predicate 测试地才返回 true。
  > 一旦有某个元素不符合就立即返回 false，因此可能没有遍历完 list。

  ```javascript
  _.every([2, 4, 5], function(num) { return num % 2 == 0; }); // false
  ```

* some: `_.some(list, [predicate], [context])`, 别名: any

  > 一旦 list 中的某个元素通过 predicate 测试，就返回 true。
  > 因此可能没有遍历完 list。

  ```javascript
  _.some([null, 0, 'yes', false]); // true
  ```

* contains: `_.contains(list, value, [fromIndex])`, 别名: includes

  > 如果 value 存在于 list 中，则返回 true。
  > 当 list 是数组时，内部使用 indexOf 实现。
  > 使用 fromIndex 指定搜索的开始位置。

  ```javascript
  _.contains([1, 2, 3], 3); // true
  ```

* invoke: `_.invoke(list, methodName, *arguments)`

  > 将 list 中的每个元素都进行方法名为 methodName 的方法调用。
  > 如果有 *arguments，也一并传入方法调用中。

  ```javascript
  _.invoke([ [5, 1, 7], [3, 2, 1] ], 'sort'); // [ [1, 5, 7], [1, 2 3] ]
  ```

* pluck: `_.pluck(list, propertyName)`

  > 这是 map 的最常用形式的一种简写，
  > 它抽取列表元素的某个属性值，并组成数组返回。

  ```javascript
  var stooges = [{name: 'moe', age: 40},
      {name: 'larry', age: 50}, {name: 'curly', age: 60}];
  _.pluck(stooges, 'name'); // ['moe', 'larry', 'curly']
  ```

* max: `_.max(list, [iteratee], [context])`

  > 返回列表中的最大值元素。
  > 如果有提供 iteratee 函数，则用来从每个列表元素中抽取出比较的因子。
  > 当 list 为空时返回 Infinity，因此可能要预先使用 isEmpty。
  > 列表中的非数字值将会忽略。

  ```javascript
  var stooges = [{name: 'moe', age: 40},
        {name: 'larry', age: 50}, {name: 'curly', age: 60}];
  _.max(stooges, function(stooge) {
    return stooge.age; 
  }); // {name: 'curly', age: 60}
  ```

* min: `_.min(list, [iteratee], [context])`

  > 类似 max，但返回最小值元素。

  ```javascript
  var stooges = [{name: 'moe', age: 40},
    {name: 'larry', age: 50}, {name: 'curly', age: 60}];
  _.min(stooges, function(stooge) {
    return stooge.age; 
  }); // {name: 'moe', age: 40}
  ```

* sortBy: `_.sortBy(list, iteratee, [context])`

  > 返回 list 的一个（稳定的）已排序复本。
  > list 中的每个元素经过 iteratee 产生排序因子，并进行升序排序。
  > iteratee 也可以是一个字符串，表示 list 中元素的属性，如("length")

  ```javascript
  _.sortBy([1, 2, 3, 4, 5, 6], function(num){
    return Math.sin(num); 
  }); // [5, 4, 6, 3, 1, 2]

  var stooges = [{name: 'moe', age: 40},
    {name: 'larry', age: 50}, {name: 'curly', age: 60}];
  _.sortBy(stooges, 'name'); // [
                             //  {name: 'curly', age: 60},
                             //  {name: 'larry', age: 50},
                             // {name: 'moe', age: 40}]
  ```

* groupBy: `_.groupBy(list, iteratee, [context])`

  > 将 list 中的元素通过 iteratee 产生分组因子，
  > 并根据分组因子将 list 分组。
  > iteratee 也可以是一个字符串，表示按 list 中元素的属性值分组。

  ```javascript
  _.groupBy([1.3, 2.1, 2.4], function(num){ 
    return Math.floor(num); 
  }); // {1: [1.3], 2: [2.1, 2.4]}

  _.groupBy(['one', 'two', 'three'], 'length'); // {
                                                // 3: ['one', 'two'],
                                                // 5: ['three']
                                                // }
  ```

* indexBy: `_.indexBy(list, iteratee, [context])`

  > list 中的每个元素，通过 iteratee（或属性名）生成一个键，
  > 键与 list 中对应的元素组成一个键值对。
  > 从而组成一个键值对对象返回。
  > 和 groupBy 类型，只不过每个键都是唯一的。

  ```javascript
  var stooges = [{name: 'moe', age: 40},
    {name: 'larry', age: 50}, {name: 'curly', age: 60}];
  _.indexBy(stooges, 'age');// { "40": {name: 'meo', age:40},
                            //   "50": {name: 'larry', age: 50},
                            //   "60": {name: 'curly', age: 60}
                            // }
  ```

* countBy: `_.countBy(list, iteratee, [context])`

  > 与 groupBy 类似，先将 list 分组，但是不返回值列表，返回值列表的个数。

  ```javascript
  _.countBy([1, 2, 3, 4, 5], function(num){
    return num % 2 == 0 ? 'even': 'odd';
  }); // {odd: 3, even: 2}
  ```

* shuffle: `_.shuffle(list)`

  > 返回 list 的一个乱序复本，使用 [Fisher-Yates shuffle](http://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle) 算法。

  ```javascript
  _.shuffle([1, 2 , 3, 4, 5, 6]); // [4, 1, 6, 3, 5, 2]
  ```

* sample: `_.sample(list, [n])`

  > 根据 list 中的值返回一个随机样本，
  > 传入 n 时会返回有 n 个元素的样本列表，
  > 否则返回单个值。

  ```javascript
  _.sample([1, 2, 3, 4, 5, 6]); // 4

  _.sample([1, 2, 3, 4, 5, 6], 3); // [1, 6, 2]
  ```

* toArray: `_.toArray(list)`

  > 从 list（或任何可迭代对象）创建一个真正的数组。
  > 在处理 arguments 对象时很有用。

  ```javascript
  (function(){
    return _.toArray(arguments).slice(1);
  })(1, 2, 3, 4); // [2, 3, 4]
  ```

* size: `_.size(list)`

  > 返回列表的元素个数

  ```javascript
  _.size({one: 1, two: 2, three: 3}); // 3
  ```

* partition: `_.partition(array, predicate)`

  > 将数组分割成 2 个数组：能通过 predicate 测试的
  > 所有元素在一组，不能通过测试的在另一组。

  ```javascript
  _.partition([0, 1, 2, 3, 4, 5], function(num){
    return num % 2 == 0;
}); // [[0, 2, 4], [1, 3, 5]]
  ```


# 参考 

+ [Underscorejs.org](http://underscorejs.org/)
