---
title: ExtJS 核心概念--Learning ExtJS(4th)
date: 2017-02-08
writing-time: 2017-03-28 09:55--2017-03-29 16:25
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
+ Ext Core 层：包含用来管理 DOM 的类，对事件进行设置和触发，对 Ajax 请求的支持，及使用 CSS 选择子对 DOM 进行搜索的类，与数据有关的包（如 field, store 等）。
+ Ext JS 层：包含所有的组件及特性。


ExtJS 组件只有在 DOM 及 Ext JS 加载解析后才能创建，可以用以下方法确保：

```javascript
Ext.onReady(function(){
    Ext.Msg.alert("Hello", "my first Ext JS app");
}):
```

也可以是另一种方法：

```javascript
Ext.application({
    name: 'MyFirstApplication',
    launch: function(){
        Ext.Msg.alert("Hello", "my first Ext JS app");
        Ext.Msg.confirm("Confirm","Do you like Ext JS 5?");
    }
}):
```

使用 Ext 库的一个好处是所有的类和对象都位于这个全局的 `Ext` 中。


Ext 的消息和警告窗口不会阻塞 Javascript 线程，这和本地的浏览器对话窗口不同。同时，由于 Ext.Msg 是一个单例实例。因此上面的 Ext.Msg.alert 会首先显示，并立即被 Ext.Msg.confirm 替换，从而我们不会看到 Ext.Msg.alert 窗口。


# 类系统

创建类时，Ext 内部使用 `Ext.ClassManager` 对象来管理名字 (name)、别名 (alias) 以及我们定义的其它名字 (aletrnate name) 间的关联性。并且所有的类都基于 `Ext.Base`。

推荐使用下面的快捷写法来创建和使用类：

+ Ext.define: 在创建一个新类，扩展类，或需对类进行一些重载时使用。
+ Ext.create: 用来创建一个类实例，可以引用类的全名 (fullname)，别名 (alias) 或 alternate name。使用这些选项时，类管理器会将它映射到相应的类;也可以用该方法来创建现有类的实例。
+ Ext.widget: 通过使用 xtype(alias) 属性或配置对象来创建一个组件。


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

## 预处理器 preprocessor 和后处理器 postprecessor

Ext 中所有的类是 `Ext.Base` 的子类，同时也是 `Ext.Class` 的一个实例。当使用 `Ext.define` 来创建一个类时，实际是创建一个 Ext.Class 的实例。

Ext.Class 是一个工厂，这意味着，当使用 `Ext.create` 方法时，Ext 会运行一些后台处理过程。每个处理过程在类创建的整个过程中都有专门的目的。

处理过程可以是异步也可以是同步的。

一个预处理器 (preprocessor) 是在创建 Ext.Class 类实例（即我们的类）前进行的处理过程，它可以用来修改我们的类行为。

而一个后处理器 (postprocessor) 是当 Ext.Class 类实例 （即我们的类）创建后进行的处理过程。这些后处理器的功能包含：创建我们类的一个单例实例，定义别名等。

Ext 中已经内置有一些处理器了，但我们可以自定义一些处理器，并添加到处理器队列中。

Ext 默认登记的一组处理器可用下列代码得到：

```javascript
var pre = Ext.Class.getDefaultPreprocessors();
var post = Ext.ClassManager.defaultPostprecessors;
console.log(pre);
console.log(post);

//Output: ["className", "loader", "extend", "privates", "statics", "inheritableStatics", "platformConfig", "config", "cachedConfig", "mixins", "alias"]
// ["alias", "singleton", "alternateClassName", "debugHooks", "deprecated", "uses"]
```

一些预处理器的功能描述如下：


预处理器名         | 描述
className          | 定义命名空间及类名
loader             | 检查依赖文件，当未加载时进行加载
extend             | 将父类的所有方法和属性继承到新类中
statics            | 为当前类创建已定义的静态方法或属性
inheritableStatics | 如果可行，从父类继承静态方法和属性
config             | 为 config 中的各属性创建 getter 和 setter 方法
mixins             | 从 mixin 中的所有类中继承所有的方法和属性
alias              | 为新类设置别名


一些后处理器的功能描述如下：


后处理器名         | 描述
alias              | 将该新类登记到类管理器，并登记别名
singleton          | 为该新类创建一个单例实例
alternateClassName | 为新创建的类定义另一个名字
uses               | 加载该新类，及用到的所有其它类


