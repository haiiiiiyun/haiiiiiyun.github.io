---
title: Angular docs-模板与数据绑定-Lifecycle Hooks
date: 2017-09-30
writing-time: 2017-09-30
categories: programming
tags: angular node Angular&nbsp;docs
---


Angular 对组件的生命期进行管理，它首先创建组件、呈现组件、再创建和呈现其子组件，当其有数据绑定的属性时有修改时进行检测，在将其从 DOM 中删除前进行销毁。

Angular 为组件生命期中的每个关键时刻提供了挂钩。

![生命期挂钩执行顺序](/assets/images/angular-docs/hooks-in-sequence.png)

## 组件生命期挂钩概述

挂钩接口定义在 `core` 库中，每个接口内都只包含一个挂钩方法，其名字是接口名加 `ng` 前缀，例如 `OnInit` 接口中的方法名为 `ngOninit`。


## 生命期顺序

在通过调用构造器合建一个组件/指令后，Angular 按以下顺序在特定时刻调用以下挂钩方法：

挂钩           | 目的和时间
--------------|
ngOnChanges() | 当有数据绑定的输入属性有更新有进行响应。该方法接收一个 `SimpleChanges` 对应，它包含属性的当前和之前值。在 `ngOnInit()` 之前及当各数据绑定的输入属性值有修改时调用。
ngOnInit()    | 当 Angular 在首次显示有数据绑定的属性及对指令/组件的输入属性进行设置后，对指令/组件进行初始化。在首次调用 `ngOnChanges()` 后调用，且只调用一次。
ngDoCheck     | 检测那些 Angular 无法自动检测到的修改，并进行响应。每次在运行 `ngOnChanges()` 和 `ngOnInit()` 后立即调用。
ngAfterContentInit() | 当 Angular 将外部内容放入组件视图后进行响应。在首次调用 `ngDoCheck()` 后调用（只一次）。组件专有的挂钩。
ngAfterContentChecked() | 在 Angular 检测放入到组件中的内容后进行响应。在调用 `ngAfterContentInit()` 及每次 `ngDoCheck()` 后进行调用。组件专有的挂钩。
ngAfterViewInit()  | 在 Angular 对组件的视图及其子视图初始化后进行响应。在首次调用 `ngAfterContentChecked()` 后进行调用（只一次）。组件专有的挂钩。
ngAfterViewChecked() | 在 Angular 检测组件的视图及其子视图后进行响应。在调用 `ngAfterViewInit()` 及每次 `ngAfterContentChecked()` 后调用。组件专有的挂钩。
ngOnDestroy        | 在销毁指令/组件前进行清理。Unsubcrible Observables and detach event handlers to avoid memory leaks. 

## 间谍指令

实现了 OnInit 和 OnDestroy 接口的指令可以应用在任意的标签或组件上，从而对标签或组件的创建和销毁进行监测，例如以下代码实现了一个间谍指令：

```typescript
//src/app/spy.directive.ts
// Spy on any element to which it is applied.
// Usage: <div mySpy>...</div>
@Directive({selector: '[mySpy]'})
export class SpyDirective implements OnInit, OnDestroy {

  constructor(private logger: LoggerService) { }

  ngOnInit()    { this.logIt(`onInit`); }

  ngOnDestroy() { this.logIt(`onDestroy`); }

  private logIt(msg: string) {
    this.logger.log(`Spy ${msg}`);
  }
}
```

将它应用在 div 上：

```html
<div *ngFor="let hero of heroes" mySpy class="heroes">
  {{hero}}
</div>
```

### OnInit

`ngOnInit()` 主要有 2 种用途：

1. 在调用构造器后，用它来指靠复杂的初始化工作，如从服务端获取数据
2. 在 Angular 首次调用 ngOnChanges 对输入属性完成设置后，对组件进行其它设置。

### OnDestroy

`ngOnDestroy()` 中适合进行一些清理工作，并通知系统的其它部分即将销毁。

### OnChanges

