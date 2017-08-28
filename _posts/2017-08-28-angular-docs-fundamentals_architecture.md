---
title: Angular docs-体系结构
date: 2017-08-28
writing-time: 2017-08-28
categories: programming
tags: angular node Angular&nbsp;docs
---


# 体系结构

## 概述

写 Angular 应用的方式：用 Angular 化的标签组织 HTML 模板 *template*，编写组件 *component* 类来管理这些模板，在服务 *service* 中添加应用逻辑，最后在模块 *module* 中组合组件和服务。

最后通过启动根模块 *root module* 来加载应用。

![Angular 体系结构](/assets/images/angular-docs/overview2.png)


## 模块 Module

Angular 应用是模块化的，Angular 有自己的模块化系统，叫 *NgModules*。

每个应用都至少有一个 NgModule 类，即 [root module](https://angular.io/guide/bootstrapping)，通常命名为 `AppModule`。

复杂的系统会有多个 module，即每个特性一个 module。

一个 NgModule，实际上就是一个带有 `@NgModule` 装饰器的类。

`NgModule` 装饰函数接收一个 metadata 对象作为参数，该对象中的属性值用来描述该模块。其中最重要的属性有：

+ `declarations`: 属性该模块的视图类。共有 3 种视图类： 组件（component），指令 （directive） 和 管道（pipe）。
+ `exports`: `declarations` 的一个子集，这些能在组件模板和其它模块中可访问。
+ `imports`: 其它模块，它们的导出类要在本模板中声明的组件模板访问。
+ `providers`: 服务（service）的生成器，这里面的服务将变成全局的，可在所有组件中使用。
+ `bootstrap`: 应用的主视图，称为 *root component*。只有 *root module* 才需要设置该属性。


根模块的简单例子：

```typescript
//src/app/app.module.ts
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
@NgModule({
  imports:      [ BrowserModule ],
  providers:    [ Logger ],
  declarations: [ AppComponent ],
  exports:      [ AppComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
```

通过启动根模块来加载应用，在开发时一般在 `main.ts` 中启动 `AppModule`:

```typescript
//src/main.ts
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule);
```


### NgModule vs JavaScript 模块

NgModule 就是带有 `@NgModule` 装饰器的类，它是 Angular 的一个基本特性。

而 JavaScript 自己的模块系统用来管理 JavaScript 的对象集。JavaScript 中一个文件就是一个模块，里面定义的对象都属性该模块。需要公开的对象使用 `export` 关键字声明，而其它模块通过 `import` 语句导入公开的对象后才能使用：

```typescript
import { NgModule }     from '@angular/core';
import { AppComponent } from './app.component';

export class AppModule { }
```

### Angular 库

Angular 带有一些 JavaScript 模块，可认为是库模块，它们的名字中都带有 `@angular` 前缀。通过 `npm` 安装，并使用 `import` 加载。

例如，从库中 `import` `Component` 装饰器：

```typescript
import { Component } from '@angular/core';
```

也可以从库中 `import` NgModule：

```typescript
import { BrowserModule } from '@angular/platform-browser';
```

在上面的 root module 例子中，应用模块需要 `BrowserModule` 中的东西，因此，需要将它添加到 `@NgModule` metadata 的 `imports` 中：

```typescript
imports:      [ BrowserModule ],
```

## 组件 Component

一个组件控制一个视图。

支持视图的组件逻辑定义在一个类中。类通过属性和方法与视图交互。

当用户使用应用过程中，Angular 会自动创建、更新和销毁各组件。而通过 [lifecycle hooks](https://angular.io/guide/lifecycle-hooks)，如 `ngOnInit()`，可以定制组件生命期间各时刻的行为。

## 模板 Template

组件视图通过模板定义。一个模板是用 Angular 化的标签组成的 HTML，如：

```typescript
//src/app/hero-list.component.html
<h2>Hero List</h2>

<p><i>Pick a hero from the list</i></p>
<ul>
  <li *ngFor="let hero of heroes" (click)="selectHero(hero)">
    {{hero.name}}
  </li>
</ul>

<hero-detail *ngIf="selectedHero" [hero]="selectedHero"></hero-detail>
```

![组件树](/assets/images/angular-docs/component-tree.png)



## Metadata

Metadata 告诉 Angular 如何处理一个类。

在 TypeScript 中，通过使用装饰器来关联 metadata，如：

```typescript
//src/app/hero-list.component.ts (metadata)
@Component({
  selector:    'hero-list',
  templateUrl: './hero-list.component.html',
  providers:  [ HeroService ]
})
export class HeroListComponent implements OnInit {
/* . . . */
}
```

![template-metadata-component](/assets/images/angular-docs/template-metadata-component.png)

上例中，`@Component` 中的 metadata 告诉 Angular 到哪里为该组件获取主要的构建块。

模板、metadata 和组件共同描述一个视图。


## 数据绑定

Angular 支持数据绑定，即一种将组件中的部件与模板中的部件关联起来的一种机制。在模板 HTML 中添加绑定标签，告诉 Angular 如何连接两端。

![databinding](/assets/images/angular-docs/databinding.png)

从图中可见，共有 4 种 绑定形式语法。每种形式都有一个方向：到 DOM，从 DOM，或双向。

下例的模板中用了 3 种形式：

```typescript
//src/app/hero-list.component.html (binding)
<li>{{hero.name}}</li>
<hero-detail [hero]="selectedHero"></hero-detail>
<li (click)="selectHero(hero)"></li>
```

第 4 种形式是很重要的双向数据绑定，它使用 `ngModel` 指令将属性和事件绑定组合在一个语句中，例如：

```typescript
//src/app/hero-detail.component.html (ngModel)
<input [(ngModel)]="hero.name">
```

上例中，作为属性绑定，属性值从组件流向 input。而作为事件绑定，用户的修改也会流回到组件。

从根组件树到所有的子组件，Angular 在每次 JavaScript 事件周期中一次性处理所有的数据绑定。

数据绑定在模板与模板的交互，以及父子组件间的交互中起来了重要的作用。

![component-databinding](/assets/images/angular-docs/component-databinding.png)

![component-databinding](/assets/images/angular-docs/component-databinding.png)


## 指令 Directive

Angular 模板是动态的。当呈现时，它根据 Directive 中的指令变换 DOM。

一个 Directive 就是一个带有 `@Directive` 装饰器的类。`@Component` 装饰器实际上就是带有模板功能特性的 `@Directive` 装饰器的扩展装饰器，因此，一个组件实际上就是一个带有模板的 Directive。

共有 2 种指令，结构指令（structural directive) 和属性指令（attribute directive)。

