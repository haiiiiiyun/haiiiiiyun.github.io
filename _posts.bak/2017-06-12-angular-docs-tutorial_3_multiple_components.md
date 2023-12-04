---
title: Angular docs-教程 3： 多组件
date: 2017-06-12
writing-time: 2017-08-21
categories: programming
tags: angular node Angular&nbsp;docs
---


# 教程 3： 多组件

目前所有功能都在根组件 `AppComponent` 中实现，现将其分解成多个子组件，每个关注到特定的任务或工作流。最终，`AppComponent` 将只用来组件这些子组件。

## hero detail 组件

在 `app/` 下添加 `hero-detail.component.ts` 文件，用来保存 `HeroDetailComponent` 组件。

文件名和组件名遵循 [Angular 风格指南](https://angular.io/guide/styleguide#naming)：

+ 组件名用 *upper camel case*，并以 "Component" 结尾。
+ 组件文件名用 *lower dash case*，每个字用 `-` 分开，并以 `.component.ts` 结尾。

```typescript
//app/hero-detail.component.ts (initial version)
import { Component } from '@angular/core';

@Component({
  selector: 'hero-detail',
})
export class HeroDetailComponent {
}
```

`@Component` 装饰器为组件提供 metadata。这里的 CSS 选择子名 `hero-detail`，可用来在父组件的模板中标识该组件，例如 `<hero-detail>`。

将组件 `export` 后，可在其它地方对它进行 `import`。

### Hero detail 模板

将 `AppComponent` 模板中关于 hero detail 的内容移到 `HeroDetailComponent` 组件的 `template` 中。由于 HeroDetailComponent 有一个 *hero*，没有选中的 *seletedHero*，因此将模板中的 `selectedHero` 改为 `hero`。

```typescript
//src/app/hero-detail.component.ts (template)
@Component({
  selector: 'hero-detail',
  template: `
    <div *ngIf="hero">
      <h2>{{hero.name}} details!</h2>
      <div><label>id: </label>{{hero.id}}</div>
      <div>
        <label>name: </label>
        <input [(ngModel)]="hero.name" placeholder="name"/>
      </div>
    </div>
  `
})
```

### 添加 hero 属性

```typescript
//src/app/hero-detail.component.ts (hero property)
hero: Hero;
```

`hero` 属性的类型是 `Hero`，但 `Hero` 类还定义在 `app.component.ts`，当有多个组件引用同个类时，Angular 风格指南建议一个类一个文件进行实现。

```typescript
//src/app/hero.ts
export class Hero {
  id: number;
  name: string;
}
```

再在 app.component.ts 和 hero-detail.component.ts 文件中将 `Hero` 类导入：

```typescript
//src/app/hero-detail.component.ts
import { Hero } from './hero';
```

### *hero* 属性将是一个 *input* 属性

之后， 父组件 `AppComponent` 会通过将它的 `selectedHero` 绑定给 `HeroDetailComponent` 组件的 `hero` 属性，从而告诉子组件 `HeroDetailComponent` 将显示哪个 hero。

绑定操作如下：

```html
<!--src/app/app.component.html-->
<hero-detail [hero]="selectedHero"></hero-detail>
```

方括号中的是表达式的绑定目标，即组件的 `input` 属性，用 `[]` 来绑定 `input` 属性，就如同对象的属性赋值，因此很好记。

方括号的绑定表达式中，目标属性必须是一个 `input` 属性。

先从 `core` 中导入 `Input` 符号：

```typescript
//src/app/hero-detail.component.ts (excerpt)
import { Component, Input } from '@angular/core';
```

再通过 `@Input()` 装饰器将 `hero` 声明为一个 `input` 属性：

```typescript
//src/app/hero-detail.component.ts (excerpt)
@Input() hero: Hero;
```

`HeroDetailComponent` 组件将通过它的 `hero` `input` 属性接收一个 hero 对象，再将它绑定到模板上输出。

完整的 `HeroDetailComponent`:

```typescript
//src/app/hero-detail.component.ts
import { Component, Input } from '@angular/core';

import { Hero } from './hero';
@Component({
  selector: 'hero-detail',
  template: `
    <div *ngIf="hero">
      <h2>{{hero.name}} details!</h2>
      <div><label>id: </label>{{hero.id}}</div>
      <div>
        <label>name: </label>
        <input [(ngModel)]="hero.name" placeholder="name"/>
      </div>
    </div>
  `
})
export class HeroDetailComponent {
  @Input() hero: Hero;
}
```

## 在 AppModule 中声明 HeroDetailComponent

每个组件都必须要在 `NgModule` 中声明。

在 `app.module.ts` 中导入 `HeroDetailComponent`：

```typescript
//src/app/app.module.ts
import { HeroDetailComponent } from './hero-detail.component';
```

将 `HeroDetailComponent` 加入 `declarations` 数组：

```typescript
//src/app/app.module.ts
declarations: [
  AppComponent,
  HeroDetailComponent
],
```

`declarations` 数组中通常包含一组应用组件， pipes, directives。组件必须要先在模块中声明后才能在其它组件中引用。


## 将 HeroDetailComponent 添加到 AppComponent

在 `AppComponent` 模板的底部添加 `hero-detail` 标签，用来引用 HeroDetailComponent 组件，并将根组件的 `selectedHero` 属性绑定到 HeroDetailComponent 中 `hero` `input` 属性：

```typescript
//app.component.ts (excerpt)
<hero-detail [hero]="selectedHero"></hero-detail>
```

现在每次 `selectedHero` 修改后，`HeroDetailComponent` 都会相应更新。

## 参考

+ https://angular.io/tutorial/toh-pt3
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_3_mutiple_components.ipynb)
