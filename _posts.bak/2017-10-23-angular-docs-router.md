---
title: Angular docs-路由
date: 2017-10-23
writing-time: 2017-10-23
categories: programming
tags: angular node Angular&nbsp;docs
---

# 路由

Angular 的 `Router` 借鉴了浏览器的导航模型。它将浏览器的 URL 解析为导航到一个视图的指令。它能将可选的参数传给支持的视图组件以呈现特定的内容。可将路由器绑定到页面的链接中，当用户点击时导航到相应视图。当用户点击按钮、选择一个下拉框等时可用命令式进行导航。路由器的操作事件也被同步到浏览器的浏览器历史中，从而可以使用浏览器中的按钮进行前进后退操作。

## 基础

需要路由功能的应用在其 `index.html` 的 `<head>` 中要添加 `<base>` 元素，用来告诉路由器如何组合导航 URL。

如果 `app` 目录就是应用的根目录，则设置为：

```html
<!--src/index.html (base-href)-->
<base href="/">
```

### 导入路由器功能

```typescript
//src/app/app.module.ts (import)
import { RouterModule, Routes } from '@angular/router';
```

### 配置

一个有路由功能的应用中，只有一个单例的 `Router` 服务实例。当 URL 有变化时，路由器将从中匹配到相应的 `Route` 来呈现相应组件。

下例通过 `RouterModule.forRoot` 方法在根模块中定义了 4 个路由：

```typescript
//src/app/app.module.ts (excerpt)
const appRoutes: Routes = [
  { path: 'crisis-center', component: CrisisListComponent },
  { path: 'hero/:id',      component: HeroDetailComponent },
  {
    path: 'heroes',
    component: HeroListComponent,
    data: { title: 'Heroes List' }
  },
  { path: '',
    redirectTo: '/heroes',
    pathMatch: 'full'
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
    // other imports here
  ],
  ...
})
export class AppModule { }
```

每个 `Route` 将一个 URL `path` 映射到一个组件。`path` 中没有 `/` 前缀。

`:id` 表示路由参数，在 URL 像 `/hero/42` 中，`id` 参数值为 42。

`data` 属性中可以保存任意数据，以与该路由关联。这些数据可在每个激活的路由中访问。因此可用来保存页面标题等只读数据。

重定向路由需要 `pathMatch` 属性说明匹配方法，值为 `full` 是完全匹配，值为 `prefix` 表示是前缀匹配。

`**` 能匹配任何 URL，而 Django 中用的是 `*`。

当在 `RouterModule.forRoot()` 的第 2 个参数对象中传入  `enableTracing:true` 后，导航生命周期中发生的所有事件都会显示到浏览器的 console 中，便于调试。

### Router outlet

该标签放在主视图页面的 HTML 中，当用匹配的路由要显示时，将显示在该标签位置之后：

```html
<router-outlet></router-outlet>
<!-- Routed views go here -->
```

### 制作路由器链接

```typescript
//src/app/app.component.ts (template)
template: `
  <h1>Angular Router</h1>
  <nav>
    <a routerLink="/crisis-center" routerLinkActive="active">Crisis Center</a>
    <a routerLink="/heroes" routerLinkActive="active">Heroes</a>
  </nav>
  <router-outlet></router-outlet>
`
```

`RouterLink` 指令使得路由器能控制该元素，进行航导。URL 的 query parameters 参数可以通过 `[queryParams]` 绑定一个键值对对象进行，而 URL fragment 参数可以通过 `[fragment]` 绑定一个字符串进行。

`RouterLinkActive` 指令用来指定当链接状态为活跃或不活跃时要切换的 CSS 类名。它基于当前 `RouterState` 中的值来判断当前活跃的 `RouterLink`，并且默认将当前活跃 `RouterLink` 及其子一并设置为活跃。如果不想对其子链接产生作用，可以绑定 `[routerLinkActiveOptions]={exact:true}`。

### 路由器状态

当导航完成后，路由器会构建一个 `ActivedRoute` 对象树，用来表示路由器的当前状态。可以通过注入 `Router` 服务，访问其 `routerState` 属性来访问路由器的当前状态（`RouterState`)。

`RouterState` 中的 `ActivatedRoute` 都有进行上下遍历相关路由信息的函数。

### Activated route

路由的路径和参数可以通过注入 `ActivatedRoute` 服务来获取。该服务中包含如下信息：

