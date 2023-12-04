---
title: Angular docs-模板与数据绑定-模板语法
date: 2017-09-27
writing-time: 2017-09-27
categories: programming
tags: angular node Angular&nbsp;docs
---


# 模板语法

以 model-view-controller(MVC) 或 model-view-viewmodel(MVVM) 为例，Angular 中的组件就是 controller/viewmodel，而模板就是 view。

## 模板中的 HTML

几乎所有的 HTML 语法都是有效的模板语法，但有以下例外：

+ 为安全原因，禁止使用 `<script>` 元素。实际上如果使用，会被忽略并在浏览器 console 中警告。
+ 一些合法的 HTML，如 `<html>`, `<body>`, `<base>` 等在模板中几乎没什么意义。
+ 可以扩展自己的模板 HTML 词汇，组件对应标签，指令对应属性。


## 插补用 `{{...}}`

`{{...}}` 间的模板表达式会先求值，再转成字符串作为该插补表达式的最终值。模板表达式中还可以调用主组件中的函数。

如：

```html
<h3>
  {{title}}
  <img src="{{heroImageUrl}}" style="height:30px">
</h3>

<p>My current hero is {{currentHero.name}}</p>

<!-- "The sum of 1 + 1 is 2" -->
<p>The sum of 1 + 1 is {{1 + 1}}</p>

<!-- "The sum of 1 + 1 is not 4" -->
<p>The sum of 1 + 1 is not {{1 + 1 + getVal()}}</p>
```

## 模板表达式 template expression

Angular 执行模板表达式，获取值，并将值赋值给绑定目标的属性。目标可以是一个 HTML 元素，一个组件或一个指令。

在 `{{1 + 1}}` 中，插补括号包围模板表达式。而在 `[property]="expression"` 这样的属性绑定中，模板表达式出现在 `=` 右边的引号中。

模板表达式语言和 JavaScript 类似，但不全相同。

会出现副作用的 JavaScript 表达式都禁止在模板表达式中使用，包括：

+ 赋值语句，如 `=`, `+=`, `-=`, ...
+ `new`
+ 用 `;` 或 `,` 相连的表达式
+ `++`, `--`

其它不同还有：

+ 不支持位操作符 `|` 和 `&`
+ 新的 [模板表达式操作符](https://angular.io/guide/template-syntax#expression-operators)，如 `|`, `?`, `!`


### 表达式的上下文

上下文通常就是组件实例。如下例中，`title` 和 `isUnchanged` 都引用 `AppComponent` 中的属性：

```typescript
//src/app/app.component.html
{{title}}
<span [hidden]="isUnchanged">changed</span>
```

模板表达式也可以引用模板上下文（如模板输入变量 `let hero`）或模板引用变量（如 `#heroInput`)：

```typescript
//src/app/app.component.html
<div *ngFor="let hero of heroes">{{hero.name}}</div>
<input #heroInput> {{heroInput.value}}
```

因此，模板表达式的上下文是如下的混合（优先次序从上到下）：

1. 模板上下文对象
2. 指令上下文对象
3. 组件

例如上面的 `hero` 变量引用有冲突时，优先使用由 `let hero` 定义的模板变量，而不是组件属性。

此外，模板表达式中不能引用任何全局命名空间中的变量，如 `window`, `document`, `console.log`, `Math.max` 等。

### 模板表达式编写指南

**无可见副作用**

不应该对除目标属性外的任何应用状态进行修改。

**可快速执行**

因表达式会在每个改动检测周期后都要执行。

**简洁**

**幂等性**

表达式多次运行的结果要相同，即没有副作用。


## 模板语句 template statement

模板语句就是对由绑定目标（如一个元素、组件、指令）引起的一个事件的应答。在事件绑定中，如 `(event)="statement"` 中，模板语句出现在 `=` 右边的引号中。

```typescript
//src/app/app.component.html
<button (click)="deleteHero()">Delete hero</button>
```

模板语句需要有副作用，这也是事件的初衷：基于用户动作更新应用状态。

和模板表达式语言类似，模板语句语言也类似 JavaScript。但它与模板表达式语言又不一样，特别地，它支持基本的赋值 `=` 和链接表达式（用 `;` 或 `,`）。

但下列的 JavaScrit 语法不能使用：

