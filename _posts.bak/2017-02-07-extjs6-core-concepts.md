---
title: ExtJS 6 核心概念
date: 2017-02-07
writing-time: 2017-02-07 10:02--2017-02-08 12:00
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

# 类系统

Ext 提供了很多用于创建和使用类的辅助函数。

Ext JS 6 的类系统中有以下类：

+ Ext
+ Ext.Base
+ Ext.Class
+ Ext.ClassManager
+ Ext.Loader


## Ext

`Ext` 是一个全局的 singleton 对象，它封闭了所有类、singleton、工具函数等。它包含了许多常用的工具函数，同时也为位于其它类中的常用函数创建了快捷方式。

### Ext.application

`Ext.application` 用于初始化应用。该函数会加载 `Ext.app.Application` 类，并在页面加载后启动应用。

`Ext.app.Application` 类表示整个的应用，举例如下：

```javascript
Ext.application({
    name: 'MyApp',
    extend: 'MyApp.Application',
    launch: function() {
    }
});
```

### Ext.define

用于创建或重载一个类。

形式为 `Ext.define(name, data, callback)`：

+ name: 类名
+ data: 应用到该类的属性
+ callback: 一个可选函数，在类创建后会调用


例如，定义一个 Car 类如下：

```javascript
Ext.define('Car', {
    name: null,
    constructor: function(name){
        if (name){
            this.name = name;
        }
    },
    start: function(){
        alert('Car started');
    }
});
```

通过 `define` 来扩展一个类：

```javascript
Ext.define('ElectricCar', {
    extend: 'Car',
    start: function() {
        alert('Electric Car started');
    }
});
```

通过 `define` 进来重载如下：

```javascript
Ext.define('My.ux.field.Text', {
    override: 'Ext.form.field.Text',
    setValue: function(val){
        this.callParent(['In override']);
        return this;
    }
});
```

创建一个 singleton 类：

```javascript
Ext.define('Logger', {
    singleton: true,
    log: function(msg){
        console.log(msg);
    }
});
```


### Ext.create

用于创建类实例，声明为 `Ext.create(Class, Options)`。

例如：

```javascript
var myCar = Ext.create('ElectricCar', {
    name: 'MyElectricCar'
});
```

如果启用了 `Ext.Loader`，那么当 ElectricCar 不存在时， `Ext.create` 在自动下载其相应的 JS 文件。`Ext.Loader` 默认是启用的，可以通过设置 `Ext.Loader` 为 `false` 来禁用。

当然也可以使用 `new` 来实例化类，如 `var myCar = new ElectricCar('MyElectricCar');`，但是这种方式不能享用自动下载机制的好处。


### Ext.onReady

该函数只在页面加载后被调用一次：

```javascript
Ext.onReady(function(){
    new Ext.Component({
        renderTo: document.body,
        html: 'DOM ready!'
    });
});
```

大多数情况下，我们不需要使用该函数。


### Ext.widget

定义一个类时，可以给它一个别名。例如 `Ext.panel.Panel` 的别名为 `widget.panel`。当定义 widget 时，也可以用 `xtype` 来引用一个类，例如 `Ext.panel.Panel` 的 xtype 为 `panel`。通过 `xtype` 定义的 widget 能实现 lazy 初始化。

`Ext.widget` 是一个基于 `xtype` 值创建 widget 的快捷函数。

例如，创建 Panel 的一般方式为：

```javascript
Ext.create('Ext.panel.Panel', {
    renderTo: Ext.getBody(),
    title: 'Panel'
});
```

也能通过别名创建：

```javascript
Ext.create('widget.panel', {
    renderTo: Ext.getBody(),
    title: 'Panel'
});
```

而通过 xtype 值创建如下：

```javascript
Ext.widget('panel', {
    renderTo: Ext.getBody(),
    title: 'Panel'
});
```

