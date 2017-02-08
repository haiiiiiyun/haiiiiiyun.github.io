---
title: ExtJS 6 基本组件
date: 2017-02-08
writing-time: 2017-02-08 12:32--23:21
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

# 基本组件

## Ext.Button

```javascript
Ext.create('Ext.Button', {
    text: 'My Button',
    renderTo: Ext.getBody(),
    handler: function(){
        alert('click');
    }
});
```

也可以通过 `listeners` 配置项添加多个事件处理函数：

```javascript
Ext.create('Ext.Button', {
    text: 'My Button',
    renderTo: Ext.getBody(),
    listeners: {
        click: {
            fn: function(){
                alert('click');
            }
        },
        mouseout: {
            fn: function(){
                alert('mouseout');
            }
        }
    }
});
```

还可以创建多种类型的按钮, 如链接按钮、带菜单的按钮、状态切换按钮等。

通过设置 `href` 属性创建链接按钮：

```javascript
Ext.create('Ext.Button', {
    renderTo: Ext.getBody(),
    text: 'Link Button',
    href: 'http://www.sencha.com/'
});
```

通过设置 `menu` 属性创建菜单按钮：

```javascript
Ext.create('Ext.Button', {
    text: 'My Button',
    renderTo: Ext.getBody(),
    menu: [
        {text: 'Item 1'},
        {text: 'Item 2'},
        {text: 'Item 3'}
    ]
});
```

`Ext.Button` 还有 bind, cls, disabled, html, tooltip, tpl 等属性可以设置。


## Ext.MessageBox

`Ext.window.MessageBox` 类实现了信息窗口功能，而 `Ext.MessageBox` 是该类的 singleton 实例，同时 `Ext.MessageBox` 还有一个别名 `Ext.Msg`。可以通过 `Ext.MessageBox` 显示 alert, confirmation, prompt 窗口，例如：

```javascript
Ext.Msg.alert('Info', 'Document saved!');

Ext.Msg.confirm('Confirm', 'Are you want to cancel the updates?',
    function(button){
        if ('yes'==button){
        }
        else {
        }
    }
);

Ext.MessageBox.show({
    title: 'Save Changes?',
    msg: 'Do you want to save the file?',
    buttons: Ext.MessageBox.YESNO,
    fn: function(button){
        if ('yes'==button){
        }
        else {
        }
    },
    icon: Ext.MessageBox.QUESTION
});
```


# 表单和表单项

## Ext.form.Panel

它继承自 Panel, 添加了与表单相关的功能，如表单项管理，验证，提交等。表单 Panel 默认是 anchor 布局，里面的表单项大小相对与表单 Panel 的大小确定。

表单 Panel 有一个便捷的配置项 `fieldDefaults`，里面可以为表单中的所有表单项设置默认值。

常用的内置表单项有：

+ Ext.form.field.Checkbox
+ Ext.form.field.ComboBox
+ Ext.form.field.Date
+ Ext.form.field.File
+ Ext.form.field.Hidden
+ Ext.form.field.HtmlEditor
+ Ext.form.field.Number
+ Ext.form.field.Radio
+ Ext.form.field.Text
+ Ext.form.field.TextArea
+ Ext.form.field.Time


### Ext.form.field.Text

就是基本的文本项，它的 `vtype` 属性用来设置验证信息，如：

```javascript
Ext.create('Ext.form.field.Text', {
    renderTo: Ext.getBody(),
    name: 'email',
    fieldLabel: 'Email',
    allowBlank: false,
    vtype: 'email' // 验证输入的必须是有效的 email 地址
});
```


### Ext.form.field.Number

扩展至 spinner 项，而 spinner 项扩展至 Text 项。

```javascript
Ext.create('Ext.form.field.Number', {
    renderTo: Ext.getBody(),
    name: 'count',
    fieldLabel: 'Count',
    value: 0,
    maxValue: 10,
    minValue: 0
});
```

它还有 hideTrigger, keyNavEnabled, mouseWheelEnabled 属性可配置。

### Ext.form.field.ComboBox

下拉框，它的数据必须通过 `store` 属性来指定，它的 `queryMode` 属性的值可为 `local` 或 `remote`，以确定 `store` 加载数据时是否要向远程服务器发送请求。例如：

```javascript
var months = Ext.create('Ext.data.Store', {
    fields: ['abbr', 'name'],
    data: [
        {"abbr":"JAN", "name":"January"},
        {"abbr":"FEB", "name":"February"},
        {"abbr":"MAR", "name":"March"},
        {"abbr":"APR", "name":"April"},
        {"abbr":"MAY", "name":"May"},
        {"abbr":"JUN", "name":"June"},
        {"abbr":"JUL", "name":"July"},
        {"abbr":"AUG", "name":"August"},
        {"abbr":"SEP", "name":"September"},
        {"abbr":"OCT", "name":"October"},
        {"abbr":"NOV", "name":"November"},
        {"abbr":"DEC", "name":"December"}
    ]
});

Ext.create('Ext.form.ComboBox', {
    fieldLabel: 'Choose Month',
    store: months,
    queryMode: 'local',
    displayField: 'name',
    valueField: 'abbr',
    renderTo: Ext.getBody()
});
```

