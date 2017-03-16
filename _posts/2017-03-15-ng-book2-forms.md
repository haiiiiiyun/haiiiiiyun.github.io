---
title: Angular2 的表单功能
date: 2017-03-15
writing-time: 2017-03-15 15:47--2017-03-16 16:18
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2 form JSONPlaceholder
---

# 表单很重要也很复杂

它复杂是因为：

+ 表单输入项即是用来修改页面数据，又要用来修改服务端数据
+ 修改后通常要在页面的某处反映出来
+ 用户输入时会很随意，故还要进行输入验证
+ UI 还要清楚地显示异常和错误
+ 相关的输入项间可能会有复杂的逻辑
+ 还要不依赖 DOM 选择子，能够对表单进行测试


Angular 2 中用于处理表单的工具有：

+ FormControl: 将表单中的输入项封装成一个对象
+ Validator: 用于验证输入数据
+ Observer: 使我们能监测表单的修改情况并相应作出回应


# FormControl 和 FormGroup

```typescript
// FormControl
// FormControl 表示一个输入项，是 Angular 表单中的最小单元。
let nameControl = new FormControl("Nate"); //创建一个值为 "Nate" 的 FormControl 对象
let name = nameControl.value; // -> Nate
// FormControl 封装了输入项的值，状态（如是否有效，是否有修改等）及错误信息。
nameControl.errors // -> StringMap<string, any> of errors
nameControl.dirty // -> false
nameControl.valid // -> true

// FormGroup
// 多数表单会有多个输入项。FormGroup 可以将表单中的多个 FormControl 对象封装起来。
// 由于 FormControl 和 FormGroup 都继承着 AbstractControl，因此有相同的接口：
let personInfo = new FormGroup({
    firstName: new FormControl("Nate"),
    lastName: new FormControl("Murray"),
    zip: new FormControl("90210")
});
personInfo.value; // -> {
                  //       firstName: "Nate",
                  //       lastName: "Murray",
                  //       zip: "90210",
                  //    }
personInfo.errors // -> StringMap<string, any> of errors
personInfo.dirty // -> false
personInfo.valid // -> true
```

# 制作表单

## 导入 form 库
首先加载相关的 form 库。

```typescript
import {  // 加载 form 的相关模块
  FormsModule,
  ReactiveFormsModule
} from '@angular/forms';

// ...

@NgModule({
  declarations: [
    //...
  ],
  // 将 FormsModule 和 ReactiveFormsModule 加入本应用的依赖中，
  // 从而确保我们在模板中可以使用下列指令：
  //    + ngModel 和 NgForm （来自 FormsModule）
  //    + formControl 和 ngFormGroup （来自 ReactiveFormsModule）
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule
  ],
  bootstrap: [ FormsDemoApp ]
})
class FormsDemoAppModule {}
```

## 使用 ngForm 和 ngModule

