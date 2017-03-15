---
title: Angular2 的表单功能
date: 2017-03-15
writing-time: 2017-03-15 15:47
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2 form JSONPlaceholder
---

# 表单很重要也很复杂

它复杂是因为：

+ 表单输入框即是用来修改页面数据，又要用来修改服务端数据
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
// FormControl 表示一个输入域，是 Angular 表单中的最小单元。
let nameControl = new FormControl("Nate"); //创建一个值为 "Nate" 的 FormControl 对象
let name = nameControl.value; // -> Nate
// FormControl 封装了输入项的值，状态（如是否有效，是否有修改等）及错误信息。
nameControl.errors // -> StringMap<string, any> of errors
nameControl.dirty // -> false
nameControl.valid // -> true


// FormGroup
// 多数表单会有多个输入域。FormGroup 可以将表单中的多个 FormControl 对象封装起来。
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

# 制作首个表单

首先加载相关的 form 库。

```typescript
import {  // 加载 form 的相应模块
  FormsModule,
  ReactiveFormsModule
} from '@angular/forms';

// ...

@NgModule({
  declarations: [
    //...
  ],
  // 将 FormsModule 和 ReactiveFormsModule 加入本应用的依赖中，
  // 从而确保我们在模板中可以使用下列的指令：
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

```typescript
import { Component } from '@angular/core';

// 该组件显示一个提交 SKU 的表单
@Component({
  selector: 'demo-form-sku',

  // 由于已在 @NgModule 中增加了 FormsModule 依赖，现可以在模板中使用 NgForm。
  // Angular 2 中任何指令，一旦应用到视图中时，它们都会与视图中和指令的选择子
  // 匹配的所有元素关联。由于 NgForm 指令的选择子有 form 标签，这意味着：
  // 当将 `FormsModule` 导入后， `NgForm` 指令将自动关联到视图中的所有 form 标签。
  // NgForm 提供了 2 个重要功能：
  //    1. 一个名为 ngForm 的 FormGroup 对象
  //    2. 一个 (ngSubmit) 输出
  // 下面的模板中，通过 `#f="ngForm"`，实现将表单中由 NgForm 指令自动生成的名为 ngForm 
  // 的 FormGroup 对象，创建一个本地别名变量 f。
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



续

# 参考 

+ [Forms in Angular 2](https://www.ng-book.com/2/)
