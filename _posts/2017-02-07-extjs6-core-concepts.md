---
title: ExtJS 6 核心概念
date: 2017-02-07
writing-time: 2017-02-07 10:02
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

# 类系统

Ext 提供了很多用于创建和使用类的辅助函数。

Ext JS 6 的类系统中有以下的类：

+ Ext
+ Ext.Base
+ Ext.Class
+ Ext.ClassManager
+ Ext.Loader


## Ext

`Ext` 是一个全局的 singleton 对象，它封闭了所有类、singleton，工具函数。它包含子许多常用的工具函数，同时也为位于其它类中的常用函数创建了快捷方式。

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

+ name: 为类名
+ data: 应用到该类的属性
+ callback: 一个可靠函数，在类创建后会调用


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

通过 `define` 来扩展一个类如下：

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

当然也可以使用 `new` 来实例化类，如 `var myCar = new ElectricCar('MyElectricCar');`，但是这样的话不能享用自动下载机制的好处。


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

当在定义一个类时，可以给它一个别名。例如 `Ext.panel.Panel` 的别名为 `widget.panel`。当定义 widget 时，也可以用 `xtype` 来引用一个类，例如 `Ext.panel.Panel` 的 xtype 为 `panel`。通过 `xtype` 定义的 widget 能实现 lazy 初始化。

`Ext.widget` 是一个能根据 `xtype` 值创建 widget 的快捷函数。

例如，创建 Panel 的一般方式为：

```javascript
Ext.create('Ext.panel.Panel', {
    renderTo: Ext.getBody(),
    title: 'Panel'
});
```

也可能通过别名来创建：

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








参考： 

+ [Core Concepts](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
