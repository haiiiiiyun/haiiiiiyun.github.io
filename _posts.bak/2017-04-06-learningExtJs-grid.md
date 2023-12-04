---
title: ExtJS 中的 Grid --Learning ExtJS(4th)
date: 2017-04-06
writing-time: 2017-04-06 11:01--2017-04-08 17:02
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---


# 数据连接

Grid 面板的主要功能是显示数据，其数据来自 Store。Grid 负责显示数据，而 Store 负责获取、更新、清除和处理数据。


```javascript
// 定义测试的 Model 和 Store
Ext.define('Myapp.model.Contract',{
    extend:'Ext.data.Model',
    idProperty: 'id',
    fields: [
        {name: 'id' , type: 'int'},
        {name: 'contractId' , type: 'string'},
        {name: 'documentType' , type: 'string'}
    ]
});

Ext.define('Myapp.model.Customer', {
    extend:'Ext.data.Model',
    requires: ['Myapp.model.Contract'],
    idProperty:'id',
    fields:[
        {name: 'id' , type: 'int'},
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},
        {name: 'website' , type: 'string'},
        {name: 'status' , type: 'string'},
        {name: 'country' , type: 'string'},
        {name: 'sendnews', type: 'boolean'},
        {name: 'clientSince', type: 'date', dateFormat: 'Y-m-d H:i'},
        {name: 'contractInfo', reference: 'Contract', unique:true }
    ]
});

Ext.define('Myapp.store.customers.Customers', {
    extend: 'Ext.data.Store',
    model: 'Myapp.model.Customer',
    data: [
        {
            "id": 10001,
            "name": "Acme corp2",
            "phone": "+52-01-55-4444-3210",
            "website": "www.acmecorp.com",
            "status": "Active",
            "clientSince": "2010-01-01 14:35",
            "sendNews": true,
            "contractInfo":{
                "id":444,
                "contractId":"ct-001-444",
                "documentType":"PDF"
            }
        },
        {
            "id": 10002,
            "name": "Candy Store LTD",
            "phone": "+52-01-66-3333-3895",
            "website": "www.candyworld.com",
            "status": "Active",
            "clientSince": "2011-01-01 14:35",
            "sendNews": false,
            "contractInfo":{
                "id":9998,
                "contractId":"ct-001-9998",
                "documentType":"DOCX"
            }
        }
    ]
});

var myStore = Ext.create("Myapp.store.customers.Customers");

// 定义一个简单的 Grid
var myGrid = Ext.create('Ext.grid.Panel',{
    height: 250,
    width: 800,
    title: 'My customers',

    // Grid 的列定义
    columns: [
        {
            width: 70, // 该列的宽度，如果内容过长，会自动缩成 'xxx...'
            dataIndex: 'id',// Store Model 中的 'id' 项显示到该列
            text: 'Id' // 该列头标题
        },
        {
            width: 160,
            dataIndex: 'name',
            text: 'Customer name'
        },
        {
            width: 110,
            dataIndex: 'phone',
            text: 'Phone'
        },
        {
            width: 160,
            dataIndex: 'website',
            text: 'Website'
        },
        {
            width: 80,
            dataIndex: 'status',
            text: 'Status'
        },
        {
            width: 160,
            dataIndex: 'clientSince',
            text: 'Client Since'
        }
    ],
    store: myStore,
    renderTo: Ext.getBody()
});
```

# 列定义与 Renderer

Grid 的 `columns` 属性可以是一个数组，或者直接是一个对象。默认每列都是可排序的。

Ext 提供了多种类型的列，都位于 `Ext.grid.column` 命名空间内。

Renderer 用于定制 Grid 中每个单元格的行为和呈现方式，它会关联到每个列，并会运行以呈现/生成该列中的每个单元格。

Ext 内置的 Renderer 都定义在 `Ext.util.Format` 类中，例如 Ext.util.Format.dateRenderer, Ext.util.Format.uppercase 等。

