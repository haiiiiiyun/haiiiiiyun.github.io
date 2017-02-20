---
title: ExtJS 6 图表功能
date: 2017-02-19
writing-time: 2017-02-19 11:08
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript Chart
---

# 图表类型

共有 3 种图表： 直角坐标图表 (cartesian chart)，极坐标图表 (polar chart) 和 空间填充图表 (spacefilling chart)。

## cartesian chart

Ext.chart.CartesianChart (xtype: cartesian 或 chart)。

这些图表有两个方向： X 和 Y。默认 X 是水平方向，而 Y 是垂直方向。使用直角坐标的图表有 column, bar, area, line, scatter。

## polar chart

Ext.chart.PolarChart (xtype: polar)。

这些图表有两个轴： 角度轴和径向轴。使用极坐标的图表有 pie 和 radar。

## spacefilling chart

Ext.chart.SpaceFillingChart (xtype: spacefilling)。

这些图表会填充图表的全部空间区域。


# Bar 和 Column 图表

创建这些图表，至少要提供 Store，轴和序列项设置。

## 基本的 Column 图表


```javascript
Ext.define('MyApp.model.Population', {
    extend: 'Ext.data.Model',
    fields: ['year', 'population']
});
Ext.define('MyApp.store.Population', {
    extend: 'Ext.data.Store',
    storeId: 'population',
    model: 'MyApp.model.Population',
    data: [
        { "year": "1610","population": 350 },
        { "year": "1650","population": 50368 },
        { "year": "1700", "population": 250888 },
        { "year": "1750","population": 1170760 },
        { "year": "1800","population": 5308483 },
        { "year": "1900","population": 76212168 },
        { "year": "1950","population": 151325798 },
        { "year": "2000","population": 281421906 },
        { "year": "2010","population": 308745538 }
    ]
});

var store = Ext.create("MyApp.store.Population");

Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 500,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'chart',
            insetPadding: { top: 60, bottom: 20, left: 20, right: 40 },
            store: store,
            axes: [
                {
                    type: 'numeric',
                    position: 'left',
                    grid: true,
                    title: { text: 'Population in Millions', fontSize: 16 }
                },
                {
                    type: 'category',
                    position: 'bottom',
                    title: { text: 'Year', fontSize: 16 }
                }
            ],
            series: [
                {
                    type: 'bar',
                    xField: 'year',
                    yField: ['population']
                }
            ],
            sprites: {
                type: 'text',
                text: 'United States Population',
                font: '25px Helvetica',
                width: 120,
                height: 35,
                x: 100,
                y: 40
            }
        }
    ]
});
```

在序列项 `series` 各项中， 类型设置为了 `bar`，从而 ExtJS 会呈现 Column 或 Bar 图表，默认为 Column 图表，如果要显示 Bar 图表，则还要设置 `flipXY: true`。

`sprites` 是可选配置，可设置表头等的信息。

各轴都可以设置 `grid` 属性，控制是否显示水平或垂直的网格。

`insetPadding` 用来设置边距，从而为图表的表头、坐标轴信息等留出位置。

## Bar 图表

在上节的代码基础上，只需将 `flipXY` 设置为 true，然后切换两轴的位置即可：

```javascript
Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 500,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'chart',
            flipXY: true,
            insetPadding: { top: 60, bottom: 20, left: 20, right: 40 },
            store: store,
            axes: [
                {
                    type: 'numeric',
                    grid: true,
                    position: 'bottom',
                    title: { text: 'Population in Millions', fontSize: 16 }
                },
                {
                    type: 'category',
                    position: 'left',
                    title: { text: 'Year', fontSize: 16 }
                }
            ],
            series: [
                {
                    type: 'bar',
                    xField: 'year',
                    yField: ['population']
                }
            ],
            sprites: {
                type: 'text',
                text: 'United States Population',
                font: '25px Helvetica',
                width: 120,
                height: 35,
                x: 100,
                y: 40
            }
        }
    ]
});
```