错误的处理器名会被忽略（不会运行），故要注意名字大小写。


## 合并入多个类（使用 mixin）

Ext 只能进行单继承，但使用 mixin 处理器可以模拟多重继承。

以上面的 Employee 和 Supervisor 为例，每个职位执行不同的任务，如秘书要接电话，接待客户;财务要接待客户，创建财务报表及开会;而经理要监督员工。

```javascript
// Mixins
Ext.define('Myapp.sample.tasks.attendPhone', {
    answerPhone: function(){
        onsole.log( this.name + ' is answering the phone');
    }
});

Ext.define('Myapp.sample.tasks.attendClient',{
    attendClient:function(clientName){
        console.log( this.name + ' is attending client: ' + clientName);
    }
});

Ext.define('Myapp.sample.tasks.attendMeeting',{
    attendMeeting:function(person){
        console.log( this.name + ' is attending a meeting with ' +
        person);
    }
});

Ext.define('Myapp.sample.tasks.superviseEmployees',{
    superviseEmployee:function(supervisor, employee){
        console.log( supervisor.name + ' is supervising : ' +
            employee.name + ' ' + employee.lastName);
    }
});

// 每个职位有不同的职能，并通过 mixin 继承
Ext.define('Myapp.sample.Secretary', {
    extend: 'Myapp.sample.Employee',
    mixins: {
        answerPhone: 'Myapp.sample.tasks.attendPhone'
    },
    constructor: function(config){
        Ext.apply(this, config || {});
        console.log('Secretary class created – fullname:' + this.name
            + ' ' + this.lastName);
    }
});

Ext.define('Myapp.sample.Accountant',{
    extend:'Myapp.sample.Employee',
    mixins:{
        attendClient: 'Myapp.sample.tasks.attendClient',
        attendMeeting: 'Myapp.sample.tasks.attendMeeting'
    },
    constructor: function (config){
        Ext.apply(this, config || {});
        console.log('Accountant class created – fullname:' + this.name
            + ' ' + this.lastName);
}
});

Ext.define('Myapp.sample.Manager',{
    extend:'Myapp.sample.Employee',
    mixins:{
        attendClient: 'Myapp.sample.tasks.attendClient',
        attendMeeting: 'Myapp.sample.tasks.attendMeeting',
        supervisePersons:'Myapp.sample.tasks.superviseEmployees'
    },
    constructor: function (config){
        Ext.apply(this, config || {});//this.name= config.name;
        console.log('Manager class created – fullname:' + this.name +
            ' ' + this.lastName);
    },

    supervise: function(employee){
        console.log( this.name + ' starts supervision ');

        // 这里调用了 mixin 类中的方法
        this.mixins.supervisePersons.superviseEmployee(this, employee);
        console.log( this.name + ' finished supervision ');
    }
});

// 使用
var patricia = Ext.create('Myapp.sample.Secretary', {
    name:'Patricia', lastName:'Diaz', age:21 } );
patricia.work('Attending phone calls');
patricia.answerPhone();

var peter = Ext.create('Myapp.sample.Accountant', {name:'Peter',
    lastName:'Jones', age:44 } );
peter.work('Checking financial books');
peter.attendClient('ACME Corp.');
peter.attendMeeting('Patricia');

var robert = Ext.create('Myapp.sample.Manager', {name:'Robert',
    lastName:'Smith', age:34 } );
robert.work('Administration of the office');
robert.attendClient('Iron Tubes of America');
robert.attendMeeting('Patricia & Peter');
robert.supervise(patricia);
robert.supervise(peter);
```

### 使用 mixinConfig 属性

使用了 mixinConfig 属性的 mixin 类，能为新创类中的方法设置 before 和 after 挂钩，即当运行关联方法时，会在运行前和运行后调用相应的挂钩方法。

例如，为 Secretary 类的 answerCellPhone 方法创建一个 mixinConfig 类：