```javascript
columns: [

    // 行号列（从 1 开始）
    {
        xtype: 'rownumberer',
        align: 'left', // 默认也为 right
        width: '50'
    },

    // 数字列
    // 用于显示数值数据，
    // 可通过 'format' 属性来设置显示数值的格式
    {
        xtype: 'numbercolumn',
        width: 70,
        dataIndex: 'id',
        text: 'Id',

        format: '000.00' // 显示的值为 10001.00, 10002.00 等
        //format: '0,000.00' // 显示的值为 10,001.00, 10,002.00 等
        // format: '0' // 这是默认格式，同 format:'0,000.00'
    },

    // 模板列
    // 定义 Ext.XTemplate 来设置显示格式
    // 由于会作用到所有的行上，故推荐使用简单模板，
    // 以减少对性能的影响,
    // 模板中使用 {} 来引用记录中的值
    //  使用 [] 来运行代码，其中的 `values` 指当前的记录对象
    {
        xtype: 'templatecolumn',
        text: 'Country',
        dataIndex: 'country',
        tpl: '<div><div class="flag_{[values.country.toLowerCase()]}">' +
            '&nbsp</div>&nbsp;&nbsp;{country}</div>
    },
    {
        xtype: 'gridcolumn', // 默认的列类型
        width: 150,
        dataIndex: 'name',
        text: 'Customer name',

        // 定义列的 renderer:
        // 其参数如下：
        //    value: 当前单元格对应的数值
        //    metaData: 当前单元格关联的 metadata，
        //              如 tdCls, tdAttr, tdStyle 等。
        //              可用来修改或覆盖内置的风格
        //    record: 当前行的记录
        //    rowIndex: 当前行索引
        //    colIndex: 当前列索引
        //    store: Grid Store
        //    view: Grid Panel
        // 返回是一个字符串，用来表示单元格的显示内容
        renderer: function(value, metaData, record, rowIndex, colIndex, store, view ){
            if (record.get('country')!="USA"){
                metaData.tdCls = 'customer_foregin';
            }
            return value;
        }
    },

    // 日期列
    // 基于本地设置或 format 属性值
    // 显示日期值
    {
        xtype: 'datecolumn',
        dataIndex: 'clientSince',
        width: 110,
        text: 'Client Since',
        format: 'Y-m-d', // 显示 2017-04-06
        //format: 'M-d-Y H:i', // 显示 Apr-06-2017 15:10

        // 当设置了 renderer 后， format 属性失效不起作用
        renderer: function(value, metaData, record, rowIndex, colIndex, store, view ){
            if (value.getFullYear() < 2014 ){
                metaData.tdStyle = " font-size:0.9em; color:#666; ";
            }
            return Ext.util.Format.date(value, 'Y-M-d');
        }
    },

    {
        width: 150,
        dataIndex: 'status',
        align:'center',
        text: 'Status',
        renderer: function(value, metaData, record, rowIndex, colIndex, store, view ){
            var myclass= 'cust_' + value.toLowerCase();
            metaData.tdCls = myclass;
            if (value.toLowerCase()=='inactive'){
                metaData.tdStyle = " font-size:0.9em; ";
            } else if (value.toLowerCase()=='suspended'){
                metaData.tdStyle = " font-size:0.9em; ";
                metaData.tdAttr = 'bgcolor="ffc6c6"';
            }
            return value;
        }
    },

    // 布尔列
    // 通过设置 falseText 和 trueText，可以
    // 将布尔值显示为不同的信息
    {
        xtype: 'booleancolumn',
        dataIndex:'sendnews',
        width: 120,
        text: 'Send News?',
        falseText: 'No',
        trueText: 'Yes'
    },

    // Checkbox 列
    // 在列中显示一个 checkbox
    // 一般用于 Grid 编辑功能中
    {
        xtype: 'checkcolumn',
        dataIndex:'sendnews',
        width: 120,
        text: 'Send News ?'
    },

    // 动作列
    // 可以显示多个图标，点击每个图标
    // 会触发处理函数
    {
        xtype: 'actioncolumn',
        width: 90,
        text: 'Actions',
        items: [
            {
                iconCls: 'editicon-16',
                tooltip: 'Edit customer',
                handler: function(grid, rowIndex, colIndex){
                    var rec = grid.getStore().getAt(rowIndex);
                    alert("Edit customer:" + rec.get('name'));
                }
            },
            {
                iconCls: 'sendmail-16',
                tooltip: 'Send email to customer',
                handler: function(grid, rowIndex, colIndex){
                    var rec = grid.getStore().getAt(rowIndex);
                    alert("Send email to :" + rec.get('name'));
                }
            },

            // icon, tooltip 也可以根据条件设置
            {
                getClass: function(v, meta, rec) {
                    if (rec.get('sendnews')==0) {
                        return 'sendmailblock-16';
                    } else {
                        return 'sendmail-16';
                    }
                },
                getTip: function(v, meta, rec) {
                    if (rec.get('sendnews')==0) {
                        return 'Do not Send';
                    } else {
                        return 'Send Email for news...!';
                    }
                },
                handler: function(grid, rowIndex, colIndex) {
                    var rec= grid.getStore().getAt(rowIndex),
                    action = (rec.get('sendnews')==0 ?'' : 'Send');
                    if (action==''){
                        Ext.Msg.alert('Alert..!', "you can't send news...!");
                    } else {
                        Ext.Msg.alert(action, action +' news to '+ rec.get('name'));
                    }
                }
            }
        ]
    }
]
```

