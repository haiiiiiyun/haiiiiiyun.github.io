---
title: Angular docs-教程 6： HTTP
date: 2017-06-15
writing-time: 2017-08-25
categories: programming
tags: angular node Angular&nbsp;docs
---


# 教程 6：HTTP


## 提供 HTTP 服务

`HttpModule` 不是核心的 NgModule，它位于 `@angular/http` 模块中。

### 注册 HTTP 服务

`@angular/http` 库中的 `HttpModule` 中提供了所有的 HTTP 服务，要想能在所有组件中使用这些服务，只需将 `HttpModule` 加入到全局模块 `AppModule` 的 `imports` 即可。

```typescript
//src/app/app.module.ts (v1)
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent }         from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { HeroesComponent }      from './heroes.component';
import { HeroDetailComponent }  from './hero-detail.component';
import { HeroService }          from './hero.service';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    HeroDetailComponent,
    HeroesComponent,
  ],
  providers: [ HeroService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 模拟 web API

推荐将全局范围的服务注册在 `AppModule` 的 `providers` 中。

现使用模拟的 Web 服务器 in-memory web api，本例中的 HTTP 客户端都与该模拟服务器交互。

```typescript
//src/app/app.module.ts (v2)
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';

import { AppRoutingModule } from './app-routing.module';

// Imports for loading & configuring the in-memory web api
import { InMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService }  from './in-memory-data.service';