+ `new`
+ `++`, `--`
+ `+=`, `-=`
+ 位操作符 `|` 和 `&`
+ 模板表达式操作符。

### 模板语句的上下文

是一个混合体，按优先顺序如下：

+ 模板本身的上下文对象，如模板的 `$event` 对象，模板输入变量 (`let hero`), 模板引用变量（如 `#heroForm`）。
+ 组件


例如：

```typescript
//src/app/app.component.html
<button (click)="onSave($event)">Save</button>
<button *ngFor="let hero of heroes" (click)="deleteHero(hero)">{{hero.name}}</button>
<form #heroForm (ngSubmit)="onSubmit(heroForm)"> ... </form>
```

两样，模板语句都也不能引用任何全局命名空间中的东西。

## 绑定语法：概述

根据数据流的方向可将绑定类型分为 3 类： source-to-view, view-to-source, 双向序列 view-to-source-to-view。

数据方向              | 语法 | 类型
---------------------|
单向，从数据源到目标视图 | `{{expression}}`, `[target]="expression"`, `bind-target="expression"` | Interpolation, Property,Attribute,Class,Style
单向，从目标视图到数据源 | `(target)="statement"`, `on-target="statement"` | Event
双向                  | `[(target)]="expression"`, `bindon-target="expression"` | 双向


绑定目标必须是一个 *property* 名，不能是 *attribute* 名，并且只在等式的左边。其中 `[]` 与 `bind-` 等价，`()` 与 `on-` 等价，`[()]` 与 `bindon-` 等价。

### 一种新的心智模型

模板绑定只作用在 properties 和 events 上，而不是 attributes 上。

```html
<!-- Bind button disabled state to `isUnchanged` property -->
<button [disabled]="isUnchanged">Save</button>
```

如上代码中的绑定 `[disabled]="isUnchanged"`，是对 DOM 元素、组件或指令（本例中是 DOM 元素）的 disabeld *property* 进行设置，而不是对其 `attribute` 进行设置。

HTML attribute vs. DOM property

Attribute 由 HTML 定义，property 由 DOM 定义。

+ 有些 HTML attribute 和 DOM property 是一一对应的，如 id
+ 有些 HTML attribute 没有对应的 DOM property, 如 colspan
+ 有些 DOM property 没有对应的 HTML attribute，如 textContent
+ 许多 HTML attribute 有对应的 DOM property，但名字映射关系不统一。

Attribute 只用来初始化 DOM 的 property 值，但是 property 值之后是可变的，而 attribute 值不可变。例如当浏览器呈现 `<input type="text" value="Bob">` 后，它将创建一个 DOM 结点，其 `value` property 的值将初始化成 "Bob", 当用户输入 "Sally" 后， DOM 元素的 `value` property 会变成 "Sally"（当前值），而 HTML attribute 值（初始值）不变，即 `input.getAttribute('value')` 还是会返回 "Bob"。

### 绑定目标

数据问题绑定到 DOM 中的某个目标上。基于绑定类型，可以是 DOM 元素、组件、指令的 property, 事件或一个 attribute 上（极少情况）：


类型      | 目标 | 案例
---------|
Property | Element,Component, Directive property | `<img [src]="heroImageUrl"><hero-detail [hero]="currentHero"></hero-detail><div [ngClass]="{'special': isSpecial}"></div>`
Event    | Element,Component, Directive event | `<button (click)="onSave()">Save</button><hero-detail (deleteRequest)="deleteHero()"></hero-detail><div (myClick)="clicked=true" clickable>click me</div>`
双向      | Event and property | `<input [(ngModel)]="name">`
Attribute | Attribute(the exception) | `<button [attr.aria-label]="help">help</button>`
Class    | `class` property | `<div [class.special]="isSpecial">Special</div>`
Style    | `style` property | `<button [style.color]="isSpecial ? 'red' : 'green'">`

当绑定到指令的 property 时，如 `<div [ngClass]="classes">[ngClass] binding to the classes property</div>`，Angular 会将 property 名与指令中的 `inputs` 数组中的 property 名或有 `@Input()` 装饰的 property 名进行匹配。


## Attribute, class, style 绑定

模板语法为一些特殊情况提供了单向的绑定。

### Attribute 绑定

直接通过 attribute 绑定来设置一个 attribute 值，适用在没有对应 元素 property 的情况，如 ARIA, SVG, colspan 等。

