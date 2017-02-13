---
title: 使用 ExtJS 6 的 Grid
date: 2017-02-13
writing-time: 2017-02-13 15:35
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

Ext Grid 具有丰富的功能，比如：分页、排序、过滤、查询、行编辑、单元格编辑、分组、浮动工具栏、buffered scrolling，列大小改变及隐藏、分组的表头、多级排序、行扩展等。

# Grid 基础

Grid 组件类，在 classic 工具集中名为 `Ext.grid.Panel`，而在 modern 工具集中是通过 `Ext.grid.Grid`，两者只有很小的差异。

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

# 排序

可以通过默认列菜单进行排序。列菜单可用来排序、隐藏或显示列。在 Grid 的列定义中，`sortabled: false` 将禁用











# 参考 

+ [Working with Grids](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
