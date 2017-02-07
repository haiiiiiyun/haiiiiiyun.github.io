---
title: Ext JS 6 应用的结构
date: 2017-02-06
writing-time: 2017-02-06 08:54--2017-02-07 09:21
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

它处理与 view 相关的所有逻辑，view 的事件处理，及应用的所有逻辑。

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

这是 Ext JS 应用最先开始运行的代码。它先定义应用名为 `MyApp`，从而创建一个全局变量(即命名空间) MyApp，该应用的所有变量都位于该命名空间中。

本应用扩展至 `MyApp.Application`，而 `MyApp.Application` 在 `app/Application.js` 中定义。

依赖的类在 `requires` 中指定，这些指定的依赖类在实例化时会先自动下载并加载进来。


## app/Application.js

```javascript
/
**
 * The main application class. An instance of this class is created by app.js when it
 * calls Ext.application(). This is the ideal place to handle application launch and
 * initialization details.
 */
Ext.define('MyApp.Application', {
    extend: 'Ext.app.Application',
    
    name: 'MyApp',

    stores: [
        // TODO: add global / shared stores here
    ],
    
    launch: function () {
        // TODO - Launch the application
    },

    onAppUpdate: function () {
        Ext.Msg.confirm('Application Update', 'This application has an update, reload?',
            function (choice) {
                if (choice === 'yes') {
                    window.location.reload();
                }
            }
        );
    }
});
```

`launch` 是在 `Ext.app.Application` 中定义的一个函数，它在页面加载后自动被调用。


## app/view/main/MainModel.js

```javascript
/**
 * This class is the view model for the Main view of the application.
 */
Ext.define('MyApp.view.main.MainModel', {
    extend: 'Ext.app.ViewModel',

    alias: 'viewmodel.main',

    data: {
        name: 'MyApp',

        loremIpsum: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    }

    //TODO - add data, formulas and/or methods to support your view
});
```

这是 Main View 对应的 View Model，该 View Model 的别名为 `viewmodel.main`，别名的前缀是类型的小写形式，还比如 Controller 的 `controller.` 等。


## app/view/main/MainController.js

```javascript
/**
 * This class is the controller for the main view for the application. It is specified as
 * the "controller" of the Main view class.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('MyApp.view.main.MainController', {
    extend: 'Ext.app.ViewController',

    alias: 'controller.main',

    onItemSelected: function (sender, record) {
        Ext.Msg.confirm('Confirm', 'Are you sure?', 'onConfirm', this);
    },

    onConfirm: function (choice) {
        if (choice === 'yes') {
            //
        }
    }
});
```

这是 Main View 对应的 Controller。共两种类型的 Controller： `Ext.app.ViewController` 和 `Ext.app.Controller`。

## Main.js

如果通过 Sencha Cmd 6 的 `--modern` 或 `--classic` 创建的，那么位于 `app/view/main/Main.js`，如果创建的是一个 universal 应用，那么 Main.js 分别位于 `modern/src/view/main/` 和 `classic/src/view/main/` 下。

### modern/src/view/main/Main.js

```javascript
/**
 * This class is the main view for the application. It is specified in app.js as the
 * "mainView" property. That setting causes an instance of this class to be created and
 * added to the Viewport container.
 *
 * TODO - Replace the content of this view to suit the needs of your application.
 */
Ext.define('MyApp.view.main.Main', {
    extend: 'Ext.tab.Panel',
    xtype: 'app-main',

    requires: [
        'Ext.MessageBox',

        'MyApp.view.main.MainController',
        'MyApp.view.main.MainModel',
        'MyApp.view.main.List'
    ],

    controller: 'main',
    viewModel: 'main',

    defaults: {
        tab: {
            iconAlign: 'top'
        },
        styleHtmlContent: true
    },

    tabBarPosition: 'bottom',

    items: [
        {
            title: 'Home',
            iconCls: 'x-fa fa-home',
            layout: 'fit',
            // The following grid shares a store with the classic version's grid as well!
            items: [{
                xtype: 'mainlist'
            }]
        },{
            title: 'Users',
            iconCls: 'x-fa fa-user',
            bind: {
                html: '{loremIpsum}'
            }
        },{
            title: 'Groups',
            iconCls: 'x-fa fa-users',
            bind: {
                html: '{loremIpsum}'
            }
        },{
            title: 'Settings',
            iconCls: 'x-fa fa-cog',
            bind: {
                html: '{loremIpsum}'
            }
        }
    ]
});
```

在该 View 中定义了 controller, viewmodel 属性值，并且可以将 viewmodel 中定义的 data 用于绑定。

### classic/src/view/main/Main.js

```javascript
/**
 * This class is the main view for the application. It is specified in app.js as the
 * "mainView" property. That setting automatically applies the "viewport"
 * plugin causing this view to become the body element (i.e., the viewport).
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('MyApp.view.main.Main', {
    extend: 'Ext.tab.Panel',
    xtype: 'app-main',

    requires: [
        'Ext.plugin.Viewport',
        'Ext.window.MessageBox',

        'MyApp.view.main.MainController',
        'MyApp.view.main.MainModel',
        'MyApp.view.main.List'
    ],

    controller: 'main',
    viewModel: 'main',

    ui: 'navigation',

    tabBarHeaderPosition: 1,
    titleRotation: 0,
    tabRotation: 0,

    header: {
        layout: {
            align: 'stretchmax'
        },
        title: {
            bind: {
                text: '{name}'
            },
            flex: 0
        },
        iconCls: 'fa-th-list'
    },

    tabBar: {
        flex: 1,
        layout: {
            align: 'stretch',
            overflowHandler: 'none'
        }
    },

    responsiveConfig: {
        tall: {
            headerPosition: 'top'
        },
        wide: {
            headerPosition: 'left'
        }
    },

    defaults: {
        bodyPadding: 20,
        tabConfig: {
            plugins: 'responsive',
            responsiveConfig: {
                wide: {
                    iconAlign: 'left',
                    textAlign: 'left'
                },
                tall: {
                    iconAlign: 'top',
                    textAlign: 'center',
                    width: 120
                }
            }
        }
    },

    items: [{
        title: 'Home',
        iconCls: 'fa-home',
        // The following grid shares a store with the classic version's grid as well!
        items: [{
            xtype: 'mainlist'
        }]
    }, {
        title: 'Users',
        iconCls: 'fa-user',
        bind: {
            html: '{loremIpsum}'
        }
    }, {
        title: 'Groups',
        iconCls: 'fa-users',
        bind: {
            html: '{loremIpsum}'
        }
    }, {
        title: 'Settings',
        iconCls: 'fa-cog',
        bind: {
            html: '{loremIpsum}'
        }
    }]
});
```
classic 版本中增加了针对 responsive 设计的相关配置项。


> 参考： 

+ [The application architecture](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
