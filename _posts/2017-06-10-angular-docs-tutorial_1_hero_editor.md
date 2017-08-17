---
title: Angular docs-教程 1： Hero Editor
date: 2017-06-10
writing-time: 2017-08-17
categories: programming
tags: angular node Angular&nbsp;docs
---

# 教程 1： Hero Editor

运行以下命令：

```bash
$ npm start
```

该命令使 TypeScript 编译器进入“侦听模式”，当代码有修改时会自动重编译，同时刷新浏览器内的页面。功能类似 `ng serve`。

## 显示 hero

在主组件 `AppComponent` 中添加属性： `title` 应用名，`hero` 属性是一个英雄名。

```typescript
//file: app.component.ts (AppComponent class)
export class AppComponent {
  title = 'Tour of Heroes';
  hero = 'Windstorm';
}
```

同时在相同文件中的 `@Component` 部分更新模板 template 设置，将数据绑定到这两个属性上。


```typescript
//file: app.component.ts (@Component)
template: `<h1>{{title}}</h1><h2>{{hero}} details!</h2>`
```

保存后浏览器后自动刷新，现可看到更新了的 title 和 hero name。

这里 `{{}}` 是数据绑定语法，而撇号引号可用来包含多行的字符串。

## Hero 对象

在 src/app/app.component.ts 的前面创建 Hero 类。


```typescript
// src/app/app.component.ts (Hero class)
export class Hero {
  id: number;
  name: string;
}
```

并将 `AppComponent` 中的 `hero` 属性从一个字符串转变成类对象，以存储更多属性值。

```typescript
// src/app/app.component.ts (hero property)
hero: Hero = {
  id: 1,
  name: 'Windstorm'
};
```

同时同步更新 template 中的绑定，使用多行字符串模式，并显示更多的属性值：

```typescript
// app.component.ts (AppComponent's template)
template: `
  <h1>{{title}}</h1>
  <h2>{{hero.name}} details!</h2>
  <div><label>id: </label>{{hero.id}}</div>
  <div><label>name: </label>{{hero.name}}</div>
  `
```

## 编辑 hero 名

用户在 input 中输入名字时，`hero.name` 属性也要相应更新，即 `<input>` 表单元素要和 `hero.name` 进行双向绑定。这通过 `[(ngModel)]` 语法实现。

将 template 中的 name 部分改为：

```typescript
//src/app/app.component.ts
<div>
  <label>name: </label>
  <input [(ngModel)]="hero.name" placeholder="name">
</div>
```

保存后，浏览器控制台会有 `"ngModel ... isn't a known property of input."` 之类的错误。这里因此，虽然 `NgModel` 是 Angular 中的一具有效指令，但是它位于 `FormsModule` 这个可选模块中，要想使用该指令，必须先导入 FormsModule 模块。

打开 `app.module.ts` 文件，从 `@angular/forms` 库中导入 `FormsModule`，然后将它添加到 `@NgModule` 无数据的 `imports` 数组中。

```typescript
//app.module.ts (FormsModule import)
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms'; // <-- NgModel lives here

import { AppComponent }  from './app.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule // <-- import the FormsModule before binding with [(ngModel)]
  ],
  declarations: [
    AppComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 参考

+ https://angular.io/tutorial/toh-pt1
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_1_hero_editor.ipynb)
