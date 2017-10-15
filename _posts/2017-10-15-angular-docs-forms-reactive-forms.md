---
title: Angular docs-表单-Reactive 表单
date: 2017-10-14
writing-time: 2017-10-14
categories: programming
tags: angular node Angular&nbsp;docs
---


Reactive forms 是用 reactive 风格创建表单的一种技术。

Reactive forms 和 template-driven forms 是 Angular 中创建表单的 2 种技术。它们都位于 `@angular/forms` 库，共享一组通用的表单控件类。它们在理念、编程风格上有区别。它们有不同的模块名： `ReactiveFormsModule` 和 `FormsModule`。

## Reactive 表单

Reactive 编码风格偏好显式管理数据流：即管理非 UI 的数据模型（data model, 通常从服务端获取）和 UI 的表单模型 (form model) 间的数据流，而表单模型可用来保存屏幕上 HTML 控件的值和状态。同时 reactive forms 提供了使用 reactive 模式、测试和验证的使用方法。

使用 reactive forms 时，我们在组件中先创建 Angular 表单控件对象树，再在模板中将它们绑定到表单元素上。

直接在组件类中创建和处理表单控件对象。由于组件类可直接访问数据模型和表单控件结构，我们可以将数据模板的值推送到表单控件中，也能抽回用户修改的值。组件能观测到表单控件的状态并作出响应。

直接操作表单控件对象的一个好处是：值和有效性的更新 [总是同步的并且在你的控制下](https://angular.io/guide/reactive-forms#async-vs-sync)，从而不会碰到模板驱动的表单中的时间点的问题，因此，reactive forms 的单元测试也更加容易。

按照 reactive 范式，组件会保持数据模型的不变性，只将它作为一个纯粹的数值源。组件不直接更新数据模型，它先将用户的修改抽取出来，转发给外部组件或服务，外部组件或服务进行处理后（例如进行保存）将返回一个新的数据模型，组件将返回的新数据模型用来更新数据模型。

## 模板驱动的表单

将 HTML 表单控制（如 `<input>`) 放在组件模板中，使用 `ngModel` 将它们绑定到组件的数据模型的属性上。

我们不直接创建 Angular 表单控件对象，Angular 基于数据绑定信息为我们自动创建。我们不抽取的推送数据值，Angular 通过 `ngModel` 进行处理。当有修改时，Angular 更新那个可修改的数据模型。

因此，`ngModle` 指令不存在于 `ReactiveFormsModule`。


## 异步 vs. 同步

reactive 表单是同步的，模板驱动的表单是异步的。

在 reactive 表单中，我们直接创建整个表单控件对象树，因此可以更新所有控件数据。

而模板驱动的表单中，表单控件的创建是由指令进行的。为避免 "changed after checked" 错误，这些指令都要花费多一个周期来创建整个控件树，即必须等待一个 tick 后才能在组件类中处理控件。

例如，如果用 `@ViewChild(NgForm)` 语句来获取注入的表单控件，并在 `ngAfterViewInit` 挂钩中检查，我们会发现组件没有该子对象。必须等待一个 tick( 使用 `setTimeout`) 后，才能访问该控件。

模板驱动表单的异步性也使单元测试很复杂。必须将测试块包装在 `async()` 或 `fakeAsync()` 中来避免表单还不可用的问题。


# 下面以例子说明


## 创建数据模型

```typescript
//src/app/data-model.ts
export class Hero {
  id = 0;
  name = '';
  addresses: Address[];
}

export class Address {
  street = '';
  city   = '';
  state  = '';
  zip    = '';
}

export const heroes: Hero[] = [
  {
    id: 1,
    name: 'Whirlwind',
    addresses: [
      {street: '123 Main',  city: 'Anywhere', state: 'CA',  zip: '94801'},
      {street: '456 Maple', city: 'Somewhere', state: 'VA', zip: '23226'},
    ]
  },
  {
    id: 2,
    name: 'Bombastic',
    addresses: [
      {street: '789 Elm',  city: 'Smallville', state: 'OH',  zip: '04501'},
    ]
  },
  {
    id: 3,
    name: 'Magneta',
    addresses: [ ]
  },
];

export const states = ['CA', 'MD', 'OH', 'VA'];
```


## 创建 reactive forms 的组件


```typescript
//src/app/hero-detail.component.ts
import { Component }              from '@angular/core';
import { FormControl }            from '@angular/forms';

@Component({
  selector: 'hero-detail',
  templateUrl: './hero-detail.component.html'
})

export class HeroDetailComponent1 {
  name = new FormControl();
}
```

