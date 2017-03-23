---
title: Angular2 的依赖注入
date: 2017-03-20
writing-time: 2017-03-20 19:35--2017-03-23:15:55
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

+ 假如想在测试时使用 MockB 来替代 B
+ 假如想在整个应用内共享 B 类的一个单例实例（单例模式）
+ 假如想每次调用时都创建 B 类的一个新实例（工厂模式）


注入依赖（Dependency Injection, DI）能解决以上问题。

Dependency Injection 这个术语既可用来描述这个设计模式，也可用来指代 Angular 内置的这个 DI 库。

使用注入依赖的主要好处是：客户端组件无需了解如何去创建依赖对象，所有组件所要了解的只是如何与这些依赖交互。


# 注入的例子： PriceService

假设有一个 Product 类。每个产品都有一个基础价格，要计算该产品的实际价格，我们需要用下面数据作为输入的一个服务来计算：

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

现假设要为该 Product 类编写测试代码。假设 PriceService 类是通过数据库查询来获取特定州的税率的。从而测试代码可以如下：

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

以上代码有以下问题：

+ 运行测试时数据库必须要开启
+ Florida 州的税率必须要和我们预期的一致


以上问题是由于在 Product 类和 PriceService 类间增加了一层无谓的关联，并同时又关联上了数据库造成的。

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

处理 DI 时有多种方式。其中最最常见的情况是：为整个应用提供一个相同的服务或值，这种情况覆盖了 99% 的使用情况。

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

      // 需要注意的是：注入的是同一个单例实例
      // 因此，这里输出是 "Same instance? true"
    console.log('Same instance?', this.myService === injector.get(MyService));
  }

  invokeService(): void {
    console.log('MyService returned', this.myService.getValue());
  }
}

// 由于使用了自己的 Injector 实现，因此无需和以前那样
// 将 MyService 放入 NgModule 的 providers 列表中
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
    // 需要提供 MyService 的一个单例实例。
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

注入一个类的单例实例可能是最常见的注入类型，其配置为：

```typescript
// 这里 provide 部分的 MyComponent 是用来表示注入的标识(token)
// 而 useClass 部分的 MyComponent 指定注入内容
// 从而实现了将 MyComponent 类映射为了 MyComponent 标识。
// 这里的类名和标识名是相同的（最常见用法），但是它们不需要相同
// 当用这种注入法时，我们每次将它注入时，Injector 会在幕后
// 创建该类的单例实例，并返回相同的对象。
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

# 在应用中使用依赖注入


要使用依赖一般需 3 个步骤：

+ 创建服务类(injectable)
+ 在接收组件中声明依赖
+ 配置注入（例如使用 Angular 中的 NgModule 进行注入登记）


## 创建服务类

```typescript
export class ApiService {
    get(): void {
        console.log('Getting resource ...');
    }
}
```

## 在接收组件中声明依赖

之前是直接通过 Injector 类完成的，但是 Angular 为我们提供了 2 种简单的方式。

第 1 种方式是在组件构造器中声明可注入类，如：

```typescript
import {ApiService} from 'services/ApiService';

class DiSampleApp {
    // Angular DI 系统会核查可用的注入，并返回一个 ApiService 的单例实例
    constructor(private apiService: ApiService) {
    }
}
```

第 2 种方式是使用 @Inject 注解，从而为 Angular 提供更多有关注入的信息，如：

```typescript
class DiSampleApp {
    private apiService: ApiService;
    constructor(@Inject(ApiService) ate apiService) {
        this.apiService = apiService;
    }
}
```

##配置注入（例如使用 Angular 中的 NgModule 进行注入登记）

例如：

```typescript
// 这里使用 ApiService 标识来暴露出 ApiService 类的单例实例
{ provide: ApiService, useClass: ApiService }

// 最后将 ApiService 添加到 NgModule 的 providers  
@NgModule({
    //...
    providers: [ ApiService ]
})
```

# 使用注入器 (Injector)

当需要控制何时创建依赖的单例实例时，需要显式使用注入器 (Injector)。

例如，某个应用需要使用上面的 ApiService，以及另一个服务。另一个服务基于浏览器视图的大小，初始化其他 2 个服务，如果小于 800px，返回 SmallService 服务实例，否则返回 LargeService 服务实例。

```typescript
export class SmallService {
    run(): void {
        console.log('Small service...');
    }
}

export class LargeService {
    run(): void {
        console.log('Large service...');
    }
}


export class ViewPortService {
    determineService(): any {
        let w: number = Math.max(document.documentElement.clientWidth,
                                window.innerWidth || 0);
        if (w < 800) {
            return new SmallService();
        }
        return new LargeService();
    }
}

// 在 @NgModule 中定义依赖
@NgModule({
    //...
    providers: [
        ApiService, // 等同于 { provide: 'ApiService', useClass: ApiService }

        // 为现有的 ApiService 创建一个别名
        { provide: 'ApiServiceAlias', useExisting: ApiService },

        {
          provide: 'SizeService', // token
          // 工厂将获取到 deps 中指定的类的实例
          useFactory: (viewport: any) => {
            return viewport.determineService();
          },
          deps: [ViewPortService]
        }
    ]
})
class DiSampleAppModule {}


