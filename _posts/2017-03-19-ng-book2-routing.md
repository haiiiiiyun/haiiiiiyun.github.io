---
title: Angular2 的路由功能
date: 2017-03-19
writing-time: 2017-03-19 17:54--2017-03-21 10:05
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 概述

Web 开发中，路由通常是指基于浏览器中的当前 URL，根据某种规则将应用分割成不同的部分。例如，当访问 `/` 时，路由到主页面，而当访问 `/about` 时，则路由到关于页面等。

在应用中定义路由的好处：

+ 能将应用分割成不同的部分
+ 能维护应用的状态
+ 能基于某种规则保护应用的各部分


## 客户端的路由如何运作

服务端的路由很简单，只需根据进入的 URL 调用不同的控制器来处理。

而客户端路由中，当每次 URL 修改时，我们无需向服务端请求。这种应用称为 "Single Page Pages"(SPA)，服务端只提供一个页面，然后由 JavaScript 呈现不同的页面内容。

客户端的路由主要有 2 种实现方法。

### 老办法：使用 anchor 标签

比如，在页面中，为 a 标签加 `name`，如：

```html
<a name="about"><h1>About</h1></a>
```

之后访问 `http://something/#about`，浏览器直接跳到该标签。SPA 用的是相同的原则，但是对标签名进行了小小改进，使它们看起来更像路径，例如，`about` 路由可为 `http://something/#/about`。这种路由叫 *hash-based routing*。


### 新办法：HTML5 客户端路由

HTML5 中，JavaScript 可以通过 `history.pushState` 方法创建浏览历史，无需向服务器再次请求就能改变显示的 URL。

多数的现代框架都依赖 `pushState`，通过对浏览历史的处理实现路由。

Angular 2 中，默认使用的模式是 HTML5 的，不过可以手动修改为 anchor 标签模式。

使用 HTML5 模式时，需要注意：

+ 很多旧版本的浏览器不支持
+ 服务端必须支持基于 HTML 5 的路由


# 编写首个路由

本例使用 anchor 标签模式的路由。

配置路由就是将 **路径** 映射到 **处理组件**。

本例中，将创建 3 个路由：

+ main 页路由，使用 `/#/home` 路径
+ about 页路由，使用 `/#/about` 路径
+ contact 页路由，使用 `/#contact` 路径
+ 当访问根路径 `/#/` 时，将重定向到 `/#/home`


## 定义路由


```typescript
import { // 加载路由的相关模块
  RouterModule,
  Routes
} from '@angular/router';

// 定义应用的路由：
// + path: 指定该路由要处理的 URL
// + component: 关联该路由的处理组件
// + redirectTo(可选): 用于将某个路径重定向到现存的路由
const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'about', component: AboutComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'contactus', redirectTo: 'contact' },
];
```

## 安装路由

```typescript
// 在应用的 NgModule 中的 imports 区域，通过 RouterModule.forRoot 来安装路由
@NgModule({
  declarations: [
    //...
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes) // <-- 通过这里安装路由
  ],
  bootstrap: [ RoutesDemoApp ],
  providers: [
    { provide: LocationStrategy, useClass: HashLocationStrategy }
  ]
})
class RoutesDemoAppModule {}
```

## 在模板中建立路由链接及定义路由页的内容位置

```typescript
// 在模板中使用 router-outlet 元素定义路由内容的放置位置，
// 即路由链接的内容都会呈现在这个元素内
//
// 使用 <a href="/#/home">Home</a> 也可以定义链接，但是这样的话，
// 当点击链接时，页面会重加载，不适合在 SPA 中使用
// Angular2 中使用 [routerLink] 指令来建立路由链接，这样创建的
// 链接点击时页面不会重加载。
// [routerLink] 指令右侧的表达式是一个数组，其中第一个元素指的是
// 对应的路由路径，其它的元素可以是子元素，路由参数等。
@Component({
  selector: 'router-app',
  template: `
  <div>
    <nav>
      <a>Navigation:</a>
      <ul>
        <li><a [routerLink]="['home']">Home</a></li>
        <li><a [routerLink]="['about']">About</a></li>
        <li><a [routerLink]="['contact']">Contact Us</a></li>
      </ul>
    </nav>

    <router-outlet></router-outlet>
  </div>
  `
})
class RoutesDemoApp {
}
```

