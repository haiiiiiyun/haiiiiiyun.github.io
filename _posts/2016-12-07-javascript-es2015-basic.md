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

需要注意的是，由于箭头函数绑定上下文的特性，故不能随意在顶层作用域中使用，以防出错，例如：

```javascript
// 假设当前运行环境为浏览器，故顶层上下文为 `window`
let obj = {
    msg: 'pong',

    ping: () => {
        return this.msg; // Warning!
    }
}

obj.ping()  // => undefined
let msg = 'bang!";
obj.ping() // => bang!
```

上面代码中，箭头函数 ping 绑定的上下文是定义它时(即定义 obj 时的作用域 window），故会出现这种情况。

上面的代码等价于：

```javascript
let obj = {
    // ...
    ping: (function() {
        return this.msg; // Warning!
    }).bind(this)
}

// 同样等价于：
let obj = { /* ... */ };
obj.ping = (function() {
    return this.msg;
}).bind(this /* this -> window */)
```

## 模板字符串

模板字符串使用 **`** 代替单/双引号来包围字符串。它支持变量注入和换行。

变量注入的例子：

```javascript
let name = 'Will Wen Gunn'
let title = 'Founder'
let company = 'LikMoon Creation'

let greet = `Hi, I'm ${name}, I am the ${title} at ${company}`
console.log(greet) //=> Hi, I'm Will Wen Gunn, I am the Founder at LikMoon Creation
```

支持换行很适合用于写 SQL 语句：

```javascript
let sql = `
SELECT * FROM Users
WHERE FirstName='Mike'
LIMIT 5;
`
```

## Object Leteral Extensions

### 方法属性可省略 function

```javascript
let obj = {
    // 之前的格式
    foo: function() {
        return 'foo';
    },

    // ES2015 格式
    bar() {
        return 'bar';
    }
}
```

### 支持 __proto__ 注入

将 __proto__ 赋予一个对象，使其成为这个址属性类的一个实例，如：

```javascript
class Foo {
    constructor() {
        this.pingMsg = 'pong';
    }

    ping() {
        console.log(this.pingMsg);
    }
}

let o = {
    __proto__: new Foo()
}

o.ping(); // => pong
```

这个特性的使用场景：想扩展或覆盖一个类的方法，并生成一个实例，但又觉得另外定义一个类感觉浪费时，可以这样：

```javascript
let o = {
    __proto__: new Foo(),
    
    constructor() {
        this.pingMsg = 'alive';
    },

    msg: 'bang',
    yell() {
        console.log(this.msg);
    }
}

o.yell(); // => bang
o.ping(); // => alive
```


### 同名方法属性省略语法

在做 JavaScript 模块化时有用。

例如：

```javascript
// module.js
export default {
    someMethod
}

function someMethod() {
    // ...
}

// app.js
import Module from './module'

Module.someMethod()
```

### 可动态计算的属性名称

例如：

```javascript
let arr = [1, 2, 3]
let arrOut = arr.map(n => {
    return {
        [ n ]: n,
        [ `${n}^2` ]: Math.pow(n, 2)
    }
})

console.dir(arrOut); // =>
    // [
    //    { '1': 1, '1^2': 1 },
    //    { '2': 2, '2^2': 4 },
    //    { '3': 3, '3^2': 9 },
    // ]
```

上面的 **[ n ]** 和 **[ `${n}^2` ]** 就是动态计算对象属性名称的语法。


### 表达式解构

```javascript
// unpack.js

// Matching with object
function search(query) {
    // ...
    // let users_value = [ ... ]
    // let posts_value = [ ... ]
    // ...

    return {
        users: users_value,
        posts: posts_value
    }
}

let { users, posts } = search('fafadsada');
console.log(users); // => 输出 users_value
console.lgo(posts); // => 输出 posts_value

// Matching with array
let [x, y] = [1, 2];
// missing one
let [x, ,y] = [1, 2, 3];

function hello({name: x}) {
    console.log(x);
}
hello({name: 'hy'}); // => hy

// Fail-soft destructuring
var [a] = [];
a === undefined // => true

// Fail-soft destructuring with defaults
var [a=1] = [];
a === 1 // => true
```


## 函数参数

### 参数默认值

在开发类库时较有用，可实现一些可选参数：

```javascript
import fs from 'fs'
import readline from 'readline'
import path from 'path'

function readLineInFile(filename, callback = noop, complete = noop){
    let rl = readline.createInterface({
        input: fs.createReadStream(path.resolve(__dirname, filename))
    })

    rl.on('line', line => {
        // ... do something with the current line
        callback(line)
    })

    rl.on('close', complete)

    return rl
}

function noop() { return false }

readLineInFile('big_file.txt', line => {
    // ...
})
```


### 后续参数

`call` 和 `apply` 方法都是用于切换对象上下文的方法。

`call` 方法的语法为 `call([thisObj[,arg1[, arg2[, [,.argN]]]]])`，参数 thisObj 是可选项，它将被用作当前对象(this值)。 arg1, arg2, , argN 可选项。将被传递方法参数序列。call 方法可以用来代替另一个对象调用一个方法。call 方法可将一个函数的对象上下文从初始的上下文改变为由 thisObj 指定的新对象。如果没有提供 thisObj 参数，那么 Global 对象被用作thisObj。

`apply` 方法的语法为 `apply([thisObj[,argArray]])`，如果 argArray 不是一个有效的数组或者不是 arguments 对象，那么将导致一个 TypeError。　如果没有提供 argArray 和 thisObj 任何一个参数，那么 Global 对象将被用作 thisObj， 并且无法传递任何参数。

如果想实现和 `call` 一样的参数，在 ES2015 之前，需要：

```javascript
function fetchSomethings() {
    var args = [].slice.apply(arguments)
    // ...
}

function doSomeOthers(name) {
    var args = [].slice.apply(arguments, 1)
    // ...
}
```


而在 ES2015 中，可以这样：

```javascript
function fetchSomethings(...args) {
    // ...
}

function doSomeOthers(name, ...args) {
    // ...
}
```

需要注意的是， `...args` 后不能再有参数。

从语言角度看， `arguments` 和 `...args` 可同时使用。但在箭头函数中，由于 arguments 会随上下文绑定到上层，所以在不确定上下文绑定结果的情况下，尽可能不要在箭头函数中再使用 arguments，而用 ...args。

`...args` 在绝大部分场景下可代替 `arguments` 使用，除非在很特殊的场景需要使用到 arguments.callee 和 arguments.caller。不过，在严格模式 （Strict Mode）中，arguments.callee 和 arguments.caller 也是被禁用的。


### 解构传参

...args 还有一个功能：无上下文绑定的 apply。例如：

```javascript
function sum(...args) {
    return args.map(Number)
               .reduce((a, b) => a + b)
}

console.log(sum(...[1, 2, 3])) // => 6
```

## 新的数据结构

ES2015 前已有的数据结构：

+ String 字符串
+ Number 数字 （含整型和浮点型）
+ Boolean 布尔值
+ Object 对象
+ Array 数组


其中，Array 其实是 Object 的一个子类。

### Set 和 WeakSet

集内的元素是唯一的，若添加了已存在的元素，会被忽略：

```javascript
let s = new Set()
s.add('hello').add('world').add('hello')
console.log(s.size) // => 2
console.log(s.has('hello')) // => true
```

WeakSet 是一个特殊的 Set，JavaScript 会检查它包含的元素的变量引用情况。如果元素的引用已被全部解除，则该元素会被删除，以节省内存空间。这意味着无法直接加入数字或者字符串。WeakSet 对元素有严格要求，必须是 Object，当然，可以用 new String('...') 等形式处理元素。

例如：

```javascript
let weaks = new WeakSet()
weaks.add('hello')  // => Error
weaks.add(3.1415)  // => Error

let foo = new String("bar")
let pi = new Number(3.1415)
weaks.add(foo)
weaks.add(pi)
weaks.has(foo) // => true
foo = null
weaks.has(foo) // => false
```

### Map 和 WeakMap

Map 和 Object 非常相似，都是键值对结构。但是 Object 限制键必须是字符串或数字。

而 Map 的键可以是任何对象，例如：

```javascript
let map = new Map()
let object = { id: 1}

map.set(object, 'hello')
map.set('hello', 'world')
map.has(object) // => true
map.get(object) // => hello
```

WeakMap 和 WeakSet 类似，只不过 WeakMap 的键和值都会被检查变量引用，只要其中一个引用被解除，该键值对就会被删除。

例如：

```javascript
let weakm = new WeakMap()
let keyObject = { id: 1 }
let valObject = { score: 100 }

weakm.set(keyObject, valObject)
weakm.get(keyObject) // => { score: 100 }
keyObject = null
weakm.has(keyObject) // => false
```


## 类 Classes

ES2015 中的类也只是一种语法糖，用于定义原型(Prototype)的：

```bash
$ node
> class Foo {}
[Function: Foo]
```

### 类定义的语法

与许多 C 语言家族的语法类似：

```javascript
class Person {
    constructor(name, gender, age) {
        this.name = name
        this.gender = gender
        this.age = age
    }

    isAdult() {
        return this.age >= 18
    }
}

let me = new Person('hy', 'male', 19)
console.log(me.isAdult()) // => true
```

然而，ES2015 中对类的定义依然不支持默认属性的语法：

```javascript
// 理想型
class Person {
    name: String
    gender = 'male'
    // ...
}
```

### 继承

```javascript
class Animal {
    yell() {
        console.log('yell)
    }
}

class Person extends Animal {
    constructor(name, gender, age) {
        super() // must call super before using 'this' if this class has a superclass
        this.name = name
        this.gender = gender
        this.age = age
    }

    isAdult() {
        return this.age >= 18
    }
}

class Man extends Person {
    constructor(name, age) {
        super(name, 'male', age)
    }
}

let me = new Man('hy', 19)
console.log(me.isAdult()) // => true
me.yell()
```


### 静态方法

若希望定义 Man.isMan() 方法用于类型检查，可以：

```javascript
class Man {
    // ...
    static isMan(obj) {
        return obj instanceof Man
    }
}

let me = new Man()
console.log(Man.isMan(me)) // => true
```

但是 ES2015 的类并不能直接支持定义静态成员变量，只能通过在 get 和 set 语句前加 static 实现：

```javascript
class SyncObject {
    // ...
    static get baseUrl() {
        return 'http://example.com/api/sync/'
    }
}
```

ES2015 的类机制的不足：

+ 不支持私有属性 private
+ 不支持静态属性定义，但可用 get 和 set 语句实现
+ 不支持多重继承
+ 没有类似协议 Protocol 和 接口 Interface 等的概念


## 生成器 Generator

### 生成器函数

它与普通函数定义的区别是它需要在 function 后加一个 `*`：

```javascript
function* FunctionName() {
    // ... Generator body
}
```

生成器函数的声明琖也不是必须的，同样可以用匿名函数： `let FunctionName = function*() { /* ... */ }`。

生成器函数中的 yeild 语法，它的作用与 return 有点相似，但它并不退出函数，而是切出生成器运行时。

生成器可以看做是与 Javascript 主线程分离的运行时，经可以被 yield 切回到主线程。每一次生成器运行时被 yield 都可牵出一个值，使其回到主线程，也可以从主线程返回一个值回到生成器运行时中：

```javascript
let inputValue = yield outputValue
```

上面全码中，生成器切出主线程后带出 outputValue，主函数经过处理后，通过 generator.next(inputValue) 把 inputValue 返回到生成器运行时中。

### 使用举例

```javascript

// 创建生成器函数

function* fibo() {
    let [a, b] = [1, 1]

    yield a
    yield b

    while (true) {
        [a, b] = [b, a+b]
        yield b
    }
}

// 创建和启动生成器
let gen = fibo()

// 运行生成器，获取数据
let arr = []
for (let i=0; i<10; i++)
    arr.push(gen.next().value)

console.log(arr) // => [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```


## 模块化

### 全局导入

这是最基本的导入方式，将目标模块中的所有暴露的接口导入到一个命名空间中：

```javascript
import name from 'module-name'
import * as name from 'module-name'
```

### 局部导入

导入模块的部分暴露接口，这在大型的组件开发中很方便，如 React 的组件导入便使用了该特性。

```javascript
import {A, B, C} from 'module-name'

A()
B()
C()
```


### 接口暴露

有下面几种用法：

```javascript
// 暴露单独接口
// module.js
export function method() { /* ... */ }

// main.js
import M from './module'
M.method()
```

```javascript
// 覆盖整个模块的暴露对象
// module.js
export default {
    method1,
    method2
}

// main.js
import M from './module'
M.method1()
```

### 降级兼容

实际应用中，目前还需要用 babel 等工具对代码进行降级兼容，babel 支持 CommonJS，AMD，UMD 等模块化标准的降级兼容：


```bash
$ babel -m common -d dist/common/ src/
$ babel -m amd -d dist/amd/ src/
$ babel -m umd -d dist/umd/ src/
```

参考： [给 JavaScript 初心者的 ES2015 实战](http://www.open-open.com/lib/view/open1447222864319.html)