属性           | 描述
:-------------|:-------
`url`         | 一个包含路由路径的 `Observable`，路由路径中的所有部分以字符串列表表示。
`data`        | 一个包含该路由中 `data` 对象及其它数据的 `Observable`。
`paramMap`    | 一个包含该路由中必需和可选参数信息的 `map` 的 `Observable`。
`queryParamMap` | 类似 `paramMap`，但是是 query parameters
`fragment`    | 一个包含对所有路由都可用的 URL fragment 的 `Observable`。
`outlet`      | 用来呈现该路由的 `RouterOutlet` 的名字，未命令的自动命令为 `primary`。
`routeConfig` | 该路由的配置对象，包含 origin path。
`parent`      | 该路由的父 `ActivatedRoute`。
`firstChild`  | 该路由的第一个子 `ActivatedRoute`。
`children`    | 该路由的所有子 `ActivatedRoute`。


### 路由器事件

`Router` 在导航过程中通过 `Router.events` 属性发送出导航事件，事件表如下：

路由器事件               | 描述
:----------------------|:--
`NavigationStart`      | 导航开始时
`RoutesRecognized`     | 当路由器解析 URL 并匹配到路由时
`RouteConfigLoadStart` | 在路由器加载一个路由配置信息前
`RouterConfigLoadEnd`  | 当路由完成加载后
`NavigationEnd`        | 导航成功完成后
`NavigationCancel`     | 导航取消后
`NavigationError`      | 导航由于未知错误而失败后


## base href 和 history.pushState

路由器使用浏览器的 `history.pushState` 来实现导航。从而我们可以使用应用内 URL（和服务端 URL 无区别）。`pushState` 技术能对浏览器的地址栏和历史记录进行修改，并不向服务端发送请求。

浏览器需要使用 `<base href>` 值作为相对路径的前缀来引用 CSS，脚本和图片文件。

## 专门路由的模块 routing module

一般将应用的路由信息写在独立文件 `app/app-routing.module.ts` 中，将 `RouterModule.forRoot()` 这该模块中调用。

依照惯例，创建类名 `AppRoutingModule`，export，使它能在 `AppModule` 中使用。

例如：

```typescript
//src/app/app-routing.module.ts
import { NgModule }              from '@angular/core';
import { RouterModule, Routes }  from '@angular/router';

import { CrisisListComponent }   from './crisis-list.component';
import { HeroListComponent }     from './hero-list.component';
import { PageNotFoundComponent } from './not-found.component';

const appRoutes: Routes = [
  { path: 'crisis-center', component: CrisisListComponent },
  { path: 'heroes',        component: HeroListComponent },
  { path: '',   redirectTo: '/heroes', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: true } // <-- debugging purposes only
    )
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}
```

之后，根模块 `app.module.ts` 中只需导入 `AppRoutingModule` 来替换 `RouterModule.forRoot` 即可：

```typescript
//src/app/app.module.ts
import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';

import { AppComponent }     from './app.component';
import { AppRoutingModule } from './app-routing.module';

import { CrisisListComponent }   from './crisis-list.component';
import { HeroListComponent }     from './hero-list.component';
import { PageNotFoundComponent } from './not-found.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    HeroListComponent,
    CrisisListComponent,
    PageNotFoundComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 功能模块中的路由功能

一般将相关的业务功能封装在独立功能模块中，例如将有关 hero 管理的功能全部组织到 `src/app/heroes` 目录下。并将该模块中所有的组件、服务等都组织成一个模块，例如：

```typescript
//src/app/heroes/heroes.module.ts (pre-routing)
import { NgModule }       from '@angular/core';
import { CommonModule }   from '@angular/common';
import { FormsModule }    from '@angular/forms';

import { HeroListComponent }    from './hero-list.component';
import { HeroDetailComponent }  from './hero-detail.component';

import { HeroService } from './hero.service';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
  ],
  declarations: [
    HeroListComponent,
    HeroDetailComponent
  ],
  providers: [ HeroService ]
})
export class HeroesModule {}
```

而功能模块中的路由配置信息一般也独立成一个文件，例如这里放在 `heroes-routing.module.ts` 中，但这里只能调用 `RouterModule.forChild()` 来配置路由，不能调用 `RouterModule.forRoot()`，例如：

```typescript
//src/app/heroes/heroes-routing.module.ts
import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeroListComponent }    from './hero-list.component';
import { HeroDetailComponent }  from './hero-detail.component';

