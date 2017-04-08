---
title: ExtJS 中的树--Learning ExtJS(4th)
date: 2017-04-08
writing-time: 2017-04-08 21:01--22:25
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

`Ext.tree.Panel` 组件用来显示层级数据（如文件目录）。Ext.tree.Panel 和 Ext.grid.Panel 都扩展至 Ext.panel.Table，因此都有列、排序、过滤、renderer，拖放、插件等功能。

`Ext.tree.Panel` 所需的 Store 类型是 `Ext.data.TreeStore`。

# 一个基本的树面板

```javascript
// 创建一个 TreeStore 实例
// 其表示的是一个树型结构数据，
// TreeStore 的每个结点都具有特定的数据项，如：
//   expanded, text, leaf 等，从而确保 Tree Panel
// 可以正确显示
var MyTreeStore = Ext.create('Ext.data.TreeStore',{
    storeId: 'myTreeStoreDS',
    root: {
        text: 'My Application',
        expanded: true,
        children: [
            {
                text: 'app',
                children:[
                    { leaf:true, text: 'Application.js' }
                ]
            },
            {
                text: 'controller',
                expanded: true,
                children: []
            },
            {
                text: 'model', expanded:true,
                children: [
                    { leaf:true, text: 'clients.js' },
                    { leaf:true, text: 'providers.js'},
                    { leaf:true, text: 'users.js' }
                ]
            }
        ]
    }
});

var MyTreePanel = Ext.create('Ext.tree.Panel',{
    title: 'My tree panel',
    width: 250,
    height: 350,
    frame: true,
    store: MyTreeStore,
    renderTo: 'myPanel'
});
```

# TreeStore

TreeStore 用于树型结构。创建 TreeStore 实例时如果没有指定 Model，Ext 会隐式基于配置数据创建一个 Model（使用 Ext.data.NodeIterface 接口）。 该接口包含了用于实现结点 API 的一组方法，同时定义了一些属性用于维护树和 UI 的状态。

而自定义的 Model 用于 TreeStore 时，如果没有完整实现 NodeIterface 接口，Ext 也会自动基于 NodeIterface 进行统一化。

NodeIterface 中包含：

+ text: 该属性是结点标签
+ root: 该属性值为 true 时，则表示该结点为根结点
+ leaf: 该属性值为 true 时，则表示该结点没有子结点
+ expanded: 该属性值为 true 时，则结点会展开
+ iconCls: 该结点的图标 CSS 类名
+ children: 子结点数组
+ checked: 该属性值为 true 或 false 时，该结点旁会显示一个 checkbox


# Check 树

树的每个结点旁都会显示一个 checkbox。而 TreeStore 数据源中每个结点都必须设置 `checked` 属性，值为 true 或 false。如果没有设置 checked 属性，则不会显示 checkbox。


# Tree Grid Panel

这种 Panel 兼具 Tree 和 Grid 的功能。只需和 Grid 一样进行列定义即可。其中第一列显示的是树结点，要用 `treecolumn`，如：

```javascript
columns:[{
    //column provide tree structure
    xtype: 'treecolumn',
    text: 'Module',
    dataIndex:'text',
    flex: 1,sortable: true
}//...
]
```


 参考 

+ [Chapter8: The Tree Panel](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
