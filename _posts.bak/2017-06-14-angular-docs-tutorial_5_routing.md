---
title: Angular docs-教程 5： 路由
date: 2017-06-14
writing-time: 2017-08-24
categories: programming
tags: angular node Angular&nbsp;docs
---

# 教程 5： 路由

新需求：

+ 添加一个 Dashboard 视图
+ 能在 Heroes 和 Dashboard 视图间导航切换
+ 在任何视图中点击 hero 时，导航到该 hero 的详细信息视图
+ 从粘贴的 URL 直接导航到详细信息视图


## 实施方案

+ 将 `AppComponent` 组件改造成只处理应用导航的 application shell
+ 当前 `AppComponent` 中与 Heroes 有关的内容，移到独立的 `HeroesComponent` 组件中
+ 添加路由
+ 创建一个新的 `DashboardComponent` 组件
+ 将 Dashboard 关联到导航结构中

Routing 就是 navigation。router 就是在视图间进行导航的一种机制。


## 分割 AppComponent

改造后的应用将只显示一个 shell，并显示一组可选视图（Dashboard 和 Heroes)，并显示一个默认视图。

`AppComponent` 将只处理导航，故应将关于 Heroes 的呈现功能移到一个独立的 `HeroesComponent` 组件中。

### HeroesComponent

+ 将 `app.component.ts` 文件重命名为 `heroes.component.ts`
+ 将类名 `AppComponent` 改为 `HeroesComponent`
+ 将选择子 `my-root` 改为 `my-heroes`。

```typescript
//src/app/heroes.component.ts (showing renamings only)
@Component({
  selector: 'my-heroes',
})
export class HeroesComponent implements OnInit {
}
```

### 创建  AppComponent

新的 AppComponent 将作为应用的 shell。它将在视图的上部显示导航链接，并在下面设置一个显示区域。

+ 创建文件 `src/app/app.component.ts`
+ 定义一个导出的类 `AppComponent`
+ 添加 `@Component` 装饰器，并设置选择子为 `my-root`
+ 将 HeroesComponent 中的以下内容移回来：
    - `title` 类属性
    - `@Component` 模板中的 `<h1>` 元素，并绑定到 `title`
+ 在模板中添加 `<my-heroes>` 元素
+ 将 `HeroesComponent` 添加到 `AppModule` 的 `declarations` 数组中，从而 Angular 可以认识 `<my-heroes>` 标签
+ 将 `HeroService` 添加到 `AppModule` 的 `providers` 数组中，这样可以在其它视图中使用（这是全局设置，将生成一个全局的 singleton 实例，并注入所有组件中），从而现在可以将 `HeroService` 从 `HeroesComponent` 的 `providers` 数组中移除了。


## 添加路由

Angular 路由器是一个外部的可选 Angular NgModule，叫做 `RouterModule`。它包含有许多 provided services（如 `RouterModule`), 许多指令（如 `RouterOutlet`, `RouterLink`, `RouterLinkActive`），及一个配置对象（`Routers`）。


对于路由功能来说， `index.html` 的 `<head>` 中必须要有 `<base href>` 元素设置，如：

```html
<!--src/index.html (base-href)-->
<head>
  <base href="/">
```

### 配置路由

路由能告诉路由器，当用户点击链接或直接将 URL 粘贴到地址栏时该显示哪个视图。

配置一个到 heroes 组件的路由：

```typescript
//src/app/app.module.ts (heroes route)
import { RouterModule }   from '@angular/router';

RouterModule.forRoot([
  {
    path: 'heroes',
    component: HeroesComponent
  }
])
```

一个路由定义由以下部分组件：

+ `path`: 路由器拿该值与 URL 进行匹配
+ `component`: 路由对应要显示的组件类


### 启用路由器

加载 `RouterModule`，并将路由器配置加入到 `AppModule` 装饰器的 `imports` 数组中：