例如 `<tr><td colspan="{{1 + 1}}">Three-Four</td></tr>` 会出错，因为 `<td>` 元素没有 `colspan` 属性。

Attribute 绑定的讲法类似 property 绑定，但是要绑定的 attribute 名前要有 `attr.` 前缀。因此上例中可修改为 `<tr><td [attr.colspan]="1 + 1">Three-Four</td></tr>`。

Attribute 绑定最主要应用在 设置 ARIA attribute 中，如：

```html
<!-- create and set an aria attribute for assistive technology -->
<button [attr.aria-label]="actionName">{{actionName}} with Aria</button>
```

### Class 绑定

实现在元素的 `class` attribute 中添加或删除类名。

例如初始 CSS 类为：

```html
<!-- standard class attribute setting  -->
<div class="bad curly special">Bad curly special</div>
```

如果用 `[class]` 的 property 绑定，例如：

```html
<!-- reset/override all class names with a binding  -->
<div class="bad curly special"
     [class]="badCurly">Bad curly</div>
```

则会将 `class` 中的类名直接设置为 "badCurly"。

如果用 `[class.special]` 这样的 class 绑定，如：

```html
<!-- toggle the "special" class on/off with a property -->
<div [class.special]="isSpecial">The class binding is special</div>

<!-- binding to `class.special` trumps the class attribute -->
<div class="special"
     [class.special]="!isSpecial">This one is not so special</div>
```

则能对 `class` attribute 中的特定类名进行开关。


### Style 绑定

用来设置内联 style，如:

```html
<button [style.color]="isSpecial ? 'red': 'green'">Red</button>
<button [style.background-color]="canSave ? 'cyan': 'grey'" >Save</button>
```

有单位的 style 要添加单位后缀，如：

```html
<button [style.font-size.em]="isSpecial ? 3 : 1" >Big</button>
<button [style.font-size.%]="!isSpecial ? 150 : 50" >Small</button>
```

style 名可以为 dash-case 形式，如 font-size，也可以是 camelCase 形式，如 fontSize。

## 事件绑定

例如：

```html
<!-- `myClick` is an event on the custom `ClickDirective` -->
<div (myClick)="clickMessage=$event" clickable>click with myClick</div>
```

事件绑定时，等式左边的 `()` 中是要绑定的事件，右边是 template statement。Angular 会自动为目标事件设置一个 event handler。当事件发生时，event handler 会执行 template statement 中的内容。

有关事件的信息的数据值等都会封装在一个命名为 `$event` 的 event 对象中。当事件绑定到 HTML 元素时，`$event` 是一个 [DOM event object](https://developer.mozilla.org/en-US/docs/Web/Events)，具有 target 和 target.value 等属性。 而如果绑定到指令（组件也是指令时），`$event` 可以是指令中实现的任何值。

### 使用 EventEmitter 实现定制的事件

指令通常使用 EventEmitter 触发自定义事件。先创建一个 EventEmitter 实例并导出为一个 property，再调用 `EventEmitter.emit(payload)` 来触发事件，并通过 payload 传入事件的返回值。父指令通过事件绑定侦听该事件，并在 `$event` 中访问 payload 值。

下列中，当用户点击 button 时，组件会触发 `deleteRequest` 事件：

```typescript
//src/app/hero-detail.component.ts (template)
template: `
<div>
  <img src="{{heroImageUrl}}">
  <span [style.text-decoration]="lineThrough">
    {{prefix}} {{hero?.name}}
  </span>
  <button (click)="delete()">Delete</button>
</div>`
```

```typescript
//src/app/hero-detail.component.ts (deleteRequest)
// This component makes a request but it can't actually delete a hero.
deleteRequest = new EventEmitter<Hero>();

delete() {
  this.deleteRequest.emit(this.hero);
}
```

而父组件可父 `deleteRequest` 事件进行绑定，并通过 `$event` 变量获取要删除的对象。

``````typescript
//src/app/app.component.html (event-binding-to-component)
<hero-detail (deleteRequest)="deleteHero($event)" [hero]="currentHero"></hero-detail>
```

## 双向绑定 [()]

`[()]` = banana in a box.

`[(x)]` 语法要求元素有一个要设置的 property `x`，及有一个名为 `xChange` 的事件。这里的 `SizerComponent` 符合这种模式，它有一个 `size` property, 及 `sizeChange` 事件：

```typescript
//src/app/sizer.component.ts
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'my-sizer',
  template: `
  <div>
    <button (click)="dec()" title="smaller">-</button>
    <button (click)="inc()" title="bigger">+</button>
    <label [style.font-size.px]="size">FontSize: {{size}}px</label>
  </div>`
})
export class SizerComponent {
  @Input()  size: number | string;
  @Output() sizeChange = new EventEmitter<number>();

