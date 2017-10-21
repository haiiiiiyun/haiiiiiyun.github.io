---
title: Angular docs-Http
date: 2017-10-21
writing-time: 2017-10-21
categories: programming
tags: angular node Angular&nbsp;docs
---

# Http

## HttpClient

现代浏览器一般用 `XMLHttpRequest` 接口和 `fetch()` API 来完成 HTTP 请求。`@angular/common/http` 中的 `HttpClient` 是基于 `XMLHttpRequest` 接口实现的。

### 设置

```typescript
// app.module.ts:

import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

// Import HttpClientModule from @angular/common/http
import {HttpClientModule} from '@angular/common/http';

@NgModule({
  imports: [
    BrowserModule,
    // Include it under 'imports' in your application module
    // after BrowserModule.
    HttpClientModule,
  ],
})
export class MyAppModule {}
```

### 请求 JSON 数据

使用 `HttpClient.get()` 直接访问数据：

```typescript
@Component(...)
export class MyComponent implements OnInit {

  results: string[];

  // Inject HttpClient into your component or service.
  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Make the HTTP request:
    this.http.get('/api/items').subscribe(data => {
      // Read the result field from the JSON response.
      this.results = data['results'];
    });
  }
}
```

### 应答对象的类型

上面返回的应答对象 `data` 是 `Object`，没有类型信息，因此只能用 `data['results']` 访问，不能用 `data.results` 访问。

可以为应答对象创建接口，将接口作为类型参数传入 `get()`，可实现对返回的应答对象的类型限定：

```typescript
interface ItemsResponse {
  results: string[];
}

http.get<ItemsResponse>('/api/items').subscribe(data => {
  // data is now an instance of type ItemsResponse, so you can do this:
  this.results = data.results;
});
```

### 读取全部的应答信息

上面只读取了应答的 body 部分，要读取 header, status codes 等全部应答信息，可为 `get()` 提供 `observe` 选项实现：

```typescript
http
  .get<MyJsonData>('/data.json', {observe: 'response'})
  .subscribe(resp => {
    // Here, resp is of type HttpResponse<MyJsonData>.
    // You can inspect its headers:
    console.log(resp.headers.get('X-Custom-Header'));
    // And access the body directly, which is typed as MyJsonData as requested.
    // resp.body is type of MyJsonData
    console.log(resp.body.someField);
  });
```

### 错误处理

`.subscribe` 的第 2 个参数是错误处理回调函数：

```typescript
http
  .get<ItemsResponse>('/api/items')
  .subscribe(
    // Successful responses call the first callback.
    data => {...},
    // Errors will call this callback instead:
    err => {
      console.log('Something went wrong!');
    }
  );
```

### 错误详细信息

上面的 `err` 参数是 `HttpErrorResponse` 类型。共有 2 种类型的错误，一种是后端返回失败代码（如 404, 500)，另一种是客户端出错（如网络问题请求未发出），此时会抛出 `Error`。这种错误都能通过 `HttpErrorRespose` 对象识别出：

```typescript
http
  .get<ItemsResponse>('/api/items')
  .subscribe(
    data => {...},
    (err: HttpErrorResponse) => {
      if (err.error instanceof Error) {
        // A client-side or network error occurred. Handle it accordingly.
        console.log('An error occurred:', err.error.message);
      } else {
        // The backend returned an unsuccessful response code.
        // The response body may contain clues as to what went wrong,
        console.log(`Backend returned code ${err.status}, body was: ${err.error}`);
      }
    }
  );
```

### 重发请求

```typescript
import 'rxjs/add/operator/retry';

http
  .get<ItemsResponse>('/api/items')
  // Retry this request up to 3 times.
  .retry(3)
  // Any errors after the 3rd retry will fall through to the app.
  .subscribe(...);
```
 
### 请求非 JSON 数据

```typescript
http
  .get('/textfile.txt', {responseType: 'text'})
  // The Observable returned by get() is of type Observable<string>
  // because a text response was specified. There's no need to pass
  // a <string> type parameter to get().
  .subscribe(data => console.log(data));
```

## 发送 POST 请求

