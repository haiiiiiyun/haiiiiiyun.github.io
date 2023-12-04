---
title: Angular docs-模板与数据绑定-动画
date: 2017-10-13
writing-time: 2017-10-13
categories: programming
tags: angular node Angular&nbsp;docs
---

## 概述

Angular 的动画系统基于 [Web Animations API](https://w3c.github.io/web-animations/) 实现，在不支持该 API 的浏览器上需要 polyfill 才能运行，要加载 [web-animations.min.js](https://github.com/web-animations/web-animations-js)。

## 加载相关的动画模块

```typescript
//app.module.ts (animation module import excerpt)
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  imports: [ BrowserModule, BrowserAnimationsModule ],
  // ... more stuff ...
})
export class AppModule { }
```

## 两个状态间的切换动画

下面是一个例子：


```typescript
// hero.service.ts (Hero class)
export class Hero {
  constructor(public name: string, public state = 'inactive') { }

  toggleState() {
    this.state = this.state === 'active' ? 'inactive' : 'active';
  }
}


//hero-list-basic.component.ts
import {
  Component,
  Input
} from '@angular/core';
import {
  trigger,
  state,
  style,
  animate,
  transition
} from '@angular/animations';

import { Hero } from './hero.service';

@Component({
  selector: 'hero-list-basic',
  template: `
    <ul>
      <li *ngFor="let hero of heroes"
          [@heroState]="hero.state"
          (click)="hero.toggleState()">
        {{hero.name}}
      </li>
    </ul>
  `,
  styleUrls: ['./hero-list.component.css'],
  animations: [
    trigger('heroState', [
      state('inactive', style({
        backgroundColor: '#eee',
        transform: 'scale(1)'
      })),
      state('active',   style({
        backgroundColor: '#cfd8dc',
        transform: 'scale(1.1)'
      })),
      transition('inactive => active', animate('100ms ease-in')),
      transition('active => inactive', animate('100ms ease-out'))
    ])
  ]
})
export class HeroListBasicComponent {
   @Input() heroes: Hero[];
}
```

动画可以定义在 `@Component` metadata 中的 `animations` 列表中，其中每个 `trigger` 定义就是一个动画定义。在组件模板中的任何元素上通过 `[@triggerName]` 语法来应用动画，动画关联的状态与组件的属性绑定，`[]` 是绑定的语法, `[@..]` 是动画绑定的语法。


## 状态与转换

Angular 动画定义为一组状态与其转换。

状态值都是字符串，它都来源与绑定属性的可能值，如上例中的 `inactive`, `active` 状态值。定义状态后，可指定该状态下的样式：

```typescript
//src/app/hero-list-basic.component.ts
state('inactive', style({
  backgroundColor: '#eee',
  transform: 'scale(1)'
})),
state('active',   style({
  backgroundColor: '#cfd8dc',
  transform: 'scale(1.1)'
})),
```

之后定义状态间的转换过程，每个转换定义控制一组样式间的切换过程及时序，如：

```typescript
//src/app/hero-list-basic.component.ts
transition('inactive => active', animate('100ms ease-in')),
transition('active => inactive', animate('100ms ease-out'))
```

如果多个转换有相同的时间配置，则可合并成一个转换定义中：

```typescript
transition('inactive => active, active => inactive',
 animate('100ms ease-out'))
```

当双向转换都有相同的时间配置时，可用 `<=>` 简写：

```typescript
transition('inactive <=> active', animate('100ms ease-out'))
```

可以在转换中定义临时的样式，转换结束后不保留：

```typescript
transition('inactive => active', [
  style({
    backgroundColor: '#cfd8dc',
    transform: 'scale(1.3)'
  }),
  animate('80ms ease-in', style({
    backgroundColor: '#eee',
    transform: 'scale(1)'
  }))
]),
```

### `*` 状态

在转换定义中用来匹配任何状态：

+ `active => *` 转换在当元素的状态从 `active` 变成其它任何状态时应用
+ `* => *` 转换在发生任何状态变化时都应用


### `void` 状态

用来指定元素未关联到视图时的状态（未加入或已删除时），对定义进入或离开时的动画有用。例如 `* => void` 转换可应用在元素离开视图时，而 `void => *` 是进入时应用。

`*` 状态也能匹配 `void` 状态。

例子：

```typescript
//hero-list-enter-leave.component.ts (excerpt)
animations: [
  trigger('flyInOut', [
    state('in', style({transform: 'translateX(0)'})),
    transition('void => *', [
      style({transform: 'translateX(-100%)'}),
      animate(100)
    ]),
    transition('* => void', [
      animate(100, style({transform: 'translateX(100%)'}))
    ])
  ])
]
```

进入来离开动态很常用，故有如下简写法：

```
transition(':enter', [ ... ]); // void => *
transition(':leave', [ ... ]); // * => void
```

## Animatable 属性和单位

包括 position, size, transform, color, border 等，见 [a list of animatable properties](https://www.w3.org/TR/css3-transitions/#animatable-properties)。

有数字值的属性，可以加单位后缀，如 `50px`, `3em`, `100%`，如果没有指定单位时，默认为 `px`，如 `50` 变成 `50px`。


## 自动属性值计算

不知道确切值的属性值用 `*` 表示，能自动计算出来，如下例中高度从当前大小变为 0：

```typescript
//src/app/hero-list-auto.component.ts
animations: [
  trigger('shrinkOut', [
    state('in', style({height: '*'})),
    transition('* => void', [
      style({height: '*'}),
      animate(250, style({height: 0}))
    ])
  ])
]
```

## 动画时间配置

每个转换定义中有 3 个时间配置属性： duration, delay, easing function

### 持续时间 duration

控制动态从开始到结束的总时间，有 3 种格式：

+ 纯数字，单位是毫秒： 如 100
+ 毫秒字符串，如： '100ms'
+ 秒字符串，如: '0.1s'

### 延迟开始的时间 delay

格式同 duration，写在 duration 后，例如延迟 100ms 后再运行 200ms 的动画：  `0.2s 100ms`。

## Easing

[easing function](http://easings.net/) 控制运行中的如何加速和减速。它写成最后，例如： `0.2s 100ms ease-out`。


## 用 keyframes 实现多步动画

keyframes 动画在进行两组状态的转换过程中会经历多个中间状态。对于每个 keyframe，都要指定一个介于 0(动画的开始时间）和 1（动画的结束时间）的偏移量 offset。

下面是在用 keyframes 实现 bounce 效果的例子：

```typescript
//hero-list-multistep.component.ts (excerpt)
animations: [
  trigger('flyInOut', [
    state('in', style({transform: 'translateX(0)'})),
    transition('void => *', [
      animate(300, keyframes([
        style({opacity: 0, transform: 'translateX(-100%)', offset: 0}),
        style({opacity: 1, transform: 'translateX(15px)',  offset: 0.3}),
        style({opacity: 1, transform: 'translateX(0)',     offset: 1.0})
      ]))
    ]),
    transition('* => void', [
      animate(300, keyframes([
        style({opacity: 1, transform: 'translateX(0)',     offset: 0}),
        style({opacity: 1, transform: 'translateX(-15px)', offset: 0.7}),
        style({opacity: 0, transform: 'translateX(100%)',  offset: 1.0})
      ]))
    ])
  ])
]
```

offset 就是动画时间点，如果没有指定，会平均分配后指定，例如当 3 个 keyframe 时，相应会是 0, 0.5 和 1。


## 并行动画组

将多个转换定义（有不同的时间配置）合并时一组，那么动画中的不同转换会并行同时运行在同一个元素上。例如：

```typescript
//hero-list-groups.component.ts (excerpt)
animations: [
  trigger('flyInOut', [
    state('in', style({width: 120, transform: 'translateX(0)', opacity: 1})),
    transition('void => *', [
      style({width: 10, transform: 'translateX(50px)', opacity: 0}),
      group([
        animate('0.3s 0.1s ease', style({
          transform: 'translateX(0)',
          width: 120
        })),
        animate('0.3s ease', style({
          opacity: 1
        }))
      ])
    ]),
    transition('* => void', [
      group([
        animate('0.3s ease', style({
          transform: 'translateX(50px)',
          width: 10
        })),
        animate('0.3s 0.2s ease', style({
          opacity: 0
        }))
      ])
    ])
  ])
]
```

## 动画回调函数

可以绑定动画的开始和结束的回调函数。

例如对于名为 `@flyInOut` 的动画，绑定如下：

```typescript
//hero-list-multistep.component.ts (excerpt)
 content_copy
template: `
  <ul>
    <li *ngFor="let hero of heroes"
        (@flyInOut.start)="animationStarted($event)"
        (@flyInOut.done)="animationDone($event)"
        [@flyInOut]="'in'">
      {{hero.name}}
    </li>
  </ul>
`,
```

回调函数会接收到一个 `AnimationEvent` 对象，包含 `fromState`, `toState`, `totalTime` 等有用属性。

## 参考

+ https://angular.io/guide/animations
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_animations.ipynb)
