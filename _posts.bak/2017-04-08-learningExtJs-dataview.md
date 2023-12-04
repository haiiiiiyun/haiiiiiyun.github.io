---
title: ExtJS 中的 DataView 和模板 --Learning ExtJS(4th)
date: 2017-04-08
writing-time: 2017-04-08 20:03--20:59
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

DataView 和 Grid 类似，数据也来自 Store，但它将 Store 中的每条记录通过模板 (Ext.XTemplate) 格式化出来。

DataView 的类是 `Ext.view.View`。

# 一个基本的 DataView

```javascript
// 模板
var myTpl = [
    '<tpl for=".">',
        '<div class="user">{firstName} {lastName}</div>',
    '</tpl>'
].join('');

var myDataview = Ext.create('Ext.view.View', {
    store: myStore,
    tpl: myTpl,
    padding:6,

    // DataView 中每个 div.user 将作为一个元素
    // itemclick, itemdblclick 等事件都作用
    // 在这一元素粒度上
    // 一个元素也对应 Store 中的一条记录
    itemSelector: 'div.user',

    // 定义事件处理
    listeners: {
        itemclick: {
            fn:function(view, record, item, index, evt, eOpts){
                Ext.Msg.alert( "Dataview record selected",
                    record.get('firstName') +
                    " " + record.get('lastName') +
                    " has been selected");
            }
        }
    }

    // Store 中没有记录时显示
    emptyText: '<b>No users available</b>'
});

var MyPanel = Ext.create('Ext.panel.Panel',{
    title: 'My Dataview',
    height: 295,
    width: 450,
    items: [myDataview],
    renderTo: 'myPanel'
});
```

# 模板

Ext 中共有 2 种模板， Ext.Template 和 Ext.XTemplate：
    + Ext.Template 适合于简单的 HTML 片段
    + Ext.XTemplate 扩展至 Ext.Template，提供了高级功能。


## Ext.Template

```javascript
// 定义 Template
var myTemplate = new Ext.Template([
    '<div class="container">',
        '<div class="header">',
            '<img src="images/{logo}"width="88" height="53" alt=""/>',
        '</div>',
        '<span>{titlecontents}</span>',
    '</div>'
]);

// 将模板对象编译成内部函数，优化呈现速度
myTemplate.compile();

// 传入参数来呈现模板内容，并附加到 #myPanel 的 DIV 元素上
// 传入的数据将变成 values 变量
myTemplate.append('myPanel', {
    logo: 'Packt.png',
    titlecontents: 'Visit PACK PUB for great deals...!'
});
```

## Ext.XTemplate

支持如下高级功能：

+ 循环遍历数组
+ 基本比较与条件语句
+ 基本的数学函数
+ 执行任意内联代码，并带有特殊的内置模板变量
+ 自定义成员函数


`Ext.view.View` 使用的就是 Ext.XTemplate。

```javascript
// 创建一个 XTemplate 实例
var myXTemplate = new Ext.XTemplate(
  // 呈现模板时如果传入的是一个数组，
  // 则遍历数组中的记录进行呈现
  '<tpl for=".">',
    '<div class="user">',
      // 这里 {firstName}, {lastName} 是当前记录记录中的数据项变量
      // [xindex] 是模板的内置变量值，是当前循环记数（开始于1）
      'Record number {[xindex]}-{firstName} {lastName} - ',
      // 条件判断，active 是当前记录中的数据项变量
      '<tpl if="active==0">',
        '<span class="inactiveuser">user is Inactive (need activation)</span>',
      '<tpl else>',
        '<span class="activeuser">user is active</span>',
      '</tpl>',
      '- Reference number for user :',
      // 数值计算，id 是当前记录中的数据项变量
      '{id+1000}',
    '</div>',
  '</tpl>'
);

myStore.on({
    // Store 加载完成后调用
    'load':{
        fn:function(store, records, success, eOpts){
            var data = [];
            Ext.each(records, function(record, index, records){
                data.push(record.data);
            },this);
            var myEl = Ext.get('myPanel');

            // 覆盖 #myPanel HTMl 元素
            myXTemplate.overwrite(myEl, data);
        }
        scope:this
    }
});
myStore.load();
```

# 一个较复杂的 DataView

```javascript
// 有自定义成员函数的 XTemplate 实例
var myXTemplate = new Ext.XTemplate(
  '<tplfor=".">',
    // 调用 XTemplate 实例中的自定义函数
    // values 指呈现模板（子模板）时的当前数据块，这里指当前记录
    '<div class="user {[this.getActiveclass(values.active)]}">',
      '<div class="user_row">',
        '<div class="user_img">',
          '<img src="images/{twitter_account}.jpg" width="37" height="37">',
        '</div>',
        '<div class="usr_name">{firstName} {lastName}<br>',
          '<span class="usr_account">{twitter_account}</span>',
        '</div>',
      '</div>',
    '</div>',
  '</tpl>',
  { // 自定义成员函数定义区
      getActiveclass:function(value){
          return (value!=0)?"active":"inactive";
      }
  }
);

// 创建 DataView 实例
var myDataview = Ext.create('Ext.view.View', {
    store: myStore,
    tpl:myXTemplate,
    padding:6,
    itemSelector: 'div.user',
    emptyText: '<b>No users available</b>',
    listeners:{
        itemdblclick:{
            fn:function(view, record, item, index, event, eOpts){
                var item = Ext.fly(item);
                if(record.get('active')){
                    Ext.fly(item).removeCls('active');
                    Ext.fly(item).addCls('inactive');
                }else{
                    Ext.fly(item).removeCls('inactive');
                    Ext.fly(item).addCls('active');
                }
                record.data.active = !record.data.active;
            }
        }
    }
});
```

# 参考 

+ [Chapter7: DataViews and Templates](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
