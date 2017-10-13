---
title: Angular docs-模板与数据绑定-管道
date: 2017-10-13
writing-time: 2017-10-13
categories: programming
tags: angular node Angular&nbsp;docs
---

## 使用管道

管道接收一个数据为输入，并将其转变成需要的输出。下例中将组件的 birthday 属性转换成了可读的日期格式输出：


```typescript
//src/app/hero-birthday1.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'hero-birthday',
  template: `<p>The hero's birthday is {{ birthday | date }}</p>`
})
export class HeroBirthdayComponent {
  birthday = new Date(1988, 3, 15); // April 15, 1988
}
```

`Date` 和 `Currency` 管道需要 ECMAScript 国际化 API 的支持， Safari 和一些旧浏览器不支持，因此需要加入 polyfill 来实现：

```html
<script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=Intl.~locale.en"></script>
```

## 内置管道

像 `DatePipe`, `UpperCasePipe`, `LowerCasePipe`, `CurrencyPipe`, `PercentPipe` 等内置管道可以在任何模板中使用。

所有内置管道见 [pipes topics](https://angular.io/api?type=pipe)。

## 管道参数

管道可接收任意多个参数来调整输出。传参时以 `:arg_val` 形式进行，如 `currency:'EUR'`，`slice:1:5` 等，完整例子为：

```html
<p>The hero's birthday is {{ birthday | date:"MM/dd/yy" }} </p>
```

参数值可为任何有效的模板表达式，例如字符串值或组件的属性等。例如下例中参数值绑定到组件的一个属性，同时该属性时可动态修改：

```typescript
//src/app/hero-birthday2.component.ts
template: `
  <p>The hero's birthday is {{ birthday | date:format }}</p>
  <button (click)="toggleFormat()">Toggle Format</button>
`

export class HeroBirthday2Component {
  birthday = new Date(1988, 3, 15); // April 15, 1988
  toggle = true; // start with true == shortDate

  get format()   { return this.toggle ? 'shortDate' : 'fullDate'; }
  toggleFormat() { this.toggle = !this.toggle; }
}
```

## 多个管道可串联

```html
The chained hero's birthday is
{{ birthday | date | uppercase}}


The chained hero's birthday is
{{  birthday | date:'fullDate' | uppercase}}
```

## 自定义管道

定义一个进行指数计算的管道：

```typescript
//src/app/exponential-strength.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';
/*
 * Raise the value exponentially
 * Takes an exponent argument that defaults to 1.
 * Usage:
 *   value | exponentialStrength:exponent
 * Example:
 *   {{ 2 | exponentialStrength:10 }}
 *   formats to: 1024
*/
@Pipe({name: 'exponentialStrength'})
export class ExponentialStrengthPipe implements PipeTransform {
  transform(value: number, exponent: string): number {
    let exp = parseFloat(exponent);
    return Math.pow(value, isNaN(exp) ? 1 : exp);
  }
}
```

管道定义要点：

+ 一个管道就是由 `@Pipe` 装饰器装饰的类
+ 管道类实现 `PipeTransform` 接口中的 `transform` 方法，该方法接受一个输入值可可选的参数值，并返回一个转换后的值
+ 装饰器中的 metadata 中 name 属性可声明管道的名字,值必须是有效的 JS 标识。


应用实例：

```typescript
//src/app/power-booster.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'power-booster',
  template: `
    <h2>Power Booster</h2>
    <p>Super power boost: {{2 | exponentialStrength: 10}}</p>
  `
})
export class PowerBoosterComponent { }
```

注意自定义的管道也首先要在 AppModule 的 declarations 数据中声明后才能使用。


## 管道及修改检测

Angular 在每次修改检测过程中都要检测数据绑定值的修改情况，即每次 DOM 事件（如每次的键盘点击、鼠标移动、timer tick 及服务端应答）后都要检测，因此花销很大。

当使用管道时，Angular 会尽可以选用简单、更快速的检测算法。


## Pure 和 impure 管道

共有两类管道： pure（默认）, impure。只要将 pure flag 设置为 false 即可生成 impure 管道，例如：

```typescript
@Pipe({
  name: 'flyingHeroesImpure',
  pure: false
})
```

### pure 管道

Angular 只有检测到输入值有 *pure change* 时才会执行 pure 管道。pure change 为：对基本类型值（String, Number, Boolean, Symbol) 有修改，或对对象引用有修改（Date, Array, Function, Object)。

这种修改检测策略执行很快速。

### impure 管道

这种管道在每次组件修改检测周期中都要执行，因此执行很频繁。

### impure 管道的例子： AsyncPipe

AsyncPipe 接受一个 `Promise` 或 `Observable` 作为输入，自动订阅到该输入，并源源不断地获取从源中发送来的数据作为新的当前数据值，该管道会维护状态信息。

下面的例子中，AsyncPipe 订阅到一个发送字符串消息的 `Observalbe` 对象，运行后，模板中的消息会半秒更新一次：

```typescript
//src/app/hero-async-message.component.ts
import { Component } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/interval';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/take';

@Component({
  selector: 'hero-message',
  template: `
    <h2>Async Hero Message and AsyncPipe</h2>
    <p>Message: {{ observable_message | async }}</p>
    <button (click)="resend()">Resend</button>`,
})
export class HeroAsyncMessageComponent {
  observable_message: Observable<string>;

  private messages = [
    'You are my hero!',
    'You are the best hero!',
    'Will you be my hero?'
  ];

  constructor() { this.resend(); }

  resend() {
    this.observable_message = Observable.interval(500)
      .map(i => this.messages[i])
      .take(this.messages.length);
  }
}
```

### 实现一个 HTTP 缓存功能的 impure 管道

只有当请求 URL 有变化后才会发送新请求：

```typescript
//src/app/fetch-json.pipe.ts
import { Pipe, PipeTransform } from '@angular/core';
import { Http }                from '@angular/http';

import 'rxjs/add/operator/map';

@Pipe({
  name: 'fetch',
  pure: false
})
export class FetchJsonPipe  implements PipeTransform {
  private cachedData: any = null;
  private cachedUrl = '';

  constructor(private http: Http) { }

  transform(url: string): any {
    if (url !== this.cachedUrl) {
      this.cachedData = null;
      this.cachedUrl = url;
      this.http.get(url)
        .map( result => result.json() )
        .subscribe( result => this.cachedData = result );
    }

    return this.cachedData;
  }
}
```

应用：

```typescript
//src/app/hero-list.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'hero-list',
  template: `
    <h2>Heroes from JSON File</h2>

    <div *ngFor="let hero of ('heroes.json' | fetch) ">
      {{hero.name}}
    </div>

    <p>Heroes as JSON:
      {{'heroes.json' | fetch | json}}
    </p>`
})
export class HeroListComponent { }
```

### JsonPipe 对调试很有用


## 不提供 FilterPipe 和 OrderByPipe

因此这 2 种管道的参数都要是对象属性，故必须用 impure 实现，当列表较大时，会严重影响性能。


## 参考

+ https://angular.io/guide/pipes
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_pipes.ipynb)