# Widget 列

Ext Js 5 引用了一个轻量级的类 **widget** 及对应的 Grid 列 **widget column**。widget 类似组件，它主要由一个 Ext.dom.Element 及其关联的事件侦听器组成。但是，它们不是扩展至 Ext.Component。

我们可以自制 widget，但 Ext 内置有多个基本的 widget:

+ 进度条 (Ext.ProgressBarWidget 或 progressbarwidget)
+ 划动条 (Ext.slider.Widget 或 sliderwidget)
+ Sparklines (Ext.sparkline.*):
    - Line (sparklineline)
    - Bar (sparklinebar)
    - Discrete (sparklinediscrete)
    - Bullet (sparklinebullet)
    - Pie (sparklinepie)
    - Box (sparklinebox)
    - TriState (sparklinetristate)


```javascript
// 定义测试数据
Ext.define('Myapp.model.CustomerWidgets',{
    extend: 'Ext.data.Model',
    idProperty: 'id',
    fields: [
        {name: 'id', type: 'int'},
        {name: 'name', type: 'string'},
        {name: 'progress', type: 'float'},
        {name: 'piesequence'}
    ]
});

var myStore = Ext.create('Ext.data.ArrayStore',{
    model: 'Myapp.model.CustomerWidgets',
    data:[
        [10001,"Acme corp2", 0.75, [30,14,20,36]],
        [10002,"Candy Store LTD", 0.9, [50,14,20,16]],
        [10003,"Modern Cars of America", 0.35, [15,10,39,36]],
        [10004,"Extreme Sports Los Cabos", 0.174, [30,29,5,18]]
    ]
});

// 测试 widget 列
var myGrid = Ext.create('Ext.grid.Panel',{
    height: 250,
    width: 800,
    title: 'My customers',
    columns: [
        {
            xtype: 'rownumberer',
            align:'center'
        },
        {
            xtype: 'numbercolumn',
            dataIndex: 'id',
            text: 'Id',
            format: '0'
        },
        {
            width: 200,
            dataIndex: 'name',
            text: 'Customer name'
        },

        {
            xtype: 'widgetcolumn', // 设置为 widget 列
            text: 'Project Advances',
            dataIndex: 'progress',

            // widget 的配置信息
            widget: {
                // 进度条 widget
                xtype: 'progressbarwidget',

                // 这是一个 Ext.XTemplate 对象
                textTpl: [' <div style="font-size:0.9em;">{percent:number("0")}% done.</div> ']
            }
        },

        {
            xtype: 'widgetcolumn', // 设置为 widget 列
            text: 'Slider',
            width: 100,
            dataIndex: 'progress',
            widget: {
                xtype: 'sliderwidget',
                minValue: 0,
                maxValue: 1,
                decimalPrecision: 2,
                listeners: {
                    // 当用户有划动时更新记录中的 progress 值
                    change: function(slider, value) {
                        if (slider.getWidgetRecord) {
                            var rec = slider.getWidgetRecord();
                            if (rec) { rec.set('progress', value); }
                        }
                    }
                }
            }
        },
        {
            xtype: 'widgetcolumn', // 设置为 widget 列
            width: 100,
            align:'center',
            dataIndex:'piesequence',
            text: 'Pie chart',
            widget: { xtype: 'sparklinepie' } // 饼图
        }
    ],
    store: myStore,
    renderTo: Ext.getBody()
});
```

