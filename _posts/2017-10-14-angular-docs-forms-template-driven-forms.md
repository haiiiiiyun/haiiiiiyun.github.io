---
title: Angular docs-表单-模板驱动的表单
date: 2017-10-14
writing-time: 2017-10-14
categories: programming
tags: angular node Angular&nbsp;docs
---

# 模板驱动的表单

即在模板中使用表单相关的指令及技术直接创建表单。


下面以创建一个个人信息表单为例，说明表单创建过程，流程有：

1. 创建数据模型类 Hero
2. 创建控制表单的组件
3. 创建包含表单初始布局的模板
4. 使用 ngModel 将数据属性和各表单控件双向绑定
5. 为每个表单输入控件添加 name 属性
6. 添加自定义 CSS 来提供视觉反馈
7. 显示和隐藏验证失败消息
8. 使用 ngSubmit 使用表单提交
9. 在表单数据有效性验证通过前，使提交按钮不可用


## 创建  Hero 数据模型类


```typescript
//src/app/hero.ts
export class Hero {

  constructor(
    public id: number,
    public name: string,
    public power: string,
    public alterEgo?: string
  ) {  }

}
```

第 4 个类属性 alterEgo 带有 `?`，因此是可选的，可以不必传入。

使用如下:

```typescript
//src/app/hero-form.component.ts (SkyDog)
let myHero =  new Hero(42, 'SkyDog',
                       'Fetch any object at any distance',
                       'Leslie Rollover');
console.log('My hero is called ' + myHero.name); // "My hero is called SkyDog"
```

## 创建表单组件

```typescript
//src/app/hero-form.component.ts (v1)
import { Component } from '@angular/core';

import { Hero }    from './hero';

@Component({
  selector: 'hero-form',
  templateUrl: './hero-form.component.html'
})
export class HeroFormComponent {

  powers = ['Really Smart', 'Super Flexible',
            'Super Hot', 'Weather Changer'];

  model = new Hero(18, 'Dr IQ', this.powers[0], 'Chuck Overstreet');

  submitted = false;

  onSubmit() { this.submitted = true; }

  // TODO: Remove this when we're done
  get diagnostic() { return JSON.stringify(this.model); }
}
```

其中的 `diagnostic()` 方法可用于调试。


### 重构 app.module.ts，加载表单相关的模块和指令


```typescript
//src/app/app.module.ts
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent }  from './app.component';
import { HeroFormComponent } from './hero-form.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule
  ],
  declarations: [
    AppComponent,
    HeroFormComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

### 创建根组件 app.component.ts

```typescript
//src/app/app.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: '<hero-form></hero-form>'
})
export class AppComponent { }
```

### 创建一个初始化的 HTML 表单模板

```html
<!--src/app/hero-form.component.html-->
<div class="container">
    <h1>Hero Form</h1>
    <form>
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" class="form-control" id="name" required>
      </div>

      <div class="form-group">
        <label for="alterEgo">Alter Ego</label>
        <input type="text" class="form-control" id="alterEgo">
      </div>
      
      <div class="form-group">
          <label for="power">Hero Power</label>
          <select class="form-control" id="power" required>
            <option *ngFor="let pow of powers" [value]="pow">{{pow}}</option>
          </select>
        </div>

      <button type="submit" class="btn btn-success">Submit</button>

    </form>
</div>
```

在模板驱动的表单中，如果已经导入了 `FormsModule`，那么无需对 `<form>` 标签做任何处理，就能使用 `FormsModule` 中的指令和功能了。


## 通过 ngModel 进行双向数据绑定


为 `<input>` 标签添加双向绑定，例如：

```typescript
//src/app/hero-form.component.html (excerpt)
<input type="text" class="form-control" id="name"
       required
       [(ngModel)]="model.name" name="name">
