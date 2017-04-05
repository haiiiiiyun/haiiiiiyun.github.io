---
title: ExtJS 的按钮和工具栏--Learning ExtJS(4th)
date: 2017-04-03
writing-time: 2017-04-03 10:00--2017-04-05 15:23
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 事件驱动开发

使用观察者模式可实现实体/对象间用事件进行交流。当某对象/组件内发生一个事件时，该对象会将事件广播给订阅的所有对象。

`Ext.util.Observable` 基类可用来添加、触发和侦听某个特定对象或组件的事件，并能定义事件触发时的处理方式。

Ext JS 中的所有组件都合并了 (用 mixin 方式) Ext.util.Observable 类的功能，因此所有组件都能触发事件，并且可以侦听事件及定义相应处理方法。

在自定义组件中也可以定义新的事件。


```javascript
Ext.define('Myapp.sample.Employee', {
    // 合并了 Ext.util.Observable 类，
    // 因而 Employee 类具有了事件处理机制
    mixins: {observable: 'Ext.util.Observable'},
    //...
    constructor: function(config){
        //...
        // 在构造器中初始化事件机制
        this.mixins.observable.constructor.call(this, config);
    },
    quitJob: function(){
        // 触发一个自定义事件。
        // Ext Js 5 之前的版本中，要使用 `addEvent(...)` 方法
        // 来创建和定义事件
        this.fireEvent('quit', this.getName(), new Date(), 2,
            1, 'more params...');
    }
});

// 创建 Employee 的实例并侦听自定义事件
var patricia = Ext.create('Myapp.sample.Employee', {
    name:'Patricia',
    lastName:'Diaz',
    age:21,
    isOld:false,
    listeners:{
        // 侦听自定义事件
        'quit':function(EmployeeName, quitDate, param, paramb, paramc){
            console.log('Event quit launched');
            console.log('Employee:' + EmployeeName);
            console.log('Date:'+ Ext.util.Format.date(
            quitDate,'Y-m-d H:i'));
            console.log('Param :' + param);
            console.log('Param B:' + paramb);
            console.log('Param C:' + paramc);
        }
    }
});

console.log(Myapp.CompanyConstants.welcomeEmployee(patricia));

// 当调用 quitJob() 方法时会触发 'quit' 事件，
// 从而会触发执行 'quit' 事件的处理函数
patricia.quitJob();
```

这里讲的事件是 Ext JS 的事件，不是纯 JS 内置事件。

侦听事件还可以用 `addListener`(或简写 on) 来实现：

```javascript
patricia.on({
    'quit':function(EmployeeName, quitDate, param, paramb, paramc){
        console.log('Event quit launched');
        console.log('Employee:' + EmployeeName);
        console.log('Date:' + Ext.util.Format.date(quitDate, 'Y-m-d H:i'));
        console.log('Param :' + param);
        console.log('Param B:' + paramb);
        console.log('Param C:' + paramc);
    }
});
patricia.quitJob();
```

在上例中，Employee 类当有 quitJob 调用时只负责广播事件，它不关心谁在侦听;而定义了侦听的对象负责当接收到事件广播时进行相应反应。

# 创建一个简单按钮

```javascript
var myButton = Ext.create('Ext.button.Button', {
    text:'My first button', // 按钮上的文本

    // scale 属性用来定义按钮的尺寸，
    // 值可以为 'small'(默认值), 'medium', 'large'
    // 由于 Button 也扩展至 Component，即也是组件，
    // 因此，也可以通过 width, height 来设置尺寸
    scale: 'medium'

    // 添加按钮图标，
    // iconCls 的值为 CSS 类名，
    // 它通过将图标设置为背景实现按钮图标 
    // 图标的大小是基于 scale 值的：
    //
    //    scale  | size
    //-----------|-------
    //    small  | 16x16
    //    medium | 24x24
    //    large  | 32x32
    //
    // 因此，还需针对不同的 scale 创建不同的 CSS 规则：
    // .addicon-16{
    //   background:transparent url('images/add_16x16.png') center 0 no-repeat !important;
    // }
    // .addicon-24{
    //   background:transparent url('images/add_24x24.png') center 0 no-repeat !important;
    // }
    // .addicon-32{
    //    background:transparent url('images/add_32x32.png') center 0  no-repeat !important;
    //  }
    iconCls: 'addicon-24',

    // 默认图标放置在按钮文本的左侧，
    // 可以设置将图标放置在 'top', 'right', 'bottom', 'left'(默认值)
    iconAlign: 'right',

    tooltip:'Click me...!',
    renderTo:Ext.getBody()
});

// 侦听事件
myButton.on('click', function(){
});
```

