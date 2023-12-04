---
title: Angular2 的 HTTP
date: 2017-03-16
writing-time: 2017-03-16 20:05--2017-03-17 14:19
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2 JSONPlaceholder
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
  // TypeScript 将会把 http 赋值给 this.http，实际上等同于：
  //  private http: Http;
  //
  //  constructor(http: Http){
  //     this.http = http
  //  }
  constructor(private http: Http) {
  }

  makeRequest(): void {
    this.loading = true; // 先显示 "loading ..."
    // Http.request 发送一个 GET 请求，返回的是
    // 一个 Observable 对象，可以通过 subscribe
    // 添加侦听者。subscribe(successFn, failureFn, completedFn)。
    // Http.request 返回数据后，会发送一个 Response 对象，
    // 我们可以在 subscribe 的回调函数中进行处理。
    this.http.request('http://jsonplaceholder.typicode.com/posts/1')
      .subscribe((res: Response) => {
        this.data = res.json();
        this.loading = false;
      });
  }
}
```

# 创建一个 YouTube 查询组件 YouTubeSearchComponent

通过组件查询后，显示返回的结果，每个查询结果中包含视频缩略图，描述和视频链接等。

需要实现以下内容：

+ `SearchResult` 对象用来保存每个查询结果数据
+ `YouTubeService` 用来管理对 YouTube 的 API 请求，并将返回结果转成 `SearchResult[]` 类型
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
// 这里我们指定将可注入的 YOUTUBE_API_KEY 绑定到值 YOUTUBE_API_KEY（YOUTUBE_API_URL 也一样），
// 将可注入的 YouTubeService 绑定到类 YouTubeService。
// 将 youTubeServiceInjectables 导出后，就可以在主入口文件 app.ts 等中使用。
export var youTubeServiceInjectables: Array<any> = [
  {provide: YouTubeService, useClass: YouTubeService},
  {provide: YOUTUBE_API_KEY, useValue: YOUTUBE_API_KEY},
  {provide: YOUTUBE_API_URL, useValue: YOUTUBE_API_URL}
];
```

要使上面的可注入变量注入到我们的整个应用中，需要将它加入到应用的 NgModule 中的 `proviers` 中，因此在主入口文件中：

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
        // 在使用 JSON API 时，API 返回不会有类型定义，
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

```typescript
/**
 * SearchBox 显示搜索框，并基于搜索结果发送出事件。
 * 它是 UI 和 YouTubeService 之间的中介。
 * 它实现：
 *   1. 监听 input 上的 keyup 事件，向 YouTubeService 请求查询
 *   2. 当加载时发送出 loading 事件
 *   3. 当返回查询结果时发送出 results 事件
 */

@Component({
  outputs: ['loading', 'results'], // 定义输出事件
  selector: 'search-box',
  template: `
    <input type="text" class="form-control" placeholder="Search" autofocus>
  `
})
export class SearchBox implements OnInit {
  // 该类实现了 OnInit 接口，该接口中定义了 ngOnInit 方法，
  // 在里面可以做一些初始化任务（因为调用 constructor 时像组件的 input 元素
  // 等都还不能操作），只能在 ngOnInit 里操作。
    //
    // 定义及初始化 2 个输出事件
  loading: EventEmitter<boolean> = new EventEmitter<boolean>();
  results: EventEmitter<SearchResult[]> = new EventEmitter<SearchResult[]>();

  // 注入了 2 个对象，其中 el 就是该组件关联的元素，类型是 ElementRef，
  // 它是 Angular 对 HTML 元素的一个封装对象。
  constructor(private youtube: YouTubeService,
              private el: ElementRef) {
  }

  ngOnInit(): void {
      // 当然我们也可以手动侦听 input 框的 keyup 事件，不过由于它
      // 要完成下面的一系列操作，手动侦听有点难度：
      //   1. 过滤掉所有的空或很短的查询
      //   2. "debounce"，不在用户输入每个字符时都进行查询请求，只在用户
      //     输入后暂停一段时间后才去查询
      //   3. 如果用户进行了新的查询，那么只显示新的查询内容
      //
      // 因此，将 `keyup` 事件转成 Rx 的 Observable 流会更简单。
      // 使用 Rx.Observable.fromEvent 进行转换：
    Observable.fromEvent(this.el.nativeElement, 'keyup')  // this.el.nativeElement 就是本组件关联的 DOM 对象，
                                                          //转化成 keyup 事件流后，可以对流进行各种操作。
      .map((e: any) => e.target.value) // 流中的是 keyup 事件 e，e.target 就是事件关联的 input 元素，
                                        //这里的作用是将事件流转成 input 值的流
      .filter((text: string) => text.length > 1) // 过滤掉 input 值流中的空值
      .debounceTime(250)                         // 只有用户输入后暂停 250ms 后才进行查询
      .do(() => this.loading.next(true))        // `do` 操作是对流中的每个事件都进行该操作，但不对流本身进行修改，
                                                //这里是让 this.loading(EventEmitter对象）发送 true 值作为下一个事件，用来显示 'loading...'
      .map((query: string) => this.youtube.search(query)) // 为流中的每个查询值进行实际的查询操作
      .switch() // 表示当有新查询时，只关注最新的查询，忽略旧的查询
      // 查询后返回的是 SearchResult[]，因此现在是一个 SearchResult[] 流
      .subscribe( // 注册侦听流中的每个 SearchResult[] 返回值
        (results: SearchResult[]) => { // 流中出现一个正常的 SearchResult[] 时调用
          this.loading.next(false);  // 发送 false 作为下一个事件，表示隐藏 'loading...' 显示
          this.results.next(results); // 发送 SearchResult[] 作为下一个事件
        },
        (err: any) => { // 当流中出现一个错误时调用
          console.log(err);
          this.loading.next(false);
        },
        () => { // 当流中的某个事件操作完成时都会调用
          this.loading.next(false);
        }
      );

  }
}
```

