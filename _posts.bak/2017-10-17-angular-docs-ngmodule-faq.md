---
title: Angular docs-NgModule FAQs
date: 2017-10-17
writing-time: 2017-10-17
categories: programming
tags: angular node Angular&nbsp;docs
---

# NgModule FAQs

## 什么类需回到 `declarations` 列表中？

即 `declarable` 类：组件、指令、管道。

应用中的每个第些类只能在一个模块中声明。

## "Can't bind to 'x' since it isn't a known property of 'y'" 什么意思？

通常指还没有声明 "x" 指令，或 "x" 所属的模块还没有被导入。

例如 "x" 是 `ngModel` 时，可能你还没有从 `@angular/forms` 中导入 `FormsModule`。

可能 "x" 在应用的子模块中声明了，并还没有导出，"x" 需要放在 `exports` 列表中导出后才能被外部使用。


## 需要 import 什么？

若你的组件模板中要使用其它模块中导出的 `declarable` 类，即 import 该模块。

例如要用 `NgIf` 时需从 `@angular/common` 中导入 `CommonModule`。

先可导入共享和功能模块。

`BrowserModule` 只能在根 `AppModule` 中导入。

## 导入 BrowserModule 还是 CommonModule?

`BrowserModule` 中对 `CommonModule` 进行了重导出，它提供的另外服务对加载和运行浏览器应用很重要。

只有根应用模块 `AppModule` 中才能在 `@angular/platform-browser` 中导入 `BrowserModule`，而其它模块只能在 `@angular/common` 中导入 `CommonModule`，从而可在组件中使用 `NgIf` 等指令。

## 需要 export 什么？

导入需要在其它模块模板中使用的组件、指令和管道类（declarable 类）。不显式导出的都默认是私有的。

而服务、函数、数据模型等非 declarable 类都无法通过 `exports` 列表导出。


## 可以重导出类和模块吗？

可以。

重导出模块时，即重导出该模块中 `exports` 列表中的所有 declarable 类。

一些纯服务模块(pure service module，例如 `HttpModule`),由于其自身没有导出任何类，即重导出没有意义。


## 什么是 forRoot 方法

`forRoot` 静态方法方便开发者来配置模块的提供者 (module's providers)，它只是一个按惯例取的名字。

例如 `RouterModule.forRoot` 方法：应用传送一个 `Routers` 对象给它，从而用该路由信息列表来配置出一个应用级的 `Router` 服务，它返回一个 [ModuleWithProviers](https://angular.io/api/core/ModuleWithProviders)，可以添加到 `AppModule` 的 `imports` 列表中。

只有根 `AppModule` 才能调用并导入 `.forRoot` 的结果，而其它模块需要调用 `RouterModule.forChild` 静态方法。


## 功能模块中提供的服务为什么全局可见？

`@NgModule.providers` 列表中的提供者都是在整个应用中可用的。

当导入一个模块中，Angular 将该模块中 `providers` 列表中列出的服务提供者全部都添加到应用的根注入器（root injector) 中，从而使它们全局可见。也因为这样，只需在根模块中导入一次 `HttpModule`,在应用中都可使用该模块进行请求。

## 而按需加载（lazy-loaded) 模块中提供的服务只对本模块可见？


当 Angular 路由器按需加载一个模块时，它会创建一个新的执行上下文，该上下文有它自己的注入器，它是应用根注入器的直接子注入器。

路由器将该模块中的提供者及其导入模块的提供者都添加到该子注入器。Router 创建按需加载的模块中的组件时使用该上下文，即优先使用该子注入器中的同名服务。

## 两个模块提供相同的服务会怎样？

当两个模块一起导入，并且提供相同的服务时（provider with the same token)，最后导入的会覆盖之前导入的，因此它们都添加到相同的注入器中。

如果模块 A 中定义有名为 'X' 的服务，而其导入的模块 B 中也提供相同的服务，那么优先使用 A 中的服务。

根 `AppModule` 中提供的服务最优先。

## 如何限制服务作用域到一个模块

在 `AppModule` 中导入的模块服务都会添加到 `@NgModule.providers` 中，即添加到应用级的注入器中，从而是全局的。因此，在后序导入的同名服务有可能会覆盖之前导入的服务。

按需加载的模块，有自己独立的注入器，它是应用级根注入器的直接子注入器，因此，它内部的服务都是添加到该子注入器的，因而作为域为该模块。

如果不想用按需加载，那么在模块中可创建一个顶层组件，将服务添加到该顶层组件的 `providers` 列表中，而不是放在模块的 `providers` 列表中。因为 Angular 会为每个组件实例创建一个子注入器，并将该组件（及子组件）中的服务提供者添加到该组件的注入器中。从而实现服务作用域的限制。

## 应用级的服务提供者放在根 AppModule 中还是根 AppComponent 中？

登记在 `AppModule` 中的服务，在按需加载的模块中也能使用，而登记在 `AppComponent` 中的不能。

`AppModule` 对应的注入器是根注入器，是全局的，而  `AppComponent` 有自己的注入器（是一个子注入器），只针对该组件树中的对象。

一些服务如 `Router` 只能登记到全局的根注入器中。


## 为什么不要在共享模块中提供服务

例如在 `SharedModule` 中的 `providers` 中提供 `UserService`，由于共享模块会在不同的组件中被导入多次，当在立即导入的模块中使用时，由于该服务添加到了根注入器，虽然被导入了多次，但是各组件在注入后使用的都是根注入器中的一个单例实例。

但是当按需加载的模块使用时，由于它有自己的注入器，服务会添加到该子注入器中，从而使用的是另一个实例。


## 为什么按需加载会创建一个子注入器？