```

为 `<form>` 标签设置一个模板变量：

```html
<!--src/app/hero-form.component.html (excerpt)-->
<form #heroForm="ngForm">
```

这时，`heroForm` 变量将指向 `NgForm` 指令（不是 form 元素），用来管理整个表单。

使用模板驱动的表单时，Angular 自动为每个 `<form>` 标签创建并关联一个 `NgForm` 指令，该指令中包含了所有通过 `ngModel` 指令创建的表单控制及其 `name` 属性，监测它们的属性变量，管理它们的有效性;同时，它自身的 `valid` 属性，只有当其包含的全部控制都有效时，值才为真。

在通过 `ngModel` 绑定 `<input>` 控件时，为其设置 `name` 属性值是必要的。因此 Angular 会自动创建一个相应的 `FormControl` 实例，并以对应 `<input>` 中的 `name` 属性值为 key 登记到 `NgForm` 指令中。


全部绑定后如下：

```html
<!--src/app/hero-form.component.html (excerpt)-->
{{diagnostic}}
<div class="form-group">
  <label for="name">Name</label>
  <input type="text" class="form-control" id="name"
         required
         [(ngModel)]="model.name" name="name">
</div>

<div class="form-group">
  <label for="alterEgo">Alter Ego</label>
  <input type="text"  class="form-control" id="alterEgo"
         [(ngModel)]="model.alterEgo" name="alterEgo">
</div>

<div class="form-group">
  <label for="power">Hero Power</label>
  <select class="form-control"  id="power"
          required
          [(ngModel)]="model.power" name="power">
    <option *ngFor="let pow of powers" [value]="pow">{{pow}}</option>
  </select>
</div>
```

## 通过 ngModel 跟踪控件的状态和有效性

表单控制通过 ngModel 双向绑定后，NgModel 指令还会跟踪控件的状态和有效性，并通过更新当前控制中的 CSS 类来反映，下面是各状态下对应的 CSS 类：

状态            |为真时的类   |为假时的类
--------------|
控件有被访问过   | `ng-touched` | `ng-untouched`
控件中的值已修改 | `ng-dirty`    | `ng-pristine`   
控件中的值有效   | `ng-valid`    | `ng-invalid`


## 添加定制 CSS 来提供可视化反馈

为上节中的各 `ng-*` CSS 创建相关 CSS 定义来实现。例如效果为：

![可视化反馈](/assets/images/angular-docs/validity-required-indicator.png)

对应的 CSS 定义为：

```css
/*src/forms.css*/
.ng-valid[required], .ng-valid.required  {
  border-left: 5px solid #42A948; /* green */
}

.ng-invalid:not(form)  {
  border-left: 5px solid #a94442; /* red */
}
```

## 显示和隐藏验证错误消息

例如当用户删除用户名控件中的值时，会：

！[显示验证错误消息](/assets/images/angular-docs/name-required-error.png)

实现如下：

+ 为对应 input 标签添加模板引用变量
+ "Name is required" 消息放在附近的 `<div>` 中，只当必要时显示

例如：

```html
<!--src/app/hero-form.component.html (excerpt)-->
<label for="name">Name</label>
<input type="text" class="form-control" id="name"
       required
       [(ngModel)]="model.name" name="name"
       #name="ngModel">
<div [hidden]="name.valid || name.pristine"
     class="alert alert-danger">
  Name is required
</div>
```

上例中通过 `#name="ngModel"` 创建的模板引用变量可用来访问该控件。每个指令的实现中都有一个 `exportAs` 属性，用来指定该指令用在引用变量赋值时的名字，而 `ngModel` 指令的 `exportAs` 属性也正好是 `ngModel`。

而错误消息的显示和隐藏则通过对 `<div>` 的 `hidden` 属性进行绑定实现。

通过调用 `heroForm.reset()` 可以重围表单及其内控件的全部状态信息。


## 通过 ngSubmit 提交表单

将表单的 `ngSubmit` 事件属性绑定到组件的 `onSubmit()` 方法：

```html
<!--src/app/hero-form.component.html (ngSubmit)-->
<form (ngSubmit)="onSubmit()" #heroForm="ngForm">
```

提交按钮只有在表单数据有效时才能使用：

```html
<!--src/app/hero-form.component.html (submit-button)-->
<button type="submit" class="btn btn-success" [disabled]="!heroForm.form.valid">Submit</button>
```


### 提交后隐藏区块

组件中设置一个 `submitted` 属性，将需隐藏区域的 `hidden` 属性进行绑定：

```html
<!--src/app/hero-form.component.html (excerpt)-->
<div [hidden]="submitted">
  <h1>Hero Form</h1>
  <form (ngSubmit)="onSubmit()" #heroForm="ngForm">

     <!-- ... all of the form ... -->

  </form>
</div>
```

当将 `submitted` 值设置为 `false` 后，又会显示出来。

## 参考

+ https://angular.io/guide/forms
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/forms_template_driven_forms.ipynb)