```javascript
Ext.define('Myapp.sample.tasks.attendCellPhone', {
    extend: 'Ext.Mixin',

    // answerCellPhone 是新创类中的关联函数，
    // 而 cellPhoneRinging 和 finishCall 是当运行 answerCellPhone
    // 时调用的挂钩函数。
    // 并且继承类不能调整挂钩函数的参数。
    mixinConfig: {
        before: {
            answerCellPhone: 'cellPhoneRinging'
        },
        after: {
            answerCellPhone: 'finishCall'
        }
    },
    cellPhoneRinging: function(){
        console.log( 'cell phone is ringing you may attend call');
    },
    finishCall: function(){
        console.log( 'cell phone call is over');
    }
});

// 重新定义 Secretary
Ext.define('Myapp.sample.Secretary',{
    extend:'Myapp.sample.Employee',
    mixins:{
        answerPhone: 'Myapp.sample.tasks.attendPhone',

        // 定义挂钩
        util:'Myapp.sample.tasks.attendCellPhone'
    },
    constructor: function (config){
        Ext.apply(this, config || {});//this.name= config.name;
        console.log('Secretary class created – fullname:' + this.name
            + ' ' + this.lastName);
    },

    // 运行该函数前后都会调用挂钩函数
    answerCellPhone:function(){
        console.log( this.name + ' is answering the cellphone');
    }
});
```

Ext 中的 Ext.util.Observable, Ext.util.Floating 和 Ext.state.Stateful 等都是 mixins。

## config 属性

ExtJS 4 之前，所有的 getter 和 setter 属性都需要手动设置，如：

```javascript
Ext.define('Myapp.sample.Employee',{
    name:'Unknown',
    lastName: 'Unknown',
    age: 0,
    constructor: function (config){
        Ext.apply(this, config || {});//this.name= config.name;
        console.log('class A created – fullname:' + this.name +
            ' ' + this.lastName);
    },
    work: function( task ){
        console.log( this.name + ' is working on: ' + task);
    },

    setName: function( newName ){
        this.name = newName;
    },
    getName: function(){
        return this.name;
    }
});
```

而自 ExtJS 4 开始，这些 getter setter 属性都可以通过 config 属性设置，如：

```javascript
Ext.define('Myapp.sample.Employee',{

    // Ext 通过运行预处理器 `config`，为 config 中的每个属性
    // 在新创类原型上创建 getter 和 setter 函数（如果未定义的话），
    // 例如 age 对应 getAge 和 setAge，而如果在新创类中定义了属性的
    // apply 方法（如 applyAge），那么自动生成的 setter 函数在设置值前
    // 默认会调用该 apply 方法，如果 apply 方法没有返回值，则不会进行
    // 设置操作。
    config:{
        name: 'Unknown',
        lastName: 'Unknown',
        age: 0, // 该属性将对应生成 getAge(), setAge() 方法。
        isOld: false // 该导发对应生成 getIsOld(), setIsOld()
    },
    constructor: function ( config ){
        // 如果类直接继承自 Ext.Base，则要求调用 initConfig() 
        // 来为属性创建 getter 和 setter 方法，
        // 如果继承自使用了 config 属性的类，则无需调用 initConfig()
        this.initConfig( config );
    },
    work: function( task ){
        console.log( this.name + ' is working on: ' + task);
    },

    // 自动生成的 setter 函数在设置值前
    // 默认会调用该 apply 方法，如果 apply 方法没有返回值，则不会进行
    // 设置操作。
    applyAge: function(newAge) {
        this.setIsOld ( ( newAge >= 90 ) );
        return newAge;
    }
});

// 使用
var patricia = Ext.create('Myapp.sample.Employee',{
    name: 'Patricia',
    lastName: 'Diaz',
    age: 21,
    isOld:false
});
console.log( "employee Name = " + patricia.getName() );
console.log( "employee Last name = " +
    patricia.getLastName() );
console.log( "employee Age = " + patricia.getAge() );
patricia.work( 'Attending phone calls' );
patricia.setName( 'Karla Patricia' );
patricia.setLastName( 'Diaz de Leon' );
patricia.setAge ( 25 );
console.log("employee New Name=" + patricia.getName() );
console.log("employee New Last name=" +
    patricia.getLastName() );
console.log( "employee New Age = " + patricia.getAge() );
patricia.work('Attending phone calls');
var is_old='';
is_old= ( patricia.getIsOld() == true)? 'yes' : 'no' ;
console.log( "is patricia old? : " + is_old ) ;
patricia.setAge( 92 );
is_old='';
is_old= ( patricia.getIsOld() == true)? 'yes' : 'no' ;
console.log( "is patricia old? : " + is_old );
```

## 静态方法和属性

静态方法和属性属于类本身，不属于类实例，使用 `statics` 属性进行定义。

