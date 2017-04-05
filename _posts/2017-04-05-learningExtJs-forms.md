---
title: ExtJS 中的表单--Learning ExtJS(4th)
date: 2017-04-05
writing-time: 2017-04-05 15:25--
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

表单组件用于收集和编辑数据。

# 表单组件

`Ext.form.Panel` 组件扩展至 `Ext.panel.Panel`，并且合并了 `Ext.form.Basic`，从而包含了表单提交等表单处理功能。

```javascript
// file: appcode/view/CustomerForm01.js
// 定义 FormPanel
Ext.define('MyApp.view.CustomerForm01', {
    extend: 'Ext.form.Panel',
    alias: 'widget.customerform01',
    height: 280,
    width: 448,
    bodyPadding: 6,
    title: 'Customer ( .... )',
    items: [ ],
    dockedItems: [ ]
});


// file: app.js 
// 配置动态加载系统
Ext.Loader.setConfig({
    enabled: true,
    paths:{Myapp:'appcode'}
});

// 配置所依赖的库
Ext.require([
    'Ext.form.*',
    'Ext.toolbar.*',
    'Ext.button.*',
    'Myapp.view.CustomerForm01'
]);

Ext.onReady(function(){
    // 创建一个 FormPanel 实例
    var mypanel = Ext.create('MyApp.view.CustomerForm01',{
        title:'My first customer form...',

        // 从 ExtJs 4 开始，可以对每个表单项属性进行单独设置，
        // 可以设置的属性有 labelWidth, labelAlign 等。
        defaults: {
            anchor: '-18',
            labelWidth: 90,
            labelAlign: 'right'
        },

        defaultType: 'textfield', // 该属性设置了每个表单项的默认类型

        // FormPanel 默认的布局是 anchor
        items: [
            {
                xtype: 'numberfield',
                //anchor: '60%', // 表单项宽度为总宽度的 60%
                fieldLabel: 'Customer ID'
            },
            {
                //xtype: 'textfield',
                anchor: '-18', // 表单项宽度为总宽度 - 18px
                fieldLabel: 'Name'
            },
            {
                //xtype: 'textfield', 
                fieldLabel: 'Phone' // 表单项宽度为总宽度 - 18px，来自 defaults
            },
            {
                fieldLabel: 'Web site',
            },
            {
                xtype: 'datefield',
                fieldLabel: 'Client since'
            },
            {
                xtype: 'combobox',
                fieldLabel: 'Status'
            }
        ],
        renderTo: Ext.getBody()
    });
});
```

# 表单项解析

每个表单项都扩展至 `Ext.Component`，因此都是一个组件，故都有组件生命周期和事件机制，同时可以用在表单及其它容器中（如工具栏）。

类 `Ext.form.field.Base` 定义了表单项的通常属性、方法和事件。该其类扩展至 `Ext.form.Labelable` 和 `Ext.form.field.Field`（使用 mixin 方式）。

Labelable 类实现了标签的显示及错误提醒显示。

Field 类实现了对值的管理，并实现了 2 个重要方法： `getValue()` 和 `setValue()`。同时又引用了 `raw value` 的概念。

`raw value` 的例子：当从服务端获取以字符串表示的日期值时。`raw value` 就是文本形式的日期值，而日期表单项的值将是 JavaScrit 的 Date 对象。


## 常用的表单项

+ text
+ number
+ combobox, tag
+ date
+ checkbox, checkboxGroup
+ radio, radioGroup


```javascript
// 定义一个 FormPanel
Ext.define('Myapp.view.AvailableFields01', {
    extend: 'Ext.form.Panel',
    alias: 'widget.availablefields01',
    requires: ['Ext.form.*'],
    height: 280,
    width:448,
    bodyPadding: 6,
    title: 'Available Fields',
    defaultType:'textfield',
    defaults:{
        anchor:'-18',
        labelWidth:100,
        labelAlign:'right'
    },

    // 一般用于定义组件的属性
    initComponent: function() {
        var me = this;
        var myItems = me.createFields();
        Ext.applyIf(me,{items: myItems});
        me.callParent(arguments);
    },

    // 动态生成子组件
    // 子类可以重载该方法来定义不同的子组件
    createFields: function (){
        var newItems=[];

        // Text 表单项对应一个文本框，
        // 是 Ext.form.field.Text 的实例 (xtype: text)
        // 它将文本作为字符串值进行管理，同时定义了
        // keydown, keypress, keyup 等事件，这些事件可
        // 用来捕获用户的按键。如果要使用这些事件，必须
        // 要设置表单项的 enableKeyEvents: true
        var myTextField = Ext.create('Ext.form.field.Text',{
            fieldLabel:'Name',
            name:'firstname',
            enableKeyEvents : true,

            // 设置最短最长限制
            minLength : 4,
            minLengthText: 'Name is too short, at least {0} chars..!',
            maxLength : 25,
            maxLengthText: 'Name is too long, max length is {0} chars..!'
        });

        // 侦听 keyup 事件
        myTextField.on({
            keyup:{
                fn: function( thisField, evt, eOpts ){
                    // evt 是 Ext 对本地事件的一个封装，
                    // 定义了许多方法和属性，如 ENTER 属性等。
                    if(evt.getCharCode() === evt.ENTER){
                        if (thisField.getValue()!=''){
                            Ext.Msg.alert('Alert','Welcome: '+ thisField.getValue() );
                        }
                    }
                }
            }
        });
        newItems.push( myTextField );

        return newItems;
    }
});
```












# 参考 

+ [Chapter5: Doing It with Forms](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