  dec() { this.resize(-1); }
  inc() { this.resize(+1); }

  resize(delta: number) {
    this.size = Math.min(40, Math.max(8, +this.size + delta));
    this.sizeChange.emit(this.size);
  }
}
```

而下面的 `AppComponent.fontSizePx` 与 `SizerComponent` 进行了双向绑定：

```html
<!--src/app/app.component.html (two-way-1) -->
<my-sizer [(size)]="fontSizePx"></my-sizer>
<div [style.font-size.px]="fontSizePx">Resizable Text</div>
```

`AppComponent.fontSizePx` 的值对 `SizerComponent.size` 值进行初始设置。当点击按钮后，通过双向绑定，`AppComponent.fontSizePx` 值也会相应更新，而更新后的值，又进一步通过绑定流向到 `font-size` 的设置。

双向绑定只是一个语法糖，不用双向绑定语法，则要同时写 property 绑定和事件绑定，如：

```html
<!--src/app/app.component.html (two-way-2) -->
<my-sizer [size]="fontSizePx" (sizeChange)="fontSizePx=$event"></my-sizer>
```

其中的 `$event` 变量值就是 `SizerComponent.sizeChange` 事件的 payload 值。

HTML 中的 `<input>` 和 `<select>` 都不是内置支持这种模式的，因此不能直接使用双向 绑定，但是通过 `NgModule` 指令进行桥接，可以为表格元素进行双向绑定。

## 内置指令

### 内置 attribute 指令

Attribute 指令用来侦听和修改其它 HTML 元素、attributes、properties、及组件的行为。将它们应用到元素时，及其像在 HTML 元素上设置 attribute，因此叫 attribute 指令。

许多 NgModules 如 RouterModule 和 FormsModule 都定义有自己的 attribute 指令。最常用的 attribute 指令有：

+ NgClass: 添加或删除一组 CSS 类
+ NgStyle: 添加或删除一组 HTML styles
+ NgModel: 双向绑定到表单元素


### NgClass

类绑定适用于添加和删除单个类，如：

```html
<!-- toggle the "special" class on/off with a property -->
<div [class.special]="isSpecial">The class binding is special</div>
```

而 `NgClass` 指令通过绑定一个 key:value 型的控制对象值，能同时对多个 CSS 类进行添加和删除。其中每个 key 都是 CSS 类名，对应的值为 true 时添加该类，为 false 时则删除。例如：

```typescript
//src/app/app.component.ts
currentClasses: {};
setCurrentClasses() {
  // CSS classes: added/removed per current state of component properties
  this.currentClasses =  {
    'saveable': this.canSave,
    'modified': !this.isUnchanged,
    'special':  this.isSpecial
  };
}
```

```html
<!--src/app/app.component.html-->
<div [ngClass]="currentClasses">This div is initially saveable, unchanged, and special</div>
```

### NgStyle

style 绑定也只适用于单个 style 值设置。而 NgStyle 指令和 NgClass 类似，能同时对多个 style 进行添加和删除。例如：

```typescript
//src/app/app.component.ts
currentStyles: {};
setCurrentStyles() {
  // CSS styles: set per current state of component properties
  this.currentStyles = {
    'font-style':  this.canSave      ? 'italic' : 'normal',
    'font-weight': !this.isUnchanged ? 'bold'   : 'normal',
    'font-size':   this.isSpecial    ? '24px'   : '12px'
  };
}
```

```html
<!--src/app/app.component.html-->
<div [ngStyle]="currentStyles">
  This div is initially italic, normal weight, and extra large (24px).
