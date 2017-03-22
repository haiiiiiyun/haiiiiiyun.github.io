---
title: Underscore.js 中适用于对象的函数
date: 2017-03-22
writing-time: 2017-03-22 11:15--15:04
categories: Programming
tags: Programming JavaScript Node underscore
---

# 概述

[Underscore](http://github.com/jashkenas/underscore/) 是一个 JavaScript 库，它提供了大量用于函数式编程的辅助函数，同时并末对内置的 JavaScript 对象进行修改。


# 适用于对象的函数

* keys: `_.keys(obj)`

  > 将 obj 中所有自有的可枚举属性名作为数组返回。

  ```javascript
  _.keys({one: 1, two: 2, three: 3}); //["one", "two", "three"]
  ```


* allKeys: `_.allKeys(obj)`

  > 类似 keys，但返回的是自有及继承的属性名。

  ```javascript
  function Stooge(name){
    this.name = name;
  }
  Stooge.prototype.silly = true;
  _.allKeys(new Stooge("Moe")); // ["name", "silly"]
  ```


* values: `_.values(obj)`

  > 将 obj 中所有自有的属性值作为数组返回。

  ```javascript
  _.values({one: 1, two: 2, three: 3}); //[1, 2, 3]
  ```


* mapObject: `_.mapObject(obj, iteratee, [context])`

  > 类似 map。但将 obj 中的每个属性值进行变换。

  ```javascript
  _.mapObject({start: 5, end: 12}, function(val, key){
    return val + 5;
  }); //{start: 10, end: 17}
  ```


* pairs: `_.pairs(obj)`

  > 将 obj 转换成 [key, value] 对的数组返回

  ```javascript
  _.pairs({one: 1, two: 2, three: 3});
  //[["one",1], ["two",2], ["three",3]]
  ```


* invert: `_.invert(obj)`

  > 返回 obj 的一个复本，但将键与值进行对调。
  > obj 的每个值都必须是唯一的，且可序列化成字符串。

  ```javascript
  _.invert({Moe: "Moses", Larry: "Louis", Curly: "Jerome"});
  //{Moses: "Moe", Louis: "Larry", Jerome: "Curly"};
  ```


* create: `_.create(prototype, props)`

  > 用给定的原型创建一个新对象，
  > 并将 props 中的属性关联为新建对象的属性。
  > 类似于 Object.create

  ```javascript
  function Stooge(name){
    this.name = name;
  }
  var moe = _.create(Stooge.prototype, {name: "Moe"});
  ```


* functions: `_.functions(obj)`, 别名: methods

  > 返回 obj 的所有方法名的一个已排序数组

  ```javascript
  _.functions(_); // ["all", "any", "bind", ....]
  ```


* findKey: `_.findKey(obj, predicate, [context])`

  > 类似 findIndex。
  > 返回 obj 中能通过 predicate 测试的键，
  > 未找到返回 undefined


* extend: `_.extend(dest, *sources)`

  > 将所有 sources 对象中的所有属性都
  > 复制(shallow copy) 到 dest，并返回 dest。
  > 所有嵌套的对象或数组都使用引用复制，不会重复。
  > 按序进行，因此如果有相同的属性名，
  > 后面 source 中的会覆盖前面的。

  ```javascript
  _.extend({name: 'moe', {age: 50});//{name: 'moe', age: 50}
  ```


* extendOwn: `_.extendOwn(dest, *sources)`, 别名: assign

  > 类似 extend，但只复制自有（非继承）属性。


* pick: `_.pick(obj, *keys)`

  > 返回 obj 的一个复本，但过滤只包含在 *keys 中的键值对。
  > 或者也可以传入一个 predicate 函数，用来决定抽取哪些键值对。

  ```javascript
  _.pick({name: 'moe', age: 50, userid: 'moe1'}, 'name', 'age');
  // => {name: 'moe', age: 50}

  _.pick({name: 'moe', age: 50, userid: 'moe1'}, function(v, k, obj){
    return _.isNumber(v);
  }); // {age: 50}
  ```


* omit: `_.omit(obj, *keys)`

  > 正好与 pick 相反，*keys 指定的是排除在返回复本中的键。
  > 同样也可以传入一个 predicate 函数，用来决定排除的键值对。

  ```javascript
  _.pick({name: 'moe', age: 50, userid: 'moe1'}, 'userid');
  // => {name: 'moe', age: 50}

  _.pick({name: 'moe', age: 50, userid: 'moe1'}, function(v, k, obj){
    return _.isNumber(v);
  }); // {name: 'moe', userid: 'moe1'}
  ```


* defaults: `_.defaults(obj, *defaults)`

  > 用 *defaults 中的值作为 obj 中未定义属性的默认值。

  ```javascript
  var iceCream = {flavor: "chocolate"};
  _.defaults(iceCream, {flavor: "vanilla", sprinkles: 'lots'});
  // => {flavor: "chocolate", sprinkles: "lots"}
  ```


* clone: `_.clone(obj)`

  > 创建 obj 的一个复本(shallow copy)。
  > 所有嵌套的对象或数组都使用引用复制，不会重复。

  ```javascript
  _.clone({name: 'moe'}); // {name: 'moe'}
  ```


* tap: `_.tap(obj, interceptor)`

  > 用 obj 来调用 interceptor 函数，然后再返回原 obj。
  > 该函数的主要目的是插入到一个函数链中，从而在链的
  > 中间结果上进行一些操作。

  ```javascript
  _.chain([1, 2, 3, 200])
   .filter(function(num){ return num % == 0; })
   .tap(alert) // alert [2, 200],
   .map(function(num){ return num*num; })
   .value(); // [4, 40000]
  ```


* has: `_.has(obj, key)`

  > 对象是否含有 key 键? 等同于 `obj.hasOwnProperty(key)`，
  > 但是在[意外覆盖](http://www.devthought.com/2012/01/18/an-object-is-not-a-hash/)
  > 的情况下，它使用了 hasOwnProperty 方法的一个安全引用。

  ```javascript
  _.has({a: 1, b: 2}, 'b'); // true
  ```


* property: `_.property(key)`

  > 返回一个函数。
  > 该函数会返回传入对象的 key 属性值。

  ```javascript
  var stooge = {name: 'moe'};
  'moe' === _.property('name')(stooge); // true
  ```


* propertyOf: `_.propertyOf(obj)`

  > 和 property 相反。
  > 返回一个函数。
  > 该函数会返回传入的属性名对应的属性名。

  ```javascript
  var stooge = {name: 'moe'};
  _.propertyOf(stooge)('name'); // 'moe'
  ```


* matcher: `_.matcher(attrs)`, 别名: mathes

  > 返回一个 predicate 函数。
  > 该函数会判断传入的参数对象是否包含所有 attrs 中的键值对。

  ```javascript
  var ready = _.matcher({selected: true, visible: true});
  var readyList = _.filter(list, ready);
  ```


* isEqual: `_.isEqual(obj, other)`

  > 在两个对象间进行优化了的深度比较，以决定是否相等。

  ```javascript
  var stooge = {name: 'moe', luckyNumbers: [12, 27, 34]};
  var clone = {name: 'moe', luckyNumbers: [12, 27, 34]};
  stooge == clone; // false
  _.isEqual(Stooge, clone); // true
  ```


* isMatch: `_.isMatch(obj, properties)`

  > 决断 properties 中的键值对是否包含在 obj 中。

  ```javascript
  var stooge = {name: 'moe', age: 32};
  _.isMatch(stooge, {age: 32}); // true
  ```


* isEmpty: `_.isEmpty(obj)`

  > 若可枚举对象不包含值（没有可枚举自有属性）时，返回 true。
  > 对于字符串和数组型的对象，基于 length 属性值判断。

  ```javascript
  _.isEmpty([1, 2]); // false
  _.isEmpty({}); // true
  ```


* isElement: `_.isElement(obj)`

  > 决断 obj 是否是 DOM 元素。

  ```javascript
  _.isElement(jQuery('body')[0]); // true
  ```


* isArray: `_.isArray(obj)`

  > 决断 obj 是否是一个数组

  ```javascript
  (function(){
    return _.isArray(arguments);
  })(); // false
  _.isArray([1, 2]); // true
  ```


* isObject: `_.isObject(value)`

  > 判断 value 是否是一个 Object。
  > 注意 JavaScript 数组和函数也是 Object，
  > 而普通字符串和数字不是。

  ```javascript
  _.isObject({}); // true
  _.isObject(1); // false
  ```


* isArguments: `_.isArguments(obj)`

  > 判断是否是一个 Arguments 对象。

  ```javascript
  (function(){
    return _.isArguments(arguments);
  })(1, 2); // true
  _.isArguments([1, 2]); // false
  ```


* isFunction: `_.isFunction(obj)`

  > 判断是否是一个函数。

  ```javascript
  _.isFunction(alert); // true
  ```


* isString: `_.isString(obj))`

  > 判断是否是一个字符串

  ```javascript
  _.isString("moe"); // true
  ```


* isNumber: `_.isNumber(obj)`

  > 判断是否是一个数字（含 NaN）

  ```javascript
  _.isNumber(8.4*5); //true
  ```


* isFinite: `_.isFinite(obj)`

  > 判断是否是一个有限数字

  ```javascript
  _.isFinite(-101); // true
  _.isFinite(-Infinity); // false
  ```


* isBoolean: `_.isBoolean(obj)`

  > 判断对象要么是 true, 要么是 false

  ```javascript
  _.isBoolean(null); // false
  _.isBoolean(false); //true
  ```


* isDate: `_.isDate(obj)`

  > 判断是否是一个 Date 对象

  ```javascript
  _.isDate(new Date()); // true
  ```


* isRegExp: `_.isRegExp(obj)`

  > 判断是否是一个 RegExp

  ```javascript
  _.isRegExp(/moe/); // true
  ```


* isError: `_.isError(obj)`

  > 判断 obj 是否继承至 Error

  ```javascript
  try {
    throw new TypeError("Error");
  } catch (o_0){
    _.isError(o_0); // true
  }
  ```


* isNaN: `_.isNaN(obj)`

  > 判断是否是一个 NaN。
  > 注：这和内置的 isNaN 不同，
  > 内置的当碰到非数字值（如 undefined）时也返回 true

  ```javascript
  _.isNaN(NaN); // true
  isNaN(undefined); // true
  _.isNaN(undefined); // false
  ```


* isNull: `_.isNull(obj)`

  > 判断 obj 是否是 null

  ```javascript
  _.isNull(null); // true
  _.isNull(undefined); //false
  ```


* isUndefined: `_.isUndefined(obj)`

  > 判断 obj 是否是 undefined

  ```javascript
  _.isUndefined(window.missingVariable); // true
  ```

* # 参考 

+ [Underscorejs.org](http://underscorejs.org/)
