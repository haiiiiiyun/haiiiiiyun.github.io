---
title: ExtJS 6 高级组件
date: 2017-02-18
writing-time: 2017-02-18 15:28--2017-02-19 11:07
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript Tree
---

# Tree Panel

Tree panel 将层级数据以树结构表示。

和 `Ext.grid.Panel` 类似，`Ext.tree.Panel` 也继承自 `Ext.panel.Table`，因此，它也支持多列功能。

和 Grid Panel 不同的是，Tree Panel 需要传入一个 Tree Store `Ext.data.TreeStore`。

## 基本树

创建 Tree Panel 时至少要传入一个 Tree Store 用于获取数据。以下例子中的 Tree Store 使用了硬编码的内联数据：

```javascript
var store = Ext.create('Ext.data.TreeStore', {
    root: {
        expanded: true,
        text: 'Continents',
        children: [
            {
                text: 'Antarctica',
                leaf: true
            },
            {
                text: 'South America',
                expanded: true,
                children: [
                    {
                        text: 'Brazil',
                        leaf: true
                    },
                    {
                        text: 'Chile',
                        leaf: true
                    }
                ]
            },
            {
                text: 'Asia',
                expanded: true,
                children: [
                    {
                        text: 'India',
                        leaf: true
                    },
                    {
                        text: 'China',
                        leaf: true
                    }
                ]
            },
            {
                text: 'Afria',
                leaf: true
            }
        ]
    }
});

Ext.create('Ext.tree.Panel', {
    title: 'Basic Tree',
    width: 200,
    height: 450,
    store: store,
    rootVisible: true,
    renderTo: Ext.getBody()
});
```

以上代码可以到 https://fiddle.sencha.com/ 上进行测试，观看效果。


## 为树添加拖放功能

只需在 Tree Panel 中添加 `treeviewdragdrop` 插件，然后在 Tree Store 中为每个结点设置 `checked` 属性值即可。

设置后，树中的结点可以进行拖放操作。代码如下：

```javascript
var store = Ext.create('Ext.data.TreeStore', {
    root: {
        expanded: true,
        text: 'Continents',
        checked: true,
        children: [
            {
                text: 'Antarctica',
                leaf: true,
                checked: false
            },
            {
                text: 'South America',
                expanded: true,
                checked: true,
                children: [
                    {
                        text: 'Brazil',
                        leaf: true,
                        checked: true
                    },
                    {
                        text: 'Chile',
                        leaf: true,
                        checked: true
                    }
                ]
            },
            {
                text: 'Asia',
                expanded: true,
                checked: true,
                children: [
                    {
                        text: 'India',
                        leaf: true,
                        checked: true
                    },
                    {
                        text: 'China',
                        leaf: true,
                        checked: true
                    }
                ]
            },
            {
                text: 'Afria',
                leaf: true,
                checked: true
            }
        ]
    }
});

Ext.create('Ext.tree.Panel', {
    title: 'Basic Tree',
    width: 200,
    height: 450,
    store: store,
    rootVisible: true,
    useArrows: true,
    lines: false,
    renderTo: Ext.getBody(),
    viewConfig: {
        plugins: {
            ptype: 'treeviewdragdrop',
            containerScroll: true
        }
    }
});
```

## Tree Grid

可以在 Tree 中添加多列来创建一个 Tree Grid。Tree 默认只有一列，它显示为 Tree Store 各结点中的 text 域的值。

Tree Grid 的 Tree Store 中需要有多个域。和 Grid 类似，Tree Grid 也有排序、过滤等功能。列通过 treecolumn 定义，和 Grid 类似，每个列也可以指定任何类型，如 checkbox, picture, button, URL 等。例子如下：

```javascript
var store = Ext.create('Ext.data.TreeStore', {
    root: {
        expanded: true,
        text: 'Continents',
        children: [
            {
                name: 'Antarctica',
                population: 0,
                area: 14,
                leaf: true
            },
            {
                name: 'South America',
                population: 385,
                area: 17.84,
                expanded: true,
                children: [
                    {
                        name: 'Chile',
                        population: 18,
                        area: 0.7,
                        leaf: true
                    }
                ]
            },
            {
                name: 'Asia',
                population: 4164,
                area: 44.57,
                expanded: true,
                children: [
                    {
                        name: 'India',
                        population: 1210,
                        area: 3.2,
                        leaf: true
                    },
                    {
                        name: 'China',
                        population: 1357,
                        area: 9.5,
                        leaf: true
                    }
                ]
            },
            {
                text: 'Afria',
                population: 1110,
                area: 30,
                leaf: true
            }
        ]
    }
});

Ext.create('Ext.tree.Panel', {
    title: 'Tree Tree',
    width: 500,
    height: 450,
    store: store,
    rootVisible: false,
    useArrows: true,
    lines: false,
    scope: this,
    renderTo: Ext.getBody(),
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 1,
            sortable: true,
            dataIndex: 'name'
        },
        {
            text: 'Population (millons)',
            sortable: true,
            width: 150,
            dataIndex: 'population'
        },
        {
            text: 'Area (millons km^2)',
            sortable: true,
            width: 150,
            dataIndex: 'area'
        },
    ]
});
```