## 在 index.html 中进行拼接

```html
<!doctype html>
<html>
  <head>
    <!--
      base 标签以前是用来告诉浏览器，如何对用相对路径表示的
      图片等其它资源进行加载。
      而 Angular Router 也依赖该标签来构建路由，例如，如果
      我们有个路由的路径是 /hello，而 base 元素定义为 href="/app"，
      那么该路由的实际路径将为 "/app/#/hello"。
    -->
    <base href="/">
    <title>ng-book 2: Angular 2 Router</title>

    <!--
      这里的 htmlWebpackPlugin 来自 "webpack module bunder: https://webpack.github.io/，webpack 是一个打包资源文件的工具。
    -->
    {% for (var css in o.htmlWebpackPlugin.files.css) { %}
      <link href="{%=o.htmlWebpackPlugin.files.css[css] %}" rel="stylesheet">
    {% } %}
  </head>
  <body>
    <router-app></router-app>
    <script src="/core.js"></script>
    <script src="/vendor.js"></script>
    <script src="/bundle.js"></script>
  </body>
</html>
```

有时候，Angular 开发人员没有权限修改应用中的 HTML head 区域（比如，团队共用一个模板时）。幸运的是，这种情况下可以通过在应用的 @NgModule 中使用 `APP_BASE_HREF` provider 实现：

```typescript
@NgModule({
  declarations: [
    //...
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes) // <-- 通过这里安装路由
  ],
  bootstrap: [ RoutesDemoApp ],
  providers: [
    { provide: LocationStrategy, useClass: HashLocationStrategy },
    { provide: APP_BASE_HREF, useValue: '/' } // 同 base 标签效果
  ]
})
class RoutesDemoAppModule {}
```

## 创建 HomeComponent, AboutComponent, ContactComponent

都类似：

```typescript
import {Component} from '@angular/core';

@Component({
  selector: 'home',
  template: `<h1>Welcome!</h1>`
})
export class HomeComponent {
}
```

## 路由策略

路由策略就是 Angular 应用关于路径解析和创建路由定义的方法。

默认的策略是 `PathLocationStrategy`，也即 HTML5 路由。使用这种策略时，路由使用一般的路径表示，如 `/home`, `/contact` 等。

可以通过将应用中的 `LocationStrategy` 绑定到某个具体的策略类，来修改路由策略。例如，可将 `PathLocationStrategy` 修改为 `HashLocationStrategy`：

```typescript
@NgModule({
  declarations: [
    //...
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes) // <-- 通过这里安装路由
  ],
  bootstrap: [ RoutesDemoApp ],
  providers: [
    { provide: LocationStrategy, useClass: HashLocationStrategy }
  ]
})
class RoutesDemoAppModule {}
```

要实现自己的路由策略，可参考 HashLocationStrategy 类或 PathLocationStrategy 类的源码。

# 音乐搜索应用

## 路由参数

对于 `/articles/3`，`/articles/4` 这样的 URL，可以通过 `/route/:param` 来指定路由。这里 `:` 后的是路由的参数名。因此，`/articles/3` 等系列 URL 可以用 `articles/:id` 来定义。

```typescript
const routes: Routes = [
  { path: '', redirectTo: 'search', pathMatch: 'full' },
  { path: 'search', component: SearchComponent },
  // 路由中添加参数，当访问 /artists/123 时，
  // 123 将作为路由参数 id 的值传入我们的路由中
  { path: 'artists/:id', component: ArtistComponent }, 
  { path: 'tracks/:id', component: TrackComponent },
  { path: 'albums/:id', component: AlbumComponent },
];
```

## 在组件定义中获取路由参数

先从 `@angular/router` 中导入 ActivatedRoute：

```typescript
import { ActivatedRoute } from '@angular/router';
```

再将 ActivatedRoute 注入到组件的构造器中，例如，假设我们有如下的路由定义：

