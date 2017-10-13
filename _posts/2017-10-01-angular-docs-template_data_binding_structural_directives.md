---
title: Angular docs-模板与数据绑定-结构型指令
date: 2017-10-01
writing-time: 2017-10-01
categories: programming
tags: angular node Angular&nbsp;docs
---

# 结构型指令

结构型指令通常通过添加、删除或处理元素来重构 DOM 结构。

结构型指令在应用时指令属性名前都有 `*` 前缀，如：

```html
<div *ngIf="hero" >{{hero.name}}</div>
```

而 `*` 只是一个便捷标识法，是一种语法糖，而指令右边的字符串不是普通的模板表达式，而是 [microsyntax](https://angular.io/guide/structural-directives#microsyntax) 表达式。Angular 将这种标识最终转换成一个 `<ng-template>` 标签，用来包围主元素 (host element) 及其子元素。

一个元素可以应用多个属性指令，但是只能有一个结构型指令。


## 指令拼写方式

指令类一般用 UpperCamelCase 方式，如 NgIf，而指令属性名用 lowerCamelCase 方式，如 ngIf。

## NgIf 案例

```html
<p *ngIf="true">
  Expression is true and ngIf is true.
  This paragraph is in the DOM.
</p>
<p *ngIf="false">
  Expression is false and ngIf is false.
  This paragraph is not in the DOM.
</p>
```

`ngIf` 指令不是用 CSS 将元素隐藏，而在直接在 DOM 中进行添加和删除。

### `*` 前缀

例如：

```html
<!--src/app/app.component.html (asterisk)-->
<div *ngIf="hero" >{{hero.name}}</div>
```

内部 Angular 将 `*` 进行 2 步转换。首先将 `*ngIf="..."` 转成 `template` 属性：

```html
<!--src/app/app.component.html (ngif-template-attr)-->
<div template="ngIf hero">{{hero.name}}</div>
```

然后将 `template` 属性转成 `<ng-template>` 元素，用来包含 host element:

```html
<!--src/app/app.component.html (ngif-template)-->
<ng-template [ngIf]="hero">
  <div>{{hero.name}}</div>
</ng-template>
```

+ `*ngIf` 指令移到到 `<ng-template>` 元素内，并转换成了属性绑定 `[ngIf]`
+ `<div>` 的其它部分全部都移到了 `<ng-template>` 内

## `*ngFor`

它的 `*` 语法也会进行如上的类似转换。下面是 ngFor 的 3 种写法：

```html
<!--src/app/app.component.html (inside-ngfor)-->
<div *ngFor="let hero of heroes; let i=index; let odd=odd; trackBy: trackById" [class.odd]="odd">
  ({{i}}) {{hero.name}}
</div>

<div template="ngFor let hero of heroes; let i=index; let odd=odd; trackBy: trackById" [class.odd]="odd">
  ({{i}}) {{hero.name}}
</div>

<ng-template ngFor let-hero [ngForOf]="heroes" let-i="index" let-odd="odd" [ngForTrackBy]="trackById">
  <div [class.odd]="odd">({{i}}) {{hero.name}}</div>
</ng-template>
```

### Microsyntax

Mycrosyntax 可用来配置指令。其解析器将语句中的内容转换成 `<ng-template>` 上的属性：

+ `let` 关键字用来声明一个模板输入变量，可在模板中引用。本例中的输入变量是 `hero`, `i`, `odd`。解析器将它们转换成变量 `let-hero`, `let-i`, `let-odd`。
+ 解析器将 `of` 和 `trackBy` 转变成 `ngForOf` 和 `ngForTrackBy` 这两个 NgFor 指令的输入属性。
+ 当 `NgFor` 指令迭代列表时，会设置它上下文中的属性值。这些属性包含 `index` 和 `odd` 等，以及一个特殊属性 `$implicit`。
+ `let-i=index` 和 `let-odd=odd` 中设置的变量会更新到当前值。
+ `let-hero` 没有指定，它将会设置为当前上下文中的 `$implicit` 属性值，而该值每次迭代时初始化为当前的 hero 值。

## 模板输入变量

模板输入变量用 `let` 声明，如 `let i=index`，它只能作为用模板的单个实例中。

而模板引用变量用 `#var` 定义，它是对一个关联元素/组件/指令的一个引用，可在模板的任何地方使用。

这两种变量有独立的命名空间。


## NgSwitch 指令

它实际上是一组相互协作的指令： NgSwitch, NgSwitchCase, NgSwitchDefault。

```html
<!--src/app/app.component.html (ngswitch)-->
<div [ngSwitch]="hero?.emotion">
  <happy-hero    *ngSwitchCase="'happy'"    [hero]="hero"></happy-hero>
  <sad-hero      *ngSwitchCase="'sad'"      [hero]="hero"></sad-hero>
  <confused-hero *ngSwitchCase="'confused'" [hero]="hero"></confused-hero>
  <unknown-hero  *ngSwitchDefault           [hero]="hero"></unknown-hero>
</div>
```

`NgSwitch` 本身不是一个结构型指令，而是一个属性指令，它用来控制其它 2 个结构型  Switch 指令。

这里 `<happy-hero>` 元素是 `*ngSwitchCase` 的 host element, 而 `<unknown-hero>` 元素是 `*ngSwitchDefault` 的 host element。

NgSwitch 也将会被转换成如下：

```html
<div [ngSwitch]="hero?.emotion">
  <happy-hero    template="ngSwitchCase 'happy'"    [hero]="hero"></happy-hero>
  <sad-hero      template="ngSwitchCase 'sad'"      [hero]="hero"></sad-hero>
  <confused-hero template="ngSwitchCase 'confused'" [hero]="hero"></confused-hero>
  <unknown-hero  template="ngSwitchDefault"         [hero]="hero"></unknown-hero>
</div>

<div [ngSwitch]="hero?.emotion">
  <ng-template [ngSwitchCase]="'happy'">
    <happy-hero [hero]="hero"></happy-hero>
  </ng-template>
  <ng-template [ngSwitchCase]="'sad'">
    <sad-hero [hero]="hero"></sad-hero>
  </ng-template>
  <ng-template [ngSwitchCase]="'confused'">
    <confused-hero [hero]="hero"></confused-hero>
  </ng-template >
  <ng-template ngSwitchDefault>
    <unknown-hero [hero]="hero"></unknown-hero>
  </ng-template>
</div>
```

## `<ng-template>`


`<ng-template>` 是 Angular 内部用来呈现 HTML 的一个元素。它不会直接显示内容，如果你将内容直接放在 `<ng-template>` 内，如：

```html
<p>Hip!</p>
<ng-template>
  <p>Hip!</p>
</ng-template>
<p>Hooray!</p>
```

Angular 会将 `<ng-template>` 及其子元素全部解析成注释内容如： `<!--tempalte bindings={}-->`，从而不会显示每 2 个 Hip 信息。

## 用 `<ng-container>` 来组合兄弟元素


`<ng-container>` 元素是 Angular 中的一个组合元素，Angular 只将它作为组合用，不会将它放入 DOM 中，因此不会影响样式和布局。

可以将 `<ng-container>` 理解成是一个语法元素，类似于 JS 中的花括号：

```javascript
if (someCondition) {
  statement1;
  statement2;
  statement3;
}
```

`<ng-container>` 的使用例子：

```html
<div>
  Pick your favorite hero
  (<label><input type="checkbox" checked (change)="showSad = !showSad">show sad</label>)
</div>
<select [(ngModel)]="hero">
  <ng-container *ngFor="let h of heroes">
    <ng-container *ngIf="showSad || h.emotion !== 'sad'">
      <option [ngValue]="h">{{h.name}} ({{h.emotion}})</option>
    </ng-container>
  </ng-container>
</select>
```

## 编写一个自定义的结构型指令

这个指令为 `UnlessDirective`，它的功能和 `ngIf` 正好相反。

开始：

```typescript
//src/app/unless.directive.ts (skeleton)
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({ selector: '[myUnless]'})
export class UnlessDirective {
}
```

### TemplateRef 和 ViewContainerRef

一个简单的结构型指令会基于 Angular 生成的 `<ng-template>` 创建一个嵌入的视图，并将它插入到与指令的 host element 相邻接的视图容器（view container) 中。

