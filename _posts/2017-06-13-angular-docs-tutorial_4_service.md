---
title: Angular docs-教程 4： Service
date: 2017-06-13
writing-time: 2017-08-22
categories: programming
tags: angular node Angular&nbsp;docs
---

# 教程 4： Service


创建一个单独的可重用 data service，并将它注入到需要用到它的组件中。从而使组件只专注于实现视图功能。


## 创建  hero service

创建 `app/hero.service.ts` 文件及 `HeroService` 类。文件名和类名遵循风格指南。

```typescript
//src/app/hero.service.ts (starting point)
import { Injectable } from '@angular/core';

@Injectable()
export class HeroService {
}
```

### Injectable service

注意先导入 `Injectable` 函数，然后将 `@Injectable()` 应用为装饰器。不要忘了加括号，这种情况很难诊断出。

`@Injectable()` 装饰器告诉 TypeScript，需触发该 service 的 metadata，`()` 中的 metadata 告诉 Angular 可能需要将其它的依赖注入到该 service 中。

虽然 `HeroService` 当前没有依赖，一开始就应用 `@Injectable()` 装饰器可确保一致性。


### 创建  getHeroes() 方法

```typescript
//src/app/hero.service.ts (getHeroes stub)
@Injectable()
export class HeroService {
  getHeroes(): void {} // stub
}
```

`HeroService` 可从任意地方获取数据。


### 将模拟数据保存到单独文件中

将 `app.component.ts` 中的 `HEROES` 类移到 `app/mock-heroes.ts` 中：

```typescript
//src/app/mock-heroes.ts
import { Hero } from './hero';

export const HEROES: Hero[] = [
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
```

app.component.ts 中将 `heroes` 属性定义为 `Hero[]`:

```typescript
//src/app/app.component.ts (heroes property)
heroes: Hero[];
```

### 在 service 中返回模拟数据

```typescript
//src/app/hero.service.ts
import { Injectable } from '@angular/core';

import { Hero } from './hero';
import { HEROES } from './mock-heroes';

@Injectable()
export class HeroService {
  getHeroes(): Hero[] {
    return HEROES;
  }
}
```


## 导入 hero service

在根组件中先导入:

```typescript
//src/app/app.component.ts (hero-service-import)
import { HeroService } from './hero.service';
```

### 不要用 new 来创建 service 

当然也可以直接用 `new` 创建：

```typescript
//src/app/app.component.ts
heroService = new HeroService(); // don't do this
```

但是不用 new 直接创建有以下原因：

+ 组件需要知道如何创建一个 `HeroService` 实例，当 `HeroService` 构造器接口修改后，要相应更新。
+ 每次用 `new` 创建 service 实例时，无法实现 service 数据缓存和共享的情况。
+ 组件会耦合到 service 的某个特定实现。

### 应注入 service

用下面的两行来代替 new:

+ 创建一个构造器，并定义一个私有属性
+ 在组件中添加 `providers` metadata

```typescript
//src/app/app.component.ts (constructor)
constructor(private heroService: HeroService) { }
```

构造器平时没有内容，参数一并定义了一个私有的 heroService 属性，并作为 `HeroService` 注入的地方。

现在当创建 AppComponent 时会一并创建一个 HeroService 实例。

但是注入器目前还不知道如何创建 HeroService，先需要在 `@Component` 元数据中添加 `providers` 数据属性：

```typescript
//src/app/app.component.ts (providers)
providers: [HeroService]
```

`providers` 数组告诉 Angular 当创建一个 AppComponent 时一并创建一个新的 `HeroService` 实例，之后 AppComponent 及其子组件都能从该 service 中获取数据。


### getHeroes()

可以通过 `heroService.getHeroes()` 来获取数据：

```typescript
//src/app/app.component.ts
this.heroes = this.heroService.getHeroes();
```

## ngOnInit 挂钩

Angular 为组件生命周期中的每个关注点提供了接口：创建时，有更新时，销毁时。

每个接口都只有一个方法，当组件实现了这些方法后，Angualr 后进行调用。

`OnInit` 接口中有 `ngOnInit` 函数，可将初始化逻辑放在里面。

```typescript
//src/app/app.component.ts (ng-on-init)
ngOnInit(): void {
  this.heroes = this.heroService.getHeroes();
}
```

## 异步 service 和 Promise

一个 `Promise` 本质上即能保证当有结果到来时会回调函数。你要求异步 service 执行一些操作，并传入一个回调函数。serice 执行完操作后，最后将操作结果或错误对象作为参数调用回调函数。

Promise 详细信息见 [Promises for asynchronous programming](http://exploringjs.com/es6/ch_promises.html)。

将 HeroService 中的 `getHeroes()` 更新为 Promise 版本：

```typescript
//src/app/hero.service.ts (excerpt)
getHeroes(): Promise<Hero[]> {
  return Promise.resolve(HEROES);
}
```

以上是模拟一个快速、零延时的异步 service，即能立即返回一个 *resolved Promise*。

### 操作 Promise

现在 getHeroes() 返回的是一个 Promise，不是一个 Hero 数组。需要将一个回调函数作为参数传入 `Promise` 的 `then` 方法中：

```typescript
//src/app/app.component.ts (getHeroes - revised)
getHeroes(): void {
  this.heroService.getHeroes().then(heroes => this.heroes = heroes);
}
```

上面是无延时的版本，有延时的版本如下，创建一个 getHeroesSlowly():

```typescript
//app/hero.service.ts (getHeroesSlowly)
getHeroesSlowly(): Promise<Hero[]> {
  return new Promise(resolve => {
    // Simulate server latency with 2 second delay
    setTimeout(() => resolve(this.getHeroes()), 2000);
  });
}
```
## 参考

+ https://angular.io/tutorial/toh-pt4
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_4_services.ipynb)
