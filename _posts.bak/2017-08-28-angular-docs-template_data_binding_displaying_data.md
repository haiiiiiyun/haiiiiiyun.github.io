---
title: Angular docs-模板与数据绑定-显示数据
date: 2017-08-28
writing-time: 2017-08-28
categories: programming
tags: angular node Angular&nbsp;docs
---

# 模板与数据绑定-显示数据


## 使用 `{{var}}` 来显示组件属性值

项目为 `displaying-data`。例子为 :

```typescript
//src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <h2>My favorite hero is: {{myHero}}</h2>
    `
})
export class AppComponent {
  title = 'Tour of Heroes';
  myHero = 'Windstorm';
}
```

Angular 自动从组件中提取 `title` 和 `myHero` 这两个属性的值，并插入到 DOM 中。同时当这两个属性值有变动时，也会自动更新 DOM 中的对应信息（更加确切地说，更新发生在一些与该视图相关的异步事件之后，例如 keystroke, timer competion, HTTP 请求应答等）。

注意我们没有调用 `new` 来创建 `AppComponent` 实例。Angular 会自动创建。当在 `main.ts` 中启动`AppComponent` 后，Angular 会在 `index.html` 中看到 `<my-app>` 标签，此时，它将实例化一个 `AppComponent` 实例，并将它呈现在 `<my-app>` 标签中。


## 使用构造器还是用变量赋值法

上例是直接使用变量赋值法的（更加简洁）。不过也可以先声明属性，再在构造器中初始化，它们是造价的。如下：

```typescript
//src/app/app-ctor.component.ts (class)
export class AppCtorComponent {
  title: string;
  myHero: string;

  constructor() {
    this.title = 'Tour of Heroes';
    this.myHero = 'Windstorm';
  }
}
```

## 使用构造器参数隐式创建属性的 TypeScript 简写法

```typescript
//src/app/hero.ts (excerpt)
export class Hero {
  constructor(
    public id: number,
    public name: string) { }
}
```

这样就通过构造器参数隐式创建了两个属性： `id` 和 `name`。

以 `public id: number,` 为例，这个简洁写法含义有：

+ 声明了一个构造器参数及其类型
+ 声明了一个同名的公开属性
+ 当创建该类的实例时，用对应参数值一并初始化该属性

## 参考

+ https://angular.io/guide/displaying-data
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_displaying_data.ipynb)
