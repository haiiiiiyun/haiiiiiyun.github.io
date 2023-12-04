---
title: ExtJS 的画图和图表功能--Learning ExtJS(4th)
date: 2017-04-12
writing-time: 2017-04-12 15:20--16:51
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 概述

Draw 和 Chart 是 Ext JS 框架的扩展功能，Ext JS 6 中，它的位置是 `ext-6.x.x/packages/charts/`。


# 基本绘画

Ext 基于 SVG 和 Canvas （根据浏览器的支持情况）进行绘画，Canvas 是默认引擎。

先在项目根目录下的 `app.json` 中添加 `"requires": ["charts"]`，以启用 charts 功能。

```javascript
Ext.require([
    'Ext.*',
    'Ext.draw.*'
]);

Ext.onReady(function(){
    var myDrawCmp = Ext.create('Ext.draw.Component', {
        viewBox: false,
        itemId:'mypaneldraw',
        items:[
            {
                type: 'circle',
                radius: 8,
                x: 250,
                y: 18,
                fill: 'blue',
                zIndex: 2
            },{
                type: 'rect',
                x: 0,
                y: 69,
                width: 200,
                height: 6,
                fill: 'blue'
            },{
                type: 'ellipse',
                cx: 265,
                cy: 215,
                rx: 40,
                ry: 25,
                fill: '#66cc33',
                globalAlpha: 1,
                stroke : '#993399',
                'stroke-width':2
            },{
                type: "path",
                path: "M 230 110 L 300 110 L 265 190 z",
                globalAlpha: 1,
                fill: '#16becc',
                lineWidth: 2
            },{
                type: 'text',
                x: 50,
                y: 50,
                text: 'Sencha',
                'font-size':'38px',
                fillStyle: 'blue'
            },{
                type: "image",
                src: "images/apple-touch-icon.png",
                globalAlpha: 0.9,
                x: 205,
                y: 20,
                height: 100,
                width: 100,
                listeners: {
                    dblclick: function(){
                        Ext.Msg.alert('Logo', 'event dblclick on Sencha logo');
                    }
                }
            }
        ]
    });

    Ext.create('Ext.Window', {
        title:'drawing components',
        closable:true,
        resizable:false,
        width: 600,
        height: 300,
        layout: 'fit',
        items: [myDrawCmp]
    }).showAt(30,50);
});
```

要画出 Circle, Rect, Path, Ellipse, Text, Image 等这些元素（也叫 sprites），Ext 要先创建一个 `Ext.draw.Surface` 实例，而该 Surface 实例需要包含在 `Ext.draw.Container` 中。绘画出的每个 sprites 元素也都能触发 dblclick 等事件。

显式调用 Sprite, Surface 类：

```javascript
var myDrawCmp = Ext.create('Ext.draw.Component', {
    viewBox: false,
    itemId:'mypaneldraw',
    style:'background-color:#999999',
    items: [{
        type: 'text',
        x: 10,
        y: 10,
        text: 'My Pac-Man',
        'font-size':'18px', //fontSize: 38,
        fillStyle: 'blue'
    }]
});

// 创建一个 Sprite
var myPacman = Ext.create('Ext.draw.Sprite', {
    type: "image",
    src: "images/pacman02.gif",
    x: 10,
    y: 50,
    height: 50,
    width: 50,
    zIndex: 3
});

// 增加到 Surface
myDrawCmp.surface.add([
    myPacman,
    {
        type: "image",
        src: "images/inkyghost.gif",
        x: 160,
        y: 50,
        height: 50,
        width: 50,
        zIndex: 2
    }
]);

myDrawCmp.surface.renderAll();
```

# 图表功能 (charts)

## Legend

用于定义序列名称的位置：

```javascript
legend: {
    docked: 'left' // possible values are left, top, bottom, right
}
```

## Axis

扩展至 Axis 和 Radial 类。

+ 分类轴 (category axis)
+ 数字轴 (numeric axis)
+ 时间轴 (time axis)


## Series

`series` 类具有画线和描点功能，同时还具有事件处理、动画、阴影、激变、位移等功能。类中还包含一个元素数组，用来表示序列中各元素的位置信息。

## 图表的主题

自定义的图表主题都扩展至 `Ext.chart.theme.Base`，如：

```javascript
Ext.define('Ext.chart.theme.MyChartTheme', {
    extend: 'Ext.chart.theme.Base',
    singleton: true,
    alias: [ // 两个别名都可以用
        'chart.theme.mycharttheme',
        'chart.theme.myChartTheme'
    ],
    config: {
        baseColor: '#65a9e0',
        gradients: {
            type: 'linear',
            degrees: 90
        }
    }
});
```

要在图表上使用上面的自定义主题，只需在图表上设置 `theme: 'mycharttheme'`。



# 参考 

+ [Chapter13: From Drawing to Charting](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