```typescript
//src/app/app.module.ts (app routing)
import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';
import { RouterModule }   from '@angular/router';

import { AppComponent }        from './app.component';
import { HeroDetailComponent } from './hero-detail.component';
import { HeroesComponent }     from './heroes.component';
import { HeroService }         from './hero.service';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot([
      {
        path: 'heroes',
        component: HeroesComponent
      }
    ])
  ],
  declarations: [
    AppComponent,
    HeroDetailComponent,
    HeroesComponent
  ],
  providers: [
    HeroService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule {
}
```

`RouterModule.forRoot()` 方法用来配置应用的根路由器。


### Router outlet

当路由匹配时，你需要告诉路由器将组件显示到哪里，这通过在模板中添加 `<router-outlet>` 元素实现。`RouterOutlet` 是 `RouterModule` 提供的一个指令。路由器将每个匹配组件都显示在 `<router-outlet>` 的下面。


### Router Links

```typescript
//src/app/app.component.ts (template-v2)
template: `
   <h1>{{title}}</h1>
   <a routerLink="/heroes">Heroes</a>
   <router-outlet></router-outlet>
 `
```

注意 a 标签中的 `routerLink` 绑定。`RouterLink` 也是 `RouterModule` 提供的一个指令，它绑定一个字符串，从而当用户点击链接时，路由器能知道需导航到哪里。

因此，Angular 的路由器功能，可以替代后端开发的路由功能。

`AppComponent` 现已关联到了一个路由器，并且能显示被路由的视图。因此，为与其它类型的组件相区分，这种类型的组件叫 router component。


## 添加 dashboard

```typescript
//src/app/dashboard.component.ts (v1)
import { Component } from '@angular/core';

@Component({
  selector: 'my-dashboard',
  template: '<h3>My Dashboard</h3>'
})
export class DashboardComponent { }
```


## 配置 dashboard 的路由

在 `app.module.ts` 文件中，并定义路由：

```typescript
//src/app/app.module.ts (Dashboard route)
{
  path: 'dashboard',
  component: DashboardComponent
},
```

导入 `DashboardComponent` 并加入 `AppModule` 的 `declarations` 中：

```typescript
//src/app/app.module.ts (dashboard)
declarations: [
  AppComponent,
  DashboardComponent,
  HeroDetailComponent,
  HeroesComponent
],
```

## 添加一个重定义路由

当访问 `/` 时重定义到 `/dashboard`：

```typescript
//src/app/app.module.ts (redirect)
{
  path: '',
  redirectTo: '/dashboard',
  pathMatch: 'full'
},
```

## 在模板中添加 dashboard 导航链接

```typescript
//src/app/app.component.ts (template-v3)
template: `
   <h1>{{title}}</h1>
   <nav>
     <a routerLink="/dashboard">Dashboard</a>
     <a routerLink="/heroes">Heroes</a>
   </nav>
   <router-outlet></router-outlet>
 `
```


## 将 heroes 添加到 dashboard

将 metadata 中的 `template` 替换为 `templateUrl` 属性，并指向一个模板文件。

```typescript
//src/app/dashboard.component.ts (metadata)
@Component({
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
})
```

```html
<!--src/app/dashboard.component.html-->
<h3>Top Heroes</h3>
<div class="grid grid-pad">
  <div *ngFor="let hero of heroes" class="col-1-4">
    <div class="module hero">
      <h4>{{hero.name}}</h4>
    </div>
  </div>
</div>
```

### 重用 HeroService

之前将 `HeroService` 添加到了 `AppModule` 的 `providers` 数组中，因此 Angular 会创建 `HeroService` 的一个单例实例，并注入到应用的所有组件中。因此所有组件中都可以使用。


### 类似 HeroesComponet, 在 DashboardComponent 中获取 heroes


```typescript
//src/app/dashboard.component.ts
import { Component, OnInit } from '@angular/core';

import { Hero } from './hero';
import { HeroService } from './hero.service';


//...
export class DashboardComponent implements OnInit {

  heroes: Hero[] = [];

  constructor(private heroService: HeroService) { }

  ngOnInit(): void {
    this.heroService.getHeroes()
      .then(heroes => this.heroes = heroes.slice(1, 5));
  }
}
```

