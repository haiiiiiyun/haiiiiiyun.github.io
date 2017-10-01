---
title: Angular docs-模板与数据绑定-组件交互
date: 2017-10-01
writing-time: 2017-09-30
categories: programming
tags: angular node Angular&nbsp;docs
---

# 组件交互


## 数据从父组件通过 `input` 绑定传向子组件

子组件中的输入属性 (input properties) 使用 `@Input` 登记。


## 输入属性可用 getter 和 setter 方法

可以在 setter 中对父组件传入的值进行处理：

```typescript
//component-interaction/src/app/name-child.component.ts
import { Component, Input } from '@angular/core';

@Component({
  selector: 'name-child',
  template: '<h3>"{{name}}"</h3>'
})
export class NameChildComponent {
  private _name = '';

  @Input()
  set name(name: string) {
    this._name = (name && name.trim()) || '<no name set>';
  }

  get name(): string { return this._name; }
}
```

## 输入属性值的每次更新可以在 ngOnChanges 中检测到

例如：

```typescript
//component-interaction/src/app/version-child.component.ts
import { Component, Input, OnChanges, SimpleChange } from '@angular/core';

@Component({
  selector: 'version-child',
  template: `
    <h3>Version {{major}}.{{minor}}</h3>
    <h4>Change log:</h4>
    <ul>
      <li *ngFor="let change of changeLog">{{change}}</li>
    </ul>
  `
})
export class VersionChildComponent implements OnChanges {
  @Input() major: number;
  @Input() minor: number;
  changeLog: string[] = [];

  ngOnChanges(changes: {[propKey: string]: SimpleChange}) {
    let log: string[] = [];
    for (let propName in changes) {
      let changedProp = changes[propName];
      let to = JSON.stringify(changedProp.currentValue);
      if (changedProp.isFirstChange()) {
        log.push(`Initial value of ${propName} set to ${to}`);
      } else {
        let from = JSON.stringify(changedProp.previousValue);
        log.push(`${propName} changed from ${from} to ${to}`);
      }
    }
    this.changeLog.push(log.join(', '));
  }
}
```

## 父组件侦听子组件中的事件

子组件中的输出属性(output property）是一个用 `@Output` 装饰的 `EventEmitter` 变量。

## 父组件通过模板引用变量与子组件交互

在父组件模板中，为子组件定义一个模板引用变量，通过该变量调用子组件中的属性和方法。


## 父组件代码中通过  @ViewChild() 获取子组件，并与其交互

上面通过模板引用变量的方式，只能用在模板中，要在父组件的类代码中获取子组件，只能通过 `@ViewChild` 装饰器获取。例如：

```typescript
//component-interaction/src/app/countdown-parent.component.ts
import { AfterViewInit, ViewChild } from '@angular/core';
import { Component }                from '@angular/core';
import { CountdownTimerComponent }  from './countdown-timer.component';

@Component({
  selector: 'countdown-parent-vc',
  template: `
  <h3>Countdown to Liftoff (via ViewChild)</h3>
  <button (click)="start()">Start</button>
  <button (click)="stop()">Stop</button>
  <div class="seconds">{{ seconds() }}</div>
  <countdown-timer></countdown-timer>
  `,
  styleUrls: ['demo.css']
})
export class CountdownViewChildParentComponent implements AfterViewInit {

  @ViewChild(CountdownTimerComponent)
  private timerComponent: CountdownTimerComponent;

  seconds() { return 0; }

  ngAfterViewInit() {
    // Redefine `seconds()` to get from the `CountdownTimerComponent.seconds` ...
    // but wait a tick first to avoid one-time devMode
    // unidirectional-data-flow-violation error
    setTimeout(() => this.seconds = () => this.timerComponent.seconds, 0);
  }

  start() { this.timerComponent.start(); }
  stop() { this.timerComponent.stop(); }
}
```

## 父子组件通过服务来交互


父子共享一个服务，通过服务来双向通讯。

## 参考

+ https://angular.io/guide/component-interaction
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_component_interaction.ipynb)