# Segmented buttons

Ext JS 5 中新增了 `Ext.button.Segmented` ，它是一个容器，用于将多个按钮合并成一组。显示效果类似手机 APP 中的分组按钮。

```javascript
var mySegmentedbuttons = Ext.create('Ext.button.Segmented',{
    renderTo: Ext.getBody(),

    // 设置分组中按钮是否垂直排序
    vertical:false,

    // Ext.button.Segmented 是一个容器，
    // 定义了 defaults: { xtype: 'button' }
    // 因此 items 中的子组件默认都认为是 button
    items:[
        {
            xtype: 'button',
            text:'1st button'
        },
        {
            text:'2nd button'
        },
        {
            text:'3th button'
        },
        {
            text:'4th button'
        }
    ]
});
```

# 添加菜单

```javascript
var myButton = Ext.create('Ext.button.Button',{
    text:'Add payment method...',
    iconCls:'addicon-32',
    iconAlign:'left',
    scale:'large',
    renderTo: Ext.getBody(),

    // menu 数组内元素的默认 xtype 是 'menu'
    menu:[
        {
            text:'Master Card',
            // 第 1 种添加事件侦听器的方法
            listeners:{
                click:function(){
                    Ext.Msg.alert("Click event", "You selected Master Card..!");
                }
            }
        },
        {
            text:'Visa',
            // 第 2 种添加事件侦听器的方法
            handler: onMenuItemClick
        },
        {
            text:'PayPal',
            // 第 3 种添加事件侦听器的方法
            listeners: {
                'click': {
                    fn: onMenuItemClick,

                    // 表示只会调用一次处理函数，
                    // 下次点击事件触发时不再调用执行
                    single: true
                }
            }

        },
        {
            text:'Other...',
            handler: onMenuItemClick
        }
    ]
});

function onMenuItemClick(itemBtn, event){
    // 通过 btn.text 可以区分不同的点击按钮
    var optionString = itemBtn.text;
    //...
}

// 也可以手动进行创建
// 创建菜单项
var menuItemA = Ext.create('Ext.menu.Item',{text:'Master card'});

// 创建菜单
var menu = Ext.create('Ext.menu.Menu',{
    items : [
        menuItemA, // Variable
        Ext.create('Ext.menu.Item',{text:'Visa'}), // constructor
        {text:'Paypal'} //object config
    ]
});

var myButton = Ext.create('Ext.button.Button',{
    text:'Add payment method...',
    iconCls:'addicon-32',
    iconAlign:'left',
    scale:'large',
    renderTo:'normalbuttons',
    menu:menu
});
```

# 工具栏

工具栏组件可作为一个容器，用于排列我们的按钮。

从 Ext Js 4 开始，工具栏可以放置在容器的 4 边 (top, right, bottom, left)，同时还可以同时定义多个工具栏。同时要注意，工具栏通常用于 panel, window, grid 等容器组件上。