</div>
```

### NgModel 实现表单元素的双向绑定

```typescript
//src/app/app.component.html (NgModel-1)
<input [(ngModel)]="currentHero.name">
```

`ngModule` 指令定义在 `FormsModule` 中，故要先将导入 FormsModule 并将它添加到 NgModule 的 `imports` 列表中后才能使用。

```typescript
//src/app/app.module.ts (FormsModule import)
import { NgModule } from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // <--- JavaScript import from Angular

/* Other imports */

@NgModule({
  imports: [
    BrowserModule,
    FormsModule  // <--- import into the NgModule
  ],
  /* Other module metadata */
})
export class AppModule { }
```

手动实现表单元素的双向绑定功能如下：

```html
<input [value]="currentHero.name"
       (input)="currentHero.name=$event.target.value" >
```

而 ngModel 指令实现了将表单元素中的 value 属性和 input 事件分别映射为 ngModel 属性和 ngModel 事件，因而与其符合双向绑定语法要求的模式。因此上面的例子可重写为：

```html
<input
  [ngModel]="currentHero.name"
  (ngModelChange)="currentHero.name=$event">
```

或者：

```html
<input [(ngModel)]="currentHero.name">
```

双向绑定只实现对属性值的设置，如果要实现额外功能（如将输入值转成大写形式），则要用扩展的形式写：

```html
<input
  [ngModel]="currentHero.name"
  (ngModelChange)="setUppercaseName($event)">
```

### 内置的结构型指令 structural directive

Structural directives 用于处理 HTML 布局。它们通常通过添加、删除或修改与其关联的托管元素（host elements) 来实现对 DOM 结构的修改。

结构型指令名前都有 `*` 前缀。

最常见的结构型指令有：

+ NgIf: 依据条件添加或删除 DOM 中的元素
+ NgFor: 为列表中的每个元素进行模板化呈现
+ NgSwitch: 根据条件值在多个可选视图间进行切换


### NgIf

例如：

```html
<hero-detail *ngIf="isActive"></hero-detail>
```

如果条件表达式 `isActive` 为真，则在 DOM 中创建 hero-detail 元素，如果为假，则在 DOM 中删除。

NgIf 也可用来确保值为非 null 后才显示：

```html
<div *ngIf="currentHero">Hello, {{currentHero.name}}</div>
<div *ngIf="nullHero">Hello, {{nullHero.name}}</div>
```

### NgFor

例如：

```html
<hero-detail *ngFor="let hero of heroes" [hero]="hero"></hero-detail>
```

赋值给 `*ngFor` 的字符串不是模板表达式，它是一种独立的语言，叫 *microsyntax*。这里 `"let hero of heroes"` 的意思是：
> 抽取 heroes 数据中的每个 hero，将它保存到一个本地循环变量 hero 中，并使该变量在每次迭代的模板化 HTML 中可访问。

Angular 在 NgFor 指令的托管元素（host element)外围创建一个 `<ng-template>`，循环中生成的所有模板化元素都将绑定到该 `<ng-template>` 中。

`let` 关键字创建的 `hero` 变量是一个模板输入变量(template input variable)，可以在托管元素中使用：

```html
<div *ngFor="let hero of heroes">{{hero.name}}</div>
<hero-detail *ngFor="let hero of heroes" [hero]="hero"></hero-detail>
```

从 0 开始计数的迭代索引值可以从 NgFor 指令上下文的 `index` property 获取，可以保存为一个 template input variable：

```html
<div *ngFor="let hero of heroes; let i=index">{{i + 1}} - {{hero.name}}</div>
```

NgFor 指令上下文中还有 `last, even, odd` 等 property 等。


### ngFor 和 trackBy

在 NgFor 中，列表有更新都会触发级联的 DOM 操作。例如从服务器重新返回一组相同值的对象时，也会触发 DOM 中元素的重新创建操作（因为返回的列表不是原来的列表），这样有些会造成性能问题。

通过 `trackBy`，Angular 可以基于某值（如 id) 来判断列表和列表中的元素是否有更新。

例如，先定义一个 trackBy 函数，用来返回元素的特征值：

```typescript
//src/app/app.component.ts
trackByHeroes(index: number, hero: Hero): number { return hero.id; }
```

在 microsyntax 表达式中，将 traceBy 值设置为该函数：

```html
<!--src/app/app.component.html-->
<div *ngFor="let hero of heroes; trackBy: trackByHeroes">
  ({{hero.id}}) {{hero.name}}
