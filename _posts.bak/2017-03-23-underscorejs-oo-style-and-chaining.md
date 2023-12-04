---
title: Underscore.js 的面向对象风格和链
date: 2017-03-23
writing-time: 2017-03-23 09:51--10:09
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。


# 面向对象风格

Underscore 中的函数即可以函数风格使用，也可以面向对象风格使用。

例如，看下面的等价写法：

```javascript
_.map([1, 2, 3], function(n){ return n*2; }); // functional style
_([1, 2, 3]).map(function(n){ return n*2; }); // oo style
```

# 链

调用 `chain` 将使得所有的后继方法调用，都返回封装对象 (wrapped objects)。当完成计算后，调用 `value` 来获取最终结果。

下面的例子中，通过链接 map/flatten/reduce，以获取歌曲中的每个单词的使用次数：


```javascript
var lyrics = [
  {line: 1, words: "I'm a lumberjack and I'm okay"},
  {line: 2, words: "I sleep all night and I work all day"},
  {line: 3, words: "He's a lumberjack and he's okay"},
  {line: 4, words: "He sleeps all night and he works all day"}
];

_.chain(lyrics)
 .map(function(line){ return line.words.split(' '); }) // 每行的单词数组
 .flatten() // 所有单词数组合并成一个数组
 .reduce(function(counts, word){
    counts[word] = (counts[word] || 0) + 1;
    return counts;
 }, {})
 .value(); // {lumberjack: 2, all: 4, night: 2 ... }
```

链式对象也支持 Array 的方法，因此可以在链中使用 `reverse`，`push` 等方法。


* chain, `_.chain(obj)`

> 返回一个封装对象，在该对象上调用方法都会返回封装对象，直到调用 `value` 方法为止。

```javascript
var stooges = [{name: 'curly', age: 25},
              {name: 'moe', age: 21},
              {name: 'larry', age: 23}];
var youngest = _.chain(stooges)
  .sortBy(function(stooge){ return stooge.age; }) // 按年龄升序排序
  .map(function(stooge){ return stooge.name + ' is ' + stooge.age; })
  .first()
  .value();
=> "moe is 21"
```

* value, `_.chain(obj).value()`

> 抽取封装对象的值。

```javascript
_.chain([1, 2, 3]).reverse().value(); //[3, 2, 1]
```


* # 参考 

+ [Underscorejs.org](http://underscorejs.org/)