// 然后创建使用该服务的应用
class DiSampleApp {
    // 这里 ApiService 使用隐式地注入方式。
    // 其它两个使用了显式注入方式。
    constructor(private apiService: ApiService,
        @Inject('ApiServiceAlias') private aliasService: ApiService,
        @Inject('SizeService') private sizeService: any) {
    }

}
```

因此，在小窗口中，sizeService 将使用 SmallService。但是当将窗口调大后，如果不刷新页面，那么 sizeService 用的还是 SmallService。

这是因为 SizeService 的工厂函数只在应用启动时运行一次造成的。要克服这个问题，可以创建自定义 Injector 来实现，如下：

```typescript

// 应用组件
@Component({
  selector: 'di-sample-app',

  // useInjectors() 中将创建和使用一个 Injector
  template: `
  <button (click)="invokeApi()">Invoke API</button>
  <button (click)="useInjectors()">Use Injectors</button>
  `
})
class DiSampleApp {
  constructor(private apiService: ApiService,
              @Inject('ApiServiceAlias') private aliasService: ApiService,
              @Inject('SizeService') private sizeService: any) {
  }

  invokeApi(): void {
    this.apiService.get();
    this.aliasService.get();
    this.sizeService.run();
  }

  useInjectors(): void {
    // 创建自己的 Injector，它包含 ViewPortService 和
    // 另一个可注入对象。
    let injector: any = ReflectiveInjector.resolveAndCreate([
      ViewPortService,

      // 该可注入对象 (injectable) 的标识为 'OtherSizeService'
      // 它的工厂方法在每次调用  useInjectors 方法时都会运行。
      {
        provide: 'OtherSizeService',
        useFactory: (viewport: any) => {
          return viewport.determineService();
        },
        deps: [ViewPortService]
      }
    ]);
    let sizeService: any = injector.get('OtherSizeService');
    sizeService.run();
  }
}
```

# 值替换

使用 DI 的另一个原因是要能在运行时修改注入对象的值。例如在生产环境下使用真正的 API_URL， 而在测试环境下使用 Mock_API_URL 值。


```typescript
// file: services/ApiService.ts
import { Inject } from '@angular/core';

// 定义一个常量，将用作 API URL 注入依赖的标识 (token)，
// 即 Angular 将用字符串 'API_URL' 来存储 URL 的信息。
export const API_URL: string = 'API_URL';

export class ApiService {
  // NgModule 中定义的注入依赖 API_URL 的值将注入这里
  constructor(@Inject(API_URL) private apiUrl: string) {
  }

  get(): void {
    console.log(`Calling ${this.apiUrl}/endpoint...`);
  }
}
```

```typescript
// file: ts/app.ts
// 可以通过 WebPack 或 .env 文件来定义这些环境变量值
const isProduction: boolean = true;

@NgModule({
  declarations: [ DiValueApp ],
  imports: [ BrowserModule ],
  bootstrap: [ DiValueApp ],
  providers: [
    { provide: ApiService, useClass: ApiService },

    // 根据环境变量设置不同的值
    {
      provide: API_URL,
      useValue: isProduction ?
        'https://production-api.sample.com' :
        'http://dev-api.sample.com'
    }
  ]
})
class DiValueAppAppModule {}
```

# NgModule

NgModule 是一种用来为编译器和依赖注入组织依赖关系的方式。

Angular 运行时需要知道各组件都定义了哪些标签，以及如何获取这些依赖文件（库）。

## NgModule vs. Es6/TypeScript 的模块

使用 `import` 可以导入代码模块，而 Angular 的 `NgModule` 系统是用来组件依赖的。NgModule 特别是针对 **已编译了哪些标签** 及 **需要注入哪些依赖**。

## 编译器和组件

当 Angular 组件模板中有自定义标签时，编译器需要知道这些标签的具体功能。通过在 NgModule 中定义依赖组件（从而也知道了其标签），编译器就能知道自定义标签的功能。

## 依赖注入和提供者

DI 优于简单的 import，它有共享单例实例，创建工厂和在运行时重载依赖的标准方式。

**每个组件必须要在某个 NgModule 中声明后才能使用，并且每个组件只能属于一个 NgModule**。

我们通常将多个组件组合在一个 NgModule 中，因此 NgModule 类似于其它语言中的命名空间。


## 组件可见性

要使用组件，当前 NgModule 必须知晓该组件，例如 hello-world 组件需要使用 user-greeting 组件。

有 2 种实现方式：

+ user-greeting 和 hello-world 定义在同一个 NgModule 中，或
+ hello-world 从 user-greeting 组件的模块导入该组件


用第 2 种方式时，先定义 UserGreeting 及其 NgModule UserGreetingModule:

```typescript
@Component({
    selector: 'user-greeting',
    tempalte: `<span>hello</span>`
})
class UserGreeting {}

@NgModule({
    // 只有声明过的组件才可以导出
    declarations: [ UserGreeting ],

    // 将这些组件导出，从而可以在其它模块中进行 import
    exports: [ UserGreeting ]
})
export class UserGreetingModule {}
```

在 HelloWorld 组件中进行导入：

```typescript
@NgModule({
    //...
    imports: [ UserGreetingModule ]
})
class HelloWorldAppModule {}
```

## 指定提供者

指定可注入对象的提供者，可以在 NgModule 的 providers 中完成。

```typescript
// 有一个简单服务
export class ApiService {
    get(): void { }
}

// 将服务注册为提供者
@NgModule({
    //...
    providers: [ApiService]
})
class ApiAppModule {}

// 然后在其它组件中注入
class ApiDataComponent {
    constructor(private apiService: ApiService){
    }

    getData(): void {
        this.apiService.get();
    }
}
```

# 参考 

+ [Dependency Injection](https://www.ng-book.com/2/)