const heroesRoutes: Routes = [
  { path: 'heroes',  component: HeroListComponent },
  { path: 'hero/:id', component: HeroDetailComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(heroesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class HeroRoutingModule { }
```

和将 `appRootingModule` 添加到 `AppModule` 模块类似，将功能模块中的路由信息也添加到功能模块中，例如：

```typescript
//src/app/heroes/heroes.module.ts
import { NgModule }       from '@angular/core';
import { CommonModule }   from '@angular/common';
import { FormsModule }    from '@angular/forms';

import { HeroListComponent }    from './hero-list.component';
import { HeroDetailComponent }  from './hero-detail.component';

import { HeroService } from './hero.service';

import { HeroRoutingModule } from './heroes-routing.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    HeroRoutingModule
  ],
  declarations: [
    HeroListComponent,
    HeroDetailComponent
  ],
  providers: [ HeroService ]
})
export class HeroesModule {}
```

之后，在 `AppRoutingModule` 中去除有关 heroes 的路由信息，在 `AppModule` 中通过 `imports` 列表导入功能模块，这样功能模块中的路由信息会自动合并到应用的路由信息中。那么 `imports` 中功能模块的导入顺序就很重要，因为路由顺序以该顺序组织。

例如：

```typescript
//src/app/app.module.ts
import { NgModule }       from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';

import { AppComponent }     from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HeroesModule }     from './heroes/heroes.module';

import { CrisisListComponent }   from './crisis-list.component';
import { PageNotFoundComponent } from './not-found.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HeroesModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    CrisisListComponent,
    PageNotFoundComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 路由参数

例如路由定义： `{ path: 'hero/:id', component: HeroDetailComponent }`，对应的 URL 应该像 `localhost/hero/15`。因此在模板中构建路由链接时，要以数组形式传入 path 和 param：`['/hero', hero.id] // { 15 }`。

路由器会从 URL 中抽取出路由参数 (`id:15`)，并通过 `ActivatedRoute` 服务提供级目标组件。

下面是组件抽取参数进行处理的例如：

```typescript
import { Router, ActivatedRoute, ParamMap } from '@angular/router';
import 'rxjs/add/operator/switchMap';


//src/app/heroes/hero-detail.component.ts (constructor)
constructor(
  private route: ActivatedRoute,
  private router: Router,
  private service: HeroService
) {}

//src/app/heroes/hero-detail.component.ts (ngOnInit)
ngOnInit() {
  this.hero$ = this.route.paramMap
    .switchMap((params: ParamMap) =>
      this.service.getHero(params.get('id')));
}
```


`HeroService` 返回一个 `Observable<Hero>`，故用 `switchMap` 操作符对其扁平化。`switchMap` 还能取消之前进行中的请求。当用户用不能的 `id` 重新导航到该路由时，`switchMap` 会放弃旧的请求并返回新的 `id` 对应的返回值。

由于返回值是一个 `Observable`，在模板中要用 `AsyncPipe` 进行处理。

### ParamMap

是一个 `Observable`，因此其包含的路由参数映射值在组件使用过程中能更新。当用户用不能的参数值访问相同的组件时，路由器可重用该组件实例（如访问 “上一条”，“下一条”）。

但 `ngOnInit` 只在每个组件初始化时调用一次，故只能通过 `paramMap` 的 `Observable` 性质解决。

如果不想重用组件（即每次都重新创建），则可通过 `ActivatedRoute` 的 `snapshot` 属性获取当前的参数值，这是一种 no-observable 的方式。

```typescript
//src/app/heroes/hero-detail.component.ts (ngOnInit snapshot)
ngOnInit() {
  let id = this.route.snapshot.paramMap.get('id');

  this.hero$ = this.service.getHero(id);
}
```


### 后退：用命令式调用导航

```typescript
//src/app/heroes/hero-detail.component.ts (excerpt)
gotoHeroes() {
  this.router.navigate(['/heroes']);
}
```

### 可选路由参数

后退时，可传入一个可选路由参数，用来表示从哪个页面返回。可选参数不需要在路由定义的 URL 模块中匹配，它通过独立的对象加入：

```typescript
//src/app/heroes/hero-detail.component.ts (go to heroes)
gotoHeroes(hero: Hero) {
  let heroId = hero ? hero.id : null;
  // Pass along the hero id if available
  // so that the HeroList component can select that hero.
  // Include a junk 'foo' property for fun.
  this.router.navigate(['/heroes', { id: heroId, foo: 'foo' }]);
}
```

可选路由参数在 URL 中是以 `;` 分隔的，如： `localhost:3000/heroes;id=15;foo=foo`。

而在目标组件中，抽取可选参数和必要参数的方法是一样的，如：