这是由 Angular 的依赖注入（dependency-injection) 系统的特性决定的。一个注入器开始被使用后就不能再登记服务了。

应用启动时，在并创建任何组件实例前，Angular 会创建一个根注入器，并将立即导入的模块中的提供者都添加到该根注入器中。一旦该注入器开始注入和分发服务时，就不再能添加新的服务了。

而按需加载的模块加载时，Angular 只能创建一个新的子注入器来登记新的服务。


## 如果避免模块或服务多次加载？

一些模块及它们的服务只能被根 `AppModule` 加载一次。如果再次在按需加载的模板中导入会出错问题，并且不好诊断错误。

只需在构造器中，尝试将本模块或服务从根注入器中注入到本身，如果注入成功，那么肯定就是第二次导入了，此时可抛出异常。

`BrowserModule` 及之前的 `CoreModule` 都有这种措施：

```typescript
//src/app/core/core.module.ts (Constructor)
constructor (@Optional() @SkipSelf() parentModule: CoreModule) {
  if (parentModule) {
    throw new Error(
      'CoreModule is already loaded. Import it in the AppModule only');
  }
}
```

## 什么是 entry component

一个 entry component 就是 Angular 通过其类型以命令方式加载的任何组件。

通过组件的选择子声明式的加载的组件不是 entry component。

大部分组件都是声明式加载的，即在组件模板中使用选择子加载。

有些组件只能动态加载，并且不能在组件模板中使用。

启动根 `AppComponent` 就是一个 entry component。虽然其选择子在 `index.html` 中使用，但是 `index.html` 不是组件模板。Angular 动态加载 `AppComponent`，因为它要么通过列在 `@NgModule.bootstrap` 中加载，要么使用模块的 `ngDoBootstrape` 方法命令式的加载。

在路由定义中的组件也都是 entry component。因为路由定义通过组件类型来引用。路由会忽略组件的选择子，而通过其类型动态将组件加载到 `RouterOutlet` 中。

entry component 必须在 `@NgModule.entryComponents` 列表中列出才会被编译器识别出，此外下列的组件也会自动添加到该列表：

+ `@NgModule.bootstrap` 列表中的组件
+ 在路由配置中引用的组件

## 何时需将组件添加到 entryComponents 列表？

上个 FAQ 中，自动添加的情况已经包括了最常见的情景。因此一般的一般都无需再手工添加组件到 entryComponents。

必须手工添加到该列表的组件不能有在其它组件的模板中引用。


## 为什么 Angular 需要 entryComponents?

这是为编译生成的代码的性能考虑的（tree shaking，将用不到的组件排除到最终的代码外）。

Angular 编译器使用递归策略只为使用到的组件生成代码。模板中使用选择子引用的都包括，在 entryComponents 声明的也包括进行，而在包括进来的所有组件的模板中全部递归查找到还没有找到的组件，说明是未使用的，而排序掉，不包含在最终编译后的代码中。


## 需要哪些模块，如果使用？

### SharedModule

共享模块只封装共享的组件、指令和管道，是一个 `declarations` 型模块。也可以重导出 `CommonModule`, `FormsModule` 等模块。

但是共享模块不能提供服务，即不能有 `providers`，并且重导出的模块中也不能有 `providers`。

### CoreModule

`CoreModule` 的 `providers` 中可登记当应用开始时能使用的单例服务。它只能在 `AppModule` 中导入。一般是一个纯服务型模块（pure services module)，没有 `declarations`。


### 各种功能模块


## Angular 和 JS 模块的区别

JS 中每个文件就是一个模块，文件中可用 `export` 导出，而在其它文件中用 `import` 导入。

Angular 的模块 `NgModule` 也有 `imports` 和 `exports`。一个 `NgModule` 导入另一个 `NgModule` 后，可以在本模块的组件中使用另一个模块是导出的类。

有以下区别：

+ NgModule 只关注 declarable 类：组件、指令和管道。
+ NgModule 中的所有类在 `@NgModule.delarations` 中声明。
+ NgModule 只能导出其 declarable 类，只能导入其它模块的 declarable 类。
+ `NgModule.providers` 中的服务可扩展应用的服务功能。

下面是一个 NgModule 的例子：

```typescript
//ngmodule/src/app/contact/contact.module.ts
@NgModule({
  imports:      [ CommonModule, FormsModule ],
  declarations: [ ContactComponent, HighlightDirective, AwesomePipe ],
  exports:      [ ContactComponent ],
  providers:    [ ContactService ]
})
export class ContactModule { }
```

## Angular 如何在模板中查找组件、指令和管道？什么是模板引用？

Angular 编译器在模板中通过选择子、管道语法来匹配查找，找到时，就是一个模板引用。

## 什么是 Angular 编译器？

编译器将我们编译的代码转换成高性能的 JS 代码。而 `@NgModule` 中的 metadata 将引导编译的过程。

## NgModule 的 API

下面是 `NgModule` metadata 中的属性：

+ `declarations`: 属性该模块的一组 declarable 类：组件、指令和管道类。这些类只能在一个模板中声明。
+ `providers`: 一组 dependency-injection providers。立即加载的模块中提供的服务都登记在主注入器中，全局可见，而按需加载的模块中提供的服务都登记在另一个子注入器中，只那个模板可见了。
+ `imports`: 一组支持模块。导入后可在本模块的组件模板中使用导入模板中导出的组件、指令和管道。
+ `exports`: 一组要导出的 declarable 类，也可以包括重导出的其它模块。
+ `bootstrap`: 一组启动组件。通常只有一个，即根组件。
+ `entryComponents`: 一组不是通过模板中的选择子引用的组件。## 参考


## 参考

+ https://angular.io/guide/ngmodule-faq
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/ngmodule_faq.ipynb)
