---
title: Angular2 中的 TypeScript
date: 2017-03-13
writing-time: 2017-03-13 22:17--2017-03-14 09:33
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 概述

Angular2 是用 TypeScript 构建的。ES5 是普通的 JavaScript，ES6 是 ES5 的超集，增加了类和模块的特性，而 TypeScript 是 ES6 的超集，又增加了类型(type) 和注解(annotation) 的特性。

由于大部分浏览器都只支持 ES5，故需要将 TypeScript 和 ES6 的代码先转换成 ES5 代码才能使用。这种转换工具叫 transpiler 或 transcompiler。TypeScript 的转换器是由 TypeScript 团队开发的，而 ES6 的转换器主要有两个，Google 的 [traceur](https://github.com/google/traceur-compiler) 和 Javascript 社区的 [Babel](https://babeljs.io/)。

TypeScript 是 Microsoft 和 Google 合作开发的语言，这样安装：

```bash
$ sudo npm install -g typescript
```

TypeScript 的新特性有：

+ types
+ classes
+ annotations
+ imports
+ 语言工具，如 destructuring


# TypeScript 的 REPL

安装 [TSUN, TypeScript Upgraded Node](https://github.com/HerringtonDarkholme/typescript-repl)：

```bash
$ sudo npm install -g tsun

$ tsun
TSUN : TypeScript Upgraded Node
type in TypeScript expression to evaluate
type :help for commands in repl

> 
```

# 类型

TypeScript 增加了类型特性，但是变量也可以不用声明类型，即类型是可选的，从而能与 ES5 兼容。

```typescript
var name: string; //声明一个字符串变量

function greetText(name: string): string{ // 函数参数及返回值都声明了类型
    return "Hello " + name;
}

// 以下是内置的类型
var name: string = 'Felipe'; // String
var age: number = 36; // Number, TypeScript 中的 Number 类型都以浮点数表示
var married: boolean = true; // Boolean, 值为 true 或 false

var jobs: Array<string> = ['IBM', 'Microsoft', 'Google']; // 字符串数组，Array 类型由于是一个集合，故要指定集合中的对象的类型
var jobs: string[] = ['IBM', 'Microsoft', 'Google']; // Array 类型也可以用 type[] 形式指定
var jobs: Array<number> = [4, 5, 6]; // 数字数组
var jobs: number[] = [4, 5, 6]; // 数字数组

// 枚举类型 Enum 定义了一组命名数值
enum Role {Employee, Manager, Admin};
var role: Role = Role.Employee; // -> 0; 枚举类型的第一个值默认从 0 开始，然后按 1 递增

enum Role {Employee = 3, Manager, Admin};
var role: Role = Role.Employee; // -> 3; 重新设置初始值，后面的值从 3 开始按 1 递增

enum Role {Employee = 3, Manager = 5, Admin = 7};
var role: Role = Role.Employee; // -> 3; 也可以设置每个命名的值


enum Role {Employee = 3, Manager = 5, Admin = 7};
console.log('Roles: ', Role[3], ',', Role[5], ',', Role[7]) // -> Roles: Employee,Manager,Admin。枚举类型可根据命名值返回对应的命名名称。

var something: any = 'as string'; // Any 表示可以是任何类型，从而该变量可以赋于任何类型的值
something = 1;
something = [1, 2, 3];

function setName(name: string): void { // Void 类型表示无返回
    this.name = name;
}
```

# 类

ES5 只有基于原型的面向对象编程方式，由于不支持类，JavaScript 社区已经发展出一些最佳实践来克服这个短板，见 [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) 和 [Introduction to Object-Oriented Javascript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects)。

而 ES6 已经有内置类了。

```typescript
class Person {  // 用 class 关键字来开始类定义
    first_name: string;  // 这些都是类的属性 (property)，每个属性都可以设置一个可选的类型
    last_name: string;
    age: number;

    // 方法(method) 是在对象实例的上下文中运行的函数，方法内通过 this 关键字引用该对象实例
    // 当方法没有显式声明返回类型时，默认表示返回的类型是 any（注：不返回即返回为 void 也是有效的 any 类型值）
    greet() {
        console.log("Hello", this.first_name);
    }

    // 构造方法是当类创建一个新实例时会执行的一个函数，方法名必须为 constructor，但可以有可选的参数，且不能有返回值。
    // 注意：TypeScript 中一个类只能有一个构造方法，这和 ES6 不同，
    // ES6 中一个类可有多个构造方法，只要每个方法的参数个数不同即可。
    constructor(first_name: string, last_name: string, age: number) {
        this.first_name = first_name;
        this.last_name = last_name;
        this.age = age;
    }
}

// 调用方法，需要先创建一个类实例
var p: Person = new Person('Felipe', 'Coury', 36);
p.greet();
```

## 继承

继承是类从其父类接收行为的一种方法，之后新类可以对这些行为进行覆盖，修改和加强。要深入理解 ES5 中的继承，可参阅 [Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain)。

```typescript
class Report { // 创建一个类作为父类
    data: Array<string>;

    constructor(data: Array<string>) {
        this.data = data;
    }

    run() {
        this.data.forEach(function(line) { console.log(line); });
    }
}

var r: Report = new Report(['First line', 'Second line']);
r.run(); // -> Frist line
         //    Second line

class TabbedReport extends Report { // 使用 extends 关键字实现继承
    headers: Array<string>;

    constructor(headers: string[], values: string[]) {
        super(values); //调用父类的构造方法
        this.headers = headers;
    }

    run() {
        console.log(this.headers);
        super.run(); //调用父类的构造方法
    }
}

var header: string[] = ['Name'];
var data: string[] = ['Alice Green', 'Paul Pfifer', 'Louis Blakenship'];
var r: TabbedReport = new TabbedReport(headers, data);
r.run(); // -> Name
         //    Alice Green
         //    Paul Pfifer
         //    Louis Blakenship
```

# 工具

## Fat Arrow Function

Fat arrow `=>` 是编写函数的快捷写法。

```typescript
var data: string[] = ['Alice Green', 'Paul Pfifer', 'Louis Blakenship'];
data.forEach(function(line) { console.log(line); }); // 这是 ES5 中的函数写法
data.forEach( (line) => console.log(line) ); // 这是 Fat arrow 函数的写法
data.forEach( line => console.log(line) ); // 也可以这样，当函数只有一个参数时，括号可省略
var evens = [2, 4, 6, 8];
var odds = evens.map(v => v+1) // => 语法可以作为表达式
data.forEach( line => {        // 也可作为语句
    console.log(line.toUpperCase());
});

// => 语法的一个重要特性是，它与包围它的代码共享 this。这和用 function 创建的函数
// 的行为是显著不同的。用 function 创建函数同时也创建了函数自己的 this。因此，要访问外围的
// 数据，用 function 创建的函数需要这样写:
var nate = {
    name: "Nate",
    guitars: ["Gibson", "Martin", "Taylor"],
    printGuitars: function() {
        var self = this;
        this.guitars.forEach(function(g){
            // this.name 是未定义的，未要通过 self.name 访问
            console.log(self.name + " plays a " + g);
        });
    }
}

// 而 => 版本的可以为：
var nate = {
    name: "Nate",
    guitars: ["Gibson", "Martin", "Taylor"],
    printGuitars: function() {
        this.guitars.forEach( (g) => {
            console.log(this.name + " plays a " + g);
        });
    }
}
```

## 模板字符串

```typescript
//模板字符串 `string` 在 ES6 中引入。

// 1. 它能用来将字符串的变量自动解析扩展(string interpolation)，从而避免了使用字符串 + 操作：
var first_name = "Nate";
var last_name = "Murray";
var greeting = `Hello ${first_name} ${last_name}`;
console.log(greeting); // Hello Nate Murray

//2. 它可以用来定义多行字符串，如:
var template = `
<div>
  <h1>Hello</h1>
  <p>This is a greate website</p>
</div>
`
```

# TypeScript/ES6 的其它功能

+ Interfaces
+ Generics
+ Importing 和 Exporting Modules
+ Annotations
+ Destructuring


# 参考 

+ [TypeScript](https://www.ng-book.com/2/)