## 导航到 hero detail

现在的 HeroDetailComponent 是通过父组件中的绑定选择显示哪个 hero 的:

```typescript
<hero-detail [hero]="selectedHero"></hero-detail>
```

### 参数化的路由

定义路由时，需将 hero 的 id 值考虑进去：

```typescript
//src/app/app.module.ts (hero detail)
{
  path: 'detail/:id',
  component: HeroDetailComponent
},
```

上面 path 中的 `:id` 是 hero id 的占位符。

我们无需在模板中添加 `Hero Detail` 链接，因为用户是通过点击 hero 列表中的名字来导航的。

### 重构 HeroDetailComponent

无需从父组件获取 hero 属性绑定，故可删除 `hero` 属性。现需求从 `ActivatedRoute` 服务的 `paramMap` Observable(RxJS) 中提取 `id` 参数值，再从 `HeroService` 中提取该参数值的 hero 对象。

```typescript
//src/app/hero-detail.component.ts
// Keep the Input import for now, you'll remove it later:
import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Location }                 from '@angular/common';

import { HeroService } from './hero.service';
```

将 `ActivatedRoute`, `HeroService`, `Location` 服务注入到构造器，并保存为私有属性。

```typescript
//src/app/hero-detail.component.ts (constructor)
constructor(
  private heroService: HeroService,
  private route: ActivatedRoute,
  private location: Location
) {}
```

导入 `swithMap` 操作符来处理路由参数 `paramMap`:

```typescript
//src/app/hero-detail.component.ts (switchMap import)
import 'rxjs/add/operator/switchMap';
```

实现 `OnInit` 接口，根据 `paramMap` Observable 对象从 `ActivatedRoute` 服务器提取 `id` 参数值，并根据该 id 值，从 `HeroService` 中获取相应的 hero。

```typescript
//src/app/hero-detail.component.ts
export class HeroDetailComponent implements OnInit {
ngOnInit(): void {
  this.route.paramMap
    .switchMap((params: ParamMap) => this.heroService.getHero(+params.get('id')))
    .subscribe(hero => this.hero = hero);
}
```

`switchMap` 操作符将路由参数 `paramMap` Observable 转化成另一个 Observable，即一个 `HeroService.getHero()` 返回值的 Observable。

如果当 `getHero()` 请求还在处理时，用户再次导航到该组件，`switchMap` 会取消旧请求，然后再次调用 `HeroService.getHero()`。

`id` 值是数字，而路由参数总是字符串，故上面通过 `+` 操作进行转化。


### 添加 HeroService.getHero()

```typescript
//src/app/hero.service.ts (getHero)
getHero(id: number): Promise<Hero> {
  return this.getHeroes()
             .then(heroes => heroes.find(hero => hero.id === id));
}
```

### 返回操作

```typescript
//src/app/hero-detail.component.ts (goBack)
goBack(): void {
  this.location.back();
}
```

并在模板中进行事件绑定：

```html
<button (click)="goBack()">Back</button>
```

将模板保存为一个单独的文件并更新 metadata 中的 tempalte 为 templateUrl。

```html
<!--src/app/hero-detail.component.html-->
<div *ngIf="hero">
  <h2>{{hero.name}} details!</h2>
  <div>
    <label>id: </label>{{hero.id}}</div>
  <div>
    <label>name: </label>
    <input [(ngModel)]="hero.name" placeholder="name" />
  </div>
  <button (click)="goBack()">Back</button>
</div>
```

## 在 dashboard 中选中一个 hero

为 hero 添加路由：

```html
<!--src/app/dashboard.component.html (repeated <a> tag)-->
<a *ngFor="let hero of heroes"  [routerLink]="['/detail', hero.id]"  class="col-1-4">
```

这里的 `[routerLink]` 绑定到一个参数数组。 


## 将路由配置信息保存到独立的路由模块中

