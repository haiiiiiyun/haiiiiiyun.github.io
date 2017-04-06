---
title: ExtJS 中的表单--Learning ExtJS(4th)
date: 2017-04-05
writing-time: 2017-04-05 15:25--2017-04-06 10:58
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

表单组件用于收集和编辑数据。

# 表单组件

`Ext.form.Panel` 组件扩展至 `Ext.panel.Panel`，并且组合了 `Ext.form.Basic`，从而包含了表单提交等表单处理功能。

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

类 `Ext.form.field.Base` 定义了表单项的通用属性、方法和事件。该其类扩展至 `Ext.form.Labelable` 和 `Ext.form.field.Field`（使用 mixin 方式）。

Labelable 类实现了标签的显示及错误提醒显示。

Field 类实现了对值的管理，并实现了 2 个重要方法： `getValue()` 和 `setValue()`。同时又引用了 `raw value` 的概念。

`raw value` 的例子：当从服务端获取以字符串表示的日期值时，`raw value` 就是文本形式的日期值，而日期表单项的值将是 JavaScrit 的 Date 对象。


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
    //height: 280,
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
            maxLengthText: 'Name is too long, max length is {0} chars..!',

            // 每个表单项都有一个 msgTarget 属性，
            // 用来设置表单错误信息的显式方式，值为：
            //   qtip: tip 形式显式，鼠标放上后显式，这是默认值
            //   under: 显式在表单项下面
            //   side:  在表单项右侧显式一个红点
            msgTarget: 'side'
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

        // Number 表单项只接受数值。
        // 可以定制接受的数值范围(min, max)，
        // 小数点位置等。
        // 还自带 spinner/trigger 组件便于进行数值的增加/减少操作。
        var myAgeField = Ext.create('Ext.form.field.Number',{
            fieldLabel:'Age',
            name:'age',
            minValue: 18,
            maxValue: 70,
            allowDecimals : false, // 小数点后数字会自动删除

            // 也可以隐藏自带的 spinner/trigger
            // 隐藏后该表单项会和 text field 类似。
            // 当表单项设置了多个 trigger 后，
            // hideTrigger 默认会自动设置成 true
            hideTrigger: true
        });

        var myIncomeField = Ext.create('Ext.form.field.Number',{
            fieldLabel:'Income',
            name:'income',
            minValue: 0,
            allowDecimals : true,
            decimalPrecision : 2, // 最多 2 位小数
            negativeText : 'The income cannot be negative..!',
            msgTarget:'side',

            // 当用 spinner/trigger 组件进行数值更新时，
            // 用 step 设置步进值 (默认为 1)
            step: 500
        });

        newItems.push( myAgeField );
        newItems.push( myIncomeField );

        // ComboBox 表单项可以显示一组选项，其数值来自 Store。
        // 创建一个 Store 实例
        var occupationStore = Ext.create('Ext.data.Store',{
            fields: ['id', 'name'],
            data : [
                {id: 1 ,name: 'CEO' },
                {id: 2 ,name: 'Vicepresident' },
                {id: 3 ,name: 'Marketing manager' },
                {id: 4 ,name: 'Development manager' },
                {id: 5 ,name: 'Sales manager' }
            ]
        });

        // Store 也可以通过 AJAX 获取数据
        /*
        var occupationStore = Ext.create('Ext.data.Store',{
            fields : ['id','name'],
            autoLoad:true,
            proxy:{
                type:'ajax' ,
                url :'serverside/occupations.json',
                reader:{
                    type:'json',
                    root:'records'
                }
            }
        });
        */


        // 创建 Combobox 表单项，
        // 当有输入时，会自动根据输入过滤可选项
        var myFirstCombo = Ext.create('Ext.form.ComboBox', {
            fieldLabel: 'Occupation',
            name:'employeeoccupation',
            store: occupationStore,
            queryMode: 'local',
            displayField: 'name',
            valueField: 'id'
        });

        // 侦听选择事件
        // 当 combobox 配置为允许多选时，
        // record 参数是一个数组
        myFirstCombo.on('select', function(combo, record){
            Ext.Msg.alert('Alert', record.get('name'));
        });
        newItems.push( myFirstCombo);


        // Tag 表单项在 Ext Js 5 时引入，它是 ComboBox 的子类。
        // 它能进行多选。
        var zonesStore = Ext.create('Ext.data.Store',{
            fields : ['id','name'],
            data : [
                {id: 1 ,name: 'Zone A' },
                {id: 2 ,name: 'Zone B' },
                {id: 3 ,name: 'Zone C' },
                {id: 4 ,name: 'Zone D' },
                {id: 5 ,name: 'Zone E' }
            ]
        });

        var myFirstTag =Ext.create('Ext.form.field.Tag', {
            fieldLabel: 'Select zone',
            store: zonesStore,
            displayField: 'name',
            valueField: 'id',
            filterPickList: true, // 在可选列表中删除掉已选择了的选项
            queryMode: 'local'
        });
        newItems.push( myFirstTag );

        // Date 表单项
        var datefield = Ext.create('Ext.form.field.Date',{
            fieldLabel: 'Birthday',
            name: 'birthday',
            format: 'd/m/Y', // 用于手工输入以及显式的格式，如 04/06/2017

            // 用来提交的格式，如 2017-04-06
            // 'Y-m-d' 就是常用的 'yyyy-mm-dd'，见 Ext.Date 对象文档
            submitFormat: 'Y-m-d',

            // 输入这些格式也有效
            altFormats: 'd-m-Y|d m Y|d.m.Y',

            // 还可以设置 minValue, maxValue
            // 以及禁用一些日期，如周末，假期等：
            disabledDates: ['31/12/2014','01/01/2015']
            // 也可以用正则表达式来匹配一组禁用日期：
            // disabledDates: ['../03/2012'], // 表示禁用 2012 年 3 月的每天
            // disabledDates: ['../03/..'], // 表示禁用每年 3 月的每天
            // disabledDates: ['05/03', '21/03'], // 表示禁用每年 3 月 5 号和 21 号

            // 和 ComboxBox 类似，也可以侦听 select 事件

        });
        newItems.push( datefield );


        // Checkbox
        var mysinglecheckbox = Ext.create('Ext.form.field.Checkbox',{
            fieldLabel:' ', // 设置为空白符，则不显式 fieldLabel
            labelSeparator:' ', // fieldLabel 与表单项间的分隔符，通常是 ':'

            // 显式在格子的右边
            boxLabel: 'employee has hobbies ? ',
            name: 'hobbies'
        });
        newItems.push( mysinglecheckbox );

        //CheckboxGroup
        // 其中 Checkbox 可以水平或垂直排列
        var groupCheckboxes = Ext.create('Ext.form.CheckboxGroup',{
            fieldLabel: 'Hobbies',
            columns: 2, // 排成 2 列
            items: [
                {name: 'hobby',boxLabel: 'Videogames',inputValue: 'vg'},
                {name: 'hobby',boxLabel: 'Sports',inputValue: 'sp'},
                {name: 'hobby',boxLabel: 'Card games',inputValue: 'cg'},
                {name: 'hobby', boxLabel:'Movies',inputValue: 'mv'},
                {name: 'hobby', boxLabel:'Collecting toys',inputValue: 'ct'},
                {name: 'hobby', boxLabel:'Music',inputValue: 'ms'},
                {name: 'hobby', boxLabel:'Others...',inputValue: 'ot'}
            ]
        });
        newItems.push( groupCheckboxes );


        // Radio 和 RadioGroup
        var radioYes = Ext.create('Ext.form.field.Radio',{
            name: 'option',
            fieldLabel: 'Employee has a car?',
            labelSeparator : '',
            boxLabel: 'Yes',
            inputValue : true
        });

        var radioNo = Ext.create('Ext.form.field.Radio',{
            name: 'option',
            hideLabel:true,
            boxLabel: 'No',
            inputValue: false
        });
        newItems.push( radioYes, radioNo );

        var radioGroup = {
            xtype: 'radiogroup',
            fieldLabel: 'Employee level',
            columns: 2,
            vertical:true, // 先按垂直排列
            items: [
                { boxLabel: 'Beginner', name: 'rb', inputValue: '1' },
                { boxLabel: 'Intermediate', name: 'rb', inputValue: '2'},
                { boxLabel: 'Advanced', name: 'rb', inputValue: '3',
                    checked: true
                },
                { boxLabel: 'Ninja', name: 'rb', inputValue: '4' }
        ]};
        newItems.push( radioGroup );


        // 表单项容器
        // Ext 不仅只能用 RadioGroup 和 CheckboxGroup 来组合 Radio 和 Checkbox，
        // 表单项容器可以组合任何类型的表单项。
        // 使用表单项容器的好处是能用布局来排序组件。
        var myFieldContainer = {
            xtype: 'fieldcontainer', //表单项容器
            height: 45, //必须要设置高度
            fieldLabel: 'Shoes / Dress size',
            layout: { type: 'hbox', align: 'stretch' }, // hbox 布局
            items: [
                {
                    xtype: 'numberfield',
                    flex: 1,
                    hideLabel:true // 由于容器已经有 fieldLabel 了，故这里隐藏
                },
                {
                    xtype: 'splitter' //Step 3
                },
                {
                    xtype: 'combobox',
                    flex: 1,
                    hideLabel:true,
                    labelWidth: 10,
                    store:Ext.create('Ext.data.Store',{
                        fields : ['id','name'],
                        data: [
                            {id:1 ,name:'small'},
                            {id:2 ,name:'medium'},
                            {id:3 ,name:'large'},
                            {id:4 ,name:'Xl'},
                            {id:5 ,name:'XXL'}
                        ]
                    }),
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id'
                }
            ]
        };
        newItems.push( myFieldContainer );

        // Trigger
        // Ext Js 5 开始， Trigger 表单项已经过时了，
        // 现 trigger 可以使用 Text 表单项实现，
        // 即可以将多个 trigger 添加到单个表单项中
        var myTriggers = Ext.create( 'Ext.form.field.Text' , {
            fieldLabel: 'My Field with triggers',

            // 设置多个 Trigger
            triggers: {
                searchtext: { // 这是一个 trigger 的配置体
                    cls: 'x-form-search-trigger', // trigger 的显式内容（图标）
                    handler: function() { // 点击时的处理函数
                        Ext.Msg.alert('Alert', 'Trigger search was clicked');
                        this.setValue('searching text...');
                    }
                },
                cleartext: { // 另一个 trigger 的配置体
                    cls: 'x-form-clear-trigger',
                    handler: function() {
                        Ext.Msg.alert('Alert', 'Trigger clear was clicked');
                        this.setValue('');
                    }
                }
            }
        });
        newItems.push( myTriggers );

        return newItems;
    }
});

// 创建一个实例
Ext.create('Myapp.view.AvailableFields01', {
    renderTo: Ext.getBody()
});
```


# 提交

Ext.form.Panel 类中有一个 `Ext.form.Basic` 类的实例，用来管理表单数据。

```javascript
Ext.define('Myapp.view.CustomerForm02', {
    //...
    initComponent: function() {
        var me = this;
        me.dockedItems= [{
            xtype: 'toolbar',
            dock: 'bottom',
            items: [
                {
                    xtype: 'tbfill' // ->
                },
                {
                    xtype: 'button',
                    iconCls: 'save-16',
                    text: 'Save...',
                    handler:function(){
                        this.submitMyForm();
                    },
                    scope:this
                }
            ]
        }];
        Ext.applyIf(me,{});
        me.callParent(arguments);
    },

    submitMyForm:function (){
        var me = this;
        me.getForm().submit({
            url:'serverside/submitaction.php',
            success: function(form, action){
                Ext.Msg.alert('Success', 'Successfully saved');
            },
            failure: function(form,action){
                Ext.Msg.alert('Failure', 'Something is wrong');
            }
        });
    }
});
```

# 参考 

+ [Chapter5: Doing It with Forms](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