`FormControl` 是一个指令，可用来创建和管理 `FormControl` 实例，实例将绑定到模板中的 `<input>` 上。其构造器接收 3 个可选参数：初始值，一组验证器，另一个异步验证器。

## 创建模板

```html
<!--src/app/hero-detail.component.html-->
<h2>Hero Detail</h2>
<h3><i>Just a FormControl</i></h3>
<label class="center-block">Name:
  <input class="form-control" [formControl]="name">
</label>
```

使用 `[formControl]="name"` 将 input 元素绑定到组件中的一个名为 name 的 `FormControl` 实例属性。


## 导入 ReactiveFormsModule

```typescript
//src/app/app.module.ts (excerpt)
import { NgModule }            from '@angular/core';
import { BrowserModule }       from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';  // <-- #1 import module

import { AppComponent }        from './app.component';
import { HeroDetailComponent } from './hero-detail.component'; // <-- #1 import component

@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule // <-- #2 add to @NgModule imports
  ],
  declarations: [
    AppComponent,
    HeroDetailComponent, // <-- #3 declare app component
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## 核心的表单类

+ [AbstractControl](https://angular.io/api/forms/AbstractControl) 是 3 个具体表单控制类 `FormControl`, `FormGroup`, `FormArray` 的抽象基类。它提供它们的通用行为和属性，有些是可 observalbe 的。
+ [FormControl](https://angular.io/api/forms/FormControl) 用来跟踪单个表单控件的值和有效性状态。它对应于一个 HTML 表单控件。
+ [FormGroup](https://angular.io/api/forms/FormGroup) 用来跟踪一组 `AbstractControl` 实例的值和有效性状态。组属性中包含它的所有子控件。组件中的顶层表单就是一个 `FormGroup`。
+ [FormArray](https://angular.io/api/forms/FormArray) 用来跟踪一组用数字索引的 `AbstractControl` 实例的值和有效性状态。

## 添加一个 FormGroup

如果有多个 `FormControl` 的话，通常将它们登记在一个父 `FormGroup` 下：

```typescript
//src/app/hero-detail.component.ts
import { Component }              from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

export class HeroDetailComponent2 {
  heroForm = new FormGroup ({
    name: new FormControl()
  });
}
```

同步更新模板中的绑定方式：

```html
<!--src/app/hero-detail.component.html-->
<h2>Hero Detail</h2>
<h3><i>FormControl in a FormGroup</i></h3>
<form [formGroup]="heroForm" novalidate>
  <div class="form-group">
    <label class="center-block">Name:
      <input class="form-control" formControlName="name">
    </label>
  </div>
</form>
```

+ `<form>` 元素中的 `novalidate` 属性避免浏览器使用本地的 HTML 验证。
+ `formGroup` 是一个 reactive forms 中的指令，它将当前表单关联到一个 `FormGoup` 实例。
+ `<form>` 中的 `<input>` 使用 `fromControlName="name"` 绑定，它将绑定到父 `FormGroup` 实例中的一个名为 `name` 的控件实例。


### 查看表单的数据模型

```html
<!--src/app/hero-detail.component.html-->
<p>Form value: {{ heroForm.value | json }}</p>
<p>Form status: {{ heroForm.status | json }}</p>
```

`heroForm.value` 返回表单的数据模型。


## 使用 FormBuilder 来创建和维护复杂的表单

```typescript
//src/app/hero-detail.component.ts (excerpt)
import { Component }              from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

export class HeroDetailComponent3 {
  heroForm: FormGroup; // <--- heroForm is of type FormGroup

  constructor(private fb: FormBuilder) { // <--- inject FormBuilder
    this.createForm();
  }

  createForm() {
    this.heroForm = this.fb.group({
      name: '', // <--- the FormControl called "name"
    });
  }
}
```

+ 先声明 heroForm 属性为 FormGroup
+ 将 FormBuilder 注入到构造器
+ FormBuilder.group 是一个能创建 FormGroup 实例的工厂函数，接收的参数是一个键值对对象，用来定义 FormControl 的名字和定义。本例中， `name` 控件的初始值被设置为 ''


## 使用 Validator.required 验证器

```typescript
//src/app/hero-detail.component.ts (excerpt)
import { Component }                          from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

