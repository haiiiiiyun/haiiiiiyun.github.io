---
title: 使用 ExtJS 6 的 Grid
date: 2017-02-13
writing-time: 2017-02-13 15:35--2017-02-14 13:45
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

Ext Grid 具有丰富的功能，比如：分页、排序、过滤、查询、行编辑、单元格编辑、分组、浮动工具栏、buffered scrolling，列大小改变及隐藏、分组的表头、多级排序、行扩展等。

# Grid 基础

Grid 组件类，在 classic 工具集中名为 `Ext.grid.Panel`，在 modern 工具集中名为 `Ext.grid.Grid`，两者只有很小的差异。

创建 Grid 时，必须至少要指明有哪些列，以及用于获取数据的 Store。

下面的例子创建了一个 Grid：

```javascript
Ext.define('Product', {
    extend: 'Ext.data.Model',
    fields: ['id', 'productname', 'desc', 'price']
});

var productStore = Ext.create('Ext.data.Store', {
    model: 'Product',
    data: [
        {
            id: 'P1',
            productname: 'Ice Pop Maker',
            desc: 'Create fun and healthy treats anytime',
            price: '$16.33'
        },
        {
            id: 'P2',
            productname: 'Stainless Steel Food Jar',
            desc: 'Thermos double wall vacuum insulated food jar',
            price: '$14.87'
        },
        {
            id: 'P3',
            productname: 'Shower Caddy',
            desc: 'No-slip grip keeps your caddy i place',
            price: '$17.99'
        },
        {
            id: 'P4',
            productname: 'VoIP phone Adapter',
            desc: 'Works with Up to Four VoIP Services Across One Phone Port',
            price: '$47.50'
        }
    ]
});

Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: productStore,
    width: 600,
    title: 'Products',
    columns: [
        {
            text: 'Id',
            dataIndex: 'id',
            hidden: true
        },
        {
            text: 'Name',
            width: 150,
            dataIndex: 'productname'
        },
        {
            text: 'Description',
            dataIndex: 'desc',
            sortable: false,
            flex: 1 // 将占据该行剩下的所有空间
        },
        {
            text: 'Price',
            dataIndex: 'price',
            width: 100,
        }
    ]
});
```

## 排序

可以通过默认列菜单进行排序。列菜单可用来排序、隐藏或显示列。在 Grid 的列定义中，`sortable: false` 将禁用基于该列的排序操作。排序操作默认都在客户端进行，要在服务端进行，在列定义中设置 `remoteSort: true`，此后每次排序都将排序信息（排序列和排序次序）发送到服务端。

## Renderer

列定义体中的 `renderer` 属性值可以设置为一个函数，用来修改该列数据的呈现方式，例如修改上例中 price 列的数值显示方式，加前缀 `$`：

```javascript
columns:[
//...
    {
        text: 'Price',
        dataIndex: 'price',
        width: 100,
        renderer: function(value){
            return Ext.String.format('${0}', value);
        }
    }
]
```

通过 `renderer` 函数还可以在列中显示 HTML 标签，添加 URL 和图片等。

## 过滤

要添加过滤功能，只需在 Grid 中加入 `Ext.grid.filters.Filters` 插件(ptype: gridfilters)，然后在相应列定义中添加过滤配置即可：

```javascript
Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: productStore,
    width: 600,
    title: 'Products',
    plugins: 'gridfilters',
    columns: [
        {
            text: 'Id',
            dataIndex: 'id',
            hidden: true
        },
        {
            text: 'Name',
            width: 150,
            dataIndex: 'productname',
            filter: 'string'
        },
        {
            text: 'Description',
            dataIndex: 'desc',
            sortable: false,
            flex: 1, // 将占据该行剩下的所有空间
            filter: {
                type: 'string',
                itemDefaults: { emptyText: 'Search for...' }
            }
        },
        {
            text: 'Price',
            dataIndex: 'price',
            width: 100,
        }
    ]
});
```

之后，相应列的列菜单中都会有过滤菜单项。每个列都可以设置过滤类型，如 string, bool 等，以及其它的配置信息如 emptyText 等。

上面例子中，过滤配置都是在创建 Grid 时设置的，当然，在创建 Grid 之后也可以设置过滤信息。


## 分页

通过使用 `Ext.toolbar.Paging`(xtype: pagingtoolbar) 添加分页工具条。下面例子中，我们将分页工具条添加到 `dockedItems` 中，这是 `Ext.panel.Panel` 的一个属性，并且将该工具条放置在 Panel 的 top, bottom, left, right 侧。