```javascript
var myPanel = Ext.create( 'Ext.panel.Panel' ,{
    title: 'My first toolbar...',
    //width: 450,
    //height: 200,

    // 该数组中定义的组件可以放置到任何 4 个边上 (top, right, bottom, left)
    // 通常该数组中的组件为工具栏，但也可以定义其它组件，
    // 如 grid, panel, form 等。
    dockedItems: [
        {
            xtype : 'toolbar',
            dock: 'top', //放置到 top 边，未设置该属性时，默认值也是 top

            // 工具栏组件中的 items 中的组件默认的 xtype 为 button
            // 也可以加入其它组件，如 textfield, combo box, radiobutton 等。
            items: [
                {text: 'New record'},
                {text: 'Edit record'},
                {text: 'Remove record'},

                // 可用 Ext.container.ButtonGroup (xtype: buttongroup) 将工具栏中的多个
                // 按钮组合成一组。ButtonGroup 扩展至 Ext.panel.Panel，因此可以设置
                // title 等属性
                { xtype:'buttongroup',
                    title:'Actions',

                    // buttongroup 分组内按钮默认是水平排列的，
                    // 即每个按钮一列，可以用 column 属性来调整
                    items:[
                        {text: 'New', iconCls: 'addicon-16'},
                        {text: 'Edit', iconCls: 'editicon-16'},
                        {text: 'Remove', iconCls: 'deleteicon-16'}
                    ]
                },
                {
                    xtype: 'buttongroup',
                    title: 'Print / Export & Help',

                    // 这个分组设置为只有 2 列
                    columns: 2,

                    // 子组件（按钮）的默认属性值
                    defaults:{scale:'large', iconAlign:'top'},

                    items:[
                        {
                            text: 'Export', 
                            iconCls: 'export-32',
                            rowspan: 2, // 该按钮占据了 2 行，从而在第 1 列
                        },
                        // 下面 2 个按钮在第 2 列
                        {text: 'Print', iconCls: 'print-32'},
                        {text: 'Help', iconCls: 'help-32'}
                    ]
                }
            ]
        }
    ],
    renderTo:Ext.getBody()
});
```

# 面包屑导航栏 (breadcrumb bar)

面包屑栏在 Ext Js 5 时引进，它能将 TreeStore 中的数据显示为一条导航按钮。

```javascript
// 定义 TreeStore
Ext.define('Myapp.sample.store.mainMenu', {
    extend: 'Ext.data.TreeStore',
    root: {
        text: 'My app',
        expanded: true,
        children: [
            {
                text: 'Modules',
                expanded: true,
                children: [
                    {leaf: true, text: 'Employees'},
                    {leaf: true, text: 'Customers'},
                    {leaf: true, text: 'Products'}
                ]
            }
            ,{
                text: 'Market',
                expanded: true,
                children: [
                    {leaf: true, text: 'Sales'},
                    {leaf: true, text: 'Budgets'},
                    {leaf: true, text: 'SEO'},
                    {leaf: true, text: 'Statistics'}
                ]
            },
            {
                text: 'Support',
                iconCls:'help-16',
                children: [
                    {leaf: true, text: 'Submit a ticket'},
                    {leaf: true, text: 'Forum'},
                    {leaf: true, text: 'Visit our web site'}
                ]
            },
            {leaf: true, text: 'Reports'},
            {leaf: true, text: 'Charts'}
        ]
    }
});

// 创建 TreeStore 实例
var myMenuStore = Ext.create('Myapp.sample.store.mainMenu',{});

var myPanel = Ext.create('Ext.panel.Panel',{
    title:'My first breadcrumb bar...',
    width:600,
    height:200,
    dockedItems:[
        { // 创建面包屑导航栏
            xtype : 'breadcrumb',
            dock: 'top',
            store: myMenuStore, // 用 TreeStore 中的数据来创建按钮，菜单等组件
            showIcons: true, // 在显示的按钮上显示图标

            // 设置初始选中的结点。
            // 这里选择了 {leaf: true, text: 'Submit a ticket'},
            selection: myMenuStore.getRoot().childNodes[2].childNodes[0],

            listeners: {
                // 当面包屑导航栏中的按钮或菜单点击时会
                // 触发 selectionchange 事件
                // 参数：
                //   mybreadcrumb: 当前的面包屑导航栏实例
                //   node: 选中的 TreeStore 结点
                //   eOpts: 传入 Ext.util.Observable.addListener 的选项内容
                'selectionchange':{
                    fn: function(mybreadcrumb, node, eOpts){
                        var panel = mybreadcrumb.up('panel');
                        panel.update( 'This is the zone for:<b>' + node.data.text + '</b>' );
                    },
                    delay:200
                }
            }
        }
    ],
    renderTo:Ext.getBody()
});
```


# 参考 

+ [Chapter5: Buttons and Toolbars](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