大部分的 Ext JS 代码都可以直接在 [fiddle.sencha.com](https://fiddle.sencha.com/) 上试验和运行。


### Ext.getClass

返回实例的类，如：

```javascript
var button = new Ext.Button();
Ext.getClass(button); // returns Ext.Button
```


### Ext.getClassName

返回实例或类的类名，如：

```javascript
Ext.getClassName(button); // returns "Ext.Button"
Ext.getClassName(Ext.Button); // returns "Ext.Button"
```

### Ext.Base

它是 Ext 中所有类的基类。

### Ext.Class

是一个低层的工厂类，`Ext.ClassManager` 在创建类时会使用它，在应用代码中一般不直接使用。

### Ext.ClassManager

用于管理类名和类对象的映射关系。在调用以下函数时会间接用到它：

+ Ext.define
+ Ext.create
+ Ext.widget
+ Ext.getClass
+ Ext.getClassName


### Ext.Loader

用于动态依赖加载。通常通过 `Ext.require` 来启用，如：

```javascript
Ext.require(['widget.window', 'layout.border', 'Ext.data.Connection']);
```

依赖某个命名空间内的所有组件/类，可以：

```javascript
Ext.require(['widget.*', 'layout.*', 'Ext.data.*']);
```

排除不要的依赖：

```javascript
Ext.exclude('Ext.data.*').require('*');
```

通过这种方式，所需的类会按需异步加载。所需的类对应的文件路径是基于类名计算的，如 `MyApp.view.About` 类的路径为 `/myapp/view/about.js`。



# 事件

事件可以是用户动作，Ajax 调用响应等。

## 添加事件监听器

在创建对象时添加：

```javascript
Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    listeners: {
        click: function() {
            Ext.Msg.alert('Button clicked!');
        },
        mouseout: function() {
            // Do something
        }
    }
});
```

在创建实例后通过 `on` 添加：

```javascript
var button = Ext.create('Ext.Button');

button.on('click', function() {
    // Do something
});

// add multiple listeners
button.on({
    'mouseover', function() {
    // Do something
    },
    'mouseout', function() {
    // Do something
    }
});
```

## 删除事件的监听器

删除时，事件处理函数必须要有引用，不能是匿名函数：


```javascript
var HandleClick = function(){
    Ext.Msg.alert('Button clicked!');
}

var button = Ext.create('Ext.Button', {
    listeners: {
        click: HandleClick
    }
});

button.un('click', HandleClick);
```

## DOM 结点的事件处理

可以在 DOM 元素上添加事件监听器：

```javascript
var div = Ext.get('mydiv');
div.on('click', function(e, t, eOpts) {
    // Do something
});
```

# DOM 存取

## Ext.get

通过 DOM 结点的 ID 值查找，返回一个 `Ext.dom.Element` 对象。

## Ext.query

基于传入的 CSS 选择子返回某个根结点下的相关子结点。返回结点的一个数组（`HTMLElement[]/Ext.dom.Element[]`）。例如：

```javascript
var someNodes = Ext.get('.oddRow', myCustomComponent.getEl().dom);
```
 
## Ext.select

基于 CSS/XPath 选择子，返回一个 `CompositeElement` 对象（代表元素的集合）。`CompositeElement` 对象的方法能对集合中的所有元素进行过滤、遍历、批量操作等，如：

```javascript
var rows = Ext.select('div.row');
rows.setWidth(100); // All elements become 100 width

Ext.select('div.row').setWidth(100); // also can combine togethor

Ext.select('div.row, span.title'); // like jquery, multiple selections

Ext.select('div.row[title=bar]:first'); // like jquery, selection chaining
```

`Ext.select` 默认将 `body` 对象作为根结点进行查找，指定根结点如下：

```javascript
Ext.get('myEl').select('div.row'); // or 
Ext.select('div.row', true, 'myEl'); 
```

## Ext.ComponentQuery

可以基于组件的 ID，xtype，属性等在全局或某个根组件下查找组件。


```javascript
Ext.ComponentQuery.query('button'); // 返回 xtype 值为 button 的所有组件

Ext.ComponentQuery.query('#foo'); // 返回一个 ID 为 foo 的组件

Ext.ComponentQuery.query("button[title='my button']"); // 返回 xtype 值为 button 且 title 属性值为 my button 的所有组件

Ext.ComponentQuery.query('formpanel numberfield'); // 嵌套查找，只返回 form 下的 numberfield

parent.child('button[itemId=save]'); // 返回符合选择子的容器首个直接子组件，类似地，还可以用 nextNode, up, down, previousSibling 等函数
```

# 组件、容器和布局

## 组件

所有组件都继承于 `Ext.Component`，从而都具有 create, resize, render 组件的功能。

所有组件都有一个 `xtype` 属性，它在动态创建组件(lazy load) 时很有用。

## 容器

容器是一种特殊类型的组件，它能用来包含其它组件。`Ext.container.Container` 是所有容器的基类。

内置的容器有 `Ext.toolbar.Toolbar`， `Ext.panel.Panel`， `Ext.Editor` 等。

## 布局

布局定义了容器包含的组件如何确定位置和大小。所有容器都有一个布局，默认布局是 auto，不对包含的组件进行位置和大小的限制。


### updateLayout

它是 `Ext.container.Container` 的一个方法，它根据布局规则重新布局容器中的组件。

### suspendLayout

在改变容器大小或添加删除子组件时，会调用 `updateLayout` 函数。为提高性能，通常在添加删除多个子组件时，会先设置 `suspendLayout` 属性值为 true, 完成添加删除后，再将 `suspendLayout` 设置回 false, 并调用 `updateLayout` 函数。

针对整个框架的操作为：

```javascript
Ext.suspendLayouts();
Ext.resumeLayouts(true);
```

## 内置布局

内置布局有 ：

+ absolute
+ accordion
+ anchor
+ border
+ card
+ center
+ column
+ fit
+ hbox
+ table
+ vbox


### absolute 布局

通过 x 和 y 属性设置组件的位置。由于组件定位到绝对位置，组件有可能会重叠。


### accordion 布局

该布局同一时间只显示一个子组件，同时内置了展开/收缩功能。

### anchor 布局

容器内组件的大小可以相对于容器的大小进行设置。

+ 容器内的组件要么指定宽度，要么在 anchor 中同时指定高/宽度
+ anchor 值为百分比时，表示为容器大小的百分比
+ anchor 值为负值时（正值没有意义），表示容器大小减去该值
+ anchor 值必须为字符串

例如：

```javascript
var panel1 = new Ext.Panel({
    title: "panel1",
    height: 100,
    anchor: '-50',
    html: "高度等于100，宽度=容器宽度-50"
});

var panel2 = new Ext.Panel({
    title: "panel2",
    height: 100,
    anchor: '50%',
    html: "高度等于100,宽度=容器宽度的50%"
});     

var panel3 = new Ext.Panel({
    title: "panel3",
    anchor: '-10, -250',
    html: "宽度=容器宽度-10,高度=容器高度-250"
});     
```

### border 布局

子组件的 `region` 属性可基于 center, north, south, west, east 指定位置。使用 border 布局中，必须有一个组件是位于 center 区的。


### card 布局

只可看到一个子组件，它几乎覆盖整个容器。通常用于 wizard 和 tabs。

例如：

```javascript
Ext.create('Ext.panel.Panel', {
    renderTo: Ext.getBody(),
    width: 700,
    height: 400,
    layout: 'card',
    defaultListenerScope: true,
    bbar: ['->',
        {
            itemId: 'btn-prev',
            text: 'Previous',
            handler: 'showPrevious',
            disabled: true
        },
        {
            itemId: 'btn-next',
            text: 'Next',
            handler: 'showNext'
        }
    ],
    items: [
        {
            index: 0,
            title: 'Item 1',
            html: 'Item 1'
        },
        {
            index: 1,
            title: 'Item 2',
            html: 'Item 2'
        },
        {
            index: 2,
            title: 'Item 3',
            html: 'Item 3'
        }
    ],
    showNext: function(){
        this.navigate(1);
    },
    showPrevious: function(){
        this.navigate(-1);
    },
    navigate: function(incr){
        var layout = this.getLayout();
        var index = layout.activeItem.index + incr;
        layout.setActiveItem(index);

        this.down('#btn-prev').setDisabled(index===0);
        this.down('#btn-next').setDisabled(index===2);
    }
});
```

### center 布局

将子组件放置在容器的水平和垂直的中间部分。

### column 布局

+ 子组件可通过 width 设置宽度。
+ 子组件可通过 columnWidth 设置宽度值，所有子组件设置的 columnWidth 的和必须为 1
+ 容器的宽度先减去通过 width 设置的宽度值，剩下的宽度根据 columnWidth 的设置在子组件间分享


### fit 布局

子组件将适应容器的大小。容器与子组件边界的间隔由 `bodyPadding` 设置。

### hbox 布局

类似 column 布局，但能拉伸列的高度。

+ 子组件可通过 width 设置宽度
+ 子组件可通过 flex 设置宽度值，flex 值为整数
+ 容器的宽度先减去通过 width 设置的宽度值，剩下的宽度根据 flex 的设置在子组件间按比例分享


例如：

```javascript
Ext.create('Ext.panel.Panel', {
    renderTo : Ext.getBody(),
    width : 700,
    height : 400,
    layout : {
        type: 'hbox',
        pack: 'start',
        align: 'stretch',
    },
    items: [{
            title: 'Item 1'
            html: 'Item 1',
            flex: 1
        },
        {
            title: 'Item 2',
            html: 'Item 2',
            width: 100
        },
        {
            title: 'Item 3',
            html: 'Item 3',
            flex: 2
        }
    ]
});
```

### table 布局

可通过 rowspan, colspan 创建复杂布局。

### vbox 布局

类似 hbox 布局，但是是垂直分布。


参考 

+ [Core Concepts](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