```typescript
import { Component } from '@angular/core';

// 该组件显示一个提交 SKU 的表单
@Component({
  selector: 'demo-form-sku',

  // 由于已在 @NgModule 中增加了 FormsModule 依赖，现可以在模板中使用 NgForm 指令。
  // Angular 2 中的任何指令，一旦应用到视图中时，它们都会与视图中和指令的选择子
  // 匹配的所有元素关联。由于 NgForm 指令的选择子有 form 标签，这意味着：
  // 当将 `FormsModule` 导入后， `NgForm` 指令将自动关联到视图中的所有 form 标签。
  // NgForm 提供了 2 个重要功能：
  //    1. 一个名为 ngForm 的 FormGroup 对象
  //    2. 一个 (ngSubmit) 输出
  // 下面的模板中，通过 `#f="ngForm"`，实现将表单中由 NgForm 指令自动生成的名为 ngForm 
  // 的 FormGroup 对象，赋给一个本地别名变量 f。
  // 而 (ngSubmit) 也是来自 NgForm 指令，其回调函数的参数是 f.value，由于 f 是一个 FormGroup
  // 对象，因此 f.value 是一个键值对。
  //
  // NgModel 指令的选择子有 ngModel，因此，只要在 input 标签中加入 `ngModel="whatever"` 等属性时，该指令就会与此 input 关联。
  // 下面模板中添加的 ngModel 属性没有属性值，表示其属性值和 input 的 name 值相等，即也是 "sku"
  // 当在 input 上加个一个无属性值的 ngModel 属性时，表示：
  //   1. 建立一个单向数据绑定
  //   2. 根据该 input 的 name 值，创建一个同名的 FormControl 对象
  // 由 ngModel 创建的 FormControl 对象会自动添加到父 FormGroup 对象中（本例中 f），
  // 并将 DOM 元素也和新建的该 FormControl 对象绑定。
  template: `
  <div class="ui raised segment">
    <h2 class="ui header">Demo Form: Sku</h2>
    <form #f="ngForm"
          (ngSubmit)="onSubmit(f.value)"
          class="ui form">

      <div class="field">
        <label for="skuInput">SKU</label>
        <input type="text"
               id="skuInput"
               placeholder="SKU"
               name="sku" ngModel>
      </div>

      <button type="submit" class="ui button">Submit</button>
    </form>
  </div>
  `
})
export class DemoFormSku {
  onSubmit(form: any): void {
    console.log('you submitted value:', form);
  }
}
```

## 使用 FormBuilder

```typescript
// 使用 ngForm 和 ngControl 隐含地创建 FormControl 和 FormGroup 虽然方便，
// 但是不能进行过多设置。
// FormBuilder 是一种更加灵活的配置表单的方式。
// FormBuilder 类似于工厂对象(factory)，可以用来创建 FormControl 和 FormGroup。
import { Component } from '@angular/core';
import { // 导入这些类，以便在模板中使用 formGroup 和 formControl 指令。
  FormBuilder,
  FormGroup
} from '@angular/forms';

// 在上例中，因为导入了 FormsModule，所以 ngForm 会自动关联到每一个 form 标签，
// 并为它们创建各自的 FormGroup 对象。
//
// 本例中，我们不想让 ngForm 为我们创建 FormGroup 对象，需要使用自己通过
// FormBuilder 创建的 myForm 对象。
// 只需 '<form [formGroup]="myForm"`，即将 formGroup 指令添加到 form 标签上即可。
// 这是因为 ngForm 的选择子实际是 `form:not([ngNotForm]):not([formGroup]),ngForm,[ngForm]`，
// 因此，当 form 标签上加上 [formGroup] 或 [ngNotForm] 等属性后，ngForm 指令不会
// 应用到这些表单上。
//
// 绑定 FormControl 到 input 标签： `[formControl]="myForm.controls['sku']"`。
// 使用了 formControl 指令，同时，访问 FormGroup 对象中的 FormControl 对象，
// 用了 myForm.controls['sku']。
@Component({
  selector: 'demo-form-sku-builder',
  template: `
  <div class="ui raised segment">
    <h2 class="ui header">Demo Form: Sku with Builder</h2>
    <form [formGroup]="myForm" 
          (ngSubmit)="onSubmit(myForm.value)"
          class="ui form">

      <div class="field">
        <label for="skuInput">SKU</label>
        <input type="text" 
               id="skuInput" 
               placeholder="SKU"
               [formControl]="myForm.controls['sku']">
      </div>

    <button type="submit" class="ui button">Submit</button>
    </form>
  </div>
  `
})
export class DemoFormSkuBuilder {
  myForm: FormGroup;

  // 通过在构造器中加入该参数，从而注入(inject)了 FormBuilder
  // 在注入过程中，会创建一个 FormBuilder 实例，并赋给 fb 变量。
  // FormBuilder 中有两个主要函数：
  //   + control: 用于创建 FormControl
  //   + group: 用于创建 FormGroup
  constructor(fb: FormBuilder) {
    // 创建的 FormGroup 实例存储在组件属性 myForm 中。
    // 同时，该 FormGroup 实例中只有一个 FormControl 对象 'sku', 其值为 'ABC123'。
    // 这里创建 FormControl 的参数是一个数组，这是因为还可以添加 Validator 等参数。
    this.myForm = fb.group({
      'sku': ['ABC123']
    });
  }

