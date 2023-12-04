---
title: Angular docs-教程 2： Master/Detail
date: 2017-06-11
writing-time: 2017-08-17
categories: programming
tags: angular node Angular&nbsp;docs
---


# 教程 2： Master/Detail

## 显示 hero 列表

先创建一个 Hero 对象数组：

```typescript
//src/app/app.component.ts (hero array)
const HEROES: Hero[] = [
  { id: 11, name: 'Mr. Nice' },
  { id: 12, name: 'Narco' },
  { id: 13, name: 'Bombasto' },
  { id: 14, name: 'Celeritas' },
  { id: 15, name: 'Magneta' },
  { id: 16, name: 'RubberMan' },
  { id: 17, name: 'Dynama' },
  { id: 18, name: 'Dr IQ' },
  { id: 19, name: 'Magma' },
  { id: 20, name: 'Tornado' }
];
```

`HEROES` 数组是 `Hero` 类型的。

### 导出 heroes

在 `AppComponent` 中创建一个公共属性 heroes，从而实现导出，用于数据绑定。

```typescript
//app.component.ts (hero array property)
heroes = HEROES;
```

这里属性 `heroes` 无需声明类型，TypeScript 会自动根据 HEROES 设置。

## 在模块中显示多个 hero 名

```typescript
//app.component.ts (heroes template)
<h2>My Heroes</h2>
<ul class="heroes">
  <li>
    <!-- each hero goes here -->
  </li>
</ul>
```

### 使用 ngFor 遍历

目的是实现将组件中的 heroes 属性绑定到模板，遍历并显示每个名字。

修改 `<li>` 标签，添加内置的 `*ngFor` 指令：

```typescript
//app.component.ts (ngFor)
<li *ngFor="let hero of heroes">
```

`ngFor` 的 `*` 前缀是语法的关键部分，它表示 `<li>` 元素及其子元素构成了一个 master template。

`ngFor` 指令遍历组件中的 `heroes` 属性（数组），为数组中的每个 hero 实例呈现该 master template 的内容。

`let hero` 实现将每次遍历出的实例保存为模板的输入变量 `hero`，从而可在模块中引用该变量。

在 `<li>` 标签中，引用 `hero` 变量：

```typescript
//app.component.ts (ngFor template)
<li *ngFor="let hero of heroes">
  <span class="badge">{{hero.id}}</span> {{hero.name}}
</li>
```

## 添加样式

在组件的 `@Component` 装饰器中，设置 `styles` 属性，为本组件添加样式信息。

```typescript
//src/app/app.component.ts (styles)
styles: [`
  .selected {
    background-color: #CFD8DC !important;
    color: white;
  }
  .heroes {
    margin: 0 0 2em 0;
    list-style-type: none;
    padding: 0;
    width: 15em;
  }
  .heroes li {
    cursor: pointer;
    position: relative;
    left: 0;
    background-color: #EEE;
    margin: .5em;
    padding: .3em 0;
    height: 1.6em;
    border-radius: 4px;
  }
  .heroes li.selected:hover {
    background-color: #BBD8DC !important;
    color: white;
  }
  .heroes li:hover {
    color: #607D8B;
    background-color: #DDD;
    left: .1em;
  }
  .heroes .text {
    position: relative;
    top: -3px;
  }
  .heroes .badge {
    display: inline-block;
    font-size: small;
    color: white;
    padding: 0.8em 0.7em 0 0.7em;
    background-color: #607D8B;
    line-height: 1em;
    position: relative;
    left: -1px;
    top: -4px;
    height: 1.8em;
    margin-right: .8em;
    border-radius: 4px 0 0 4px;
  }
`]
```

这些样式信息也可以保存在独立的文件中。

在模板中添加样式信息：

```typescript
//src/app/app.component.ts (styled heroes)
<h2>My Heroes</h2>
<ul class="heroes">
  <li *ngFor="let hero of heroes">
    <span class="badge">{{hero.id}}</span> {{hero.name}}
  </li>
</ul>
```

## 选择一个 hero

将 hero 列表和详情视图关联起来，当用户从列表中选中一个 hero 时，该选中的 hero 信息应该显示在详情视图中。

这种 UI 模式叫 "master/detail"。这里 master 是 hero 列表，detail 是选中的 hero。

### 处理click 事件

将 click 事件绑定到 `<li>` 中：

```typescript
//app.component.ts (template excerpt)
<li *ngFor="let hero of heroes" (click)="onSelect(hero)">
  ...
</li>
```

在标签到使用 `(event)` 语法进行事件绑定，这里实现了：当在 li 上点击时，会调用组件中定义的 `onSelect()` 方法，并传入模板中的 `hero` 变量作为参数值。

### 导出选中的 hero

现在组件中不再需要 `hero` 属性了，而是需要一个 `selectedHero` 属性用来保存选中的 hero:

```typescript
//src/app/app.component.ts (selectedHero)
selectedHero: Hero;
```

组件的 `onSelect()` 方法将设置选中的 hero:

```typescript
//src/app/app.component.ts (onSelect)
onSelect(hero: Hero): void {
  this.selectedHero = hero;
}
```

模板中也同步更新 selectedHero:

```typescript
//app.component.ts (template excerpt)
<h2>{{selectedHero.name}} details!</h2>
<div><label>id: </label>{{selectedHero.id}}</div>
<div>
    <label>name: </label>
    <input [(ngModel)]="selectedHero.name" placeholder="name"/>
</div>
```

此时保存后，编译会出现异常，因为 `selectedHero` 的值未定义，从而在模板中无法引用 `selectedHero.name`。

可以用内置的 `ngIf` 指令判断是否有选中的 hero:

```typescript
//src/app/app.component.ts (ngIf)
<div *ngIf="selectedHero">
  <h2>{{selectedHero.name}} details!</h2>
  <div><label>id: </label>{{selectedHero.id}}</div>
  <div>
    <label>name: </label>
    <input [(ngModel)]="selectedHero.name" placeholder="name"/>
  </div>
</div>
```

### 为选中的 hero 添加样式

将 `[class.selected]` 绑定到 li 上：

```typescript
//app.component.ts (setting the CSS class)
<li *ngFor="let hero of heroes"
  [class.selected]="hero === selectedHero"
  (click)="onSelect(hero)">
  <span class="badge">{{hero.id}}</span> {{hero.name}}
</li>
```

这里，当 `hero === selectedHero` 时，Angular 会为 li 添加 `selected` 类。

## 参考

+ https://angular.io/tutorial/toh-pt2
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/tutorial_2_master_and_detail.ipynb)