```javascript
Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: productStore,
    width: 600,
    title: 'Products',
    columns: [
        {
            text: 'Id',
            dataIndex: 'id',
            hidden: true
        },
        {
            text: 'Name',
            width: 150,
            dataIndex: 'productname'
        },
        {
            text: 'Description',
            dataIndex: 'desc',
            sortable: false,
            flex: 1 // 将占据该行剩下的所有空间
        },
        {
            text: 'Price',
            dataIndex: 'price',
            width: 100,
        }
    ],
    dockedItems: [
        {
            xtype: 'pagingtoolbar',
            store: productStore,
            dock: 'bottom',
            displayInfo: true
        }
    ]
});
```

然后为分页工具条的 Store 设置分页信息：

```javascript
var productStore = Ext.create('Ext.data.Store', {
    model: 'Product',
    pageSize: 10,
    autoLoad: true,
    proxy: {
        type: 'ajax',
        url: 'data.json',
        reader: {
            type: 'json',
            rootProperty: 'data',
            totalProperty: 'total'
        }
    }
});
```

分页工具条必须要有 Store 的 `totalProperty` 信息才能正常工作。`pageSize` 用来向服务器限制返回记录条数。URL 请求会类似为： `http://localhost:8000/data.json?page=1&start=0&limit=10`。


## 单元格编辑

在 Grid 中添加 `Ext.grid.plugin.CellEditing` 插件（ptype: cellediting)，然后在相应列定义中设置编辑器。编辑器可以是一个 textfield，combobox，data picker, number field 等所有支持的 form 项。例如：

```javascript
Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: productStore,
    width: 600,
    title: 'Products',
    plugins: ['cellediting', 'gridfilters'],
    columns: [
        {
            text: 'Id',
            dataIndex: 'id',
            hidden: true
        },
        {
            text: 'Name',
            width: 150,
            dataIndex: 'productname',
            editor: {
                allowBlank: false,
                type: 'string'
            }
        },
        {
            text: 'Description',
            dataIndex: 'desc',
            sortable: false,
            flex: 1 // 将占据该行剩下的所有空间
        },
        {
            text: 'Price',
            dataIndex: 'price',
            width: 100,
            editor: new Ext.form.field.ComboBox({
                typeAhead: true,
                triggerAction: 'all',
                store: [
                    ['1.0', '1.0'],
                    ['10.0', '10.0'],
                    ['100.0', '100.0'],
                    ['1000.0', '1000.0']
                ]
            })
        }
    ]
});
```

还可以给编辑器设置验证器。记录修改后，默认不会保存到服务器上。我们需要将 Store 的 `autosync` 设置为 true，从而任何的 CRUD 操作都会向服务器触发请求。如果不想立即同步，也可以通过调用 Store 的 `save` 或 `sync` 方法进行保存，比如在 Grid 表添加一个 “保存” 按钮来调用。


## 行编辑

行编辑每次对整行进行编辑。开启行编辑只需在 Grid 中加入 `Ext.grid.plugin.RowEditor` (ptype: rowediting) 插件，在设置单元格编辑的基本上，只需将插件中的 `cellediting` 替换为 `rowediting` 即可（因为行编辑还是需要设置每个单元格的编辑器）。

## 分组

要对列进行分组，只需在 Store 中通过 `groupField` 属性指定要分组的项，然后在 Grid 中设置 `Ext.grid.feature.Feature`，例如：

```javascript
var productStore = Ext.create('Ext.data.Store', {
    model: 'Product',
    pageSize: 10,
    autoLoad: true,
    proxy: {
        type: 'ajax',
        url: 'data.json',
        reader: {
            type: 'json',
            rootProperty: 'data',
            totalProperty: 'total'
        }
    },
    groupField: 'type'
});

Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: productStore,
    width: 600,
    title: 'Products',
    features: [
        { // 添加分组特性
            id: 'group',
            ftype: 'grouping',
            groupHeaderTpl: '{name}',
            hideGroupedHeader:  true,
            enableGroupingMenu: true // 在列菜单中动态分组
        }
    ],
    columns: [
        {
            text: 'Id',
            dataIndex: 'id',
            hidden: true
        },
        {
            text: 'Name',
            width: 150,
            dataIndex: 'productname'
        },
        {
            text: 'Description',
            dataIndex: 'desc',
            sortable: false,
            flex: 1, // 将占据该行剩下的所有空间
            groupable: false // 禁止该列分组
        },
        {
            text: 'Price',
            dataIndex: 'price',
            width: 100,
        },
        {
            text: 'Type',
            width: 100,
            dataIndex: 'type'
        }
    ]
});
```

`groupHeaderTpl` 设置分组头中的显示模板，可以在其中显示分组中的记录条数等信息，如 `groupHeaderTpl: '{columnName}: {name} ({rows.length} Item{[values.rows.length > 1 ? "s":""]})'`。

# Pivot grid

它能根据选择的行列数据，重组并按行轴或列轴统计出所需的报表。

Pivot Grid 是 ExtJS 的高级组件，需要另外下载后才能使用。

下面例子中，某公司的员工花费列表如下：