//...
this.heroForm = this.fb.group({
  name: ['', Validators.required ],
});
```

+ 这里 `name` 控件的定义体是一个数组，有 2 元素分别是：初始值，验证器
+ Reactive 验证器都是简单的，可组合的函数。使用 `Validators.required` 后，`heroForm.status` 的值可为 `"INVALID"` 或 `"VALID"`。


## 更多 FormControl

添加 address 等，address 还有 state 属性，需要使用 `<select>` 来实现选择：

```typescript
//src/app/hero-detail.component.ts (excerpt)
import { Component }                          from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { states } from './data-model';

//...
export class HeroDetailComponent4 {
  heroForm: FormGroup;
  states = states;

  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  createForm() {
    this.heroForm = this.fb.group({
      name: ['', Validators.required ],
      street: '',
      city: '',
      state: '',
      zip: '',
      power: '',
      sidekick: ''
    });
  }
}
```

在模板中绑定：

```html
<!--src/app/hero-detail.component.html-->
<h2>Hero Detail</h2>
<h3><i>A FormGroup with multiple FormControls</i></h3>
<form [formGroup]="heroForm" novalidate>
  <div class="form-group">
    <label class="center-block">Name:
      <input class="form-control" formControlName="name">
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">Street:
      <input class="form-control" formControlName="street">
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">City:
      <input class="form-control" formControlName="city">
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">State:
      <select class="form-control" formControlName="state">
          <option *ngFor="let state of states" [value]="state">{{state}}</option>
      </select>
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">Zip Code:
      <input class="form-control" formControlName="zip">
    </label>
  </div>
  <div class="form-group radio">
    <h4>Super power:</h4>
    <label class="center-block"><input type="radio" formControlName="power" value="flight">Flight</label>
    <label class="center-block"><input type="radio" formControlName="power" value="x-ray vision">X-ray vision</label>
    <label class="center-block"><input type="radio" formControlName="power" value="strength">Strength</label>
  </div>
  <div class="checkbox">
    <label class="center-block">
      <input type="checkbox" formControlName="sidekick">I have a sidekick.
    </label>
  </div>
</form>


<p>Form value: {{ heroForm.value | json }}</p>
```

## 嵌套的 FormGroup

可将 street, city 等地址相关的控件组合成一个名为 address的 `FormGroup`，这样可以对这组控件的状态和有效性进行集中跟踪。

之前用 `FormBuilder.group` 为表单创建了一个 FormGroup，现可再用 `group` 创建嵌套的 `FormGroup`：

```typescript
//src/app/hero-detail.component.ts (excerpt)
export class HeroDetailComponent5 {
  heroForm: FormGroup;
  states = states;

  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  createForm() {
    this.heroForm = this.fb.group({ // <-- the parent FormGroup
      name: ['', Validators.required ],
      address: this.fb.group({ // <-- the child FormGroup
        street: '',
        city: '',
        state: '',
        zip: ''
      }),
      power: '',
      sidekick: ''
    });
  }
}
```

在模板中绑定时，将创建一个 `<div>` 来包围所有地址控件，其 `formGroupName` 绑定到 `address`（从而创建了一个类型 FormGroup 的父对象），再在 `<div>` 内部声明各控件，并通过 `formControlName` 进行绑定（相对于其直接父对象）：

```typescript
//src/app/hero-detail.component.html (excerpt)
<div formGroupName="address" class="well well-lg">
  <h4>Secret Lair</h4>
  <div class="form-group">
    <label class="center-block">Street:
      <input class="form-control" formControlName="street">
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">City:
      <input class="form-control" formControlName="city">
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">State:
      <select class="form-control" formControlName="state">
        <option *ngFor="let state of states" [value]="state">{{state}}</option>
      </select>
    </label>
  </div>
  <div class="form-group">
    <label class="center-block">Zip Code:
      <input class="form-control" formControlName="zip">
    </label>
  </div>
</div>
```

## FormControl 属性研究

在 `FormGroup` 对象中，可直接用 `get()` 来获取其包含的 `FormControl` 实例，例如：

```html
<p>Name value: {{ heroForm.get('name').value }}</p>
<p>Street value: {{ heroForm.get('address.street').value}}</p>
```

`FormControl` 有如下属性：

属性名            | 描述
:----------------|:------
`obj.value`      | 控件的值
`obj.status`     | 控件的状态值，有 `VALID`, `INVALID`, `PENDING`, `DISABLED`。
`obj.pristine`   | 当用户没有进行修改时为真，与 `obj.dirty` 相反
`obj.untouched`  | 当用户没有使用过该控件时为真，与 `obj.touched` 相反


## 数据模型和表单模型

数据模型（本例是 `hero`)一般从服务端获取。 `FormControl` 树就是表单模型。

组件必须将数据模型中的 hero 值复制到表单模型中。需注意 2 点：

1. 必须理解数据模型中的属性是如何映射到表单模型中的属性上的
2. 用户的修改从 DOM 元素流向表单模型，而不是到数据模型。表单控件不可能会修改数据模型。

表单和数据模型结果无需完全匹配，我们一般只在特定页面上显示数据模型中的一个子块。

本例中，数据模型和表单模型非常相似，如下：

```typescript
//src/app/data-model.ts (classes)
export class Hero {
  id = 0;
  name = '';
  addresses: Address[];
}

