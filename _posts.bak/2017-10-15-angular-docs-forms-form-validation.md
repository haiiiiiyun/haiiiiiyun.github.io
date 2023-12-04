---
title: Angular docs-表单-表单验证
date: 2017-10-15
writing-time: 2017-10-15
categories: programming
tags: angular node Angular&nbsp;docs
---

# 表单验证


## 模板驱动表单的验证

添加验证器跟在本地 HTML 表单中添加验证器是一样的。Angular 用指令将这些验证器属性匹配成框架中的验证器函数。

每当表单控件中的值有修改时，Angular 将运行验证器，生成一组验证错误信息（使控件的状态为 `INVALID`），或生成 `null`（控件的状态为 `VALID`）。

通过将控件的 `ngModel` 导出为一个本地模板变量，可通过该变量查看控件的状态：

```
<!--template/hero-form-template.component.html (name)-->
<input id="name" name="name" class="form-control"
       required minlength="4" forbiddenName="bob"
       [(ngModel)]="hero.name" #name="ngModel" >

<div *ngIf="name.invalid && (name.dirty || name.touched)"
     class="alert alert-danger">

  <div *ngIf="name.errors.required">
    Name is required.
  </div>
  <div *ngIf="name.errors.minlength">
    Name must be at least 4 characters long.
  </div>
  <div *ngIf="name.errors.forbiddenName">
    Name cannot be Bob.
  </div>

</div>
```

`<input>` 以普通属性的形式（`required`, `minlength`, 及自定义验证器指令 `forbiddenName`) 来添加验证器。


## Reactive 表单的验证

可直接在组件类中的表单控件模型中添加。


## 验证函数

共有 2 种：

+ 同步型验证函数接收一个控件实例为参数，立即返回，要么返回一组验证错误，要么返回 `null`。它能作为第 2 个参数传给 `FormControl`。
+ 异步型验证函数接收一个控件实例为参数，返回 Promise 或 Observable，之后再触发返回一组验证错误或 `null`。能作为第 3 个参数传给 `FormControl`。


为性能的原因，只有全部同步型验证函数通过后才会运行异步型验证函数。每个函数都必须运行完成后才能设置错误。

## 内置验证器

见 [Validators](https://angular.io/api/forms/Validators)。

这些验证器都定义在 `Validators` 类中。使用在模板驱动的表单中时，直接使用其名字，而使用时 reactive 表单中时，使用时函数形式，如 `Validators.required`：

```typescript
//reactive/hero-form-reactive.component.ts (validator functions)
ngOnInit(): void {
  this.heroForm = new FormGroup({
    'name': new FormControl(this.hero.name, [
      Validators.required,
      Validators.minLength(4),
      forbiddenNameValidator(/bob/i) // <-- Here's how you pass in the custom validator.
    ]),
    'alterEgo': new FormControl(this.hero.alterEgo),
    'power': new FormControl(this.hero.power, Validators.required)
  });
}

get name() { return this.heroForm.get('name'); }

get power() { return this.heroForm.get('power'); }
```


## 自定义验证器

```typescript
//shared/forbidden-name.directive.ts (forbiddenNameValidator)
/** A hero's name can't match the given regular expression */
export function forbiddenNameValidator(nameRe: RegExp): ValidatorFn {
  return (control: AbstractControl): {[key: string]: any} => {
    const forbidden = nameRe.test(control.value);
    return forbidden ? {'forbiddenName': {value: control.value}} : null;
  };
}
```

这个函数实际是一个工厂函数，它返回一个 Validator 函数。

### 添加到 Reactive 表单

只需简单地将函数添加入即可：

```typescript
//reactive/hero-form-reactive.component.ts (validator functions)
this.heroForm = new FormGroup({
  'name': new FormControl(this.hero.name, [
    Validators.required,
    Validators.minLength(4),
    forbiddenNameValidator(/bob/i) // <-- Here's how you pass in the custom validator.
  ]),
  'alterEgo': new FormControl(this.hero.alterEgo),
  'power': new FormControl(this.hero.power, Validators.required)
});
```

### 添加到模板驱动型表单

模板中需要以指令的形式进行添加，故用 `ForbiddenValidatorDirective` 指令来包装 `forbiddenNameValidator` 验证器。

```typescript
//shared/forbidden-name.directive.ts (directive)
@Directive({
  selector: '[forbiddenName]',
  providers: [{provide: NG_VALIDATORS, useExisting: ForbiddenValidatorDirective, multi: true}]
})
export class ForbiddenValidatorDirective implements Validator {
  @Input() forbiddenName: string;

  validate(control: AbstractControl): {[key: string]: any} {
    return this.forbiddenName ? forbiddenNameValidator(new RegExp(this.forbiddenName, 'i'))(control)
                              : null;
  }
}
```

该指令实现了 `Validator` 接口，从而能与表单进行整合。指令通过将它自身登记为 `NG_VALIDATORS` 的提供者，从而在验证进程中，Angular 能识别出该指令的角色。

之后，在模板中，直接用指令的选择子进行添加：

```html
<input id="name" name="name" class="form-control"
       required minlength="4" forbiddenName="bob"
       [(ngModel)]="hero.name" #name="ngModel" >
```


## 控件状态的 CSS 类

Angular 会自动将控件中的许多属性以 CSS 类的形式反映到表单控件上。当前支持的 CSS 类有：

+ `.ng-valid`
+ `.ng-invalid`
+ `.ng-pending`
+ `.ng-pristine`
+ `.ng-dirty`
+ `.ng-untouched`
+ `.ng-touched`


下面是根据状态 CSS 设置不能边框颜色的例子：

```css
.ng-valid[required], .ng-valid.required  {
  border-left: 5px solid #42A948; /* green */
}

.ng-invalid:not(form)  {
  border-left: 5px solid #a94442; /* red */
}
```

## 参考

+ https://angular.io/guide/form-validation
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/forms_form_validation.ipynb)