## 实现 SearchResultComponent

```typescript
// 该组件显示单个查询结果
@Component({
  inputs: ['result'], // 定义输入域，类型为 SearchResult
  selector: 'search-result',
  template: `
   <div class="col-sm-6 col-md-3">
      <div class="thumbnail">
        <img src="{{result.thumbnailUrl}}">
        <div class="caption">
          <h3>{{result.title}}</h3>
          <p>{{result.description}}</p>
          <p><a href="{{result.videoUrl}}"
                class="btn btn-default" role="button">
                Watch</a></p>
        </div>
      </div>
    </div>
  `
})
export class SearchResultComponent {
  result: SearchResult;
}
```


## 实现 YouTubeSearchComponent

```typescript
// 该组件用来整合所有的组件
@Component({
  selector: 'youtube-search',

  template: `
  <div class='container'>
      <div class="page-header">
        <h1>YouTube Search

          <!-- 
           loadingGif 变量来自程序中的 `require` 语句，
           这是 webpack 的图片加载功能（见 https://github.com/tcoopman/image-webpack-loader）
           这里当本地变量 'loading' 为 true 时会显示该图片
          -->
          <img
            style="float: right;"
            *ngIf="loading"
            src='${loadingGif}' />
        </h1>
      </div>

      <div class="row">
        <div class="input-group input-group-lg col-md-12">
          <!--
            绑定 SerarchBox 的输出：
              1. `(loading)="loading = $event"` 表示当 SearchBox 出现 loading 事件时，
                会运行 `loading=$event` 表达式，其中的 $event 是事件发送出的值。
              2. `(results)="updateResults($event)"` 表示当 SearchBox 出现 results 事件时，
                运行组件的 updateResults 方法，其中的 $event 是事件发送出的值 (SearchResult[] 类型）
          -->
          <search-box
             (loading)="loading = $event"
             (results)="updateResults($event)"
              ></search-box>
        </div>
      </div>

      <div class="row">
        <search-result
          *ngFor="let result of results"
          [result]="result">
        </search-result>
      </div>
  </div>
  `
})
export class YouTubeSearchComponent {
  results: SearchResult[];

  updateResults(results: SearchResult[]): void {
    this.results = results;
    // console.log("results:", this.results); // uncomment to take a look
  }
}
```

# @angular/http API 中的其它请求方法

## POST 请求

```typescript
  makePost(): void {
    this.loading = true;
    this.http.post(
      'http://jsonplaceholder.typicode.com/posts',

      // 将参数 Object 对象先转成 JSON 字符串
      JSON.stringify({
        body: 'bar',
        title: 'foo',
        userId: 1
      }))
      .subscribe((res: Response) => {
        this.data = res.json();
        this.loading = false;
      });
  }
```

## PUT/PATCH/DELETE/HEAD 等

+ http.put 和 http.patch 分别对应 PUT 和 PATCH，调用参数是 URL + 参数体
+ http.delete 和 http.head 对应 DELETE 和 HEAD，调用参数只有 URL

```typescript
  makeDelete(): void {
    this.loading = true;
    this.http.delete('http://jsonplaceholder.typicode.com/posts/1')
      .subscribe((res: Response) => {
        this.data = res.json();
        this.loading = false;
      });
  }
```

## RequestOptions

上面的所有 http 请求方法都可带上一个可选参数 `RequestOptions`，该对象封装了：

+ method
+ headers
+ body
+ mode
+ credentials
+ cache
+ url
+ search


例如：

```typescript
  makeHeaders(): void {
    // 添加一个新的 Header
    let headers: Headers = new Headers();
    headers.append('X-API-TOKEN', 'ng-book');

    let opts: RequestOptions = new RequestOptions();
    opts.headers = headers;

    this.http.get('http://jsonplaceholder.typicode.com/posts/1', opts)
      .subscribe((res: Response) => {
        this.data = res.json();
      });
  }
```


# 参考 

+ [HTTP](https://www.ng-book.com/2/)