```javascript
Ext.define('Myapp.sample.Employee',{
    // 定义静态方法和属性
    statics:{
        instanceCount: 0,
        payrollId: 1000,
        nextId : function(){
            return ( this.payrollId + this.instanceCount );
        }
    },
    config:{
        name: 'Unknown',
        lastName: 'Unknown',
        age: 0,
        isOld: false,
        payrollNumber: 0
    },

    constructor: function ( config ){
        this.initConfig( config );

        // 调用静态方法
        this.setPayrollNumber( this.statics().nextId() );

        // 调用静态属性
        // 这里 `this.self` 指类本身
        this.self.instanceCount ++; // 等价于 `this.statics().instanceCount ++;`
    },

    work: function( task ){
        console.log( this.getName() + ' is working on: ' + task);
    },
    applyAge: function( newAge ) {
        this.setIsOld ( (newAge >= 90) );
        return newAge;
    },
    getTotalEmployees: function(){
        return this.statics().instanceCount;
    }
});

var patricia = Ext.create('Myapp.sample.Employee', {
    name: 'Patricia',
    lastName: 'Diaz',
    age: 21,
    isOld: false
});
console.log( "patricia payrollId = " +
    patricia.getPayrollNumber());
console.log( "total employees = " + patricia.getTotalEmployees());

var peter = Ext.create('Myapp.sample.Employee', {
    name: 'Peter',
    lastName: 'Pan',
    age: 16,
    isOld: false
});
console.log( "Peter payrollId = " + peter.getPayrollNumber() );
console.log( "total employees = " + patricia.getTotalEmployees());
console.log( "instance(s) of employee class = " +
    Myapp.sample.Employee.instanceCount );
```

## 单例类 singleton

单例类只能实例化一次，在定义类时，只需设置 `singleton: true` 即触发 `singleton` 后处理器，将该类转变成单例类。

```javascript
Ext.define('Myapp.CompanyConstants',{
    // 该设置触发 singleton 后处理器，将该类转变成单例类
    singleton: true,

    companyName: 'Extjs code developers Corp.',
    workingDays: 'Monday to Friday',
    website: 'www.extjscodedevelopers.com',
    welcomeEmployee: function (employee){
        "Hello " + employee.getName() + ", you are now working for " +
            this.companyName;
    }
});

// 单例类只有一个实例，故无需使用 `Ext.create` 来创建实例，只需使用
// 类时即可：
alert( Myapp.CompanyConstants.companyName );
// will alert "Extjs code developers Corp."

var patricia = Ext.create('Myapp.sample.Employee', {
    name:'Patricia',
    lastName:'Diaz',
    age:21,
    isOld:false
});
console.log(Myapp.CompanyConstants.welcomeEmployee(patricia));
// Hello Patricia you are now working for Extjs code developers Corp.
```

单例类通常用于保存常数，配置信息，实用函数等，如应用的基路径，图片文件的某路径等。


## 别名 alias

别名即类的缩写名字。类管理器管理别名与实际类对象的映射关系。别名通常都用小写。

```javascript
Ext.define('Myapp.sample.EmployeePanel',{
    extend: 'Ext.panel.Panel',

    // 定义一个别名，由于这是一个组件，
    // 故使用了 `widget` 命名空间作为前缀
    // Ext 中用命名空间表示别名的用途：
    // 如：
    //   + feature: 表示 Grid 的功能特性
    //   + plugin: 表示插件
    //   + store: 表示 Ext.data.Store
    //   + widget: 表示组件
    alias: 'widget.employeePanel',

    // 该属性值即可是字符串，也可是一个数组，
    // 如： `alternateClassName: ['employeepanel', 'customerEmployeePanel']`
    alternateClassName: 'mycustomemployeepanel',
    title: 'Employee Panel',
    html: 'Employee content here..!'
});
```

使用别名来创建类实例：

```javascript
Ext.onReady (function(){
    Ext.create('widget.employeePanel',{
        title: 'Employee Panel: Patricia Diaz...',
        height:250,
        width:450,
        renderTo: Ext.getBody()
    });
});
```

也可以用 `Ext.widget`：

```javascript
Ext.onReady (function(){
    Ext.widget('employeePanel',{
        //using the xtype which is employeePanel
        title: 'Employee Panel: Patricia Diaz...',
        height:250,
        width:450,
        renderTo: Ext.getBody()
    });
});
```

由于别名由类管理器管理，故可通过类管理类进行引用：