它们通常像标签的属性一样出现，有时是以名字形式出现，但更多时候是作为赋值或绑定语句的目标值出现。

结构指令通过在 DOM 中添加、删除和替换元素来修改布局。

下面的模板中使用了 2 个内置的结构指令：

```typescript
//src/app/hero-list.component.html (structural)
<li *ngFor="let hero of heroes"></li>
<hero-detail *ngIf="selectedHero"></hero-detail>
```

属性指令修改一个现有元素的外观或行为。在模板中它们使用名字的形式，因而像普通的 HTML 属性。。

`ngModel` 就是一个属性指令，它实现双向数据绑定。`ngModel` 修改了元素（一般是 `<input>`) 的行为：设置其显示值属性，并响应修改事件。

```typescript
//src/app/hero-detail.component.html (ngModel)
<input [(ngModel)]="hero.name">
```

Angular 有很多指令，如 ngSwitch, ngStyle, ngClass, 不过也可以自己编写指令。

## 服务 Service

服务 (Service) 可以包含值、函数、或应用所有的功能。Angular 对服务没有特别的定义，没有 service base class, 无需注册等。一个完成特定功能的类就可以称为是一个服务。

组件的工作通常只关注用户体验。它在视图和应用逻辑间作协调。一个好组件只为数据绑定呈现属性和方法，而其它的所有事情都委派服务来完成。


## 依赖注入 Dependency injection

依赖注入是供应所需（所依赖）的类的新实例的一种新方式。大多数依赖都是服务。Angular 使用依赖注入为新创建的组件提供所需的服务。

Angular 通过组件构造器的参数，可了解组件所需的服务，例如下面的 HeroListComponent 需要 `HeroService`：

```typescript
//src/app/hero-list.component.ts (constructor)
constructor(private service: HeroService) { }
```

当创建一个组件中，Angular 会首先向一个注射器（`injector`)请求该组件所需的服务。

一个注射器组件一个容器，里面包含了它之前已创建的所有服务实例。如果请求的服务实现还没有有容器中，注射器会创建一个并添加后容器后，之后才返回。当所请求的服务都返回后，Angular 将这些服务实例作为参数来调用组件的构造器。这就是依赖注入。

`HeroService` 的注入过程如下：

![injector-injects](/assets/images/angular-docs/injector-injects.png)

当注射器中没有 `HeroService` 时，它需要创建一个，因此，我们必须为注射器事物注册该 `HeroService` 的一个 provider。一个 provider 就是一个能创建或返回一个服务的东西，通常就是服务类本身。

可以在模块或组件中注册 provider。

通常，在根组件的 `providers` 中注册后，该服务的相同实例可以在所有地方使用（单例模式）：

```typescript
//src/app/app.module.ts (module providers)
providers: [
  BackendService,
  HeroService,
  Logger
],
```

而在 `@Component` 的 metadata 中注册的是组件级的，因此当每次创建该组件实例时，都会得到一个新的服务实例：

```typescript
//src/app/hero-list.component.ts (component providers)
@Component({
  selector:    'hero-list',
  templateUrl: './hero-list.component.html',
  providers:  [ HeroService ]
})
```

依赖注入的要点：

+ 依赖注入在 Angular 框架中有大量使用
+ 注射器 injector 是主要机制：
    - injector 维护一个它的服务实例的一个容器
    - injector 能根据 provider 创建一个新的服务实例
+ 一个 provider 就是创建一个服务的一种方法
+ 用注射器注册 providers


## 参考

+ https://angular.io/guide/architecture
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/fundamentals_architecture.ipynb)
