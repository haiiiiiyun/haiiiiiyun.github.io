---
title: Angular2 的依赖注入
date: 2017-03-20
writing-time: 2017-03-20 19:35
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2 dependency&nbsp;injection
---

# 概述

当应用中的不同模块之间进行交互，例如当模块 A 需要有模块 B 才能运行时，我们说 B 是 A 的一个依赖。

访问依赖模块的最常用方法是用 `import`，例如：

```typescript
// in A.ts
import {B} from 'B'; // a dependency

B.foo(); // using B
```

多数情况下，简单地进行 `import` 就可以了，但是在很些时候，我们必须用更复杂的方法来提供依赖，例如：

+ 假如我们想在测试时使用 MockB 来替代 B
+ 假如我们想在整个应用内共享 B 类的一个单独实例（单例模式）
+ 假如我们想每次调用时都创建 B 类的一个新实例（工厂模式）


注入依赖（Dependency Injection, DI）能解决以上问题。

Dependency Injection 这个术语既可用来描述这个设计模式，也可用来指代 Angular 内置的这个 DI 库。

使用注入依赖的主要好处是：客户端组件无需了解如何去创建依赖，所有组件所要了解的只是如何与这些依赖交互。

# 注入的例子： PriceService

假设有一个 Product 类。每个产品都有一个基础价格，要计算该产品的实际价格，我们需要用一个以下面数据作为输入的一个服务来计算：
+ 该产品的基础价格
+ 当前在哪个州


不使用依赖注入，可以这样实现：

```typescript
class Product {
    constructor(basePrice: number){
        this.service = new PriceService();
        this.basePrice = basePrice;
    }

    price(state: string) {
        return this.service.calculate(this.basePrice, state);
    }
}
```

现假设要为该 Product 类编写测试代码。假设 PriceService 类是通过数据库查询来获取特定销售状态的税率的。从而测试代码可以如下：

```typescript
let product;

beforeEach(() => {
    product = new Product(11);
});

describe('price', () => {
    it('is calculated based on the basePrice and the state', () => {
        expect(product.price('FL')).toBe(11.66);
    });
});
```

上面的代码有下面的问题：

+ 运行测试时数据库必须要开启
+ Florida 州的税率必须要和我们预期的一致


上面的这些问题，是由于在 Product 类和 PriceService 类间增加了一层无谓的关联，并同时又关联上了数据库。

可以将 Product 改进为：

```typescript
class Product {
    constructor(service: PriceService, basePrice: number) {
        this.service = service;
        this.basePrice = basePrice;
    }

    price(state: string) {
        return this.service.calculate(this.basePrice, state);
    }
}
```

现在，当创建 Product 实例时，客户端负责决定使用哪个具体的 PriceService 实现。从而，当在测试时，可以使用 PriceService 的 Mock 版本，如下：

```typescript
class MockPriceService {
    calculate(basePrice: number, state: string) {
        if (state === 'FL'){
            return basePrice * 1.06;
        }

        return basePrice;
    }
}
```

经过以上的小小改进后，可以简化测试代码，并去除与数据库的关联：

```typescript
let product;

beforeEach(() => {
    const service = new MockPriceService();
    product = new Product(service, 11);
});

describe('price', () => {
    it('is calculated based on the basePrice and the state', () => {
        expect(product.price('FL')).toBe(11.66);
    });
});
```

## Don't Call US ...

注入依赖的技术基于 **控制反转(inversion of control, IoC)** 原则，也非正式地称为 "Hollywood principle"，即好莱坞格言："don't call us, we'll call you"。

使用 DI 后，应用的体系结构会实现松耦合，只要组件间的接口未变，我们可以随意替换具体的组件实现。

Angular 使用依赖注入来解决依赖问题。

组件 A 依赖于组件 B 的传统实现是：在组件 A 内创建一个 B 的实例。而 Angular 使用依赖注入：如果需要将组件 B 放置在组件 A 中，我们将 B 传给 A。

DI 优于传统实现，例如，当要测试 A 时，我们可以简单地为 B 实现一个 Mock 版本，然后注入到 A 中。

# 依赖注入的组成部分

要登记一个依赖，需要将它绑定到某个标识，即依赖标识 (dependency token)。例如，假如要登记一个 API URL，我们可以用 "API_URL" 这个标识(token)，而如何想登记一个类，可以简单以该类作为它的标识(token)。

Angular 依赖注入有 3 个部分：

+ **Provider**(也叫绑定) 将一个标识（可以是字符串或一个类）映射到一组依赖上。它能告诉 Angular，给定一个标识，如何创建一个对象
+ **Injector** 中持有一组绑定(provider)，它负责解析依赖，并在创建对象时注入依赖
+ 注入的 **Dependency**


每个组成部分的角色如下：

![依赖注入, Dependency Injection](/assets/images/ng-book2/DI.png)

处理 DI 时有很多种方式。其中最最常见的情况是：为整个应用提供一个相同的服务或值，这种情况覆盖了 99% 的使用方式。

## 玩转 Injector 

Angular 能够在幕后为我们设置好 DI，但是在使用注解将其注入我们的组件前，首先手动使用 Injector 来实现。