```typescript
const routers: Router = [
    { path: 'articles/:id', component: ArticlesComponent }
]
```

然后在 ArtistComponent 组件定义中：

```typescript
//...
export class ArtistComponent {
    id: string;

    constructor(private route: ActivatedRoute) {
        // 这里 route.params 是一个 observable。
        // 可以将 params 中的参数值抽取出来
        // 保存到组件属性中
        route.params.subscribe(params => { thid.id = params['id']; });
    }
}
```

## 音乐搜索应用的功能如下 

+ 搜索与关键字匹配的音轨
+ 在网格中显示匹配的音轨
+ 在歌手名上点击时显示歌手的详情
+ 显示唱片的详情，当点击唱片名时显示其中的音轨列表
+ 显示歌曲详情，当点击歌曲名时允许用户播放预览


该应用的路由如下：

+ /search - 搜索表单和结果
+ /artists/:id - 艺术家的信息，通过 Spotify ID 表示
+ /albums/:id - 唱片信息，包含一组音轨，通过 Spotify ID 表示
+ /tracks/:id - 音轨信息与预览，也通过 Spotify ID 表示


这里使用 [Spotify API](https://developer.spotify.com/web-api/) 来获取音轨、艺术家和唱片的信息。

## 导入


```typescript
import {
  Component
} from '@angular/core';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { HttpModule } from '@angular/http';
import { FormsModule } from '@angular/forms';
import {
  RouterModule,
  Routes
} from '@angular/router';
import {
  LocationStrategy,
  HashLocationStrategy,
  APP_BASE_HREF
} from '@angular/common';
```

## SpotifyService 组件来封装 Spotify API

```typescript
import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import {Observable} from 'rxjs/Observable';

import 'rxjs/Rx';

/**
 * SpotifyService works querying the Spotify Web API
 * https://developer.spotify.com/web-api/
 */

// 该类注解为可注入
@Injectable()
export class SpotifyService {
  static BASE_URL: string = 'https://api.spotify.com/v1';

  constructor(private http: Http) {
  }

  // 拼接参数，并实际请求 Spotify API，返回是一个 Observable，
  // 这里通过 RxJS 的 map 函数将 http.request 返回的 Response 对象
  // 转换成 JSON 对象
  query(URL: string, params?: Array<string>): Observable<any[]> {
    let queryURL: string = `${SpotifyService.BASE_URL}${URL}`;
    if (params) {
      queryURL = `${queryURL}?${params.join('&')}`;
    }

    return this.http.request(queryURL).map((res: any) => res.json());
  }

  // 使用 https://developer.spotify.com/web-api/search-item/
  // 可以根据关键字指定类型的元素，如 type=track 时搜索音轨
  search(query: string, type: string): Observable<any[]> {
    return this.query(`/search`, [
      `q=${query}`,
      `type=${type}`
    ]);
  }

  // 搜索音轨
  searchTrack(query: string): Observable<any[]> {
    return this.search(query, 'track');
  }

  // 搜索特定音轨的详情
  getTrack(id: string): Observable<any[]> {
    return this.query(`/tracks/${id}`);
  }

  // 搜索特定艺术家的详情
  getArtist(id: string): Observable<any[]> {
    return this.query(`/artists/${id}`);
  }

  // 搜索特定唱片的详情
  getAlbum(id: string): Observable<any[]> {
    return this.query(`/albums/${id}`);
  }
}

export var SPOTIFY_PROVIDERS: Array<any> = [
  {provide: SpotifyService, useClass: SpotifyService}
];
```


## SearchComponent

```typescript
// 导入
import {Component, OnInit} from '@angular/core';
import {
  Router,
  ActivatedRoute,
} from '@angular/router';

// 导入我们实现的 SpotifyService
import {SpotifyService} from 'services/SpotifyService';

@Component({
  selector: 'search',
  template: `
  <h1>Search</h1>

  <!--
  搜索框部分，
  这里定义当 input 元素的 (keydown.enter) 事件，即当在 input 元素中
  输入回车键时也能触发 form 提交。
  -->
  <p>
    <input type="text" #newquery
      [value]="query"
      (keydown.enter)="submit(newquery.value)">
    <button (click)="submit(newquery.value)">Search</button>
  </p>

  <!--
  显示搜索结果部分，
  使用 ngFor 指令来遍历搜索结果
  -->
  <div *ngIf="results">
    <div *ngIf="!results.length">
      No tracks were found with the term '{{ query }}'
    </div>

    <div *ngIf="results.length">
      <h1>Results</h1>

      <div class="row">
        <div class="col-sm-6 col-md-4" *ngFor="let t of results">
          <div class="thumbnail">
            <div class="content">
              <img src="{{ t.album.images[0].url }}" class="img-responsive">
              <div class="caption">
                <h3>
                  <!--
                  通过数组的第 2 个元素传入路由的参数
                  -->
                  <a [routerLink]="['/artists', t.artists[0].id]">
                    {{ t.artists[0].name }}
                  </a>
                </h3>
                <br>
                <p>
                  <a [routerLink]="['/tracks', t.id]">
                    {{ t.name }}
                  </a>
                </p>
              </div>
              <div class="attribution">
                <h4>
                  <a [routerLink]="['/albums', t.album.id]">
                    {{ t.album.name }}
                  </a>
                </h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  `
})
export class SearchComponent implements OnInit {
  query: string;
  results: Object;

  // 注入 SpotifyService, Router, ActivatedRoute 对象，
  // 以成为组件的属性
  constructor(private spotify: SpotifyService,
              private router: Router,
              private route: ActivatedRoute) {
    // this.route.queryParams 和 this.route.params 不同：
    // + this.route.queryParams 将 URL 参数组织成对象，
    //   例如在 URL http://localhost/#/search?query=cats&order=asc 中，
    //   queryParams['query'] 值为 'cats'
    // + this.route.params 将路由的参数组织成对象
    this.route
      .queryParams
      // 将查询参数保存为组件的属性，以便在刷新时可使用
      .subscribe(params => { this.query = params['query'] || ''; });
  }

  // 在页面加载时进行搜索，
  // 即当我们直接访问带有 query 参数的该 URL 时，也进行搜索操作
  // 组件的构造器中适合对值进行初始化操作，但是要想编写出
  // 好的易测试的代码，那么应该尽可能减少构造器中的代码量，
  // 而最好将组件的初始化逻辑放在下面的挂钩(hook) 方法中。
  // ngOnInit 是 OnInit 接口中的方法
  ngOnInit(): void {
    this.search();
  }

  // 提交表单后进行搜索操作
  // 同时，当访问带有 query 参数的该 URL 时（共享了一个链接或收藏了页面后），
  // 也会进行搜索操作
  submit(query: string): void {
    // 手动告诉路由，导航到 search 路由，并提供了一个 query 参数，
    // 然后再执行实际的搜索。
    // 这种方式有个很大的好处：当浏览器重新加载页面时，可以看到相同的搜索结果。
      // 这就是 "pesisting the search term on the URL"
    this.router.navigate(['search'], { queryParams: { query: query } })
      .then(_ => this.search() );
  }

  // 实际的搜索操作
  search(): void {
    console.log('this.query', this.query);
    if (!this.query) {
      return;
    }

    this.spotify
      .searchTrack(this.query)
      .subscribe((res: any) => this.renderResults(res));
  }

  // 我们将 results 定义为了组件属性，当它的值有修改后，
  // Angular 会自动为我们更新与其关联的视图
  renderResults(res: any): void {
    this.results = null;
    if (res && res.tracks && res.tracks.items) {
      this.results = res.tracks.items;
    }
  }
}
```

进行可以进行搜索测试了。


## TrackComponent

```typescript
import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Location} from '@angular/common';

/*
 * Services
 */
import {SpotifyService} from 'services/SpotifyService';


// angular2 中不能用 'track' 作为选择子
// 因为这是一个已存在的 HTML 元素
// https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track
// 该组件显示音轨的名字，唱片封面图片，
// 并使用 HTML5 audio 标签进行预览播放
@Component({
  selector: 'theTrack',
  template: `
  <div *ngIf="track">
    <h1>{{ track.name }}</h1>

    <p>
      <img src="{{ track.album.images[1].url }}">
    </p>

    <p>
      <audio controls src="{{ track.preview_url }}"></audio>
    </p>

    <p><a href (click)="back()">Back</a></p>
  </div>
  `
})
export class TrackComponent implements OnInit {
  id: string;
  track: Object;

  constructor(private route: ActivatedRoute, private spotify: SpotifyService,
              private location: Location) {
    // 将路由的参数保存为组件的属性
    route.params.subscribe(params => { this.id = params['id']; });
  }

  // 当初始化后，获取音轨的详细信息进行显示
  ngOnInit(): void {
    this.spotify
      .getTrack(this.id)
      .subscribe((res: any) => this.renderTrack(res));
  }

  // 实现页面返回（后退）功能
  back(): void {
    this.location.back();
  }

  renderTrack(res: any): void {
    this.track = res;
  }
}
```

# 路由挂钩 (Router Hooks)

有时需要在切换路由时进行某些操作，例如认证操作等。

假设有一个 login 路由和一个 protected 路由。我们只让已经通过 login 页面登录后的用户才能转到 protected 页面。

实现时，需要为路由添加挂钩，当路由被激活时，调用该挂钩，来确认认证信息等。

## AuthService 服务

```typescript
//file: services/AuthService.ts
//创建登录认证服务
import { Injectable } from '@angular/core';

@Injectable()
export class AuthService {
  login(user: string, password: string): boolean {
    if (user === 'user' && password === 'password') {
      // 成功登录后，将 username 保存到 `localStorage` 
      // localStorage 是 HTML5 提供的键/值对，它能用来
      // 将持久数据保存到浏览器中。
      // API：https://developer.mozilla.org/en-US/docs/Web/API/Storage
      localStorage.setItem('username', user);
      return true;
    }

    return false;
  }

  logout(): any {
    localStorage.removeItem('username');
  }

  getUser(): any {
    return localStorage.getItem('username');
  }

  isLoggedIn(): boolean {
    return this.getUser() !== null;
  }
}

export var AUTH_PROVIDERS: Array<any> = [
  { provide: AuthService, useClass: AuthService }
];
```

## LoginComponent 组件

```typescript
//file:components/LoginComponent.ts

// 该组件当用户登录后显示用户信息和退出链接，
// 用户未登录时显示登录表单
import {Component} from '@angular/core';

/*
 * Services
 */
import {AuthService} from 'services/AuthService';

@Component({
  selector: 'login',
  template: `
  <div class="alert alert-danger" role="alert" *ngIf="message">
    {{ message }}
  </div>

  <!-- 在用户未登录时显示 -->
  <form class="form-inline" *ngIf="!authService.getUser()">
    <div class="form-group">
      <label for="username">User:</label>
      <input class="form-control" name="username" #username>
    </div>

    <div class="form-group">
      <label for="password">Password:</label>
      <input class="form-control" type="password" name="password" #password>
    </div>

    <a class="btn btn-default" (click)="login(username.value, password.value)">
      Submit
    </a>
  </form>

  <!-- 在用户登录后显示 -->
  <div class="well" *ngIf="authService.getUser()">
    Logged in as <b>{{ authService.getUser() }}</b>
    <a href (click)="logout()">Log out</a>
  </div>
  `
})
export class LoginComponent {
  message: string;

  constructor(private authService: AuthService) {
    this.message = '';
  }

  login(username: string, password: string): boolean {
    this.message = '';
    if (!this.authService.login(username, password)) {
      this.message = 'Incorrect credentials.';
      setTimeout(function() {
        this.message = '';
      }.bind(this), 2500);
    }
    return false;
  }

  logout(): boolean {
    this.authService.logout();
    return false;
  }
}
```

## 路由挂钩 canActivate

先创建一个 guard 类，并实现 CanActive 接口（接口中有 canActive 方法）。


```typescript
// file: guards/loggedIn.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { AuthService } from 'services/AuthService';

@Injectable()
export class LoggedInGuard implements CanActivate { // 实现 CanActivate 接口
  // 构造器中 AuthService 注入
  constructor(private authService: AuthService) {}

  // 由于路由的 `canActive` 挂钩配置为了该类，
  // 那么当路由被激活时会调用 canActivate 方法
  canActivate(): boolean {
    return this.authService.isLoggedIn();
  }
}
```

为路由配置挂钩：


```typescript
const routes: Routes = [
  { path: '',          redirectTo: 'home', pathMatch: 'full' },
  { path: 'home',      component: HomeComponent },
  { path: 'about',     component: AboutComponent },
  { path: 'contact',   component: ContactComponent },
  { path: 'protected', component: ProtectedComponent,
    canActivate: [LoggedInGuard]}
];
```

# 嵌套路由

嵌套路由就是将路由包含在路由中。使用嵌套路由后，我们就能封装父路由中的功能，然后将这些功能应用在子路由上。例如，显示所有产品的页是一个父路由，而显示单个产品的页是一个子路由。

## 组件中定义子路由

```typescript
// file: components/ProductsComponent.ts
@Component({
  selector: 'products',

  // 模板中的本地路由用 `./` 作为前缀，例如 ['./main']，
  // 从而表明这些路由是相对于父路由路径的。
  // 我们也可以写成 ['products', 'main']，明确写出父路由，
  // 但是这样写后，子路由就需要了解父路由，当父路由修改
  // 名字后，子路由中也需要跟着修改。
  template: `
  <h2>Products</h2>

  <div class="navLinks">
    <a [routerLink]="['./main']">Main</a> |
    <a [routerLink]="['./interest']">Interest</a> |
    <a [routerLink]="['./sportify']">Sportify</a> |
    Enter id: <input #id size="6">
    <button (click)="goToProduct(id.value)">Go</button>
  </div>

  <!-- 这里的 router-outlet 是为子路由使用的 -->
  <div class="products-area">
    <router-outlet></router-outlet>
  </div>
  `
})

export class ProductsComponent {
  constructor(private router: Router, private route: ActivatedRoute) {
  }

  goToProduct(id:string): void {
    // 这里使用了相对路由
    this.router.navigate(['./', id], {relativeTo: this.route});
  }
}

// 本组件定义了自己的路由
export const routes: Routes = [
  // 当访问 /products 时，会重定向到 /products/main
  { path: '', redirectTo: 'main', pathMatch: 'full' },

  { path: 'main', component: MainComponent },

  // URL 中在 `/products/` 后的数据都会抽取后保存在路由的 id 参数中
  // 如果 id 值与本路由配置中明确定义的 id 值都不同，即
  // 不等于 main, interest, sportify 后，才会激活本条路由
  { path: ':id', component: ByIdComponent },

  { path: 'interest', component: InterestComponent },
  { path: 'sportify', component: SportifyComponent },
];
```

## 在父组件中使用子路由

```typescript
//file: app.ts
import {
  routes as childRoutes,
  ProductsComponent,
  ProductsComponentModule
} from 'components/ProductsComponent';

@Component({
  selector: 'router-app',
  template: `
  <div class="page-header">
    <div class="container">
      <h1>Router Sample</h1>
      <div class="navLinks">
        <a [routerLink]="['/home']">Home</a>
        <a [routerLink]="['/products']">Products</a>
      </div>
    </div>
  </div>

  <div id="content">
    <div class="container">
      <router-outlet></router-outlet>
    </div>
  </div>
  `
})
class RoutesDemoApp {
  constructor(private router: Router) {
  }
}

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'products', component: ProductsComponent, children: childRoutes }
];
```

## 嵌套路由中的链接

用 `[routerLink]="['myRoute']"` 创建的是同级的链接。如果想在子路由中创建父路由级的链接，用 `['/myRoute']`。而在父路由级，想创建子路由链接，则需要将每个路由级都写出，如 `['products', 'sportify']`。



# 参考 

+ [Routing](https://www.ng-book.com/2/)