`ngOnChanges()` 会检测到组件输入属性 (input property) 的修改情况。当输入属性值是一个对象引用时，对象中某些属性值的修改不会触发 ngOnChanges(因为输入属性值对应的对象本身不变）。

### DoCheck

而 `ngDoCheck()` 用来检测像上面 `ngOnChanges()` 中 Angular 无法自动检测到修改的情况。 `ngDoCheck()` 会在 Angular 的每次检测周期时都会调用，因此会被非常频繁地调用。

### AfterView

下面是一个子视图(child view):

```typescript
//ChildComponent
@Component({
  selector: 'my-child-view',
  template: '<input [(ngModel)]="hero">'
})
export class ChildViewComponent {
  hero = 'Magneta';
}
```

下面是父组件的模板，里面包含了一个子视图：

```html
<!--AfterViewComponent (template)-->
template: `
  <div>-- child view begins --</div>
    <my-child-view></my-child-view>
  <div>-- child view ends --</div>`
```

父组件中的 `ngAfterViewInit()` 在其子视图初始化后调用。子视图只能通过属性装饰器 `@ViewChild` 来获取，例如：

```typescript
//AfterViewComponent (class excerpts)
export class AfterViewComponent implements  AfterViewChecked, AfterViewInit {
  private prevHero = '';

  // Query for a VIEW child of type `ChildViewComponent`
  @ViewChild(ChildViewComponent) viewChild: ChildViewComponent;

  ngAfterViewInit() {
    // viewChild is set after the view has been initialized
    this.logIt('AfterViewInit');
    this.doSomething();
  }

  ngAfterViewChecked() {
    // viewChild is updated after the view has been checked
    if (this.prevHero === this.viewChild.hero) {
      this.logIt('AfterViewChecked (no change)');
    } else {
      this.prevHero = this.viewChild.hero;
      this.logIt('AfterViewChecked');
      this.doSomething();
    }
  }
  // ...
}
```

### 遵守单向数据流规则

Angular 的单向数据流规则 (unidirectional data flow rule) 禁止在组件视图组合以后再对组件进行更新。而 `ngAfterViewInit()` 和 `ngAfterViewChecked()` 这两个挂钩都是在组件视图已经组合后触发，此时如果在回调函数中立即修改组件中有数据绑定的属性会出错（如下面代码中直接修改 comment 属性值），应通过 `LoggerService.tick_then()` 延后一个 JS 周期后进行。如下：

```typescript
//AfterViewComponent (doSomething)
// This surrogate for real business logic sets the `comment`
private doSomething() {
  let c = this.viewChild.hero.length > 10 ? `That's a long name` : '';
  if (c !== this.comment) {
    // Wait a tick because the component's view has already been checked
    this.logger.tick_then(() => this.comment = c);
  }
}
```

和 `ngDoCheck()` 类似，`ngAfterViewChecked()` 也会被频繁调用。


## AfterContent

内容投放(content projection) 是将导入组件外的 HTML 内容，并将其插入到组件模板中的指定位置的一种方法。（这种技术叫 transclusion)。

例如在父组件 AfterContentParentComponent 的模板中，包含了子组件标签 `<after-content>`，同时在该标签内嵌入了 `<my-child>` 标签：

```typescript
//AfterContentParentComponent (template excerpt)
`<after-content>
   <my-child></my-child>
 </after-content>`
```

将标签嵌入到组件标签，只在将外部内容投入到组件中时才能使用。

子组件的模板为：

```typescript
//AfterContentComponent (template)
template: `
  <div>-- projected content begins --</div>
    <ng-content></ng-content>
  <div>-- projected content ends --</div>`
```

模板中的 `<ng-content>` 就是外部内容的投入位置的点位符。本位中，会将 `<my-child>` 的内容投入到这里。

AfterContent 挂钩和 AfterView 挂钩的区别：

+ AfterView 挂钩关注 ViewChildren, 子组件的元素标签在组件的模板中
+ AfterContent 挂钩关注 ContentChildren，子组件内容被投入到组件中去

投入的内容对象只能通过属性装饰器 `@ContentChild` 来获取：

```typescript
//AfterContentComponent (class excerpts)
export class AfterContentComponent implements AfterContentChecked, AfterContentInit {
  private prevHero = '';
  comment = '';

  // Query for a CONTENT child of type `ChildComponent`
  @ContentChild(ChildComponent) contentChild: ChildComponent;

  ngAfterContentInit() {
    // contentChild is set after the content has been initialized
    this.logIt('AfterContentInit');
    this.doSomething();
  }

  ngAfterContentChecked() {
    // contentChild is updated after the content has been checked
    if (this.prevHero === this.contentChild.hero) {
      this.logIt('AfterContentChecked (no change)');
    } else {
      this.prevHero = this.contentChild.hero;
      this.logIt('AfterContentChecked');
      this.doSomething();
    }
  }
  // ...
}
```

由于  AfterContent 挂钩在 AfterView 挂钩前被调用，即在完成内容投放后组件视图的组合过程还没有完成，因此 AfterContent 挂钩中可直接对有组件中有数据绑定的属性进行更新，无法像 AfterView 挂钩一样要等待一个 JS 周期。## 参考

+ https://angular.io/guide/lifecycle-hooks
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_lifecycle_hooks.ipynb)
