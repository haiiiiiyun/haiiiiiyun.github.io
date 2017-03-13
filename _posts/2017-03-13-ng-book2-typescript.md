---
title: Angular2 中的 TypeScript
date: 2017-03-13
writing-time: 2017-03-13 22:17
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 概述

Angular2 是用 TypeScript 构建的。ES5 是普通的 JavaScript，ES6 是 ES5 的超集，增加了类和模块的特性，而 TypeScript 是 ES6 的超集，又添加了类型(type) 和注解(annotation) 的特性。

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

TypeScript 增加了类型特性，但是变量也可以不用声明类型，即类型是可选的，从而和与 ES5 兼容。

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
var role: Role = Role.Employee; // -> 0; 因为枚举类型的第一个值默认从 0 开始，然后按 1 递增

enum Role {Employee = 3, Manager, Admin};
var role: Role = Role.Employee; // -> 3; 重新设置初始值，后面的值从 3 开始按 1 递增

enum Role {Employee = 3, Manager = 5, Admin = 7};
var role: Role = Role.Employee; // -> 3; 也可以设置每个命名的值


enum Role {Employee = 3, Manager = 5, Admin = 7};
console.log('Roles: ', Role[3], ',', Role[5], ',', Role[7]) // -> Roles: Employee,Manager,Admin。枚举类型可根据命名值返回对应有命名字符名。

var something: any = 'as string'; // Any 表示可以是任何类型，从而该变量可以赋于任何类型的值
something = 1;
something = [1, 2, 3];

function setName(name: string): void { // Void 类型表示无返回
    this.name = name;
}
```

续 ...










# 参考 

+ [TypeScript](https://www.ng-book.com/2/)