# Data View

`Ext.view.View` (xtype: dataview) 可通过自定义模板显示数据，因此使用时需要提供自定义模板及 Data Store。而模板通过 `Ext.XTemplate` 定义。

Data view 为包含的项提供了各种事件，如 click, doubleclick, mouseover, mouseout 等。下面的例子中先创建了 Person 数据模型及 Data Store：

```javascript
Ext.define('Person', {
    extend: 'Ext.data.Model',
    fields: [
        { name: 'name', type: 'string' },
        { name: 'age', type: 'int' },
        { name: 'gender', type: 'int' }
    ]
});

Ext.create('Ext.data.Store', {
    id: 'employees',
    model: 'Person',
    data: [
        { name: 'Mike', age: 22, gender: 0 },
        { name: 'Woo', age: 32, gender: 1 },
        { name: 'John', age: 33, gender: 1 },
        { name: 'Kalai', age: 25, gender: 0 }
    ]
});
```

模板支持循环、条件判断等操作。要绑定数据模型中的域，可用 `{fieldname}` 形式进行：

```javascript
var empTpl = new Ext.XTemplate(
    '<tpl for=".">',
        '<div style="margin-bottom: 10px;" class="data-view">',
            '<table style="width:100%">',
                '<tr>',
                    '<td style="font-size: 100px;width:100px;" rowspan="3"><i class="fa fa-user"></i></td>',
                    '<td>Name: {name}</td>',
                '</tr>',
                '<tr>',
                    '<td>Age:{age}</td>',
                '</tr>',
                '<tr>',
                    '<td>Gender: <tpl if="gender == 1">',
                        '<i class="fa fa-mars"></i>',
                    '<tpl else>',
                        '<i class="fa fa-venus"></i>',
                    '</tpl></td>',
                '</tr>',
        '</div>',
    '</tpl>'
);
```

模板中用到了 awesome font, 故在 HTML 文件中还要加上 '<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/fontawesome/4.3.0/css/font-awesome.min.css">'。

创建 Data View，指定 Store，模板，以及用于确定 Data View 中元素的 CSS 选择子 itemSelector：

```javascript
Ext.create('Ext.view.View', {
    store: Ext.getStore('employees'),
    tpl: empTpl,
    itemSelector: 'div.data-view',

    renderTo: Ext.getBody(),
    listeners: {
        itemclick: function(node, rec, item, index, e){
            alert(rec.data.name);
        }
    }
});
```

itemSelector 确定的每个元素都会对应 Store 中的一条记录。而各种事件的处理函数，也是作用在由 itemSelector 确定的 HTML 元素上。


# 拖放功能

任何元素或组件都可使用拖放功能。实现拖放功能需要完成三件事：

1. 将元素配置为 draggable
2. 创建 drop target
3. 完成 drop target


## 配置为 draggable

为每个需要配置为 draggable 的元素对应创建一个 `Ext.dd.DD` 实例。例如，将所有 'pics' 下的 div 元素配置为 draggable：

```javascript
var pics = Ext.get('pics').select('div');
Ext.each(pics.elements, function(el) {
    var dd = Ext.create('Ext.dd.DD', el, 'picsDDGroup', {
        isTarget: false
    });
});
```

这里 `Ext.get` 是通过 DOM 结点的 ID 值返回一个 Ext.dom.Element 对象。而 `Ext.select` 是基于 CSS/XPath 选择子返回一个 CompositeElement 对象（元素的集合）。

## 创建 drop target

使用 `Ext.dd.DDTarget` 创建 drop target 容器：

```javascript
var albums = Ext.get('album').select('div');
Ext.each(album.elements, function(el){
    var albumDDTarget = Ext.create('Ext.dd.DDTarget', el, 'picsDDGroup');
});
```

## 完成 drop target

当 draggable 元素拖放到 drop target 上时，我们需要将该元素移到 drop target 容器中。这通过重载 Ext.dd.DD 实例的 onDragDrop 方法实现：

```javascript
var overrides = {
    onDragDrop: function(evtObj, targetElId){
        var dropEl = Ext.get(targetElId);

        if (this.el.dom.parentNode.id != targetElId) {
            dropEl.appendChild(this.el);
            this.onDragOut(evtObj, targetElId);
            this.el.dom.style.position = '';
            this.el.dom.style.top = '';
            this.el.dom.style.left = '';
        }
        else {
            this.onInvalidDrop();
        }
    },
    onInvalidDrop: function() {
        this.invalidDrop = true;
    }
}

// Apply this override to the instances of the DD element.
var albums = Ext.get('album').select('div');
var pics = Ext.get('pics').select('div');

Ext.each(pics.elements, function(el){
    var dd = Ext.create('Ext.dd.DD', el, 'picsDDGroup', {
        isTarget: false
    });
    Ext.apply(dd, overrides);
});
```


# 参考 

+ [Advanced Components](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