# 堆叠图表

如果想在 Column 图表的同一个分类上显示多个值，可以有两种方法：

1. 在同个分类柱上堆叠显示
2. 同个分类有两条柱子

要显示堆叠图表，Store 中需要有多个数值项，然后在 `series` 各项的 `yField` 中设置多个数值项。例如：

```javascript
Ext.define('MyApp.model.Population', {
    extend: 'Ext.data.Model',
    fields: ['year', 'total', 'slaves']
});

Ext.define('MyApp.store.Population', {
    extend: 'Ext.data.Store',
    storeId: 'population',
    model: 'MyApp.model.Population',
    data: [
        { "year": "1790", "total": 3.9, "slaves": 0.7 },
        { "year": "1800", "total": 5.3, "slaves": 0.9 },
        { "year": "1810", "total": 7.2, "slaves": 1.2 },
        { "year": "1820", "total": 9.6, "slaves": 1.5 },
        { "year": "1830", "total": 12.9, "slaves": 2 },
        { "year": "1840", "total": 17, "slaves": 2.5 },
        { "year": "1850", "total": 23.2, "slaves": 3.2 },
        { "year": "1860", "total": 31.4, "slaves": 4 },
    ]
});

var store = Ext.create("MyApp.store.Population");

Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 500,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'cartesian', // or chart
            insetPadding: { top: 60, bottom: 20, left: 20, right: 40 },
            store: store,
            axes: [
                {
                    type: 'numeric',
                    position: 'left',
                    grid: true,
                    title: { text: 'Population in Millions', fontSize: 16 }
                },
                {
                    type: 'category',
                    position: 'bottom',
                    title: { text: 'Year', fontSize: 16 }
                }
            ],
            series: [
                {
                    type: 'bar',
                    xField: 'year',
                    yField: ['total', 'slaves']
                }
            ],
            sprites: {
                type: 'text',
                text: 'United States Slaves Distribution 1790 to 1860',
                font: '16px Helvetica',
                width: 120,
                height: 35,
                x: 100,
                y: 40
            }
        }
    ]
});
```

如果要多柱显示，只需在 `series` 各项中设置 `stacked: false`，如：

```javascript
            series: [
                {
                    type: 'bar',
                    stacked: false,
                    xField: 'year',
                    yField: ['total', 'slaves']
                }
            ]
```

图表中还有一些常用的配置项：

+ tooltip: 为各 series 项设置提示信息
+ legend: 图表头信息，可以设置为显示在某个边（上下左右）
+ sprites: 一个数组，可以设置 header, footer 等信息

下面是使用例子：

```javascript
Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 500,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'cartesian', // or chart
            legend: { docked: 'bottom' },
            insetPadding: { top: 60, bottom: 20, left: 20, right: 40 },
            store: store,
            axes: [
                {
                    type: 'numeric',
                    position: 'left',
                    grid: true,
                    title: { text: 'Population in Millions', fontSize: 16 }
                },
                {
                    type: 'category',
                    position: 'bottom',
                    title: { text: 'Year', fontSize: 16 }
                }
            ],
            series: [
                {
                    type: 'bar',
                    xField: 'year',
                    stacked: false,
                    title: ['Total', 'Slaves'],
                    yField: ['total', 'slaves'],
                    tooltip: {
                        traceMouse: true,
                        style: 'background: #fff',
                        /*
                        renderer: function (toolTip, record, ctx) {
                              toolTip.setHtml('In ' + record.get('year') + ': Population total was ' + record.get('total') + ' m');
                          }
                        renderer: function(storeItem, item){
                            this.setHtml('In ' + storeItem.get('year') + ' ' + item.field + ' population was ' + storeItem.get(item.field) + ' m');
                        }*/
                    }
                }
            ],
            sprites: [
                {
                    type: 'text',
                    text: 'United States Slaves Distribution 1790 to 1860',
                    font: '16px Helvetica',
                    width: 120,
                    height: 35,
                    x: 100,
                    y: 40
                },
                {
                    type: 'text',
                    text: 'Source: http://www.wikipedia.org',
                    fontSize: 10,
                    x: 12,
                    y: 440
                }
            ]
        }
    ]
});
```

