---
title: Angular docs-表单-启动
date: 2017-10-16
writing-time: 2017-10-16
categories: programming
tags: angular node Angular&nbsp;docs
---


# 启动

新建的工程都会如下的 `AppModule`:

```typescript
//src/app/app.module.ts
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent }  from './app.component';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
```

`@NgModule` 装饰器将 `AppModule` 类装饰为一个 `NgModule` 类，其 metadata 告诉 Angular 如何编译和加载应用：

+ `imports`: 所有需要在浏览器中运行的应用都需要 `BrowserModule`
+ `declarations`: 应用包含的所有组件
+ `bootstrap`: 所有的根组件，Angular 会创建并插入 `index.html` 中

## imports 数组

NgModule（即 Angular 模块）是将相关功能组合在一起的一种方式。Angular 中的很多功能都组合为 NgModule 的形式，如 HTTP 服务的 `HttpModule`，路由功能的 `RouterModule` 等。

当应用需要需要某些功能时，则将相关 NgModule 加入到 `imports` 数组中。同时，只有 `NgModule` 类才能加入该 `imports` 数组中，其它类都不行。

## declarations 数组

通过将组件在该数组中列出，来告诉 Angular 哪些组件属性该 `AppModule`。用个的每个组件都必须先要在一个 `NgModule` 类（这里是 AppModule) 中声明。

自定义的指令和管道，也必须在该数组中声明。除这 3 种类型的类之外的类，都不能放在该数组中（如 NgModule, service, model 类等）。

## bootstrap 数组

启动时，Angular 会创建该数组中列出的所有组件实例，并全部插入到 DOM 中。

每个启动组件都是一个组件树的根。虽然是数组，但一般的应用都只列出一个组件，即根组件（如 `AppComponent`）。

## 在 `main.ts` 中启动

启动应用有多种方式，基于采取何种编译方式和在哪里运行应用。

开始时，可采用 Just-in-Time(JIT) 编译器来动态编译应用，并在浏览器中运行。

推荐在 `src/main.ts` 中启动 JIT 编译型的浏览器应用：

```typescript
//src/main.ts
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule }              from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule);
```

## 参考

+ https://angular.io/guide/bootstrapping
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/bootstrapping.ipynb)