# 选择模式

Ext 中有 2 种主要的选择模式 `Ext.selection.RowModel (rowmodel)` 和 `Ext.selection.CellModel (cellmodel)`。

默认的是 rowmodel，在 Grid 中通过 selModel 属性来配置选择模式：

```javascript
selModel: {
    selType: 'rowmodel', // 设置为按行选择, 'cellrow' 为按单元格选择

    // mode 值为 3 种：
    //   - SINGLE: 一次只能选择一个元素
    //   - SIMPLE: 可通过一个一个选中多个元素
    //   - MULTI: 可用 Ctrl 和 Shift 键选中多个元素
    mode: 'SINGLE' 
}
```


下面是按行选择模式下的例子：

```javascript
{
    xtype: 'actioncolumn',
    width: 90,
    text: 'Actions',
    items: [{
        iconCls: 'editicon-16',
        tooltip: 'Edit customer',
        handler: function(grid, rowIndex, colIndex){
            var mysm = grid.getSelectionModel();

            // 如果是多选模式时，返回是多个记录，故是数组
            var selection = mysm.getSelection();
            var record = selection[0]; // 行记录
            alert('You are going to edit ' + record.get('name'));
        }
    }]
}
```

下面是按单元格选择模式下的例子：

```javascript
{
    xtype: 'actioncolumn',
    width: 90,
    text: 'Actions',
    items: [{
        iconCls: 'editicon-16',
        tooltip: 'Edit customer',
        handler: function(view, rowIndex, colIndex){
            // 从 Grid 中获取列配置对象
            var model = view.getNavigationModel();

            var columnName = model.column.text; // 列名
            var columnDataIndex = model.column.dataIndex; // 列值索引
            var myData = model.record.get(columnDataIndex); // 单元格数值
            alert('You are going to edit column: '+ columnName + ' with the value: ' + myData);
        }
    }]
}
```

# Grid 事件