```typescript
const body = {name: 'Brad'};

http
  .post('/api/developers/add', body)
  // See below - subscribe() is still necessary when using post().
  .subscribe(...);
```

注意 `subscribe()` 方法，`HttpClient` 中所有其它方法返回都是 `Observable` ，它只是一个发送请求的 blueprint, 没有实际发送出去，只有调用 `subscribe()` 后才实际发送出去，而且调用一次即发送一次：

```typescript
const req = http.post('/api/items/add', body);
// 0 requests made - .subscribe() not called.
req.subscribe();
// 1 request made.
req.subscribe();
// 2 requests made.
```

### 配置 POST 请求头

```typescript
http
  .post('/api/items/add', body, {
    headers: new HttpHeaders().set('Authorization', 'my-auth-token'),
  })
  .subscribe();
```

`HttpHeaders` 类是不能修改的，因此每次 `set()` 后才会返回一个应用修改后的新实例。


### 配置 POST 的 URL 参数

```typescript
http
  .post('/api/items/add', body, {
    params: new HttpParams().set('id', '3'),
  })
  .subscribe();
```

此时的 URL 为 `/api/items/add?id=3`。


## 高级用法

使用拦截功能，可以在请求发送到服务端前进行修改，应答在应用接收到前进行修改。

### 编写一个拦截器

实现一个拦截器，即实现一个 `HttpInterceptor` 接口，其中只有一个 `intercept` 方法，例如：

```typescript
import {Injectable} from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest} from '@angular/common/http';

@Injectable()
export class NoopInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req);
  }
}
```

`intercept` 方法实现将一个请求对象转换成一个 Observable, 该 Observable 最终返回一个应答对象。拦截器对请求进行修改后，传到拦截链的下一站，其处理模式类似一些系统中的 middleware 框架。

### 使用自定义拦截器

```typescript
import {NgModule} from '@angular/core';
import {HTTP_INTERCEPTORS} from '@angular/common/http';

@NgModule({
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: NoopInterceptor,
    multi: true,
  }],
})
export class AppModule {}
```

注意 `mult:true` 选项，表示 `HTTP_INTERCEPTORS` 是一个列表值，`HTTP_INTERCEPTORS` 会收集所有的拦截器。

### 事件

`intercept` 和 `HttpHandler.handle` 返回的是 `Observable<HttpEvent<any>>` 而不是 `Observable<HttpResponse<any>>`，这是因为拦截器工作在 `HttpClient` 接口的更低层。每个请求都会产生多个事件，包括上传和下载过程事件。`HttpResponse` 类实际上是一个 `type` 为 `HttpEventType.HttpResponseEvent` 的事件。

### 次序

多个拦截器的应用次序，就是其在 `providers` 中的次序。

### 不可修改性

`HttpRequest` 和 `HttpResponse` 类是不可修改的，这是因为可能有请求重发的情况。

不可修改性确保了在请求重试时，拦截器看到的请求对象是一样的。

同样，在拦截器中也不能直接对请求体进行修改。要修改时，先创建请求体的复本，修改后，再用 `clone()` 创建一个新的请求对象，再设置修改后的请求体：

```typescript
intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  // This is a duplicate. It is exactly the same as the original.
  const dupReq = req.clone();

  // Change the URL and replace 'http://' with 'https://'
  const secureReq = req.clone({url: req.url.replace('http://', 'https://')});
}
```

下面是设置请求头的例子：

```typescript
import {Injectable} from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest} from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the auth header from the service.
    const authHeader = this.auth.getAuthorizationHeader();
    // Clone the request to add the new header.
    const authReq = req.clone({headers: req.headers.set('Authorization', authHeader)});
    // Pass on the cloned request instead of the original request.
    return next.handle(authReq);
  }
}
```

对请求对象设置请求头可以简写为：

```typescript
const authReq = req.clone({setHeaders: {Authorization: authHeader}});
```

### 拦截器实现请求记时功能

