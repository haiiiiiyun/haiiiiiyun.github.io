---
title: Angular2 的 HTTP
date: 2017-03-16
writing-time: 2017-03-16 20:05
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2 form JSONPlaceholder
---

# 概述

Angular 自带的 HTTP 库可以用来调用外部 API，并且这些 HTTP 请求都是异步的。

Javascript 中，实现异步操作通常有 3 种方法：

1. Callback
2. Promise
3. Observable

Angular 2 中采用的是 Observable 方式。


# 导入 HTTP

在组件定义文件中，要从 HTTP 库中导入相关的对象来使用：

```typescript
import { Http, Response, RequestOptions, Headers } from '@angular/http';
```

在入口文件中，还要导入 HttpModule, 这是一个模块集：

```typescript
//...
// 导入 HTTP 模块
import { HttpModule } from '@angular/http';
//...

@NgModule({
  declarations: [
    //...
  ],
  // 将 HTTP 模块放入应用的依赖中，
  // 它能将 Http(及其它一些模块）注入(inject) 我们的组件中
  // 在组件定义中，将 Http 服务这样注入使用：
  //  class MyFooComponent {
  //     constructor(public http: Http){
  //        // 无需定义和赋值，就自动为组件创建了一个 this.http
  //     }
  // 
  //     makeRequest(): void {
  //        // do something with this.http ...
  //     }
  //  }
  imports: [
    BrowserModule,
    HttpModule // <--- right here
  ],
  bootstrap: [ HttpApp ],
  providers: [
    youTubeServiceInjectables
  ]
})
class HttpAppModule {}
```

# 基本请求

实现向 [jsonplaceholder API](http://jsonplaceholder.typicode.com/) 发送 GET 请求，jsonplaceholder API 是一个在线的免费 REST API，可以返回假数据，可用于测试和原型开发。

```typescript
import {Component} from '@angular/core';

// 导入 HTTP 库中的相关对象
import {Http, Response} from '@angular/http';

@Component({
  selector: 'simple-http',

  // 模板中，data 是一个对象，在调试时可通过
  // json 过滤器来显示
  template: `
  <h2>Basic Request</h2>
  <button type="button" (click)="makeRequest()">Make Request</button>
  <div *ngIf="loading">loading...</div>
  <pre>{{data | json}}</pre>
`
})
export class SimpleHTTPComponent {
  data: Object;
  // 通过与模板中的 ngIf 指令结合，可以在数据加载时显示 "loading..."
  loading: boolean;

  // 构造器体是空的，但是当参数是 `private http: Http` 时，
  // TypeScript 将会把 http 赋值给 this.http，实现上等同于：
  //  private http: Http;
  //
  //  constructor(http: Http){
  //     this.http = http
  //  }
  constructor(private http: Http) {
  }

  makeRequest(): void {
    this.loading = true; // 先显示 加载中 ...
    // Http.request 发送一个 GET 请求，返回的是
    // 一个 Observable 对象，可以通过 subscribe
    // 添加侦听者。subscribe(successFn, failureFn, completedFn)。
    // Http.request 返回数据后，会发送一个 Response 对象，
    // 我们可以在 subscribe 的回调函数中进处理。
    this.http.request('http://jsonplaceholder.typicode.com/posts/1')
      .subscribe((res: Response) => {
        this.data = res.json();
        this.loading = false;
      });
  }
}
```

# 创建一个 YouTube 查询组件 YouTubeSearchComponent

通过组件查询后，并显示返回的结果，每个结果的内容包含视频缩略图，描述和视频链接等。

需要实现以下内容：

+ `SearchResult` 对象用来保存每个查询结果数据
+ `YouTubeService` 用来管理到 YouTube 的 API 请求，并将返回结果转成 `SearchResult[]` 类型
+ 一个 `SearchBox` 组件，当用户输入查询条件时，向 `YouTubeService` 请求调用
+ `SearchResultComponent` 用来显示一个 SearchResult
+ `YouTubeSearchComponent` 封装整个应用，并显示所有的结果列表


Angular2 Webpack 项目模板可以使用 [Patrick Stapleton angular2-webpack-starter](https://github.com/AngularClass/angular2-webpack-starter)。


## 实现 SearchResult

```typescript
// 用来保存查询结果
class SearchResult {
  id: string;
  title: string;
  description: string;
  thumbnailUrl: string;
  videoUrl: string;

  // obj? 是一个可选参数，用来模拟关键字参数
  constructor(obj?: any) {
    this.id              = obj && obj.id             || null;
    this.title           = obj && obj.title          || null;
    this.description     = obj && obj.description    || null;
    this.thumbnailUrl    = obj && obj.thumbnailUrl   || null;
    this.videoUrl        = obj && obj.videoUrl       ||
                             `https://www.youtube.com/watch?v=${this.id}`;
  }
}
```


## 实现 YouTubeSearchComponent

```typescript
// 将 YouTube 服务的 API KEY, API URL 定义为常数
// 对于这些环境变量（生产环境、开发环境下有不同的值），
// 最好使它们能可注入(injectable)
export var YOUTUBE_API_KEY: string = 'AIzaSyDOfT_BO81aEZScosfTYMruJobmpjqNeEk';
export var YOUTUBE_API_URL: string = 'https://www.googleapis.com/youtube/v3/search';