```javascript
Ext.onReady(function(){
    Ext.tip.QuickTipManager.init();

    // 创建一个区域用来显示输出内容
    var myEventsArea = Ext.create('Ext.form.field.TextArea',{
        itemId:'myResultArea',
        width : 400,
        height : 200,
        renderTo:'myResults'
    });

    var myStore = Ext.create("Myapp.store.customers.Customers");

    var myGrid = Ext.create('Ext.grid.Panel',{
        // Grid config
        listeners:{

            // 当 Grid 呈现完成后触发
            render:{
                fn:function(grid, eOpts){
                    var myResult= Ext.ComponentQuery.query('#myResultArea')[0];
                    var currentText= '\n' + myResult.getValue();
                    myResult.setValue('Grid has render' + currentText);
                }
            },

            // 当某条记录被选中时触发（假设为行选择模式）
            select:{
                fn:function(grid, record, index, eOpts){
                    var myResult = Ext.ComponentQuery.query('#myResultArea')[0];
                    var currentText= '\n' + myResult.getValue();
                    myResult.setValue('Record #(' + (index + 1) + ') selected' + currentText);
                }
            },


            // 当 Grid 内的一个元素被点击时触发
            itemclick:{
                fn:function(grid, record, item, index, ev, Opts){
                    var myResult = Ext.ComponentQuery.query('#myResultArea')[0];
                    var currentText= '\n' + myResult.getValue();
                    var myNewMsg = 'Item #' + (index+1) + " was clicked (customer id=" + record.data.id + ")";
                    myresult.setValue(myNewMsg + currentText);
                }
            },

            // 当元素当前被选中的情况下，
            // 再按下按键时会触发
            itemkeydown:{
                fn:function(grid, record, item, index, ev, eOpts){
                    var myResult = Ext.ComponentQuery.query('#myResultArea')[0];
                    var currentText= '\n' + myResult.getValue();
                    var myNewMsg = '';
                    var myKey = ev.getKey();
                    if (myKey === ev.DELETE ){
                        myNewMsg = "Delete Record";
                    } else if (myKey == ev.RETURN ){
                        myNewMsg = "Edit customer #" + record.data.id + "";
                    } else if ((myKey === ev.N && ev.shiftKey)|| myKey=== ev.F8 ){
                        myNewMsg = "Add new record";
                    } else if ((myKey === ev.D && ev.shiftKey)){
                        myNewMsg = "view detail of customer #" + record.data.id + "";
                    } else if (myKey ===ev.F9 ){
                        myNewMsg = "Other action...";
                    } else {
                        return;
                    }
                    myResult.setValue(myNewMsg + currentText);
                }
            }
        }
    });
});
```

# Grid 的特性 (Feature)

特性是插件的一种，自 Ext Js 4 开始引用，所有特性都扩展至  `Ext.grid.feature.Feature`。它用于向 Grid 的创建过程加入附加功能。


## Ext.grid.feature.Grouping

该特性能将 Grid 行以分组显示。Store 和 Grid 需要协调才能使用该功能。

```javascript
Ext.define('Myapp.store.customers.Customers',{
    extend:'Ext.data.Store',
    model: 'Myapp.model.Customer',
    groupField: 'country', // 向 Store 和 Grid 指定用于分组的数据项
    autoLoad:true,
    proxy:{
        type:'ajax',
        url: 'serverside/customers.json',
        reader: {
            type:'json',
            rootProperty:'records'
        }
    }
});

// 创建一个 Feature 实例
var myGroupingFeature = Ext.create('Ext.grid.feature.Grouping',{

    // 分组标题头的模板
    // 模板中可引用的变量有：
    //  + groupField : String
    //      用于分组的数据项名
    //  + columnName : String
    //      groupField 如果有对应列，则为列标题名;
    //      否则为 groupField 名
    //  + groupValue : Mixed
    //      当前分组对应的分组数据项值
    //  + renderedGroupValue : String
    //      当前分组对应的分组数据项的呈现值，由列的 renderer 产生。
    //  + name : String
    //      renderedGroupValue 的别名
    //  + rows : Ext.data.Model[]
    //      已过时，用 `children` 来代替。 
    //      当前分组中所有记录的一个数组。
    //      如果在 Ext.data.BufferedStore 中则不可用。
    //  +children : Ext.data.Model[]
    //      同 `rows`
    // 模板中用 {} 引用变量，用 [] 来执行代码
    // [] 中的 `values` 是 Ext 在调用 XTemplate 时
    // 传入的参数值，表示当前作用域下的参数值。
    groupHeaderTpl: '{columnName}: {name} ({rows.length} Customer{ [values.rows.length > 1 ? "s" : ""]})',
    hideGroupedHeader: false, // 隐藏分组列的列标题
    startCollapsed: false // 初始就展开
});

var myGrid = Ext.create('Ext.grid.Panel',{
    height: 250,
    width: 900,
    title: 'My customers',
    columns: [ /* columns here....*/],
    features:[myGroupingFeature], //指定特性
    store: myStore,
    selModel:{
        selType:'rowmodel',
        mode:'SINGLE'
    },
    renderTo: 'myGrid'
});
```

## Ext.grid.feature.GroupingSummary