</div>
```

### NgSwitch 指令

它根据 switch 条件，在多个可能的元素中选择显示一个元素，并只将选中的元素加入到 DOM 中。NgSwitch 实际上是一组指令： NgSwitch(attribute directive), NgSwitchCase, NgSwitchDefault，如：

```html
<div [ngSwitch]="currentHero.emotion">
  <happy-hero    *ngSwitchCase="'happy'"    [hero]="currentHero"></happy-hero>
  <sad-hero      *ngSwitchCase="'sad'"      [hero]="currentHero"></sad-hero>
  <confused-hero *ngSwitchCase="'confused'" [hero]="currentHero"></confused-hero>
  <unknown-hero  *ngSwitchDefault           [hero]="currentHero"></unknown-hero>
</div>
```

## 模板引用变量 (Template reference variables)

模板引用变量可用来引用模板中的一个 DOM 元素、组件、指令或一个 [web component](https://developer.mozilla.org/en-US/docs/Web/Web_Components)。

使用 `#` 来声明一个引用变量，并能在模板中的任何位置都可使用该变量，如：

```html
<!--src/app/app.component.html-->
<input #phone placeholder="phone number">

<!-- lots of other elements -->

<!-- phone refers to the input element; pass its `value` to an event handler -->
<button (click)="callPhone(phone.value)">Call</button>
```

模板引用变量值是全局的，因此最好不要在 ngFor 的 microsyntax 表达式中创建同名的变量。

通常，模板引用变量值就是关联的元素对象。但是指令可能会修改其值。例如：

```html
<form (ngSubmit)="onSubmit(heroForm)" #heroForm="ngForm">
  <div class="form-group">
    <label for="name">Name
      <input class="form-control" name="name" required [(ngModel)]="hero.name">
    </label>
  </div>
  <button type="submit" [disabled]="!heroForm.form.valid">Submit</button>
</form>
<div [hidden]="!heroForm.form.valid">
  {{submitMessage}}
</div>
```

上例中，由 `NgForm` 指令处理后的引用变量值不再是 HTMLFormElement（它没有 form 属性），而是一个 NgForm 指令对象。


除了用 `#` 来声明一个引用变量外，也可用 `ref-` 前缀进行，如：

```html
<input ref-fax placeholder="fax number">
<button (click)="callFax(fax.value)">Fax</button>
```

## Input and output property( @Input, @Output)

### 声明输入和输出属性

例如：

```typescript
@Input()  hero: Hero;
@Output() deleteRequest = new EventEmitter<Hero>();
```

也可以在指令的 metadata 中进行声明：

```typescript
@Component({
  inputs: ['hero'],
  outputs: ['deleteRequest'],
})
```

### 创建别名

例如：

```typescript
@Output('myClick') clicks = new EventEmitter<string>(); //  @Output(alias) propertyName = ...
```

此时， `myClick` 就是公开的名字，在绑定时使用，而 clicks 是内置名字。

也可以在 metadata 中声明：

```typescript
@Directive({
  outputs: ['clicks:myClick']  // propertyName:alias
})
```

## 模板表达式操作符

模板表达式语言中实现了一些特殊操作符。

### 管道操作符 |

将表达式结果进行转换操作。管道是一个简单函数，一个输入，一个输出。[Angular pipes](https://angular.io/guide/pipes) 里列表出内置的一些管道。管道还可以串联，例如：

```html
<!-- Pipe chaining: convert title to uppercase, then to lowercase -->
<div>
  Title through a pipe chain:
  {{title | uppercase | lowercase}}
</div>
```

应用管道参数：

```html
<!-- pipe with configuration argument => "February 25, 1970" -->
<div>Birthdate: {{currentHero?.birthdate | date:'longDate'}}</div>
```

`json` 管道在调试时很有用：

```html
<div>{{currentHero | json}}</div>
```

### 安全导航操作符 (?.)

可自动处理属性路径中的 null 和 undefined 值的情况。

例如：

```html
<!-- No hero, no problem! -->
The null hero's name is {{nullHero?.name}}
```

如果不用 `?.`，则要这样写：

```html
The null hero's name is {{nullHero && nullHero.name}}
```

`?.` 也可以同时使用有多个，如： `a?.b?.c?.d`。

## 参考

+ https://angular.io/guide/template-syntax
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_template_syntax.ipynb)