```typescript
import 'rxjs/add/operator/do';

export class TimingInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  	const started = Date.now();
    return next
      .handle(req)
      .do(event => {
        if (event instanceof HttpResponse) {
          const elapsed = Date.now() - started;
          console.log(`Request for ${req.urlWithParams} took ${elapsed} ms.`);
        }
      });
  }
}
```

RxJS 的 `do()` 操作符在 `Observable` 上添加了一个操作，并不影响流上的值。

### 拦截器实现缓存

例如下面是缓存接口：

```typescript
abstract class HttpCache {
  /**
   * Returns a cached response, if any, or null if not present.
   */
  abstract get(req: HttpRequest<any>): HttpResponse<any>|null;

  /**
   * Adds or updates the response in the cache.
   */
  abstract put(req: HttpRequest<any>, resp: HttpResponse<any>): void;
}
```

下面是用法：

```typescript
@Injectable()
export class CachingInterceptor implements HttpInterceptor {
  constructor(private cache: HttpCache) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  	// Before doing anything, it's important to only cache GET requests.
    // Skip this interceptor if the request method isn't GET.
    if (req.method !== 'GET') {
      return next.handle(req);
    }

    // First, check the cache to see if this request exists.
    const cachedResponse = this.cache.get(req);
    if (cachedResponse) {
      // A cached response exists. Serve it instead of forwarding
      // the request to the next handler.
      return Observable.of(cachedResponse);
    }

    // No cached response exists. Go to the network, and cache
    // the response when it arrives.
    return next.handle(req).do(event => {
      // Remember, there may be other events besides just the response.
      if (event instanceof HttpResponse) {
      	// Update the cache.
      	this.cache.put(req, event);
      }
    });
  }
}
```

下面的用法中，如果请求有缓存，即返回缓存的应答，也返回最新的应答：

```typescript
intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  // Still skip non-GET requests.
  if (req.method !== 'GET') {
    return next.handle(req);
  }

  // This will be an Observable of the cached value if there is one,
  // or an empty Observable otherwise. It starts out empty.
  let maybeCachedResponse: Observable<HttpEvent<any>> = Observable.empty();

  // Check the cache.
  const cachedResponse = this.cache.get(req);
  if (cachedResponse) {
    maybeCachedResponse = Observable.of(cachedResponse);
  }

  // Create an Observable (but don't subscribe) that represents making
  // the network request and caching the value.
  const networkResponse = next.handle(req).do(event => {
    // Just like before, check for the HttpResponse event and cache it.
    if (event instanceof HttpResponse) {
      this.cache.put(req, event);
    }
  });

  // Now, combine the two and send the cached response first (if there is
  // one), and the network response second.
  return Observable.concat(maybeCachedResponse, networkResponse);
}
```

### 侦听过程事件

用来在传输大文件时提供反馈。

在创建 `HttpRequest` 实例时传入 `reportProgress` 选项后，该请求就会产生过程事件：

```typescript
const req = new HttpRequest('POST', '/upload/file', file, {
  reportProgress: true,
});
```

之后 `HttpClient.request()` 会产生一个事件的 `Observable` 对象：

```typescript
http.request(req).subscribe(event => {
  // Via this API, you get access to the raw event stream.
  // Look for upload progress events.
  if (event.type === HttpEventType.UploadProgress) {
    // This is an upload progress event. Compute and show the % done:
    const percentDone = Math.round(100 * event.loaded / event.total);
    console.log(`File is ${percentDone}% uploaded.`);
  } else if (event instanceof HttpResponse) {
    console.log('File is completely uploaded!');
  }
});
```

## XSRF 保护

在进行 HTTP 请求时，某拦截器会从 cookie 中读取一个 token 值（通常键为 `XSRF-TOKEN`)，将值设置为头 `X-XSRF-TOKEN` 的值。由于只有本域内的代码能读取 cookie，从而后端能确保该请求来自自己的客户端。

自定义 cookie/header 名如下：

```typescript
imports: [
  HttpClientModule,
  HttpClientXsrfModule.withConfig({
    cookieName: 'My-Xsrf-Cookie',
    headerName: 'My-Xsrf-Header',
  }),
]
```

## 参考

+ https://angular.io/guide/http
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/http.ipynb)