该特性要和 Grouping 特性一起使用，它在每个分组下添加一条概要行。概要行上的每列显示对应的概要信息。本特性内置的概要算法类型有: count, sum, min, max, average。

```javascript
var myGroupingSummaryFeature = Ext.create(
    'Ext.grid.feature.GroupingSummary',{
        groupHeaderTpl: '{columnName}: {name}',
        hideGroupedHeader: true,
        startCollapsed: false
});

//...
// 在需要显示分组概要信息的列定义上设置：
{
    xtype: 'numbercolumn',
    width: 100,
    dataIndex: 'id',
    text: 'Id',
    format: '000.00',
    summaryType: 'count', //本列的概要算法类型是计算个数值
    summaryRenderer: function(value){ // 本列概要信息的 renderer
        return Ext.String.format('{0} student{1}',
            value, value !== 1 ? 's': '');
    }
}

//...
{
    xtype: 'numbercolumn',
    dataIndex:'employees',
    width: 160,
    format: '0',
    text: 'Customer Employees',
    summaryType: 'sum' // 本列概要算法类型是计算总和
}

// 在 Grid 定义中
    features:[myGroupingFeature, myGroupingSummaryFeature],
```


## Ext.grid.feature.RowBody

本特性能为 Grid 的每行添加一个额外的 `Tr->Td->Div`，并能在其中设置任意的 HTML。它常用于显示与记录关联的额外信息。这个额外的显示部分还会向 Grid 视图触发事件，如 `rowbodyclick`, `rowbodydbclick`, `rowbodycontextmenu` 等。

```javascript
var myRowBodyFeature = Ext.create('Ext.grid.feature.RowBody',{
    getAdditionalData:function (data, index, record, orig){
        return { rowBody:'<span style="padding-left: 10px"><b>Website : </b> <a href="http://' + record.data.website + '" target= "_blank">' + record.data.website + '</a></span>' };
    }
});
```

## Ext.grid.feature.Summary

本特性为 Grid 的所有行增加一个概要行，各列对应的概要算法和 groupingsummary 一样，概要行的位置可以是 `bottom` 和 `top`。

```javascript
var mySummaryFeature = Ext.create('Ext.grid.feature.Summary',{
    dock:'bottom' // 位置也可以设置成 top
});
```

# 插件

使用插件，就能在不对组件进行扩展的情况下，增加额外的功能。Grid 的 2 个常用插件是 `Ext.grid.plugin.CellEditing` 和 `Ext.grid.plugin.RowEditing`，它们都扩展至 `Ext.grid.plugin.Editing`。

## Ext.grid.plugin.CellEditing

该插件能使单元格可编辑。每次只能编辑一个单元格，而编辑器由列定义中的 `editor` 指定。如果没有指定 `editor` 属性值，则该列中的单元格不能编辑。

```javascript
var myGrid = Ext.create('Ext.grid.Panel',{
    //...
    columns: [
        {
            width: 200,
            dataIndex: 'name',
            text: 'Customer name',
            // 定义编辑器
            editor:{
                xtype:'textfield',
                allowBlank:false,
                minLength:4,
                maxLength:70
            }
        },
        {
            xtype: 'datecolumn',
            dataIndex: 'clientSince',
            width: 150,
            text: 'Client Since',
            format: 'M-d-Y H:i',
            // 定义编辑器
            editor:{
                xtype: 'datefield',
                maxValue: new Date()
            }
        }
        //...
    ],
    store: myStore,

    // 设置为单元格选择模式
    selModel:{selType:'cellmodel'},

    plugins:{
        // 使用单元格编辑插件
        ptype:'cellediting',
        // 当双击时打开编辑器开始编辑
        clicksToEdit:2
    },
    renderTo: 'myGrid'
});
```


## Ext.grid.plugin.RowEditing

为 Grid 增加全行编辑功能。开始编辑时，该行中的所有可编辑单元格都会显示出编辑器，同时编辑行下会出现 `Save` 和 `Cancel` 按钮。

