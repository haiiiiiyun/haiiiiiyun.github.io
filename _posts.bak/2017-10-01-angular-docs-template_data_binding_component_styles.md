---
title: Angular docs-模板与数据绑定-组件样式
date: 2017-10-01
writing-time: 2017-10-01
categories: programming
tags: angular node Angular&nbsp;docs
---


所有的 CSS 知识都可以应用到 Angular 的应用中。此外，Angular 还可以将样式信息只应用于特定的组件，进行模块化管理。

## 使用组件样式

```typescript
//src/app/hero-app.component.ts
@Component({
  selector: 'hero-app',
  template: `
    <h1>Tour of Heroes</h1>
    <hero-app-main [hero]=hero></hero-app-main>`,
  styles: ['h1 { font-weight: normal; }']
})
export class HeroAppComponent {
/* . . . */
}
```

在组件 metadata 的 `styles` 属性中指定的 CSS 样式及其选择子，作用域只为该组件模板，因此不存在名字冲突等问题。


## 特殊选择子

基于 [shadow DOM style scoping](https://www.w3.org/TR/css-scoping-1) 的，组件样式都一些特殊的选择子。


###  :host

`:host` 伪类选择子用来选择托管（包含）该组件的元素，可以解理为组件的直接父元素。例如：

```css
:host {
  display: block;
  border: 1px solid black;
}
```

使用函数形式可以按条件应用样式，例如：

```css
:host(.active) {
  border-width: 3px;
}
```

即当直接父元素上有 `.active` 类时才应用。

### ：host-context

`:host-context()` 伪类选择子用来条件判断本组件的所有父元素（从直接父元素一直到 body 元素）是否条件某条件。适合用来基于组件外的全局基础样式来设置本组件的样式，例如：

```css
:host-context(.theme-light) h2 {
  background-color: #eef;
}
```

表示当本组件的某父元素中有 `.theme-light` 类时，则这样设置本组件中的 `h2` 的背景颜色。


## 加载组件样式

+ 在 metadata 中的 `styles` 设置
+ 在 metadata 中的 `styleUrls` 中设置，URL 相对于 `index.html` 文件所有位置
+ 组件模板中直接使用 `<style>` 来内联 CSS
+ 组件模板中直接使用嵌入 `<link>` 来联入 CSS，URL 相对位置同 styleUrls
+ 用到的 CSS 文件中也都支持使用 CSS imports


## 视图封装

组件 CSS 样式将封装成一个组件视图，不影响应用的其它部分。

视图封装模式 (view encapsulation mode) 可以在组件的 metadata 中设置，用来控制封装模式：

+ `Native` 模式使用浏览器的本地 [shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM) 来实现，只能在支持的浏览器上可选用。
+ `Emulated` 模式（默认）模拟 shadow DOM 行为。
+ `None` 模式不封装，添加的样式相同的全局样式。

封装模式通过 metadata 中的 `encapsulation` 属性设置：

```typescript
// warning: few browsers support shadow DOM encapsulation at this time
encapsulation: ViewEncapsulation.Native
```

## 参考

+ https://angular.io/guide/component-styles
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/template_data_binding_component_styles.ipynb)