export class Address {
  street = '';
  city   = '';
  state  = '';
  zip    = '';
}
```

```typescript
//src/app/hero-detail.component.ts (excerpt)
this.heroForm = this.fb.group({
  name: ['', Validators.required ],
  address: this.fb.group({
    street: '',
    city: '',
    state: '',
    zip: ''
  }),
  power: '',
  sidekick: ''
});
```

为简洁起见，重构表单模型为：

```typescript
//src/app/hero-detail-7.component.ts
this.heroForm = this.fb.group({
  name: ['', Validators.required ],
  address: this.fb.group(new Address()), // <-- a FormGroup with a new address
  power: '',
  sidekick: ''
});
```

## 通过 setValue 和 patchValue 为表单模型设置值

### setValue

参数是一个键值对，键值对中的结构（个数、名字）必须与表单模型完全匹配，不然会出错并返回错误消息，例如：

```typescript
this.heroForm.setValue({
  name:    this.hero.name,
  address: this.hero.addresses[0] || new Address()
});
```

### patchValue

只需传入感兴趣的控件设置信息，如：

```typescript
this.heroForm.patchValue({
  name: this.hero.name
});
```

## 何时设置表单模型的值 (ngOnChanges)

当组件获取到数据模型值时即要更新表单模型的值。

本例中 `HeroDetailComponent` 嵌套在一个 master/detail 的 `HeroListComponent` 中。当用户点击列表中的一个 hero 时，会将选中的 hero 通过属性绑定传给 `HeroDetailComponent`：

```html
<!--hero-list.component.html (simplified)-->
<nav>
  <a *ngFor="let hero of heroes | async" (click)="select(hero)">{{hero.name}}</a>
</nav>

<div *ngIf="selectedHero">
  <hero-detail [hero]="selectedHero"></hero-detail>
</div>
```

每当用户选中一个新 hero 时 `HeroDetailComponent` 中的 `hero` 即有修改，会触发 `ngOnChanges` 挂钩调用，因此可在组件的 `ngOnChanges` 挂钩中使用 `setValue` 来更新表单模型值：

```typescript
//src/app/hero-detail.component.ts (core imports)
import { Component, Input, OnChanges }             from '@angular/core';

//src/app/hero-detail-6.component.ts
@Input() hero: Hero;