  onSubmit(value: string): void {
    console.log('you submitted value: ', value);
  }
}
```

## 添加验证功能

```typescript
/* tslint:disable:no-string-literal */
import { Component } from '@angular/core';

// 验证器由 Validators 模块提供，最简单的验证器是 Validators.required。
// 要使用验证器，需：
//   1. 将一个验证器赋给一个 FormControl 对象
//   2. 在视图中检查验证器的状态，然后进行相关操作
//   
//  将验证器赋给 FormControl 对象，只需将验证器作为第 2 个参数
//  传入 FormControl 构造器即可，如：
//      let control = new FormControl('sku', Validators.required);
//  或者在用 FormBuilder 创建 FormControl 时，作为参数数组的第 2 个值传入，如：
//      this.myForm = fb.group({'sku':  ['', Validators.required] });
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl
} from '@angular/forms';

// 验证器在模板中使用，主要关注 4 个方面：
// 1. 检查整个表单的有效性，并显示相应消息
// 2. 检查单个项的有效性，并显示相应消息
// 3. 检查单个项的有效性，无效时设置该项颜色为红色
// 4. 检查单个项的某个特定要求，不满足时显示相应消息
@Component({
  selector: 'demo-form-with-validations-explicit',
  template: `
  <div class="ui raised segment">
    <h2 class="ui header">Demo Form: with validations (explicit)</h2>
    <form [formGroup]="myForm"
          (ngSubmit)="onSubmit(myForm.value)"
          class="ui form">

      <!-- 4. 检查单个项的某个特定要求，不满足时显示相应消息 
          当无效时，添加 error class。同时 sku.touched 确保
          只有在用户操作（如输入后再删除）过后才显示。
      -->
      <div class="field"
          [class.error]="!sku.valid && sku.touched">
        <label for="skuInput">SKU</label>
        <input type="text"
               id="skuInput"
               placeholder="SKU"
               [formControl]="sku">

         <!-- 2. 检查单个项的有效性，并显示相应消息 -->
         <div *ngIf="!sku.valid"
           class="ui error message">SKU is invalid</div>

         <!-- 4. 检查单个项的某个特定要求，不满足时显示相应消息 
              当然也可以通过 FormGroup 对象来检查，如：
              *ngIf="myForm.hasError('required', 'sku')"，它和
              下面的效果等同
         -->
         <div *ngIf="sku.hasError('required')"
           class="ui error message">SKU is required</div>
      </div>

      <!-- 1. 检查整个表单的有效性，并显示相应消息 -->
      <div *ngIf="!myForm.valid"
        class="ui error message">Form is invalid</div>

      <button type="submit" class="ui button">Submit</button>
    </form>
  </div>
  `
})
export class DemoFormWithValidationsExplicit {
  myForm: FormGroup;
  sku: AbstractControl;

  constructor(fb: FormBuilder) {
    this.myForm = fb.group({
      'sku':  ['', Validators.required] // 同时将一个验证器赋给新建的 FormControl
    });

    // 这里将创建的 FormControl 对象抽取出来存放在组件属性 sku 中 (AbstractControl 类型),
    // 从而可以在模板中直接访问
    this.sku = this.myForm.controls['sku'];
  }

  onSubmit(value: string): void {
    console.log('you submitted value: ', value);
  }
}
```

上面的例子中，将 FormControl 对象保存为了组件的属性 sku，如果 FormControl 对象较多，则为每一个都创建一个相应的组件属性会较麻烦。此时可直接通过 FormControl 的 controls 访问，如 myForm.controls['sku']。


## 自定义验证器

```typescript
// 下面是 Angular Validators.required 验证器的实现源码：
export class Validators {
    static required(c: FormControl): StringMap<string, boolean> {
        return isBlank(c.value) || c.value == "" ? {"required": true} : null;
    }
}
// 可见，一个验证器：有一个 FormControl 类型的参数作为输入，返回是一个 StringMap<string, boolean> 对象。

// 为 sku 开发一个验证器，假设 sku 都以 '123' 开头：
function skuValidator(control: FormControl): { [s: string]: boolean } {
    if (!control.value.match(/^123/)) {
        return {invalidSku: true};
    }
}