`<ng-template>` 的内容可通过 `TemplateRef` 获取，而视图容器可通过 `ViewContainerRef` 获取。

### 输入属性

需要有一个布尔值的输入属性：

```typescript
//src/app/unless.directive.ts (set)
@Input() set myUnless(condition: boolean) {
  if (!condition && !this.hasView) {
    this.viewContainer.createEmbeddedView(this.templateRef);
    this.hasView = true;
  } else if (condition && this.hasView) {
    this.viewContainer.clear();
    this.hasView = false;
  }
}
```

由于无需读取该属性，因此也无需 getter，整个指令代码为：

```typescript
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

/**
 * Add the template content to the DOM unless the condition is true.
 */
@Directive({ selector: '[myUnless]'})
export class UnlessDirective {
  private hasView = false;

  constructor(
    private templateRef: TemplateRef<any>,
    private viewContainer: ViewContainerRef) { }

  @Input() set myUnless(condition: boolean) {
    if (!condition && !this.hasView) {
      this.viewContainer.createEmbeddedView(this.templateRef);
      this.hasView = true;
    } else if (condition && this.hasView) {
      this.viewContainer.clear();
      this.hasView = false;
    }
  }
}
```

应用举例：

```html
<p *myUnless="condition" class="unless a">
  (A) This paragraph is displayed because the condition is false.
</p>

<p *myUnless="!condition" class="unless b">
  (B) Although the condition is true,
  this paragraph is displayed because myUnless is set to false.
</p>
```
## 参考

+ https://angular.io/guide/structural-directives
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_structural_directives.ipynb)