// 将这些值做成 injectable，我们使用 {provide: ..., useValue: ...} 语法。
// 这里我们指定将可注入的 YOUTUBE_API_KEY 绑定到值 YOUTUBE_API_KEY（YOUTUBE_API_URL 也一样），将可注入的 YouTubeService 绑定到类 YouTubeService。
// 所有我们将 youTubeServiceInjectables 导出了，所以可以在主入口文件 app.ts 等中使用。
export var youTubeServiceInjectables: Array<any> = [
  {provide: YouTubeService, useClass: YouTubeService},
  {provide: YOUTUBE_API_KEY, useValue: YOUTUBE_API_KEY},
  {provide: YOUTUBE_API_URL, useValue: YOUTUBE_API_URL}
];
```

可使上面的可注入变量注入到我们的整个应用中，需要将它加入到应用的 NgModule 中的 `proviers` 中，因此在主入口文件中：

```typescript
/*
 * Injectables
 */
// 先导入可注入的定义体
import { youTubeServiceInjectables } from 'components/YouTubeSearchComponent';

//...

@NgModule({
  declarations: [
    HttpApp,
    //...
  ],
  imports: [
    //...
  ],
  bootstrap: [ HttpApp ],
  providers: [ // 设置 youTubeServiceInjectables 中的变量注入到全局应用时，即可在应用的所有组件定义中使用
    youTubeServiceInjectables
  ]
})
class HttpAppModule {}
```

## 实现 YouTubeService

```typescript
/**
 * YouTubeService connects to the YouTube API
 * See: * https://developers.google.com/youtube/v3/docs/search/list
 */
// 由于 YouTubeService 类也要定义为可注入，所以使用了 @Injectable() 注解。
@Injectable()
export class YouTubeService {
  // 该构造器中注入了 3 个变量：
  //   1. Http 注入和上面例子中的一样，使用的是隐式注入
  //   2. YOUTUBE_API_KEY 和 YOUTUBE_API_URL 使用 @Inject，是显式注入
  // 注入后，组件中就会生成 this.http, this.apiKey, this.apiUrl 属性了。
  constructor(private http: Http,
              @Inject(YOUTUBE_API_KEY) private apiKey: string,
              @Inject(YOUTUBE_API_URL) private apiUrl: string) {
  }

  // 该方法返回一个 Observable 对象，该对象会发送
  // SearchResult 数组
  search(query: string): Observable<SearchResult[]> {
    let params: string = [
      `q=${query}`,
      `key=${this.apiKey}`,
      `part=snippet`,
      `type=video`,
      `maxResults=10`
    ].join('&');
    let queryUrl: string = `${this.apiUrl}?${params}`;


    // 这里使用 this.http.get 进行 GET 请求，将返回的 Response
    // 进行 map 处理，使每个查询结果转换成 SearchResult 类型。
    return this.http.get(queryUrl)
      .map((response: Response) => {
        // 这里的 `(<any>Response.json()).items`：告诉 TypeScrit 这里无需进行严格的类型检查
        // 在使用 JSON API 时，API 返回通常不会有类型定义，
        // 因此 TypeScript 不会知道返回的应用中会有 items 键，
        // 从而会抛出警告等信息
        return (<any>response.json()).items.map(item => {
          // console.log("raw item", item); // uncomment if you want to debug
          return new SearchResult({
            id: item.id.videoId,
            title: item.snippet.title,
            description: item.snippet.description,
            thumbnailUrl: item.snippet.thumbnails.high.url
          });
        });
      });
  }
}
```

## 实现 SearchBox

续...



# 参考 

+ [HTTP](https://www.ng-book.com/2/)