```typescript
//src/app/heroes/hero-list.component.ts
import { ActivatedRoute, ParamMap } from '@angular/router';
import 'rxjs/add/operator/switchMap';
import { Observable } from 'rxjs/Observable';

//src/app/heroes/hero-list.component.ts (constructor and ngOnInit)
export class HeroListComponent implements OnInit {
  heroes$: Observable<Hero[]>;

  private selectedId: number;

  constructor(
    private service: HeroService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.heroes$ = this.route.paramMap
      .switchMap((params: ParamMap) => {
        // (+) before `params.get()` turns the string into a number
        this.selectedId = +params.get('id');
        return this.service.getHeroes();
      });
  }
}
```


## 为路由组件添加动画

创建文件 `/src/app/animations.ts`:

```typescript
//src/app/animations.ts (excerpt)
import { animate, AnimationEntryMetadata, state, style, transition, trigger } from '@angular/core';

// Component transition animations
export const slideInDownAnimation: AnimationEntryMetadata =
  trigger('routeAnimation', [
    state('*',
      style({
        opacity: 1,
        transform: 'translateX(0)'
      })
    ),
    transition(':enter', [
      style({
        opacity: 0,
        transform: 'translateX(-100%)'
      }),
      animate('0.2s ease-in')
    ]),
    transition(':leave', [
      animate('0.5s ease-out', style({
        opacity: 0,
        transform: 'translateY(100%)'
      }))
    ])
  ]);
```

+ 创建了一个名为 `slideInDownAnimation` 常量，指向名为 `routeAnimation` 的 animation trigger，给需要动画效果的组件引用。
+ 定义了 2 个转变效果，进入时（`:enter`) 是从左到右，离开时（`:leave`) 是向下。

在目标组件中，通过 `@HostBing()` 为组件的托管元素设置动画名及样式：

```typescript
//hero-detail.component.ts
import 'rxjs/add/operator/switchMap';
import { Component, OnInit, HostBinding } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

import { slideInDownAnimation } from '../animations';

import { Hero, HeroService }  from './hero.service';

@Component({
  template: `
  <h2>HEROES</h2>
  <div *ngIf="hero$ | async as hero">
    <h3>"{{ hero.name }}"</h3>
    <div>
      <label>Id: </label>{{ hero.id }}</div>
    <div>
      <label>Name: </label>
      <input [(ngModel)]="hero.name" placeholder="name"/>
    </div>
    <p>
      <button (click)="gotoHeroes(hero)">Back</button>
    </p>
  </div>
  `,
  animations: [ slideInDownAnimation ]
})
export class HeroDetailComponent implements OnInit {
  @HostBinding('@routeAnimation') routeAnimation = true;
  @HostBinding('style.display')   display = 'block';
  @HostBinding('style.position')  position = 'absolute';

  hero$: Observable<Hero>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: HeroService
  ) {}

  ngOnInit() {
    this.hero$ = this.route.paramMap
      .switchMap((params: ParamMap) =>
        this.service.getHero(params.get('id')));
  }

  gotoHeroes(hero: Hero) {
    let heroId = hero ? hero.id : null;
    // Pass along the hero id if available
    // so that the HeroList component can select that hero.
    // Include a junk 'foo' property for fun.
    this.router.navigate(['/heroes', { id: heroId, foo: 'foo' }]);
  }
}
```


## 子路由

+ 每个功能都有自己的目录
+ 每个功能都有自己的功能模块
+ 每个功能都有其根组件
+ 每个功能根组件都有自己的 router outlet 及子路由
+ 功能模块中的路由很少与其它功能模块中的路由有交叉

### 功能模块中的根组件

```typescript
//src/app/crisis-center/crisis-center.component.ts
import { Component } from '@angular/core';

@Component({
  template:  `
    <h2>CRISIS CENTER</h2>
    <router-outlet></router-outlet>
  `
})
export class CrisisCenterComponent { }
```

它是访功能区域中的根组件，地位等同于整个应用中的 `AppComponent`，其模板中只有 `<router-outlet>`。

它没有选择子，因为我们无需将它嵌入到其它组件的模板中，而是通过路由器来导航。


### 功能模块中的子路由配置

例如在 `crisis-center-routing.module.ts` 中：

```typescript
//src/app/crisis-center/crisis-center-routing.module.ts (Routes)
const crisisCenterRoutes: Routes = [
  {
    path: 'crisis-center',
    component: CrisisCenterComponent,
    children: [
      {
        path: '',
        component: CrisisListComponent,
        children: [
          {
            path: ':id',
            component: CrisisDetailComponent
          },
          {
            path: '',
            component: CrisisCenterHomeComponent
          }
        ]
      }
    ]
  }
];
```