```javascript
Ext.ClassManager.instantiateByAlias("widget.employeePanel",{
    renderTo: Ext.getBody()
});

// Ext.createByAlias 是 Ext.ClassManager.instantiateByAlias 的简写
// 故也可写成
Ext.createByAlias("widget.employeePanel",{
    renderTo: Ext.getBody()
});

// 也可用配置项中的 xtype 属性进行引用：

var win = Ext.create("Ext.window.Window",{
    title: "Window", width:350, height:250,
    items: [{ xtype: "employeePanel" }]
});
win.show();
```

## 按需加载

大型应用需要将功能分成模块，并能按需加载每个脚本文件。

从 ExtJS 4 开始，可以按需动态加载类和文件了。我们可以为每个类设置依赖关系，然后 Ext 会自动加载依赖。

在生产环境中，不推荐加载所有的 Ext 类，应用将多个类组织成一个包 (package)，然后按包加载，而不是逐类加载。

要使用加载系统，在定义类时要遵循以下约定：

+ 每个文件只定义一个类
+ 类名要和 JS 文件名匹配
+ 类的命名空间要和目录结构匹配。如 `MyApp.customers.controller.Main` 应该将 Main.js 文件放置在 MyApp/customers/controller 目录下。


### 启用加载系统

在 JS 文件的最开头：

```javascript
Ext.Loader.setConfig({
    enabled: true,
    paths: {
        // 设置根命名空间对应的目录
        MyApp: 'appdir'
    }
});

// 设置后，对应的预处理器运行时会加载该类的所有依赖

// 设置依赖的类：
// `Ext.require` 方法幕后会为每个依赖在 HTML 文件中创建一个 script 标签，
// 因此这些依赖文件会在运行 Ext.onReady 前自动下载并加载。
Ext.require([
    'MyApp.Constants',
    'MyApp.samples.demoClass'
]);
```

# 与 DOM 交互

DOM 结点用 `Ext.Element` 类来表示。

## 获取元素

```javascript
Ext.onReady(function(){
    // Ext.get 函数根据 HTML 元素的 id 值获取一个 Ext.dom.Element。
    // Ext.get 是 Ext.dom.Element.get 的别名
    var div = Ext.get('main');

    // 设置 CSS 属性
    div.setStyle({
        width: "100px",
        height: "100px",
        border: "2px solid #444",
        margin: "80px auto",
        backgroundColor: "#ccc"
    });

    // 添加/删除 CSS 类
    div.addCls("x-testing x-box-component");
    div.removeCls("x-testing");

    // 设置动画效果
    div.fadeOut()
       .fadeIn({
            duration:3000
        });
});
```

## 查询

查询引擎支持绝大多数的 CSS 3 选择子和基本的 XPath 选择子。

使用 `Ext.dom.Query` 来进行查询，这是一个单例类。

```javascript
Ext.onReady(function(){
    // 返回类型是 Ext.CompositeElementLite，是一个集合
    var myElements = Ext.dom.Query.select('#main .menu ul li');

    // 将集合转换成一个 Ext.dom.Element 元素
    myElements = Ext.get(myElements);
    myElements.setStyle({
        display: "inline",
        backgroundColor: "#003366",
        margin: "3px",
        color: "#FFCC00",
        padding: "3px 20px",
        borderRadius: "10px",
        boxShadow: "inset 0 1px 15px #6699CC"
    });


    // Ext.select 是 Ext.dom.Query.select 的别名
    var h1 = Ext.select("#main div[class=content] h1");
    h1.setStyle("color","#003399");
});
```

## DOM 处理

```javascript
Ext.onReady(function(){
    // Ext.DomHelper 对象/类来处理 DOM
    Ext.DomHelper.append(Ext.getBody(),{
        tag: "div",
        style: {
            width: "100px",
            height: "100px",
            border: "2px solid #333",
            margin : "20px auto"
        },
        children : [{
            tag : "ul",
            children : [
                {tag: "li", html: "Item 1"},
                {tag: "li", html: "Item 2"}
            ]
        }]
    });

    // 或者先创建一个 DOM 结点，并插入：
    var h1 = Ext.DomHelper.createDom({
        tag: "h1",
        html: "This is the title!"
    });
    Ext.getBody().appendChild(h1);

    // 使用 Ext.Element.remove 函数来删除 DOM 元素
    // Ext.fly 类似 Ext.get，只不过它不会将
    // 获取的元素保存到内存中，因此适用于单次引用。
    Ext.fly(h1).remove();
});
```


# 参考 

+ [Chapter1: An Introduction to Ext JS 5](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
+ [Chapter2: The Core Conception](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
