---
title: Angular docs-表单-NgModule
date: 2017-10-17
writing-time: 2017-10-17
categories: programming
tags: angular node Angular&nbsp;docs
---

# NgModule

NgModule 用来将应用组织成一个个内聚的功能块。

一个 NgModule 就是一个用 `@NgModule` 装饰器函数装饰的类。`@NgModule` 的 metadata 对象告诉 Angular 如何编译和运行该模块代码。它标识了该模块自己的组件、指令和管道，公开一些功能，从而外部组件可以使用。`@NgModule` 也可以将服务提供者 (service providers) 添加到应用的依赖注入器中 (dependency injectors)。

模块可以在应用启动时立即加载，也可以通过路由在需要时异步加载（lazy load)。

`@NgModule` metadata 的功能：

+ 声明哪些组件、指令和管道属于该模块
+ 公开其中的一些类，从而其它组件的模块中可以使用
+ 导入其它模块，从而其它模块中定义的组件、指令和管道可以在本模块的组件中使用
+ 提供应用层的服务，从而应用中的任何组件都能使用

## 根模块 AppModule

每个应用至少有一个模块类，即根模块类。

```typescript
//src/app/app.module.ts (minimal)
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

`BrowserModule` 会登录一些关键的服务提供者，同时也包含一些常用指令如 `NgIf` 和 `NgFor`。

## 在 main.ts 中启动

Angular 针对不同的平台都提供了多种启动方式。对于浏览器应用，主要有 2 种方式。

### just-in-time(JIT) 编译

即动态方式，Angular 编译器在浏览器中编译后再启动应用。

```typescript
//src/main.ts (dynamic)
// The browser platform with a compiler
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

// The app module
import { AppModule } from './app/app.module';

// Compile and launch the module
platformBrowserDynamic().bootstrapModule(AppModule);
```

### ahead-of-time(AOT) 编译

即静态方式。它作为构建过程的一部分，事先进行编译，生成一些类工厂（class factories)，保存在各自的文件中。

事先生成的类工厂中有一个为 `AppModuleNgFactory`，它对应 `AppModule`，启动方式也类似：

```typescript
//src/main.ts (static)
// The browser platform without a compiler
import { platformBrowser } from '@angular/platform-browser';

// The app module factory produced by the static offline compiler
import { AppModuleNgFactory } from './app/app.module.ngfactory';

// Launch with the app module factory.
platformBrowser().bootstrapModuleFactory(AppModuleNgFactory);
```

由于应用已事先编译了，Angular 不会再将编译器包含到应用代码中分发到浏览器上，从而将应用代码量更少，加载再快（很显著）。

JIT 和 AOT 编译器都从相同的 `AppModule` 源代码创建 `AppModuleNgFactory` 类。JIT 是动态创建的，将结果存在浏览器的内存中，而 AOT 是将结果保存在文件中。

## 服务提供者

先创建一个服务，例如 `userService`，再在模块 `@NgModule` 的 metadata 中添加 `providers` 属性：

```typescript
//src/app/app.module.ts (providers)
providers: [ UserService ],
```

由于注册在应用模块中（应用级根注入器 root injector)，从而应用中的所有组件都能使用该服务。

## 导入所需的模块

```typescript
//src/app/app.module.ts (imports)
imports: [ BrowserModule ],
```

导入 `BrowserModule` 后，该模块中所有公开的组件、指令和管道殾能在本 `AppModule` 的组件模板中使用。

`NgIf` 等指令实际上是在 `@angular/common` 的 `CommonModule` 中定义的。而`BrowserModule` 中对 `CommonModule` 进行了重导出 (re-export)。


## 同名冲突

当导入的多个对象名字相同的，可用 `import .. as ..`:

```typescript
import {
  HighlightDirective as ContactHighlightDirective
} from './contact/highlight.directive';
```

## 功能模块

随着应用代码的增加，可将 AppModule 中的一些独立相关代码，分离出来组织成一个功能模板。而在根模板中，导入该功能模块。功能模块中的组件、指令和管道都是内聚的和隐藏的，只能指定公开后才能在外部使用，从而也解决了名字冲突的问题。

## 使用路由来按需加载模块

假设 `ContactComponent` 是应用启动时的页面，从而 `ContactModule` 是立即加载的，而 `HeroModule` 和 `CrisisModule` 是按需加载的。

先在根组件模板中用路由实现 3 个链接：

```html
template: `
  <app-title [subtitle]="subtitle"></app-title>
  <nav>
    <a routerLink="contact" routerLinkActive="active">Contact</a>
    <a routerLink="crisis"  routerLinkActive="active">Crisis Center</a>
    <a routerLink="heroes"  routerLinkActive="active">Heroes</a>
  </nav>
  <router-outlet></router-outlet>
`
```

而在 `AppModule` 中导入 `ContactModule`，从而实现立即加载，而 `HeroModule` 和 `CrisisModule` 没有导入，它们会当用户点击其链接时异步加载：

```typescript
//src/app/app.module.ts (v3)
import { NgModule }           from '@angular/core';
import { BrowserModule }      from '@angular/platform-browser';

