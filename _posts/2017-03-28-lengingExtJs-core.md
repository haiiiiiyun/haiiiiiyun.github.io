---
title: ExtJS 核心概念--Learning ExtJS(4th)
date: 2017-02-08
writing-time: 2017-03-28 09:55
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# ExtJS 的分层结构

共分为 3 层。

```
------------
| Ext JS   |
------------

------------
| Ext Core |
------------

----------------
|Ext Foundation |
-----------------
```

+ Ext Foundation 层： 创建 `Ext` 这个对象、一些实用工具，及类系统，用来扩展类，重载方法和属性、Mixin，对类进行配置等。
+ Ext Core 层：包含用来管理 DOM 的类，对事件进行设置和触发，对 Ajax 请求的支持，及使用 CSS 选择子对 DOM 进行搜索的类，与数据有关的包（包 field, store 等）。
+ Ext JS 层：包含所有的组件及特性。




ExtJS 组件只有在 DOM 及 Ext JS 加载解析后才能创建，可以用以下方法确保：

```Javascript
Ext.onReady(function(){
    Ext.Msg.alert("Hello", "my first Ext JS app");
}):
```

也可以是另一种方法：

```Javascript
Ext.application({
    name: 'MyFirstApplication',
    launch: function(){
        Ext.Msg.alert("Hello", "my first Ext JS app");
        Ext.Msg.confirm("Confirm","Do you like Ext JS 5?");
    }
}):
```

使用 Ext 库的一个好处是所有的类和对象都位于这个全局的 `Ext` 中。


Ext 的消息和警告窗口不会阻塞 Javascript 线程，这和本地的浏览器对话窗口不同。同时，由于 Ext.Msg 是一个单例实例。因此上面的 Ext.Msg.alert 会首先显示，并立即为 Ext.Msg.confirm 替换，从而我们不会看到 Ext.Msg.alert 窗口。


# 类系统

创建类时，Ext 内部使用 `Ext.ClassManager` 对象来管理名字 (name)、别名 (alias) 以及我们定义的其它名字 (aletrnate name) 间的关联性。并且所有的类都基于 `Ext.Base`。

推荐使用下面的快捷写法来创建和使用类：

+ Ext.define: 用来创建一个新类，扩展类，或需对类进行一些重载时使用。
+ Ext.create: 用来创建一个类的实例，可以引用类的全名 (fullname)，别名 (alias) 或 alternate name。使用这些选项时，类管理器会将它映射到相应的类;也可以用该方法来创建现有类的实例。
+ Ext.widget: 用来通过使用 xtype(alias) 属性或配置对象来创建一个组件。


别名 (alias) 是类名的简写版，它更易于记忆，例如 `Ext.grid.column.Action` 的别名为 `actioncolumn`。

## 命名约定（非强制）

+ 可以使用数字和字母，不推荐使用 - 和 \_，如：
    - `MyApp.utils-common.string-renderers` 不好
    - `MyApp.utils.Md5encyption` 好
    - `MyApp.reportFormats.FM160` 好
+ 名字应分组成 `packages/namespaces`，并用点号分隔：`(namespace).(namespace).(class)`。
+ 顶层的类名以骆驼法命名，中间的分组和命名空间都用小写，如：
    - `MyApp.grids.EmployeesGrid`
    - `MyApp.data.clients.SalesReport`
+ 非框架内的类不要用 `Ext` 作为命名空间，除非创建一个扩展组件时可用 `Ext.ux`。


创建一个单参数的类并生成一个实例如下：

```Javascript
Ext.define('Myapp.sample.Employee',{
    name: 'Unknown',
    constructor: function (name){
        this.name= name;
        console.log('class was created – name:' + this.name);
    },
    work: function(task){
        alert(this.name + ' is working on: ' + task);
    }
});

var patricia = Ext.create('Myapp.sample.Employee', 'Patricia Diaz');
patricia.work('Attending phone calls');
```

创建多参数的类并生成一个实例如下：

```Javascript
Ext.define('Myapp.sample.Employee',{
    name: 'Unknown',
    lastName: 'Unknown',
    age: 0,
    constructor: function (config){
        Ext.apply(this, config || {});
        console.log('class created – fullname:' 
            + this.name + ' ' + this.lastName);
    },
    checkAge:function(){
        console.log( 'Age of ' + this.name + ' ' 
            + this.lastName + ' is:' + this.age );
    },
    work: function(task){
        alert(this.name + ' is working on: ' + task);
    }
});

var patricia = Ext.create('Myapp.sample.Employee',{
    name:'Patricia',
    lastName:'Diaz',
    age:21
});
patricia.checkAge();
patricia.work('Attending phone calls');
```

使用 `extend` 属性来扩展一个类

```Javascript
Ext.define('Myapp.sample.Supervisor',{
    extend: 'Myapp.sample.Employee',
    constructor: function ( config ){
        Ext.apply(this, config || {});
        console.log('class B created – fullname:' + this.name +
            ' ' + this.lastName);
    },

    supervise: function( employee ){
        var employeefullname = employee.name + ' ' +
            employee.lastname;
        console.log( this.name + ' is supervising the work of '
            + employeefullname );
    }
});
```

当然，`extend` 属性也可用来扩展 `Ext.panel.Panel` 等系统类/组件。

续 ...







# 参考 

+ [An Introduction to Ext JS 5](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
