---
title: ExtJS 的响应式功能--Learning ExtJS(4th)
date: 2017-04-12
writing-time: 2017-04-12 14:29--15:02
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 概述

Ext JS 5 开始已支持触屏设备。可用于触屏设备的主题有 **Neptune Touch**, **Crisp Touch** 等。这些主题都支持基本的触屏输入，并优化了尺寸设计（字体和图标更大）。

Ext JS 能自动将鼠标事件转化成对应的触屏事件，例如：

```javascript
myDivElement.on('mousedown', function(e) {
    // event handling logic here
});
```

会转化成：

```javascript
myDivElement.on('touchstart', function(e) {
    // event handling logic here
});

//或转化成
myDivElement.on('pointerdown', function(e) {
    // event handling logic here
});
```

但是目前 Ext 不能自动转化所有的触屏交互。故一些特殊的事件需要专门处理。

触屏和浏览器的 3 个基本事件对应如下：

Event | Touch      | Pointer     | Mouse
------|------------|-------------|
Start | touchstart | pointerdown | mousedown
Move  | touchmove  | pointermove | mousemove
End   | touchend   | pointerup   | mouseup


而触屏上的 drag, swipe, long press, pinch rotate, tap 等事件，也和一般事件一样进行侦听：

```javascript
Ext.get('myDivElement').on('pinch', doSomething);
```

# 应用实现响应式功能

可用以下的 2 个基本类实现响应式功能：

+ Ext.plugin.Responsive: 必须使用在已经生成的组件上，如通过 xtype 使用组件时
+ Ext.mixin.Responsive: 必须使用在自己创建的类或组件上。


### 插件形式

```javascript
{
    xtype: 'panel',
    //...
    plugins: 'responsive', // Ext.plugin.Responsive
    responsiveConfig: {
        'width < 800': {
            // 能在这里使用的组件属性，在组件上都有相应的 setter 方法
            hidden: false,
            bodyStyle: {'background-color':'#f1f1f1','color': '#277cc0'}
        },
        '(desktop && with >= 800)': {
            hidden: true
        },
        '(tablet || phone)': {
            hidden: false,
            html: '<div>..</div>'
        },
        '!(phone)': {

            //..
        }
    }
}
```

'desktop', 'phone', 'tablet' 等值都定义在 Ext.phatformTags 中，该对象中包含了当前设备/平台的当前信息。我们也可以手动使用这些值，如： `header: (Ext.platformTags.phone || Ext.platformTags.tablet)? false:true`。


### mixin 的形式

```javascript
Ext.define('Myapp.sample.customPanel',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.customPanel',
    title: 'my Extended Panel',
    header: true,
    //...
    mixins: ['Ext.mixin.Responsive'],
    responsiveConfig: {
        'width < 800': {
            // 能在这里使用的组件属性，在组件上都有相应的 setter 方法
            hidden: false,
            bodyStyle: {'background-color':'#f1f1f1','color': '#277cc0'}
        },
        '(desktop && with >= 800)': {
            hidden: true
        },
        '(tablet || phone)': {
            hidden: false,
            html: '<div>..</div>'
        },
        '!(phone)': {

            //..
        }
    }
});
```

# 参考 

+ [Chapter12: Responsive Configurations and Tablet Support](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