/* App Root */
import { AppComponent }       from './app.component.3';
import { HighlightDirective } from './highlight.directive';
import { TitleComponent }     from './title.component';
import { UserService }        from './user.service';

/* Feature Modules */
import { ContactModule }      from './contact/contact.module.3';

/* Routing Module */
import { AppRoutingModule }   from './app-routing.module.3';

@NgModule({
  imports:      [
    BrowserModule,
    ContactModule,
    AppRoutingModule
  ],
  providers:    [ UserService ],
  declarations: [ AppComponent, HighlightDirective, TitleComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
```

`AppRoutingModule` 是路由模块：

```typescript
//src/app/app-routing.module.ts
import { NgModule }             from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'contact', pathMatch: 'full'},
  { path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' },
  { path: 'heroes', loadChildren: 'app/hero/hero.module#HeroModule' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

里面定义了 3 个路由。`contact` 路由没有在这定义，而是定义在其功能模块中。通常每个功能模块内部都有一个路由组件来定义其自己的路由。

指定路由的模块文件和模块类的方式来定义按需加载路由：

```typescript
//src/app/app-routing.module.ts
{ path: 'crisis', loadChildren: 'app/crisis/crisis.module#CrisisModule' },
{ path: 'heroes', loadChildren: 'app/hero/hero.module#HeroModule' }
```

## 根模块中调用  RouterModule.forRoot

`RouterModule` 的静态类方法 `forRoot`，接收一个配置对象，返回一个配置过后的 RouterModule(ModuleWithProviders)。

```typescript
//src/app/app-routing.module.ts
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

返回的 `AppRoutingModule` 类是一个路由模块，它包含 `RouterModule` 中的指令和 能产生路由配置信息的 dependency-injection providers。

`AppRoutingModule` 只用在应用的根模块中，即不要在功能模块中调用  `RouterModule.forRoot`。

## 功能模块中调用 RouterModule.forChild

功能模块中的路由组件：

```typescript
//src/app/contact/contact-routing.module.ts (routing)
@NgModule({
  imports: [RouterModule.forChild([
    { path: 'contact', component: ContactComponent }
  ])],
  exports: [RouterModule]
})
export class ContactRoutingModule {}
```

## Core 模块

当其它功能都分离成一个个功能模块后，一些可imports: [
  BrowserModule,
  ContactModule,
  CoreModule.forRoot({userName: 'Miss Marple'}),
  AppRoutingModule
],共享的指令和组件组成成一个 SharedModule 后，AppModule 中的核心功能组成到 CoreModule 中：

```typescript
//src/app/src/app/core/core.module.ts
import {
  ModuleWithProviders, NgModule,
  Optional, SkipSelf }       from '@angular/core';

import { CommonModule }      from '@angular/common';

import { TitleComponent }    from './title.component';
import { UserService }       from './user.service';
@NgModule({
  imports:      [ CommonModule ],
  declarations: [ TitleComponent ],
  exports:      [ TitleComponent ],
  providers:    [ UserService ]
})
export class CoreModule {
}
```

```typescript
//src/app/app.module.ts (v4)
import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';

/* App Root */
import { AppComponent }   from './app.component';

/* Feature Modules */
import { ContactModule }    from './contact/contact.module';
import { CoreModule }       from './core/core.module';

/* Routing Module */
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  imports: [
    BrowserModule,
    ContactModule,
    CoreModule,
    AppRoutingModule
  ],
  declarations: [ AppComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
```

## 使用 CoreModule.forRoot 来配置核心服务

按惯例，`forRoot` 静态方法同时提供并配置服务。它接收一个服务配置对象，并返回一个 `ModuleWithProviders`，即返回一个有下面属性的简单对象：

+ `ngModule`: 该 `CoreModule` 类
+ `providers`: 已配置了的提供者(the configured providers)

根 `AppModule` 导入 `CoreModule`，并将其 `providers` 添加到自身的 `providers`。即 Angular 先积累所有导入的 providers，再将它们放置到 `@NgModule.providers` 的后面。

更新 CoreModule 中的服务，使其能提供配置对象：

```typescript
//src/app/core/user.service.ts (constructor)
constructor(@Optional() config: UserServiceConfig) {
  if (config) { this._userName = config.userName; }
}
```

`CoreModule.forRoot`：

```typescript
//src/app/core/core.module.ts (forRoot)
static forRoot(config: UserServiceConfig): ModuleWithProviders {
  return {
    ngModule: CoreModule,
    providers: [
      {provide: UserServiceConfig, useValue: config }
    ]
  };
}
```

最后在 `AppModule` 中导入：

```typescript
//src/app//app.module.ts (imports)
imports: [
  BrowserModule,
  ContactModule,
  CoreModule.forRoot({userName: 'Miss Marple'}),
  AppRoutingModule
],
```

## 避免对 CoreModule 的重导入

只有根 `AppModule` 才能导入 `CoreModule`，其它按需加载的模块对其加载会出错。

```typescript
//src/app/core/core.module.ts
constructor (@Optional() @SkipSelf() parentModule: CoreModule) {
  if (parentModule) {
    throw new Error(
      'CoreModule is already loaded. Import it in the AppModule only');
  }
}
```
## 参考

+ https://angular.io/guide/ngmodule
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/ngmodule.ipynb)