//src/app/hero-detail.component.ts (ngOnchanges)
ngOnChanges()
  this.heroForm.setValue({
    name:    this.hero.name,
    address: this.hero.addresses[0] || new Address()
  });
}
```

## 重置表单状态

选中的 hero 修改后应重置表单，将控件值清空，状态重置为 *pristine*，可在 `ngOnChanges` 中首行调用 `this.heroForm.reset()` 实现。

而 `reset()` 和 `setValue()` 也可以合并为如下：

```typescript
//src/app/hero-detail.component.ts (ngOnchanges - revised)
ngOnChanges() {
  this.heroForm.reset({
    name: this.hero.name,
    address: this.hero.addresses[0] || new Address()
  });
}
```

## 使用 FormArray 来表示一组 FormGroup

`FormGroup` 可以嵌套 `FormControl` 和 `FormGroup`，而 `FormArray` 能表示一组 `FormGroup`。

本例中 `address` 是一个 `FormGroup`，而 hero 有多个地址，可用 `FormArray`  表示（重命名为 secretLaires)：

```typescript
//src/app/hero-detail-8.component.ts
this.heroForm = this.fb.group({
  name: ['', Validators.required ],
  secretLairs: this.fb.array([]), // <-- secretLairs as an empty FormArray
  power: '',
  sidekick: ''
});
```


### 初始化 FormArray "secretLairs"


```typescript
//src/app/hero-detail-8.component.ts
setAddresses(addresses: Address[]) {
  const addressFGs = addresses.map(address => this.fb.group(address));
  const addressFormArray = this.fb.array(addressFGs);
  this.heroForm.setControl('secretLairs', addressFormArray);
}
```

`FormGroup.setControl()` 方法用来替换原来的 `FormArray` 实例。


### 获取 FormArray

```typescript
//src/app/hero-detail.component.ts (secretLayers property)
get secretLairs(): FormArray {
  return this.heroForm.get('secretLairs') as FormArray;
};
```

### 显示 FormArray

使用 `*ngFor` 来迭代显示，有如下关键点：

+ 添加一层 `<div>`，应用 `*ngFor`，设置 `formArrayName` 指令为 `"secretLairs"`，从而将该 `FormArray` 实例设置为内部模板中的表单控件的上下文。
+ 迭代的是 `FormArray.controls`，而不是 `FormArray` 实例本身，每个 `control` 就是一个 address `FormGroup`。
+ 每个迭代的 `FormGroup` 需要一个唯一的 `formGroupName`，其值就是该 `FormGroup` 在 `FormArray` 中的索引值。

```html
<!--src/app/hero-detail.component.html (excerpt)-->
<div formArrayName="secretLairs" class="well well-lg">
  <div *ngFor="let address of secretLairs.controls; let i=index" [formGroupName]="i" >
    <!-- The repeated address template -->
    <h4>Address #{{i + 1}}</h4>
    <div style="margin-left: 1em;">
      <div class="form-group">
        <label class="center-block">Street:
          <input class="form-control" formControlName="street">
        </label>
      </div>
      <div class="form-group">
        <label class="center-block">City:
          <input class="form-control" formControlName="city">
        </label>
      </div>
      <div class="form-group">
        <label class="center-block">State:
          <select class="form-control" formControlName="state">
            <option *ngFor="let state of states" [value]="state">{{state}}</option>
          </select>
        </label>
      </div>
      <div class="form-group">
        <label class="center-block">Zip Code:
          <input class="form-control" formControlName="zip">
        </label>
      </div>
    </div>
    <br>
    <!-- End of the repeated address template -->
  </div>
</div>
```

### 为 FormArray 添加新元素

```typescript
//src/app/hero-detail.component.ts (addLair method)
addLair() {
  this.secretLairs.push(this.fb.group(new Address()));
}
```

### 观测控件的修改

`ngOnChanges` 无法观测到 hero 中名字，secret lairs 值的修改情况。

不过每个 `FormControl` 中的 `valueChanges` 属性，会返回 RxJS `Observable`，可以进行订阅，从而观测到控件的修改情况：

```typescript
//src/app/hero-detail.component.ts (logNameChange)
nameChangeLog: string[] = [];
logNameChange() {
  const nameControl = this.heroForm.get('name');
  nameControl.valueChanges.forEach(
    (value: string) => this.nameChangeLog.push(value)
  );
}

//Call it in the constructor, after creating the form.
//src/app/hero-detail-8.component.ts
constructor(private fb: FormBuilder) {
  this.createForm();
  this.logNameChange();
}
```


## 保存表单数据


### 保存

当点击提交时，先根据原数据模型中的数据和当前表单模型中的数据（用深度复制的方法）准备好要提交的数据; 提交更新，完成后设置新的数据模型数据；最后调用 `ngOnChanges()` 刷新表单模型数据：

```typescript
//src/app/hero-detail.component.ts (onSubmit)
onSubmit() {
  this.hero = this.prepareSaveHero();
  this.heroService.updateHero(this.hero).subscribe(/* error handling */);
  this.ngOnChanges();
}

//src/app/hero-detail.component.ts (prepareSaveHero)
prepareSaveHero(): Hero {
  const formModel = this.heroForm.value;

  // deep copy of form model lairs
  const secretLairsDeepCopy: Address[] = formModel.secretLairs.map(
    (address: Address) => Object.assign({}, address)
  );

  // return new `Hero` object containing a combination of original hero value(s)
  // and deep copies of changed form model values
  const saveHero: Hero = {
    id: this.hero.id,
    name: formModel.name as string,
    // addresses: formModel.secretLairs // <-- bad!
    addresses: secretLairsDeepCopy
  };
  return saveHero;
}
```


### 撤销修改

由于当表单模型数据修改后，数据模型不会自动修改，故只有调用 `ngOnChanges()` 恢复表单模型数据即可：

```typescript
//src/app/hero-detail.component.ts (revert)
revert() { this.ngOnChanges(); }
```

## 参考

+ https://angular.io/guide/reactive-forms
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/forms_reactive_forms.ipynb)