// 将多个验证器赋给同一个 FormControl
// 需要通过 Validators.compose 将多个验证器合并成一个，再赋值，如：
constructor(fb: FormBuilder) {
    this.myForm = fb.group({
      'sku':  ['', Validators.compose([ Validators.required, skuValidator])]
});
```


## 侦测表单修改

```typescript
// 每个 FormGroup 和 FormControl 对象都有 EventEmitter 这个观察者模式的对象，
// 我们可以通过该 EventEmitter 对表单或表单项进行修改情况的侦听。
// 对表单项 FormControl 的监听需要：
//   1. 通过 control.valueChanges 获取 EventEmitter 对象
//   2. 使用 `.subscribe` 添加观察者
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl
} from '@angular/forms';

@Component({
  selector: 'demo-form-with-events',
  template: `
  <div class="ui raised segment">
    <h2 class="ui header">Demo Form: with events</h2>
    <form [formGroup]="myForm"
          (ngSubmit)="onSubmit(myForm.value)"
          class="ui form">

      <div class="field"
          [class.error]="!sku.valid && sku.touched">
        <label for="skuInput">SKU</label>
        <input type="text"
               class="form-control"
               id="skuInput"
               placeholder="SKU"
               [formControl]="sku">
         <div *ngIf="!sku.valid"
           class="ui error message">SKU is invalid</div>
         <div *ngIf="sku.hasError('required')"
           class="ui error message">SKU is required</div>
      </div>

      <div *ngIf="!myForm.valid"
        class="ui error message">Form is invalid</div>

      <button type="submit" class="ui button">Submit</button>
    </form>
  </div>
  `
})
export class DemoFormWithEvents {
  myForm: FormGroup;
  sku: AbstractControl;

  constructor(fb: FormBuilder) {
    this.myForm = fb.group({
      'sku':  ['', Validators.required]
    });

    this.sku = this.myForm.controls['sku'];

    // 对单个表单项 FormControl 的修改情况进行侦听
    this.sku.valueChanges.subscribe(
      (value: string) => {
        console.log('sku changed to:', value);
      }
    );

    // 对整个表单 FormGroup 的修改情况进行侦听
    this.myForm.valueChanges.subscribe(
      (form: any) => {
        console.log('form changed to:', form);
      }
    );

  }

  onSubmit(form: any): void {
    console.log('you submitted value:', form.sku);
  }
}

// 当输入 'kj' 时，console 中会看到：
// sku changed to: k
// form changed to: Object {sku: "k"}
// sku changed to: kj
// form changed to: Object {sku: "kj"}
```

## 使用 ngModel 进行双向数据绑定

```typescript
// ngModel 指令用于将数据模型绑定到表单中。
// Angular 2 中的数据流一般是单向的（自上而下），
// 但是 ngModel 指令实现的是双向绑定。
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators
} from '@angular/forms';

@Component({
  selector: 'demo-form-ng-model',
  template: `
  <div class="ui raised segment">
    <h2 class="ui header">Demo Form: with ng-model</h2>

    <div class="ui info message">
      The product name is: {{productName}}
    </div>

    <form [formGroup]="myForm"
          (ngSubmit)="onSubmit(myForm.value)"
          class="ui form">

      <div class="field">
        <label for="productNameInput">Product Name</label>
        <!--
        由于 [] 表示输入，而 () 表示输出，
        这里 [(ngModel)] 很容易看出是双向绑定，
        实现将该 input 项的值与组件属性 productName 的值进行同步绑定
        -->
        <input type="text"
               id="productNameInput"
               placeholder="Product Name"
               [formControl]="myForm.get('productName')"
               [(ngModel)]="productName">
      </div>

      <div *ngIf="!myForm.valid"
        class="ui error message">Form is invalid</div>
      <button type="submit" class="ui button">Submit</button>
    </form>

  </div>
  `
})
export class DemoFormNgModel {
  myForm: FormGroup;
  productName: string;

  constructor(fb: FormBuilder) {
    this.myForm = fb.group({
      'productName':  ['', Validators.required]
    });
  }

  onSubmit(value: string): void {
    console.log('you submitted value: ', value);
  }
}
```


# 参考 

+ [Forms in Angular 2](https://www.ng-book.com/2/)