这里的路由定义中使用了 `children`，因此 `CrisisCenterComponent` 路由定义中其  `children` 下的子组件经路由后都呈现在 `CrisisCenterComponent` 模板的 `<router-outlet>` 下。类似地，`CrisisListComponent` 路由定义中其  `children` 下的子组件经路由后都呈现在 `CrisisListComponent` 模板中 `<router-outlet>` 下。

### 相对路径导航

使用 `Router.navigate` 进行相对路径导航时，要先注入 `ActivatedRoute` 来获取当前路由状态，在链接参数数组时，添加一个带有 `relativeTo` 属性值为 `ActivatedRoute` 注入值的参数对象：

```typescript
//src/app/crisis-center/crisis-detail.component.ts (relative navigation)
// Relative navigation back to the crises
this.router.navigate(['../', { id: crisisId, foo: 'foo' }], { relativeTo: this.route });
```

而在模板中通过 `routerLink` 时，参数值相同，但不需要加 `relativeTo` 参数。


### secondary route （第二路由）


第二路由和主路由的功能：

+ 它们相互独立
+ 同时相互组合使用
+ 第二路由组件只呈现在 named outlet 中

在应用的主组件模板中添加 named outlet:

```html
<router-outlet></router-outlet>
<router-outlet name="popup"></router-outlet>
```


在 `AppRoutingModule` 中添加最二路由（即指定显示的 named outlet):

```typescript
//src/app/app-routing.module.ts (compose route)
{
  path: 'compose',
  component: ComposeMessageComponent,
  outlet: 'popup'
},
```

添加链接，当用户点击时，在 named outlet 下呈现组件：

```html
<a [routerLink]="[{ outlets: { popup: ['compose'] } }]">Contact</a>
```

之后，用户点击时，`compose` 路由关联的组件将呈现在 `popup` named outlet 下。


当导航到 Cris Center 后再点击上面链接时，浏览器地址栏中的链接为： `http://.../crisis-center(popup:compose)`，解析为：

+ `crisis-center` 是主导航部分
+ 第二路由部分用 `()` 包围
+ 第二路由中包含一个 outlet 名 (popup)，`:` 为分隔符，最后是第二路由路径(compose)

此时当点击 `Heroes` 链接时，地址变为 `http://.../heroes(popup:compose)`，即主路由部分变了，而第二路由部分不变，它们是独立的。路由器为导航树维护多个独立的分枝。即基于不同的 outlet 呈现位置维护不同的分枝。

消除第二路由的 URL 部分：

```typescript
//src/app/compose-message.component.ts (closePopup)
closePopup() {
  // Providing a `null` value to the named outlet
  // clears the contents of the named outlet
  this.router.navigate([{ outlets: { popup: null }}]);
}
```

## 路由保护

通过将各种路由保护类添加到路由配置中，路由器在路由处理时，会预告调用该保护类中的相应接口，根据返回值决定继续下去还是取消，并且保护类接口中还能进行导航转向（也是取消当前导航的一种方式）。

保护接口可返回一个立即的布尔值，也可以返回一个 `Observable<boolean>` 或 `Promise<boolean>`，此时路由器要等待它的异步操作（如向用户提问题，将数据保存到后端等）完成。

路由器支持下面几种保护接口：

+ CanActivate：一般用于授权验证
+ CanActivateChild: 对子路由统一验证
+ CanDeactivate: 验证当前路由中有没有数据没有保存
+ Resolve: 在激活路由前执行数据获取操作
+ CanLoad: 能否按需异步加载功能模块

### CanActivate

未授权用户访问受限路由时，会重定向到登录页面，登录后再返回。

实现一个登录验证服务：

```typescript
//src/app/auth.service.ts (excerpt)
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';
import 'rxjs/add/operator/do';
import 'rxjs/add/operator/delay';

@Injectable()
export class AuthService {
  isLoggedIn = false;

  // store the URL so we can redirect after logging in
  redirectUrl: string;

  login(): Observable<boolean> {
    return Observable.of(true).delay(1000).do(val => this.isLoggedIn = true);
  }

  logout(): void {
    this.isLoggedIn = false;
  }
}
```

实现一个符合 CanActivate 接口的保护类 AuthGuard，当用户未登录时，重定义向登录组件:

```typescript
//src/app/auth-guard.service.ts (v2)
import { Injectable }       from '@angular/core';
import {
  CanActivate, Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot
}                           from '@angular/router';
import { AuthService }      from './auth.service';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    let url: string = state.url;

    return this.checkLogin(url);
  }

  checkLogin(url: string): boolean {
    if (this.authService.isLoggedIn) { return true; }

    // Store the attempted URL for redirecting
    this.authService.redirectUrl = url;

    // Navigate to the login page with extras
    this.router.navigate(['/login']);
    return false;
  }
}
```

登录组件使用 AuthService 服务来进行登录，登录完成后重导航回原来的路由：

```typescript
//src/app/login.component.ts
import { Component }   from '@angular/core';
import { Router }      from '@angular/router';
import { AuthService } from './auth.service';

@Component({
  template: `
    <h2>LOGIN</h2>
    <p>{{message}}</p>
    <p>
      <button (click)="login()"  *ngIf="!authService.isLoggedIn">Login</button>
      <button (click)="logout()" *ngIf="authService.isLoggedIn">Logout</button>
    </p>`
})
export class LoginComponent {
  message: string;

  constructor(public authService: AuthService, public router: Router) {
    this.setMessage();
  }

  setMessage() {
    this.message = 'Logged ' + (this.authService.isLoggedIn ? 'in' : 'out');
  }

  login() {
    this.message = 'Trying to log in ...';

    this.authService.login().subscribe(() => {
      this.setMessage();
      if (this.authService.isLoggedIn) {
        // Get the redirect URL from our auth service
        // If no redirect has been set, use the default
        let redirect = this.authService.redirectUrl ? this.authService.redirectUrl : '/crisis-center/admin';

        // Redirect the user
        this.router.navigate([redirect]);
      }
    });
  }

  logout() {
    this.authService.logout();
    this.setMessage();
  }
}
```

路由定义中加入保护接口：

```typescript
//src/app/admin/admin-routing.module.ts (admin routing)
import { AuthGuard }  from '../auth-guard.service';

const adminRoutes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: '',
        children: [
          { path: 'crises', component: ManageCrisesComponent },
          { path: 'heroes', component: ManageHeroesComponent },
          { path: '', component: AdminDashboardComponent }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(adminRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AdminRoutingModule {}
```

上面的第一个 children 路由中没有指定组件，这是一个 component-less 路由，专门用来组织多个子路由的。

### CanActivateChild: 保护子路由

在父路由上使用，那么其下的所有子路由在激活来都要才受它保护。

实现一个符合 CanActivatedChild 的保护类：


```typescript
//src/app/auth-guard.service.ts (excerpt)
import { Injectable }       from '@angular/core';
import {
  CanActivate, Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  CanActivateChild
}                           from '@angular/router';
import { AuthService }      from './auth.service';

@Injectable()
export class AuthGuard implements CanActivate, CanActivateChild {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    let url: string = state.url;

    return this.checkLogin(url);
  }

  canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    return this.canActivate(route, state);
  }

/* . . . */
}
```

添加到路由定义中：

```typescript
//src/app/admin/admin-routing.module.ts (excerpt)
const adminRoutes: Routes = [
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: '',
        canActivateChild: [AuthGuard],
        children: [
          { path: 'crises', component: ManageCrisesComponent },
          { path: 'heroes', component: ManageHeroesComponent },
          { path: '', component: AdminDashboardComponent }
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(adminRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AdminRoutingModule {}
```

### CanDeactivate: 处理未保存的修改

有些页面是数据是通过点击页面上的取消或保存按钮来进行数据处理的。当用户直接点击其它链接要离开当前页时，需要通过确定窗口明确用户的操作选择，并用异步等待方式等待用户的回答。

创建一个通用的保护类，对所有组件中是否有 `canDeactivate()` 方法进行检测：

```typescript
//src/app/can-deactivate-guard.service.ts
import { Injectable }    from '@angular/core';
import { CanDeactivate } from '@angular/router';
import { Observable }    from 'rxjs/Observable';

export interface CanComponentDeactivate {
 canDeactivate: () => Observable<boolean> | Promise<boolean> | boolean;
}

@Injectable()
export class CanDeactivateGuard implements CanDeactivate<CanComponentDeactivate> {
  canDeactivate(component: CanComponentDeactivate) {
    return component.canDeactivate ? component.canDeactivate() : true;
  }
}
```

具体的组件中实现 `canDeactive()`:

```typescript
//src/app/crisis-center/crisis-detail.component.ts (excerpt)
canDeactivate(): Observable<boolean> | boolean {
  // Allow synchronous navigation (`true`) if no crisis or the crisis is unchanged
  if (!this.crisis || this.crisis.name === this.editName) {
    return true;
  }
  // Otherwise ask the user with the dialog service and return its
  // observable which resolves to true or false when the user decides
  return this.dialogService.confirm('Discard changes?');
}
```

路由定义中使用：

```typescript
//src/app/crisis-center/crisis-center-routing.module.ts (can deactivate guard)
const crisisCenterRoutes: Routes = [
  {
    path: '',
    redirectTo: '/crisis-center',
    pathMatch: 'full'
  },
  {
    path: 'crisis-center',
    component: CrisisCenterComponent,
    children: [
      {
        path: '',
        component: CrisisListComponent,
        children: [
          {
            path: ':id',
            component: CrisisDetailComponent,
            canDeactivate: [CanDeactivateGuard]
          },
          {
            path: '',
            component: CrisisCenterHomeComponent
          }
        ]
      }
    ]
  }
];
```

### Resolve: 预先获取组件数据

先获取组件所需的所有数据后再呈现组件，如果没有获取到相应数据，再重导航到相关其它组件。

路由器会等待 Resolve 保护类操作完成后，才激活相应的路由导航。

实现一个符合 Resolve 接口的保护类：

```typescript
//src/app/crisis-center/crisis-detail-resolver.service.ts
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/take';
import { Injectable }             from '@angular/core';
import { Observable }             from 'rxjs/Observable';
import { Router, Resolve, RouterStateSnapshot,
         ActivatedRouteSnapshot } from '@angular/router';

import { Crisis, CrisisService }  from './crisis.service';

@Injectable()
export class CrisisDetailResolver implements Resolve<Crisis> {
  constructor(private cs: CrisisService, private router: Router) {}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Crisis> {
    let id = route.paramMap.get('id');

    return this.cs.getCrisis(id).take(1).map(crisis => {
      if (crisis) {
        return crisis;
      } else { // id not found
        this.router.navigate(['/crisis-center']);
        return null;
      }
    });
  }
}
```

`CrisisService.getCrisis()` 方法返回一个 `Observable`，从而防止路由器在数据获取完前进行加载。`take(1)` 操作使 `Observable` 发送出一个值时就表示操作完成。

使用保护：

```typescript
import { CrisisDetailResolver }   from './crisis-detail-resolver.service';
const crisisCenterRoutes: Routes = [
  {
    path: '',
    redirectTo: '/crisis-center',
    pathMatch: 'full'
  },
  {
    path: 'crisis-center',
    component: CrisisCenterComponent,
    children: [
      {
        path: '',
        component: CrisisListComponent,
        children: [
          {
            path: ':id',
            component: CrisisDetailComponent,
            canDeactivate: [CanDeactivateGuard],
            resolve: {
              crisis: CrisisDetailResolver
            }
          },
          {
            path: '',
            component: CrisisCenterHomeComponent
          }
        ]
      }
    ]
  }
];
```


这里的 Resolve 保护是基于 `Crisis` 数据模型实现的，用来预先获取 `Crisis` 数据，而获取的数据保存在注入的 `ActivatedRoute` 的 `data` 属性中，访问该数据举例如下：

```typescript
//src/app/crisis-center/crisis-detail.component.ts (ngOnInit v2)
ngOnInit() {
  this.route.data
    .subscribe((data: { crisis: Crisis }) => {
      this.editName = data.crisis.name;
      this.crisis = data.crisis;
    });
}
```

### 路由的可选参数

`fragment` 参数通过页面元素的 `id` 属性值来引用元素位置。

在 `router.navigate()` 方法中通过传入 `NavigationExtras` 对象来设置路由的可选参数（QueryParms, Fragment)：

```typescript
//src/app/auth-guard.service.ts (v3)
checkLogin(url: string): boolean {
    if (this.authService.isLoggedIn) { return true; }

    // Store the attempted URL for redirecting
    this.authService.redirectUrl = url;

    // Create a dummy session id
    let sessionId = 123456789;

    // Set our navigation extras object
    // that contains our global query params and fragment
    let navigationExtras: NavigationExtras = {
      queryParams: { 'session_id': sessionId },
      fragment: 'anchor'
    };

    // Navigate to the login page with extras
    this.router.navigate(['/login'], navigationExtras);
    return false;
  }
```

类似地，如果想在导航过程中一起保持这些可选参数，可：