import { AppComponent }         from './app.component';
import { DashboardComponent }   from './dashboard.component';
import { HeroesComponent }      from './heroes.component';
import { HeroDetailComponent }  from './hero-detail.component';
import { HeroService }          from './hero.service';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    InMemoryWebApiModule.forRoot(InMemoryDataService),
    AppRoutingModule
  ],
  declarations: [
    AppComponent,
    DashboardComponent,
    HeroDetailComponent,
    HeroesComponent,
  ],
  providers: [ HeroService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

通过在 AppModule 的 `imports` 中添加 `InMemoryWebApiModule`，实现将 HTTP 客户端的 XHR 后端服务与该模拟服务器交互。`forRoot()` 方法需要传入一个 `InMemoryDataService` 类，该类用来配置数据库，定义在 `in-memory-data-service.ts` 中：

```typescript
//src/app/in-memory-data.service.ts
import { InMemoryDbService } from 'angular-in-memory-web-api';
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const heroes = [
      { id: 0,  name: 'Zero' },
      { id: 11, name: 'Mr. Nice' },
      { id: 12, name: 'Narco' },
      { id: 13, name: 'Bombasto' },
      { id: 14, name: 'Celeritas' },
      { id: 15, name: 'Magneta' },
      { id: 16, name: 'RubberMan' },
      { id: 17, name: 'Dynama' },
      { id: 18, name: 'Dr IQ' },
      { id: 19, name: 'Magma' },
      { id: 20, name: 'Tornado' }
    ];
    return {heroes};
  }
}
```

该文件用来代替原来的 `mock-heroes.ts`，故原来的旧文件现可删除。

## Heroes 和 HTTP

将 `HeroService.getHeroes()` 转化为使用 HTTP：

```typescript
//src/app/hero.service.ts (updated getHeroes and new class members)
private heroesUrl = 'api/heroes';  // URL to web api

constructor(private http: Http) { }

getHeroes(): Promise<Hero[]> {
  return this.http.get(this.heroesUrl)
             .toPromise()
             .then(response => response.json().data as Hero[])
             .catch(this.handleError);
}

private handleError(error: any): Promise<any> {
  console.error('An error occurred', error); // for demo purposes only
  return Promise.reject(error.message || error);
}
```

并加入相关的导入语句：

```typescript
//src/app/hero.service.ts (updated imports)
import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Hero } from './hero';
```

### HTTP Promise

`http.get` 返回 RxJS Observable，它是一种异步数据流。这里通过 `.toPromise()` 它 Observable 转成 Promise。

Angular 中实现的 `Observable` 没有内置 `toPromise` 等操作符，要对 Observable 进行扩展，只需将扩展功能从 RxJS 库导入即可：

```javascript
import 'rxjs/add/operator/toPromise';
```

### 在 then 回调函数中抽取数据

```javascript
.then(response => response.json().data as Hero[])
```

### 在 catch 回调函数中处理异常

```javascript
.catch(this.handleError);
```

## 根据 id 获取 hero

```typescript
//src/app/hero.service.ts
getHero(id: number): Promise<Hero> {
  const url = `${this.heroesUrl}/${id}`;
  return this.http.get(url)
    .toPromise()
    .then(response => response.json().data as Hero)
    .catch(this.handleError);
}
```

### HeroService API 未改变

虽然 getHeroes() 和 getHero() 的实现改变了，但是接口未改变，因此系统中的其它交互部分都无需修改。

## 更新 hero details


### 保存修改

在 hero detail 模板中，添加一个 button 标签，将其 `click` 事件绑定到 `save()` 方法：

```html
<!--src/app/hero-detail.component.html (save)-->
<button (click)="save()">Save</button>
```

```typescript
//src/app/hero-detail.component.ts (save)
save(): void {
  this.heroService.update(this.hero)
    .then(() => this.goBack());
}
```

### 在 HeroService 中添加 update()

使用 `http.put()` 将数据提交到服务端。

```typescript
//src/app/hero.service.ts (update)
private headers = new Headers({'Content-Type': 'application/json'});

update(hero: Hero): Promise<Hero> {
  const url = `${this.heroesUrl}/${hero.id}`;
  return this.http
    .put(url, JSON.stringify(hero), {headers: this.headers})
    .toPromise()
    .then(() => hero)
    .catch(this.handleError);
}
```

## 添加 hero

在 hero 列表组件模板的前面，添加一个 input 及 button 标签，input 用来输入 hero 的名字，button 的 click 事件绑定到 组件的 add 函数，实现将新 hero 保存到服务端。

```html
<!--src/app/heroes.component.html (add)-->
<div>
  <label>Hero name:</label> <input #heroName />
  <button (click)="add(heroName.value); heroName.value=''">
    Add
  </button>
</div>
```

```typescript
//src/app/heroes.component.ts (add)
add(name: string): void {
  name = name.trim();
  if (!name) { return; }
  this.heroService.create(name)
    .then(hero => {
      this.heroes.push(hero);
      this.selectedHero = null;
    });
}
```

```typescript
//src/app/hero.service.ts (create)
create(name: string): Promise<Hero> {
  return this.http
    .post(this.heroesUrl, JSON.stringify({name: name}), {headers: this.headers})
    .toPromise()
    .then(res => res.json().data as Hero)
    .catch(this.handleError);
}
```

## 删除 hero

hero 列表中的每项都添加一个删除按钮。


```html
<!--src/app/heroes.component.html (li-element)-->
<li *ngFor="let hero of heroes" (click)="onSelect(hero)"
    [class.selected]="hero === selectedHero">
  <span class="badge">{{hero.id}}</span>
  <span>{{hero.name}}</span>
  <button class="delete"
    (click)="delete(hero); $event.stopPropagation()">x</button>
</li>
```


button 的 click 事件绑定到组件的 delete 方法，同时，通过 `event.stopPropagation()` 禁止 click 事件向上级流动，不然点击删除后，又会触发选中的事件。

```typescript
//src/app/heroes.component.ts (delete)
delete(hero: Hero): void {
  this.heroService
      .delete(hero.id)
      .then(() => {
        this.heroes = this.heroes.filter(h => h !== hero);
        if (this.selectedHero === hero) { this.selectedHero = null; }
      });
}
```

```typescript
//src/app/hero.service.ts (delete)
delete(id: number): Promise<void> {
  const url = `${this.heroesUrl}/${id}`;
  return this.http.delete(url, {headers: this.headers})
    .toPromise()
    .then(() => null)
    .catch(this.handleError);
}
```

为删除的按钮添加样式：

```css
/*src/app/heroes.component.css (additions)*/
button.delete {
  float:right;
  margin-top: 2px;
  margin-right: .8em;
  background-color: gray !important;
  color:white;
}
```

## Observable

每个 `Http` 服务的方法都返回一个 Http `Response` 对象的 `Observable`。

一个 `Observable` 就是一个事件流，可以像操作数组一个来操作它。Angular 内核实现了 `Observable` 的基本功能，其它的操作符和扩展功能都需要从 [RxJS 库](http://reactivex.io/rxjs) 导入。

## 添加名字查询能力

当用户在输入框中输入名字后，将重复发送 HTTP 请求，来过滤显示相应列表。

创建 `HeroSearchService` 服务：

```typescript
//src/app/hero-search.service.ts
import { Injectable } from '@angular/core';
import { Http }       from '@angular/http';

import { Observable }     from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { Hero }           from './hero';

@Injectable()
export class HeroSearchService {

  constructor(private http: Http) {}

  search(term: string): Observable<Hero[]> {
    return this.http
               .get(`api/heroes/?name=${term}`)
               .map(response => response.json().data as Hero[]);
  }
}
```


这里的 `http.get()` 返回 Observable, 链接的另一个 RxJS 操作符 `.map()` 实现从应答数据中抽取 heroes。

### HeroSearchComponent

模板中只包含一个文本枉和匹配查询结果的列表：

```html
<!--src/app/hero-search.component.html-->
<div id="search-component">
  <h4>Hero Search</h4>
  <input #searchBox id="search-box" (keyup)="search(searchBox.value)" />
  <div>
    <div *ngFor="let hero of heroes | async"
         (click)="gotoDetail(hero)" class="search-result" >
      {{hero.name}}
    </div>
  </div>
</div>
```

搜索框的 `keyup` 事件绑定组件的 `search()` 方法。`*ngFor` 遍历组件的 `heroes` 属性。但是由于该属性现在是一个 hero 数组的 Observable，不是一个简单的 hero 数组。因此并且通过 `async` 管道 (AsyncPipe) 处理后才能被 `*ngFor` 使用。`async` 订阅到该 `Observable`，并为 `*ngFor` 产生 hero 数组。

```typescript
//src/app/hero-search.component.ts
import { Component, OnInit } from '@angular/core';
import { Router }            from '@angular/router';

import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';

// Observable class extensions
import 'rxjs/add/observable/of';

// Observable operators
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';

import { HeroSearchService } from './hero-search.service';
import { Hero } from './hero';

@Component({
  selector: 'hero-search',
  templateUrl: './hero-search.component.html',
  styleUrls: [ './hero-search.component.css' ],
  providers: [HeroSearchService]
})
export class HeroSearchComponent implements OnInit {
  heroes: Observable<Hero[]>;
  private searchTerms = new Subject<string>();

  constructor(
    private heroSearchService: HeroSearchService,
    private router: Router) {}

  // Push a search term into the observable stream.
  search(term: string): void {
    this.searchTerms.next(term);
  }

  ngOnInit(): void {
    this.heroes = this.searchTerms
      .debounceTime(300)        // wait 300ms after each keystroke before considering the term
      .distinctUntilChanged()   // ignore if next search term is same as previous
      .switchMap(term => term   // switch to new observable each time the term changes
        // return the http search observable
        ? this.heroSearchService.search(term)
        // or the observable of empty heroes if there was no search term
        : Observable.of<Hero[]>([]))
      .catch(error => {
        // TODO: add real error handling
        console.log(error);
        return Observable.of<Hero[]>([]);
      });
  }

  gotoDetail(hero: Hero): void {
    let link = ['/detail', hero.id];
    this.router.navigate(link);
  }
}
```

### 查询关键字

注意到 `searchTerms`:

```typscript
private searchTerms = new Subject<string>();

// Push a search term into the observable stream.
search(term: string): void {
  this.searchTerms.next(term);
}
```

`Subject` 是 observable 事件流的生产者，因此 `searchTerms` 生产字符串的 Observable。

每次调用 `search` 都通过 `next()` 将一个字符串放入 Observable 流中。



样式文件：

```css
/*src/app/hero-search.component.css*/
.search-result{
  border-bottom: 1px solid gray;
  border-left: 1px solid gray;
  border-right: 1px solid gray;
  width:195px;
  height: 16px;
  padding: 5px;
  background-color: white;
  cursor: pointer;
}

.search-result:hover {
  color: #eee;
  background-color: #607D8B;
}

#search-box{
  width: 200px;
  height: 20px;
}
```

### 初始化 heroes 属性(ngOnInit)

一个 `Subject` 就是一个 `Observable`，故可以将查询关键字的流转换成 `Hero` 数组的流，并保存到 `heroes` 属性中。

```typescript
heroes: Observable<Hero[]>;

ngOnInit(): void {
  this.heroes = this.searchTerms
    .debounceTime(300)        // wait 300ms after each keystroke before considering the term
    .distinctUntilChanged()   // ignore if next search term is same as previous
    .switchMap(term => term   // switch to new observable each time the term changes
      // return the http search observable
      ? this.heroSearchService.search(term)
      // or the observable of empty heroes if there was no search term
      : Observable.of<Hero[]>([]))
    .catch(error => {
      // TODO: add real error handling
      console.log(error);
      return Observable.of<Hero[]>([]);
    });
}
```

[switchMap 操作符](http://www.learnrxjs.io/operators/transformation/switchmap.html)（之前叫 flatMapLatest)后，每个过滤的有效按键都触发 http() 调用。即使各请求间有 300ms 的延时，还会同时多个并行处理的 HTTP，并且返回的次序与提高的次序不同。

`switchMap()` 只从最近的 http 请求返回 observalbe, 从而确保了源请求序，之前的调用结果都将取消或作废。

### 导入 RxJS 操作符

```typescript
//src/app/hero-search.component.ts (rxjs imports)
import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';

// Observable class extensions
import 'rxjs/add/observable/of';

// Observable operators
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';
```

`import 'rxjs/add/...` 这是语法不导入符号，它只是执行库对应的脚本文件，从而实现对  `Observable` 类的扩展。

## 将 HeroSearchComponent 添加到 dashboard

```html
<!--src/app/dashboard.component.html-->
<h3>Top Heroes</h3>
<div class="grid grid-pad">
  <a *ngFor="let hero of heroes"  [routerLink]="['/detail', hero.id]"  class="col-1-4">
    <div class="module hero">
      <h4>{{hero.name}}</h4>
    </div>
  </a>
</div>
<hero-search></hero-search>
```

最后将 `HeroSearchComponent` 添加到 AppModule 的 `declarations`。


## 参考

+ https://angular.io/tutorial/toh-pt6
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_6_http.ipynb)
