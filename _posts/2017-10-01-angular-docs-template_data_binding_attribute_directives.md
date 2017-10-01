---
title: Angular docs-模板与数据绑定-属性指令
date: 2017-10-01
writing-time: 2017-10-01
categories: programming
tags: angular node Angular&nbsp;docs
---

属性指令用来修改 DOM 元素的外观或行为。

## 指令概述

共有 3 种指令：

+ 组件： 即是有模板的指令
+ 结构型指令：通过添加和删除 DOM 元素来修改 DOM 布局，如 ngFor, ngIf
+ 属性指令： 修改一个元素/组件/其它指令的外观或行为，如 ngStyle


## 构建一个简单的属性指令

属性指令的类必须要用 `@Directive` 来注解，里面指定该属性指令的选择子。

本例实现一个高亮属性指令来设置当用户鼠标移到元素上时的背景色。

```typescript
//src/app/highlight.directive.ts
import { Directive, ElementRef, Input } from '@angular/core';

@Directive({ selector: '[myHighlight]' })
export class HighlightDirective {
    constructor(el: ElementRef) {
       el.nativeElement.style.backgroundColor = 'yellow';
    }
}
```

`ElementRef` 注入到指令的构造器，从而可以访问指令对应的 DOM 元素。

`@Directive` 装饰器的 metadata 中指定该指令的 CSS 选择子，注意这里定义时的选择子名包含在 `[]` 中，如 `[myHighlight]`，但在应用该属性指令时不包含 `[]`。


## 应用属性指令

可在模板中的任何标签上应用：

```html
<!--src/app/app.component.html-->
<h1>My First Attribute Directive</h1>
<p myHighlight>Highlight me!</p>
```

```typescript
//src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  templateUrl: './app.component.html'
})
export class AppComponent {
  color: string;
}
```

同时，自定义指令先要先要 `app.module` 中先 import，再在 `@NgModule` 的 `declarations` 中声明后才能使用：

```typescript
//src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HighlightDirective } from './highlight.directive';

@NgModule({
  imports: [ BrowserModule ],
  declarations: [
    AppComponent,
    HighlightDirective
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

Angular 在 `<p>` 元素上看到有 `myHighlight` 属性时，将创建一个 `HighlightDirective` 指令类的实例，并将 `<p>` 元素的引用注入到指令的构造器中。


## 响应用户事件

```typescript
//src/app/highlight.directive.ts
import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[myHighlight]'
})
export class HighlightDirective {
  constructor(private el: ElementRef) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight('yellow');
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight(null);
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
```

`@HostListener` 装饰器可用来托管 DOM 元素上的事件，本例中对应用有该属性指令的 p 元素上的事件进行响应。


## 通过 `@Input` 为指令添加输入属性

例如设置一个高亮初始颜色的输入属性 `highlightColor`。指令的输入属性绑定有 2 种形式，例如：

```html
<p myHighlight highlightColor="yellow">Highlighted in yellow</p>
<p myHighlight [highlightColor]="'orange'">Highlighted in orange</p>
```

通过 `@Input(alias)` 为输入属性创建和指令相同的别名：

```typescript
@Input('myHighlight') highlightColor: string;
```

之后应用属性指令和绑定输入属性可同时进行：

```html
<p [myHighlight]="color">Highlight me!</p>
```

## 指令设置多个输入属性

类似地，通过 `@Input` 设置多个输入属性，例如 `defaultColor`。然后 2 个输入属性可这样绑定：

```html
<p [myHighlight]="color" defaultColor="violet">
  Highlight me too!
</p>
```

## 参考

+ https://angular.io/guide/attribute-directives
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_attribute_directives.ipynb)