```typescript
import {
  Component,
  ReflectiveInjector,
} from '@angular/core';
import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { platformBrowserDynamic } from "@angular/platform-browser-dynamic";

/*
 * Webpack
 */
require('css/styles.css');

// 先创建一个只返回一个字符串的服务：
class MyService {
  getValue(): string {
    return 'a value';
  }
}

// 应用组件
@Component({
  selector: 'di-sample-app',
  template: `
  <button (click)="invokeService()">Get Value</button>
  `
})
class DiSampleApp {
  myService: MyService;

  constructor() {
      // 使用静态方法 ReflectiveInjector.resolveAndCreate 来创建 Injector 实例
      // 传入的参数是一个数组，包含所有该 Injector 实例需知道的
      // 可注入对象，这里我们只想让它知道
      // MyService 这个可注入对象
      // ReflectiveInjector 是 Injector 的一个具体实现
      // 它是最常的 Injector 类
    let injector: any = ReflectiveInjector.resolveAndCreate([MyService]);
    this.myService = injector.get(MyService);

      // 需要注意的是：注入的是一个单例实例
      // 因此，这里输出是 "Same instance? true"
    console.log('Same instance?', this.myService === injector.get(MyService));
  }

  invokeService(): void {
    console.log('MyService returned', this.myService.getValue());
  }
}

// 由于使用了自己的 Injector 实现，因此无需和以前那样
// 将 MyService 放入 NgModule 的 providers 列表中
// no need to add injectables here
@NgModule({
  declarations: [ DiSampleApp ],
  imports: [ BrowserModule ],
  bootstrap: [ DiSampleApp ]
})
class DiSampleAppModule {}

platformBrowserDynamic().bootstrapModule(DiSampleAppModule);
```

## 使用 NgModule 来提供依赖

假设要将 MyService 的单例实例注入到全应用中，我们需要将它添加到 *NgModule* 的 *providers* 中，如下：

```typescript
@NgModule({
    declarations: [
        MyAppComponent,
        // other components...
    ],
    // 这里直接将 MyService 类放入 providers 列表中，
    // 从而告诉 Angular，当 MyService 被注入时，我们
    // 需要提供 MyService 的一个实例实例。
    // 因为这是最常用的用法，因此简化为只要将 MyService 类
    // 直接放入 providers 列表中，它实际上等价于：
    // providers: [{provide: MyService, useClass: MyService}]
    providers: [ MyService ]
})
class MyAppModule {}
```

现在 MyAppComponent 可以将 MyService 注入到它的构造器中：

```typescript
export class MyAppComponent {
    constructor(private myService: MyService /* 注入*/){
    }
}
```

除了创建类实例外，注入还有许多不同的用法。

## Provider

Angular 的 DI 系统中可用多种方式来配置注入：

+ 注入一个类的 （单例）实例
+ 调用某个函数，注入函数的返回值
+ 注入一个值
+ 创建一个别名


### 使用类

注入一个类的单例实现可能是最常见的注入类型，其配置为：

```typescript
// 这里 provide 部分的 MyComponent 是用来标识注入的标识(token)
// 而 useClass 部分的 MyComponent 指定的如何注入及注入的内容
// 从而实现了将 MyComponent 类映射为了 MyComponent 标识。
// 这里的类名和标识名是相同的（最常见用法），但是它们不需要相同
// 当用这种注入法时，我们每次将它注入时，Injector 会在幕后
// 创建该类的单例实例，并返回相同的对象
// 当然，在首次注入时，由于还没有创建 MyComponent 实例，
// DI 系统会调用该类的构造函数
{ provide: MyComponent, useClass: MyComponent }
```

### 使用工厂

使用工厂注入时，我们编写一个能返回任意对象的函数，如：

```typescript
{
    provider: MyComponent,
    useFactory: () => {
        if (loggedIn) { // loggedIn 在外部定义
            return new MyLoggedComponent();
        }
        return new MyComponent();
    }
}
```

工厂函数也可以有依赖：

```typescript
{
    provider: MyComponent,
    useFactory: (user) => {
        if (user.loggedIn) {
            return new MyLoggedComponent();
        }
        return new MyComponent();
    },
    deps: [User]
}
```

工厂方法也适用于当类的构造器需要参数时：


```typescript
// 构造器有参数的类
class ParamService {
    constructor(private phrase: string){
        console.log("created with', phrase);
    }

    getValue(): string{
        return this.phrase;
    }
}

@NgModule({
    //...
    providers: [
        {
            provide: ParamService,
            // 这里工厂函数没有入参，但是返回类型是 ParamService
            useFactory: (): ParamService => new ParamService('YOLO')
        }
    ]
})
```

### 使用值

常用于注册常量：

```typescript
{ provide: 'API_URL', useValue: 'http://my.api.com/v1' }
```

### 使用别名

```typescript
// 这里 useClass 部分对应的是之前注册过的一个标识(token)
{ provide: NewComponent, useClass: MyComponent }
```

//续..















# 参考 

+ [Dependency Injection](https://www.ng-book.com/2/)