```javascript
var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
    // 单击就能切换到另一个单元格编辑
    clicksToMoveEditor: 1,
    autoCancel: false
});

var myGrid = Ext.create('Ext.grid.Panel',{
    //...
    columns: [
        {
            xtype: 'rownumberer',
            width: 50,
            align:'center'
            // 没有定义编辑器，故不能编辑
        },
        {
            width: 200,
            dataIndex: 'name',
            text: 'Customer name',
            editor:{ //定义编辑器
                xtype:'textfield',
                allowBlank:false,
                minLength:4
            }
        },
        {
            xtype: 'datecolumn',
            dataIndex: 'clientSince',
            width: 150,
            text: 'Client Since',
            format: 'M-d-Y H:i',
            editor:{
                xtype: 'datefield',
                maxValue: new Date()
            }
        }
    ],
    store: myStore,
    // 设置为行选择模式
    selModel: {selType:'rowmodel'},
    plugins: [rowEditing], //使用行编辑插件
    renderTo: 'myGrid'
}
```

没有定义 `editor` 属性的列不能编辑，如果列不能编辑，推荐为该列设置 `editRenderer` 属性，用来在行编辑时显示该列，如：

```javascript
{
    xtype: 'numbercolumn',
    dataIndex:'employees',
    width: 160,
    format: '0',
    text: 'Customer Employees',
    editRenderer: function(value){
        return 'can\'t edit'
    }
}
```

# Grid 分页

分页功能需要 Store 及 Grid 中的 PagingToolbar 配合才能进行。

```javascript
// Store 中设置 pageSize 和 totalProperty 等值
Ext.define('Myapp.store.customers.CustomersC',{
    extend:'Ext.data.Store',
    model: 'Myapp.model.Customer',
    pageSize: 3, // 每页记录数
    autoLoad:true,
    proxy:{
        type:'ajax',
        url: 'serverside/customersc.php',
        reader: {
            type:'json',
            rootProperty:'records',
            totalProperty:'total' //总记录数
        },
        actionMethods :{read:'POST'}
    }
});

// Grid 中加入 PagingToolbar
var myStore = Ext.create("Myapp.store.customers.CustomersC");
var myGrid = Ext.create('Ext.grid.Panel',{
    //...
    // bottom bar 中加入分页工具条
    store: myStore,
    bbar: [{
        // 分页工具条
        xtype: 'pagingtoolbar',
        // 该 store 必须和 Grid 的 store 相同
        store: myStore, 
        displayInfo: true,
        // {0}, {1} 指本页的开始和结束行数，{2} 指总行数
        displayMsg: 'Displaying customers {0} - {1} of {2}'
    }],
    renderTo: 'myGrid'
})
```

# 无限滚动 (Ininite scrolling)

从 Ext Js 5 开始，Grid 基于 `Ext.data.BufferedStore` 来进行无限滚动，而无需使用 PagingToolbar。

```javascript
// 定义一个 Buffered Store
Ext.define('Myapp.store.clients',{
    extend:'Ext.data.BufferedStore',
    model: 'Myapp.model.Customer',
    autoLoad: true,
    leadingBufferZone: 150, // 当滚动时，预先缓存额外的 150 条记录
    pageSize: 100, // 每页为 100 条记录
    proxy:{
        type:'ajax',
        url: 'serverside/clients.php',
        reader: {
            type:'json',
            rootProperty:'records',
            totalProperty:'total'
        }
    }
});

var myStore = Ext.create('Myapp.store.clients');
var myGrid = Ext.create('Ext.grid.Panel',{
    //...
    store: myStore,
    loadMask: true,
    selModel:{
        // 当使用分页或 Ext.data.BufferedStore 时，缓存的记录在当页面切换，
        // 或者行滚到视图外后会自动删除掉。
        // 以下设置将使缓存不被自动删除掉。
        pruneRemoved: false
    },
    renderTo: 'myGrid'
});
```


# 参考 

+ [Chapter6: Give Me the Grid](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