### Ext.form.field.HtmlEditor

该表单项提供了字处理的常用功能。如：

```javascript
Ext.create('Ext.form.HtmlEditor', {
    width: 800,
    height: 200,
    renderTo: Ext.getBody()
});
```

### 表单项的验证

大部分的表单项都有自己的验证规则，如文本项有 allowBank, minLength, maxLength 等。而自定义的验证规则可以用正则表达式实现。

### 表单 Panel 中的事件

+ beforeaction: 在执行 action 前触发
+ actionfailed: 当 action 失败后触发
+ actioncomplete: 当 action 完成后触发
+ validitychange: 整个表单的验证状态改变时触发
+ dirtychange: 表单数据修改后触发


### 表单项的容器

`Ext.form.CheckboxGroup` 扩展至 `FieldContainer`，用于组织 checkbox 项。需注意每个组中的所有 checkbox 的 name 值必须相同，例如：

```javascript
Ext.create('Ext.form.CheckboxGroup', {
    renderTo: Ext.getBody(),
    fieldLabel: 'Skills ',
    vertical: true,
    columns: 1,
    items: [
        {boxLabel: 'C++', name: 'rb', inputValue: '1'},
        {boxLabel: '.Net', name: 'rb', inputValue: '2', checked: true},
        {boxLabel: 'C#', name: 'rb', inputValue: '3'},
        {boxLabel: 'Python', name: 'rb', inputValue: '4'}
    ]
});
```

`Ext.form.FieldContainer` 用于将想着的表单项组合起来，便于使用一个标签。下面的例子将 FirstName 和 LastName 两个表单项组合成一体：

```javascript
Ext.create('Ext.form.FieldContainer', {
    renderTo: Ext.getBody(),
    fieldLabel: 'Name',
    layout: 'hbox',
    combineErrors: true,
    defaultType: 'textfield',
    defaults: {
        hideLabel: 'true'
    },
    items: [{
        name: 'firstName',
        fieldLabel: 'First Name',
        flex: 2,
        emptyText: 'First',
        allowBlank: false
    }, {
        name: 'lastName',
        fieldLabel: 'Last Name',
        flex: 3,
        margin: '0 0 0 6',
        emptyText: 'Last',
        allowBlank: false
    }]
});
```

`Ext.form.RadioGroup` 扩展至 `CheckboxGroup`，用于组织 radio 按钮，同样，分组中的所有 radio 的 name 值必须相同。例如：

```javascript
Ext.create('Ext.form.RadioGroup', {
    renderTo: Ext.getBody(),
    fieldLabel: 'Sex ',
    vertical: true,
    columns: 1,
    items: [
        {boxLabel: 'Male', name: 'rb', inputValue: '1'},
        {boxLabel: 'Female', name: 'rb', inputValue: '2'}
    ]
});
```

### 提交表单

使用 `getForm` 获取表单，在提交前用 `isValid` 验证表单：

```javascript
var form = this.up('form').getForm();
if (form.isValid()) {
    form.submit({
        url: 'someurl',
        success:  function(){},
        failure: function(){}
    });
}
else {
}
```

## 菜单和工具条

使用 `Ext.toolbar.Toolbar` 创建工具条。`Ext.toolbar.Toolbar` 内的子组件默认都是按钮，但我们也可以添加进其它的控件，如文本项，数字项，图标，下拉框等。

要对工具条内的控件进行排列，可以用 `Ext.toolbar.Spacer`(' '), `Ext.toolbar.Separator`('|'), `Ext.toolbar.Fill`('->')。

`Ext.menu.Menu` 用于创建菜单，而用 `Ext.menu.Item` 创建菜单项。

例如：

```javascript
Ext.create('Ext.toolbar.Toolbar', {
    renderTo: Ext.getBody(),
    width: 800,
    items: [
        {
            text: 'My Button'
        },
        {
            text: 'My Button',
            menu: [{
                text: 'Item 1'
            }, {
                text: 'Item 2'
            }, {
                text: 'Item 3'
            }]
        },
        {
            text: 'Menu with divider',
            tooltip: {
                text: 'Tooltip info',
                title: 'Tip Title'
            },
            menu: {
                items: [{
                    text: 'Task 1'
                }, '-', {
                    text: 'Task 2'
                }, {
                    text: 'Task 3'
                }]
            }
        },
        '-',
        'Some Info',
        {
            xtype: 'tbspacer'
        },
        {
            name: 'Count',
            xtype: 'numberfield',
            value: 0,
            maxValue: 10,
            minValue: 0,
            width: 60
        }
    ]
});
```

# 参考 

+ [Basic Components](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
