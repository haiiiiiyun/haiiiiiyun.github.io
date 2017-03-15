---
title: Angular2 内置指令
date: 2017-03-14
writing-time: 2017-03-14 22:22
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

内置指令都是自动导入到我们的组件中的，因此可以在组件中直接使用。

```html
{% raw %}
<!-- ngIf -->
<!-- 该指令用于基于条件显示或隐藏元素 -->
<div *ngIf="false"></div>  <!-- 永远不会显示 -->
<div *ngIf="a &gt; b"></div>  <!-- 当 a 大于 b 时会显示-->
<div *ngIf="str == 'yes'"></div> <!-- 当 str 值为 'yes' 时显示-->
<div *ngIf="myFunc()"></div> <!-- 当 myFunc() 返回为 true 时显示-->


<!-- ngSwitch -->
<!-- 该指令用于基于给定条件呈现不同的元素，从而能避免使用多个 ngIf -->
<div class="container" [ngSwitch]="myVar">
    <div *ngSwitchCase="'A'">Var is A</div>
    <div *ngSwitchCase="'B'">Var is B</div>
    <div *ngSwitchCase="'A'">Var is second A</div> <!-- 可以对同一个值做多次判断-->
    <div *ngSwitchDefault>Var is something else</div>
</div>


<!-- ngStyle -->
<!-- 用 Angular 表达式设置 DOM 元素的 CSS 属性 -->
<!-- 使用该指令的最简单方式是通过 [style.cssproperty]="value" 设置，例如：-->
<div [style.background-color="'yellow'">
    Uses fixed yellow background
</div>

<!-- [ngStyle] 可以使用键值对来设置多个 CSS 属性，如：-->
<div [ngStyle]="{color: 'white', 'background-color': 'blue'}">
    Uses fixed white text on blue background
</div> <!-- ngStyle 的参数是一个键值对 JavaScript 对象，因此这里的 background-color 由于有一个 '-' 不是一个有效的键值，需要用 'background-color' 表示，而 color 是一个有效的键值，故不需要用 'color' 表示 -->

<!-- NgStyle 指令也可以使用动态值，例如，下面的例子中定义了输入颜色和字符大小的输入框及一个 apply 按钮，-->
<div class="ui input">
  <input type="text" name="color" value="{{color}}" #colorinput>
</div>
<div class="ui input">
  <input type="text" name="fontSize" value="{{fontSize}}" #fontinput>
</div>
<button class="ui primary button" (click)="apply(colorinput.value, fontinput.value)">
    Apply settings
</button>
<!-- 当点击按钮后，会调用组件中的 apply 方法，并更新组件中的 fontSize 和 color 属性值，从而下面模板中, 由于绑定了组件的 color 和 fontSize，会自动更新-->
<span [ngStyle]="{color: color}" [style.font-size.px]="fontSize">text</span>
<!-- 这里 font-size 的设置还需要设置相应的单位，参照上面的例子，还能设置 [style.font-size.em], [style.font-size.%] 等值-->


<!-- ngClass -->
<!-- 该指令能动态地设置或修改 DOM 元素的类 -->
<!-- 第一种用法是传入一个键值对，键是类名，而值为 true/false，true 时表示添加该类，false 时表示删除该类-->
<div [ngClass]="{bordered: false}">不会有 bordered 类</div>
<div [ngClass]="{bordered: true}">有 bordered 类</div>
<!-- 也可以使用组件的属性值达到动态设置的效果-->
<div [ngClass]="{bordered: isBordered}">
    Border {{ isBordered ? "ON": "OFF" }}
</div>

<!-- 键值对对象也可以定义在组件中，
export class SampleApp {
  classesObj: Object;
}
然后直接使用 classesObj: -->
<div [ngClass]="classesObj">
    Border {{ classesObj.bordered ? "ON": "OFF" }}
</div>

<!-- 如果参数是数组，则表示将这些类全部添加 -->
<div class="base" [ngClass]="['blue', 'round']">
    always have a blue and round class
</div>
<!-- 或者在组件中定义数组： this.classList = ['blue', 'round']，然后这样使用： -->
<div class="base" [ngClass]="classList">
  This is {{ classList.indexOf('blue') &lt; -1 ? "": "NOT" }} blue
  and {{ classList.indexOf('round') &lt; -1 ? "": "NOT" }} round
</div>


<!-- ngFor -->
<!-- 该指令会重复生成特定的 DOM 元素，每次都从数组中取出一个值传入 -->
<!-- 假设组件中设置了属性 this.cities = ['Miami', 'Sao Paulo', 'New York']; -->
<div class="ui list">
    <div class="item" *ngFor="let c of cities; let idx=index">
      {{ idx }}:{{ c }}
    </div>
</div>
<!-- 输出为：-->
<div class="ui list">
    <div class="item">0:Miami</div>
    <div class="item">1:Sao Paulo</div>
    <div class="item">2:New York</div>
</div>


<!-- ngNonBindable -->
<!-- 一般模板中有 {{ var }} 时会自动解析扩展出该变量的值，而用该指令后，使得 Angular 不会对里面的这种表示法进行解析，而按原样输出。-->
<span class="pre" ngNonBindable>
  This is what {{ content }} rendered
</span>
{% endraw %}
```

# 参考 

+ [Built-in Directives](https://www.ng-book.com/2/)