## 3D 效果

如果要实现 3D 效果，只需将 axes 中的 `type:'category'` 改为 `type:'category32'`，以及将 series 各项中的 `type:'bar'` 改为 `type:'bar3d'` 即可。


## Area 和 Line 图表

这两个也是直坐标图表。

### Area 图表

要显示为 Area 图表，只需将上面的 series 改为：

```javascript
series: [
    {
        type: 'area',
        xField: 'year',
        stacked: false,
        title: ['Total', 'Slaves'],
        yField: ['total', 'slaves'],
        style: {
            stroke: '#94ae0a',
            fillOpacity: 0.6
        }
    }
]
```

要设置 Area 图表的堆叠情况，只需设置 `stacked` 为 true 或 false。

### Line 图表

只需将 series 改为：

```javascript
series: [
    {
        type: 'line',
        xField: 'year',
        title: ['Total'],
        yField: ['total']
    },
    {
        type: 'line',
        xField: 'year',
        title: ['Slaves'],
        yField: ['slaves']
    }
]
```


# Pie 图表 （饼图）

通常用于报表中。使用 `Ext.chart.PolarChart` (xtype: polar) 实现。

## 基本饼图

series 中设置 `type` 为 `pie`，`angleField` 设置为 Store 中的数值域， `label` 设置为 Store 中的文本显示域即可：

```javascript
Ext.define('MyApp.store.Expense', {
    extend: 'Ext.data.Store',
    alias: 'store.expense',
    fields: [ 'cat', 'spent'],
    data: [
        { "cat": "Restaurant", "spent": 100},
        { "cat": "Travel", "spent": 150},
        { "cat": "Insurance", "spent": 500},
        { "cat": "Rent", "spent": 1000},
        { "cat": "Groceries", "spent": 400},
        { "cat": "Utilities", "spent": 300},
    ]
});

var store = Ext.create("MyApp.store.Expense");

Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 600,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'polar',
            legend: { docked: 'bottom' },
            insetPadding: { top: 100, bottom: 20, left: 20, right: 40 },
            store: store,
            series: [
                {
                    type: 'pie',
                    angleField: 'spent',
                    label: {
                        field: 'cat'
                    },
                    tooltip: {
                        trackMouse: true,
                        renderer: function (toolTip, record, ctx) {
                           var value = ((parseFloat(record.get('spent') / record.store.sum('spent')) * 100.0).toFixed(2));
                            toolTip.setHtml(record.get('cat') + ': ' + value + '%');
                        }
                    }
                }
            ]
        }
    ]
});
```

## Donut chart （圆环图）

只需为 series 中的各项设置 `donut` 属性值即可，值区间为 [0, 100], 如 40。

## 3D 饼图

Ext JS 6 对 3D 饼图功能作了增强，支持添加标签，并可对 3D 效果进行配置，如：

```javascript
Ext.create('Ext.Container', {
    renderTo: Ext.getBody(),
    width: 600,
    height: 500,
    layout: 'fit',
    items: [
        {
            xtype: 'polar',
            legend: { docked: 'bottom' },
            insetPadding: { top: 100, bottom: 20, left: 20, right: 40 },
            store: store,
            series: [
                {
                    type: 'pie3d',
                    donut: 50,
                    thickness: 70,
                    distortion: 0.5,
                    angleField: 'spend',
                    label: {
                        field: 'cat'
                    },
                    tooltip: {
                        trackMouse: true,
                        renderer: function (storeItem, item) {
                            var value = ((parseFloat(storeItem.get('spent') / storeItem.store.sum('spent')) * 100.0).toFixed(2));
                            this.setHtml(storeItem.get('cat') + ': ' + value + '%');
                        }
                    }
                }
            ]
        }
    ]
});
```

# 参考 

+ [Working with Charts](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
