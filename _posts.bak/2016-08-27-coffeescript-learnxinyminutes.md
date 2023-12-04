---
title: CoffeeScript 基础知识(Learn X in Y minutes)
date: 2016-08-27
writing-time: 2016-08-27 14:49--15:28
categories: programming
tags: Coffeescript Javascript LearnXinYminutes
---

CoffeeScript 是门小型语言，它能将语句逐行编译成等价的 Javascript 代码，因此在运行时无需再进行解析。

作为 Javascript 的继任者，它能生成易读、美观且高性能的 JavaScript 代码。

# 安装与运行

先安装 nodejs，再通过 npm 安装 CoffeeScript:

```shell
$ npm install --global coffee-script

$ coffee -v

CoffeeScript version 1.10.0
```

运行 CoffeeScript 的 REPL：

```shell
 $ coffee -c
```

# 基础知识

```coffeescript
# CoffeeScript 是门时髦的语言
# 它紧跟许多现代语言的趋势
# 因此注释方法和 Ruby、Python 一样，使用 # 号

###
块注释像这样，它们直接翻译成结果 JavaScript 代码中的 '/*' 和 '*/'
###

# 赋值:
number   = 42 #=> var number = 42;
opposite = true #=> var opposite = true;

# 条件:
number = -42 if opposite #=> if(opposite) { number = -42; }

# 函数:
square = (x) -> x * x #=> var square = function(x) { return x * x; }

fill = (container, liquid = "coffee") ->
  "Filling the #{container} with #{liquid}..." # 和 Ruby 的一样
#=>var fill;
#
#fill = function(container, liquid) {
#  if (liquid == null) {
#    liquid = "coffee";
#  }
#  返回 "Filling the " + container + " with " + liquid + "...";
#};

# 区间:
list = [1..5] #=> var list = [1, 2, 3, 4, 5]; # 和 Ruby 一样

# 对象:
math =
  root:   Math.sqrt
  square: square
  cube:   (x) -> x * square x
# 或者:
math = {
  root:   Math.sqrt,
  square: square,
  cube:   (x) -> x * square x
}
#=> var math = {
#    "root": Math.sqrt,
#    "square": square,
#    "cube": function(x) { return x * square(x); }
#   };

# Splats:
race = (winner, runners...) ->
  print winner, runners
#=>race = function() {
#    var runners, winner;
#    winner = arguments[0], runners = 2 <= arguments.length ? __slice.call(arguments, 1) : [];
#    return print(winner, runners);
#  };

# 是否存在判断:
alert "I knew it!" if elvis?
#=> if(typeof elvis !== "undefined" && elvis !== null) { alert("I knew it!"); }

# 数组推导:
cubes = (math.cube num for num in list)
#=>cubes = (function() {
#	  var _i, _len, _results;
#	  _results = [];
# 	for (_i = 0, _len = list.length; _i < _len; _i++) {
#		  num = list[_i];
#		  _results.push(math.cube(num));
#	  }
#	  return _results;
# })();

foods = ['broccoli', 'spinach', 'chocolate']
eat food for food in foods when food isnt 'chocolate'
#=>foods = ['broccoli', 'spinach', 'chocolate'];
#
#for (_k = 0, _len2 = foods.length; _k < _len2; _k++) {
#  food = foods[_k];
#  if (food !== 'chocolate') {
#    eat(food);
#  }
#}
```

# 其它资源

- [Smooth CoffeeScript](http://autotelicum.github.io/Smooth-CoffeeScript/)
- [CoffeeScript Ristretto](https://leanpub.com/coffeescript-ristretto/read)
