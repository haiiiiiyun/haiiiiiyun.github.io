---
title: Angular docs-表单-依赖注入 (Dependency Injection)
date: 2017-10-20
writing-time: 2017-10-20
categories: programming
tags: angular node Angular&nbsp;docs
---

# 依赖注入 (Dependency Injection)

这是一种重要的设计模式。

## 为什么要用依赖注入

下面例子中没有用依赖注入：

```typescript
export class Car {

  public engine: Engine;
  public tires: Tires;
  public description = 'No DI';

  constructor() {
    this.engine = new Engine();
    this.tires = new Tires();
  }

  // Method using the engine and tires
  drive() {
    return `${this.description} car with ` +
      `${this.engine.cylinders} cylinders and ${this.tires.make} tires.`;
  }
}
```

即 `Car` 构造函数内部创建和管理依赖的外部类，当外部类有变化时，`Car` 代码也要相应变化。

而使用依赖注入，即将创建 `Car` 对象时所需的外部依赖以构造器参数的形式传入。从而进行了依赖解耦，当外部依赖变化时，`Car` 类中的代码本身就不需要变化了：

```typescript
public description = 'DI';

constructor(public engine: Engine, public tires: Tires) { }
```



当然，创建外部依赖类对象的代码还是要变化，这一般通过工厂类来实现：

```typescript
import { Engine, Tires, Car } from './car';

// BAD pattern!
export class CarFactory {
  createCar() {
    let car = new Car(this.createEngine(), this.createTires());
    car.description = 'Factory';
    return car;
  }

  createEngine() {
    return new Engine();
  }

  createTires() {
    return new Tires();
  }
}
```

工厂类的维护量会很大。

Angular 内置了一个依赖注入框架，相当于能自动维护这个工厂类。它相当于一个注入器，或喷嘴。当将 `Car` 等类登记到这个注入器中后，在需要类实例时只需要求注入器返回即可：

```typescript
let car = injector.get(Car);
```

## Angular 的依赖注入

Angular 在启动应用过程中会自动创建一个应用级的注入器：

```typescript
//src/main.ts (bootstrap)
platformBrowserDynamic().bootstrapModule(AppModule);
```

### 在 NgModule 中登记提供者

在 `AppModule` 的 `@NgModule` 中登记的提供者具有应用级作用域。而在所有即时导入的模块中登记的提供者，在 `AppModule` 的 `imports` 列表中导入后，其提供者会自动加到应用级的所有提供者列表的后面。

```typescript
//src/app/app.module.ts (excerpt)
@NgModule({
  imports: [
    BrowserModule
  ],
  declarations: [
    AppComponent,
    CarComponent,
    HeroesComponent,
/* . . . */
  ],
  providers: [
    UserService,
    { provide: APP_CONFIG, useValue: HERO_DI_CONFIG }
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 在组件中登记提供者

每个组件实现都会有一个独立的注入器，因此这些提供者的作用域是该组件实现及其所有子组件。


## 依赖注入的使用方法

依赖注入模式中，组件必须通过在其构造器函数来要求服务注入，例如：

```typescript
//src/app/heroes/hero-list.component (with DI)
import { Component }   from '@angular/core';

import { Hero }        from './hero';
import { HeroService } from './hero.service';

@Component({
  selector: 'hero-list',
  template: `
  <div *ngFor="let hero of heroes">
    {{hero.id}} - {{hero.name}}
  </div>
  `
})
export class HeroListComponent {
  heroes: Hero[];

  constructor(heroService: HeroService) {
    this.heroes = heroService.getHeroes();
  }
}
```

这里的组件构造器参数类型为 `HeroService`，运行时，Angular 会先在本组件实现时先查找相应服务（本组件中没有  `providers` 登记），没有时再从其类组件中找（父组件 `HeroesComponent` 中有 `providers` 登记，找到！），找完父组件上再到应用级的注入器中找（即 `AppModule` 中的 `providers` 中）。

找到后，当创建 `HeroListComponet` 组件实例时，会要求那个注入器注入一个服务实例。

服务实例是由注入器隐式自动创建的，当然也可以显式创建，例如：

```typescript
//src/app/car/car-injector.ts
injector = ReflectiveInjector.resolveAndCreate([Car, Engine, Tires]);
let car = injector.get(Car);
```

### 单例

在同一个注入器时，返回的依赖对象都是单例实例。

### 依赖注入使测试更方便

只需为注入部分创建一个 mock 服务，例如：

```typescript
//src/app/test.component.ts
let expectedHeroes = [{name: 'A'}, {name: 'B'}]
let mockService = <HeroService> {getHeroes: () => expectedHeroes }

it('should have heroes when HeroListComponent created', () => {
  let hlc = new HeroListComponent(mockService);
  expect(hlc.heroes.length).toEqual(expectedHeroes.length);
});
```

### 当一个服务依赖于其它服务时

`@Injectable()` 装饰器用来表示该类的构造器参数可以通过注入器注入依赖。

```typescript
//src/app/heroes/hero.service (v2)
import { Injectable } from '@angular/core';

import { HEROES }     from './mock-heroes';
import { Logger }     from '../logger.service';

@Injectable()
export class HeroService {