```javascript
var store = new Ext.data.JsonStore({
    proxy: {
        type: 'ajax',
        url: 'expense.json',
        reader: {
            type: 'json',
            rootProperty: 'rows'
        }
    },
    autoLoad: true,
    fields: [
        { name: 'id', type: 'int'},
        { name: 'employee', type: 'string'},
        { name: 'amount', type: 'int'},
        { name: 'date', type: 'date', dateFormat: 'd/m/Y'},
        { name: 'cat', type: 'string'},
        { 
            name: 'year', 
            convert: function(v, record){
                return Ext.Date.format(record.get('date'), "Y");
            }
        }
    ]
});

```

用于测试可以使用一个硬编码的 store 如下：

```javascript
var store = Ext.create('Ext.data.Store', {
    fields: [
        { name: 'id', type: 'int'},
        { name: 'employee', type: 'string'},
        { name: 'amount', type: 'int'},
        { name: 'date', type: 'date', dateFormat: 'd/m/Y'},
        { name: 'cat', type: 'string'},
        { 
            name: 'year', 
            convert: function(v, record){
                return Ext.Date.format(record.get('date'), "Y");
            }
        }
    ],
    data: [
        {
            id: 1,
            employee: 'David Smith',
            amount: 345,
            date: '1/5/2011',
            cat: 'Food',
            year: 2011
        },
        {
            id: 1,
            employee: 'David Smith',
            amount: 345,
            date: '1/5/2012',
            cat: 'Hotel',
            year: 2012
        },
        {
            id: 1,
            employee: 'David Smith',
            amount: 435,
            date: '1/5/2013',
            cat: 'Travel',
            year: 2013
        },
        {
            id: 2,
            employee: 'John Smith',
            amount: 23,
            date: '1/5/2011',
            cat: 'Food',
            year: 2011
        },
        {
            id: 2,
            employee: 'John Smith',
            amount: 2363,
            date: '1/5/2012',
            cat: 'Hotel',
            year: 2012
        },
        {
            id: 2,
            employee: 'John Smith 234',
            amount: 435,
            date: '1/5/2013',
            cat: 'Travel',
            year: 2013
        }
    ]
});

```


创建 Pivot Grid，需要提供轴 Axis 和分组聚合类型 aggregation 的相关信息。

例如： 

```javascript
// 轴定义类似 Grid 的列定义，也可以设置排序方向，filter 等。

//定义左侧轴就是 employee 列：
leftAxis: [{
    width: 80,
    dataIndex: 'employee',
    header: 'Employee'
}]

//定义上边轴是由数据集中的 cat 的值动态生成中，相当于 Grid 的
// cat 列横向显示
topAxis: [{
    dataIndex: 'cat',
    header: 'Category',
    direction: 'ASC'
}]

aggregate: [{
    measure: 'amount', //进行计算的列/项
    header: 'Expense',
    aggregator: 'sum', //也可以为 avg, min, max 等
    align: 'right',
    width: 85,
    renderer: Ext.util.Format.numberRenderer(0,000.00')
}]
```

创建 Pivot Grid, 其左侧轴是固定的，但上边轴是基于报表类型动态生成的：

```javascript
var pivotGrid = Ext.create('Ext.pivot.Grid', {
    renderTo: Ext.getBody(),
    title: 'Pivot Grid - Employee Expense Claims',
    height: 600,
    width: 700,
    enableLocking: false,
    viewConfig: {
        trackOver: true,
        stripeRows: true
    },

    tbar: [
        {
            xtype: 'combo',
            fieldLabel: 'Select report',
            flex: 1,
            editable: false,
            value: '1',
            store: [
                ['1', 'How much an employee claimed in total?'],
                ['2', 'What are the expense amounts of each employee in each category?'],
                ['3', 'How much an employee claimed in a specific year?'],
            ],
            listeners: {
                select: function(combo, records, eOpts){
                    switch(records.get('field1')){
                        case '1':
                            pivotGrid.reconfigurePivot({
                                topAxis: []
                            });
                            break;
                        case '2':
                            pivotGrid.reconfigurePivot({
                                topAxis: [{
                                    dataIndex: 'cat',
                                    header: 'Category',
                                    direction: 'ASC'
                                }]
                            });
                            break;
                        case '3':
                            pivotGrid.reconfigurePivot({
                                topAxis: [{
                                    dataIndex: 'year',
                                    header: 'Year',
                                    direction: 'ASC'
                                }]
                            });
                            break;
                    }
                }
            }
        }
    ],
    store: store,

    aggregate: [{
        measure: 'amount',
        header: 'Expense',
        aggregator: 'sum',
        align: 'right',
        width: 85,
        renderer: Ext.util.Format.numberRenderer('0,000.00')
    }],

    leftAxis: [{
        width: 80,
        dataIndex: 'employee',
        header: 'Employee'
    }],

    topAxis: []
});
```

# 参考 

+ [Working with Grids](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