```typescript
//src/app/login.component.ts (preserve)
// Set our navigation extras object
// that passes on our global query params and fragment
let navigationExtras: NavigationExtras = {
  queryParamsHandling: 'preserve',
  preserveFragment: true
};

// Redirect the user
this.router.navigate([redirect], navigationExtras);
```

如果 `queryParamsHandling` 的值为 `merge`，则进行组合。


组件中对这些可选参数的抽取：

```typescript
//src/app/admin/admin-dashboard.component.ts (v2)
import { Component, OnInit }  from '@angular/core';
import { ActivatedRoute }     from '@angular/router';
import { Observable }         from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Component({
  template:  `
    <p>Dashboard</p>

    <p>Session ID: {{ sessionId | async }}</p>
    <a id="anchor"></a>
    <p>Token: {{ token | async }}</p>
  `
})
export class AdminDashboardComponent implements OnInit {
  sessionId: Observable<string>;
  token: Observable<string>;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    // Capture the session ID if available
    this.sessionId = this.route
      .queryParamMap
      .map(params => params.get('session_id') || 'None');

    // Capture the fragment if available
    this.token = this.route
      .fragment
      .map(fragment => fragment || 'None');
  }
}
```

`RouterLink` 指令中也可通过 `queryParamsHandling` 和  `preserveFragment` 绑定实现相同的效果。


## 异步加载路由

路由定义中用 `loadChildren` 指定路由模块的文件路径及模块类名：

```typescript
//app-routing.module.ts (load children)
{
  path: 'admin',
  loadChildren: 'app/admin/admin.module#AdminModule',
},
```

### CanLoad：保护未授权加载

实现一个符合 `CanLoad` 接口的保护类并应用与路由定义中：

```typescript
//src/app/auth-guard.service.ts (CanLoad guard)
canLoad(route: Route): boolean {
  let url = `/${route.path}`;

  return this.checkLogin(url);
}

//app-routing.module.ts (lazy admin route)
{
  path: 'admin',
  loadChildren: 'app/admin/admin.module#AdminModule',
  canLoad: [AuthGuard]
},
```


## 后台预先加载

`Router` 中提供了 2 种预先加载策略：

1. 不预先加载所有按需加载的模块（默认）
2. 预先加载所有按需加载的模块


通过 `RouterModule.forRoot()` 设置预先加载策略：

```typescript
//src/app/app-routing.module.ts (preload all)
import {
  PreloadAllModules
} from '@angular/router';
RouterModule.forRoot(
  appRoutes,
  {
    enableTracing: true, // <-- debugging purposes only
    preloadingStrategy: PreloadAllModules
  }
)
```

### 自定义预先加载策略

该策略中只预先加载路由定义中 `data.preload` 值为 `true` 的路由。

设置路由定义数据：

```typescript
//src/app/app-routing.module.ts (route data preload)
{
  path: 'crisis-center',
  loadChildren: 'app/crisis-center/crisis-center.module#CrisisCenterModule',
  data: { preload: true }
},
```

自定义策略：

```typescript
//src/app/selective-preloading-strategy.ts (excerpt)
import 'rxjs/add/observable/of';
import { Injectable } from '@angular/core';
import { PreloadingStrategy, Route } from '@angular/router';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SelectivePreloadingStrategy implements PreloadingStrategy {
  preloadedModules: string[] = [];

  preload(route: Route, load: () => Observable<any>): Observable<any> {
    if (route.data && route.data['preload']) {
      // add the route path to the preloaded module array
      this.preloadedModules.push(route.path);

      // log the route path to the console
      console.log('Preloaded: ' + route.path);

      return load();
    } else {
      return Observable.of(null);
    }
  }
}
```

### URL 调整

例如 `heroes` 调整为 `superheroes`，`hero/:id` 调整为 `superhero/:id`:

```typescript
//src/app/heroes/heroes-routing.module.ts (heroes redirects)
const heroesRoutes: Routes = [
  { path: 'heroes', redirectTo: '/superheroes' },
  { path: 'hero/:id', redirectTo: '/superhero/:id' },
  { path: 'superheroes',  component: HeroListComponent },
  { path: 'superhero/:id', component: HeroDetailComponent }
];
```

### 获取路由的最终配置信息（调试用）

```typescript
//src/app/app.module.ts (inspect the router config)
import { Router } from '@angular/router';

export class AppModule {
  // Diagnostic only: inspect router configuration
  constructor(router: Router) {
    console.log('Routes: ', JSON.stringify(router.config, undefined, 2));
  }
}
```

## 参考

+ https://angular.io/guide/router
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/router.ipynb)
