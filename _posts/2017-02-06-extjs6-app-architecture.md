---
title: Ext JS 6 应用的体系结构
date: 2017-02-06
writing-time: 2017-02-06 08:54
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

# 概述

Ext JS 支持 MVC 和 MVVC 两种应用体系结构。

## Model

表示数据层，可包含数据验证逻辑和用于数据持久化的逻辑。

## View

表示 UI，例如 button, form, message box 等都是 view。

## Controller

它处置任何与 view 相关的逻辑，view 的事件处理，及任何的应用逻辑。

## View model

它封装了 view 所需的呈现逻辑，将数据绑定到 view, 当数据更新时更新 view。


# Sencha Cmd 创建的一些默认文件

## app.js

```javascript
Ext.application({
    name: 'MyApp',

    extend: 'MyApp.Application',

    requires: [
        'MyApp.view.main.Main'
    ],

    // The name of the initial view to create. With the classic toolkit this class
    // will gain a "viewport" plugin if it does not extend Ext.Viewport. With the
    // modern toolkit, the main view will be added to the Viewport.
    //
    mainView: 'MyApp.view.main.Main'
	
    //-------------------------------------------------------------------------
    // Most customizations should be made to MyApp.Application. If you need to
    // customize this file, doing so below this section reduces the likelihood
    // of merge conflicts when upgrading to new versions of Sencha Cmd.
    //-------------------------------------------------------------------------
});
```

这是 Ext JS 应用的开始代码。



> 参考： 

+ [The application architecture](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