按惯例，路由模块名中应包含 "routing"， 及其所导航的所有组件声明所在的模块名，并以 ".module" 作为后缀。本例中，路由信息导航的所有组件都声明在 `app.module.ts` 中，故路由模块名为 `app-routing.module.ts`，对应 `app.module.ts`：

```typescript
//src/app/app-routing.module.ts
import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard.component';
import { HeroesComponent }      from './heroes.component';
import { HeroDetailComponent }  from './hero-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard',  component: DashboardComponent },
  { path: 'detail/:id', component: HeroDetailComponent },
  { path: 'heroes',     component: HeroesComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
```

`RouterModule.forRoot()` 产生一个 Angular [ModuleWithProviders](https://angular.io/api/core/ModuleWithProviders)。

一个路由模块通常有以下几个特点：

+ 所有路由配置信息都放置在一个变量 routers 中
+ 将 `RouterModule.forRoot(routers)` 加入 `imports` 中
+ 将 `RouterModule` 加入到 `exports` 中，从而使对应模块中的组件能访问 Router 声明，如 `RouterLink`, `RouterOutlet`
+ 没有 `declarations`，声明是对应模块的职责
+ 如何需防护服务，将添加 `providers`

即路由模块将所有的配置信息都保存到 `RouterModule` 中，将通过将 `RouterModule` 加入到 `exports` 后将其导出。而其它的模块通过在 `@NgModule` 的 `imports` 列表中加入该模块，实现对 `RouterModule` 及路由信息的访问。


### 更新 AppModule

在 AppModule 中删除路由配置信息，导入 `AppRoutingModule`，并加入 `NgModule.imports` 列表中。

```typescript
//src/app/app.module.ts
import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';

import { AppComponent }         from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { HeroDetailComponent }  from './hero-detail.component';
import { HeroesComponent }      from './heroes.component';
import { HeroService }          from './hero.service';

import { AppRoutingModule }     from './app-routing.module';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    HeroDetailComponent,
    HeroesComponent
  ],
  providers: [ HeroService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```


## 在 HeroesComponent 

当前的 HeroesComponent 中显示了一个列表，当点击选中时，在底部显示选中的 hero 信息。

更新：选中时只显示 mini 信息，并显示链接到 hero 详情的页面。

### 在模板中添加 mini 信息

```typescript
//src/app/heroes.component.ts
<div *ngIf="selectedHero">
  <h2>
    {{selectedHero.name | uppercase}} is my hero
  </h2>
  <button (click)="gotoDetail()">View Details</button>
</div>
```

模板中的 `|` 是管道格式化格式符，Angular 内置支持 [多种管道格式化](https://angular.io/guide/pipes)。

### 将 HeroesComponent 中的 模板和样式信息保存为独立文件

模板文件是 `heroes.component.html`，样式文件是 `heroes.component.css`。然后在 metadata 中用 templateUrl 和 styleUrls 引用，其中 styleUrls 的值是一个数组。

```typescript
//src/app/heroes.component.ts (revised metadata)
@Component({
  selector: 'my-heroes',
  templateUrl: './heroes.component.html',
  styleUrls: [ './heroes.component.css' ]
})
```

### 更新 HeroesComponent

现用户的点击事件绑定到 `gotoDetail()` 方法，实现导航到对应组件。

```typescript
//src/app/heroes.component.ts (gotoDetail)
gotoDetail(): void {
  this.router.navigate(['/detail', this.selectedHero.id]);
}
```

路由器的 `navigate` 方法和 `[routerLink]` 的绑定参数是相似的。

更新后的 HeroesComponent:

```typescript
//src/app/heroes.component.ts (class)
export class HeroesComponent implements OnInit {
  heroes: Hero[];
  selectedHero: Hero;

  constructor(
    private router: Router,
    private heroService: HeroService) { }

  getHeroes(): void {
    this.heroService.getHeroes().then(heroes => this.heroes = heroes);
  }

  ngOnInit(): void {
    this.getHeroes();
  }

  onSelect(hero: Hero): void {
    this.selectedHero = hero;
  }

  gotoDetail(): void {
    this.router.navigate(['/detail', this.selectedHero.id]);
  }
}
```


## 添加样式

为 DashboradComponent 的样式信息新建文件 `dashboard.component.css`， 并通过 styleUrls 引用：

```typescript
//src/app/dashboard.component.ts (styleUrls)
styleUrls: [ './dashboard.component.css' ]
```

```css
/* src/app/dashboard.component.css */
[class*='col-'] {
  float: left;
  padding-right: 20px;
  padding-bottom: 20px;
}
[class*='col-']:last-of-type {
  padding-right: 0;
}
a {
  text-decoration: none;
}
*, *:after, *:before {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
h3 {
  text-align: center; margin-bottom: 0;
}
h4 {
  position: relative;
}
.grid {
  margin: 0;
}
.col-1-4 {
  width: 25%;
}
.module {
  padding: 20px;
  text-align: center;
  color: #eee;
  max-height: 120px;
  min-width: 120px;
  background-color: #607D8B;
  border-radius: 2px;
}
.module:hover {
  background-color: #EEE;
  cursor: pointer;
  color: #607d8b;
}
.grid-pad {
  padding: 10px 0;
}
.grid-pad > [class*='col-']:last-of-type {
  padding-right: 20px;
}
@media (max-width: 600px) {
  .module {
    font-size: 10px;
    max-height: 75px; }
}
@media (max-width: 1024px) {
  .grid {
    margin: 0;
  }
  .module {
    min-width: 60px;
  }
}
```

类似地，为 HeroDetailComponent 添加样式文件 `hero-detail.component.css`。

```css
/* src/app/hero-detail.component.css */
label {
  display: inline-block;
  width: 3em;
  margin: .5em 0;
  color: #607D8B;
  font-weight: bold;
}
input {
  height: 2em;
  font-size: 1em;
  padding-left: .4em;
}
button {
  margin-top: 20px;
  font-family: Arial;
  background-color: #eee;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer; cursor: hand;
}
button:hover {
  background-color: #cfd8dc;
}
button:disabled {
  background-color: #eee;
  color: #ccc; 
  cursor: auto;
}
```

### 为导航链接添加样式

```css
/* src/app/app.component.css (navigation styles) */
h1 {
  font-size: 1.2em;
  color: #999;
  margin-bottom: 0;
}
h2 {
  font-size: 2em;
  margin-top: 0;
  padding-top: 0;
}
nav a {
  padding: 5px 10px;
  text-decoration: none;
  margin-top: 10px;
  display: inline-block;
  background-color: #eee;
  border-radius: 4px;
}
nav a:visited, a:link {
  color: #607D8B;
}
nav a:hover {
  color: #039be5;
  background-color: #CFD8DC;
}
nav a.active {
  color: #039be5;
}
```

Angular 路由器提供了 `routerLinkActive` 指令，可用来为当前匹配路由对应的导航元素添加 CSS 类，如下：

```typescript
//src/app/app.component.ts (active router links)
template: `
  <h1>{{title}}</h1>
  <nav>
    <a routerLink="/dashboard" routerLinkActive="active">Dashboard</a>
    <a routerLink="/heroes" routerLinkActive="active">Heroes</a>
  </nav>
  <router-outlet></router-outlet>
`,
```


### 全局样式

上面的样式是只针对某个组件的，全局样式放在 `src/styles.css` 中。


```css
/* src/styles.css (excerpt) */
/* Master Styles */
h1 {
  color: #369;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 250%;
}
h2, h3 {
  color: #444;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: lighter;
}
body {
  margin: 2em;
}
body, input[text], button {
  color: #888;
  font-family: Cambria, Georgia;
}
/* everywhere else */
* {
  font-family: Arial, Helvetica, sans-serif;
}
```

并在 `src/index.html` 中关联进来：

```html
<!-- src/index.html (link ref) -->
<link rel="stylesheet" href="styles.css">
```

## 参考

+ https://angular.io/tutorial/toh-pt5
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_5_routing.ipynb)