  constructor(private logger: Logger) {  }

  getHeroes() {
    this.logger.log('Getting heroes ...');
    return HEROES;
  }
}
```

对于组件等来说，`@Component`，`@Directive`， `@Pipe` 都是 `@Injectable()` 的子类，因此组件无需再装饰 `@Injectable()`。

所有服务最好都要添加 `@Injectable()` 装饰。

## 注入器提供者

例如：

```typescript
//src/app/providers.component.ts
providers: [Logger]
```

以上实际是下面的简写：

```typescript
[{ provide: Logger, useClass: Logger }]
```

第 1 个参数是 `token`，即作为定位依赖的键，也作为登记提供者的键。第 2 个参数是提供者的定义对象，相当于用来创建依赖值的菜谱（可以有多种菜谱）。

使用依赖后，可以在键不变的情况下，更新提供者，从而实现无缝升级：

```typescript
//src/app/providers.component.ts
@Injectable()
class EvenBetterLogger extends Logger {
  constructor(private userService: UserService) { super(); }

  log(message: string) {
    let name = this.userService.user.name;
    super.log(`Message to ${name}: ${message}`);
  }
}

//src/app/providers.component.ts
[ UserService,
  { provide: Logger, useClass: EvenBetterLogger }]
```

### 类提供者的别名

例如原来依赖 `OldLogger`，现升级为 `NewLogger`(接口不变），有些旧组件必须使用 `OldLogger` 依赖，可以用 `useExisting` 来为 `NewLogger` 提供者创建一个别名，从而两者都使用同一个单例实例：

```typescript
[ NewLogger,
  // Alias OldLogger w/ reference to NewLogger
  { provide: OldLogger, useExisting: NewLogger}]
```

### 值提供者

要求注入器提供返回一个值，不用通过类创建一个实例：

```typescript
//src/app/providers.component.ts
// An object in the shape of the logger service
let silentLogger = {
  logs: ['Silent logger says "Shhhhh!". Provided via "useValue"'],
  log: () => {}
};

//register
[{ provide: Logger, useValue: silentLogger }]
```

### 工厂提供者

有时需要基于当时的信息动态生成一个依赖值。例如 `HeroService` 需要基于当前用户返回不同的列表：

```typescript
//src/app/heroes/hero.service.ts (excerpt)
constructor(
  private logger: Logger,
  private isAuthorized: boolean) { }

getHeroes() {
  let auth = this.isAuthorized ? 'authorized ' : 'unauthorized';
  this.logger.log(`Getting heroes for ${auth} user.`);
  return HEROES.filter(hero => this.isAuthorized || !hero.isSecret);
}


//src/app/heroes/hero.service.provider.ts (excerpt)
let heroServiceFactory = (logger: Logger, userService: UserService) => {
  return new HeroService(logger, userService.user.isAuthorized);
};

export let heroServiceProvider =
  { provide: HeroService,
    useFactory: heroServiceFactory,
    deps: [Logger, UserService]
  };
  
//src/app/heroes/heroes.component (v3)
import { Component }          from '@angular/core';

import { heroServiceProvider } from './hero.service.provider';

@Component({
  selector: 'my-heroes',
  template: `
  <h2>Heroes</h2>
  <hero-list></hero-list>
  `,
  providers: [heroServiceProvider]
})
export class HeroesComponent { }
```

注入器在创建实例时，会调用工厂类来创建。

## 依赖注入的 token

在登记时，用依赖注入的 token 来关联其提供者，注入器会维护一个映射关系。

在使用基于类的依赖时，类对象作为 token，而组件构造器中也可正好通过类来匹配：

```typescript
//src/app/injector.component.ts
heroService: HeroService;

//src/app/heroes/hero-list.component.ts
constructor(heroService: HeroService)
```

### 非类依赖

即有时注入的是一个字符串，函数或对象

例如要注入一个配置对象：

```typescript
//src/app/app-config.ts (excerpt)
export interface AppConfig {
  apiEndpoint: string;
  title: string;
}

export const HERO_DI_CONFIG: AppConfig = {
  apiEndpoint: 'api.heroes.com',
  title: 'Dependency Injection'
};
```

该对象可以用 `useValue` 来登记，但是这里没有一个 `AppConfig` 类，而接口 interface 在最终生成的 JS 中是无效的，因此也不能作为 token 使用。

此时可以用 `InjectionToken`:

```typescript
//src/app/app.config.ts
import { InjectionToken } from '@angular/core';

export let APP_CONFIG = new InjectionToken<AppConfig>('app.config');
```

类型参数 `<AppConfig>` 是可选的，token 描述 `app.config` 也是可选的。

登记如下：

```typescript
providers: [{ provide: APP_CONFIG, useValue: HERO_DI_CONFIG }]
```

使用如下：

```typescript
//src/app/app.component.ts
constructor(@Inject(APP_CONFIG) config: AppConfig) {
  this.title = config.title;
}
```

### 可选依赖

```typescript
import { Optional } from '@angular/core';

constructor(@Optional() private logger: Logger) {
  if (this.logger) {
    this.logger.log(some_message);
  }
}
```

## 参考

+ https://angular.io/guide/dependency-injection
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/dependency_injection.ipynb)
