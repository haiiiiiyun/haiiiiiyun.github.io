---
title: ExtJS MVC MVVM 及事件域(event domain)
date: 2017-04-13
writing-time: 2017-04-13 15:52--16:48
categories: Programming
tags: Programming Sencha ExtJS Javascript 《Ext&nbsp;JS&nbsp;Application&nbsp;Development&nbsp;Blueprints》
---

# MVC

```javascript
// 视图
// file: view/Detail.js
Ext.define('MvcEx1v4.view.Detail', {
    extend: 'Ext.Container',
    alias: 'widget.app-detail',
    html: 'Double-click an Album to select'
});

// file: view/List.js
Ext.define('MvcEx1v4.view.List', {
    extend: 'Ext.grid.GridPanel',
    alias: 'widget.app-list',
    store: 'Albums',
    forceFit: true,
    frame: true,
    requires: ['Ext.Msg'],
    columns: [
        { text: 'Name', dataIndex: 'name' },
        { text: 'Artist', dataIndex: 'artist' }
    ],
    initComponent: function() {
        this.bbar = [
            '->',
            { xtype: 'button', text: 'Show Artist Summary',
            handler: this.onShowSummary, scope: this },
            '->'
        ];
        this.callParent(arguments);
    },
    onShowSummary: function() {
        var summary = this.getStore().collect('name').join(', ');
        Ext.Msg.alert('Artists', summary);
    }
});
```

```javascript
// 控制器:
// file: controller/Album.js
Ext.define('MvcEx1v4.controller.Album', {
    extend: 'Ext.app.Controller',
    refs: [
        {
            // 定义 ref 名为 "detail".
            // 这将在该控制器上创建一个叫 "getDetail" 的方法，
            // 通过该方法可获取关联的视图。
            ref: 'detail',

            // 该 selector 值将传给 Ext.ComponentQuery.query,
            // 因此任何有效的组件查询选择子都可用。
            // 这里基于视图的 alias 来查询
            selector: 'app-detail'
        }
    ],
    init: function() {
        this.control(
            {
                // 基于视图的别名 alias 选择
                'app-list': {
                    itemdblclick: this.onAlbumDblClick
                }
            }
        );
    },
    onAlbumDblClick: function(list, record) {
        var html = Ext.String.format('{0} by {1}',
            record.get('name'), record.get('artist'));
        this.getDetail().getEl().setHTML(html);
    }
});
```

# MVVM

```javascript
// 视图
//file: view/album/Album.js
Ext.define('MvvmEx1v5.view.album.Album', {
    extend: 'Ext.container.Container',
    xtype: 'app-album',
    requires: ['Ext.grid.Panel'],
    controller: 'album', // 指定 ViewController
    layout: 'hbox',
    defaults: {
        width: 250,
        margin: 20
    },
    items: [
        {
            xtype: 'grid',

            // 可以在（本组件及父组件的）ViewController 中
            // 通过 this.lookupReference('list') 来获取该组件
            reference: 'list',
            viewModel: 'album', // 指定 ViewModel，album 是 ViewModel 的别名

            // Grid 的默认 `bindProperty` 是 Store，
            // 故这里实际上是将 store 的 config 设置成 'albums'
            bind: '{albums}',

            forceFit: true,
            frame: true,
            margin: '20 10 20 20',
            columns: [
                { text: 'Album', dataIndex: 'name' },
                { text: 'Artist', dataIndex: 'artist' }
            ],
            bbar: [
                '->',
                { xtype: 'button', text: 'Show Artist Summary',
                    handler: 'onShowSummary' },
                '->'
            ],
            listeners: {
                // onAlbumDblClick 在 ViewController 中定义
                rowdblclick: 'onAlbumDblClick'
            }
        },
        { 
            xtype: 'container',
            margin: '20 10',
            reference: 'detail',
            width: 150,
            html: 'Double-click an Album to select' 
        }
    ]
});
```

```javascript
// file: view/album/AlbumModel.js
Ext.define('MvvmEx1v5.view.album.AlbumModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.album',
    requires: [
        'MvcEx1.store.Albums'
        'Ext.Msg'
    ],
    stores: {
        albums: {
            type: 'albums'
        }
    },
    buildSummary: function() {
        return this.getStore('albums').collect('name').join(', ');
    }
});
```

```javascript
//file: view/album/AlbumController.js
Ext.define('MvvmEx1v5.view.album.AlbumController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.album',
    onShowSummary: function() {
        var summary = this.lookupReference('list').getViewModel().buildSummary();
        Ext.Msg.alert('Artists', summary);
    },
    onAlbumDblClick: function(list, record) {
        var html = Ext.String.format('{0} by {1}',
            record.get('name'), record.get('artist'));
        this.lookupReference('detail').getEl().setHtml(html);
    }
});
```

# 事件域 (event domain)

复杂系统中，通常会有一个事件总线 (event bus)，系统中的各组件触发事件，事件通过总线流转至订阅者。自 Ext JS 4.2 开始，已有类似的功能。

事件域允许控制器对来自不同源的事件进行响应。默认的源有：

+ Component: 这些是由组件触发的事件。实际上控制器中通过 `Ext.app.Controller.control()` 方法设置的事件都是来自组件触发的事件。
+ Global: 这些是由一个全局源触发的事件，可用来触发任何系统级别的事件。
+ Controller: 由其它控制器触发的事件。
+ Store: 由 Store 触发的事件。
+ Direct: 由扩展至 `Ext.direct.Provider` 的类触发的事件。


一些事件域可通过选择子对接收的事件进行过滤（如与源关联的 ID），而在 Component 事件中，我们使用 Ext.Component 查询进行过滤。


## 事件域例子

```javascript
// ViewController
// file: view/album/AlbumController.js:
//...
    init: function() {
        // 通过 this.listen 进行更加显式地事件绑定
        this.listen(
            {
                // 来自 Component 源的事件绑定
                // 如果只关注来自 Component 源的事件，则可以通过
                // this.control() 进行简单地绑定
                component: {
                    'app-album grid': {
                        'rowdblclick': 'onAlbumDblClick'
                    },
                    'app-album button': {
                        'click': 'onShowSummary'
                    }
                }
            }
        );
    }
//...
```

## 使用自定义事件

一个 ViewController，当视图上的按钮点击时，会触发一个 'search' 自定义事件：

```javascript
//file:  view/search/SearchController.js
Ext.define('EventDomain1.view.search.SearchController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.search',
    init: function() {
        this.listen({
            component: {
                'app-search button': {
                    'click': 'onSearchSubmit'
                }
            }
        });
    },
    onSearchSubmit: function() {
        var val = this.lookupReference('searchfield').getValue();

        // 本控制器触发了一个事件
        this.fireEvent('search', val);
    }
});
```

在另一个控制器中，可以绑定上面的自定义事件：

```javascript
//file: partial /view/album/AlbumController.js
    init: function() {
        this.listen({
            // 来自 Controller 源的事件绑定
            controller: {
                // * 表示任何 Controller 都匹配
                '*': {
                    'search': 'onSearch'
                }
            }
        });
    },
    onSearch: function(searchTerm) {
        var list = this.lookupReference('list');
        list.getViewModel().search('searchTerm');
    }
//...
```

# 参考 

+ [Chapter2: MVC and MVVM](https://www.amazon.com/Ext-JS-Application-Development-Blueprints/dp/1784395307/)
