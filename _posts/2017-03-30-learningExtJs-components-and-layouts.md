---
title: ExtJS 组件和布局--Learning ExtJS(4th)
date: 2017-03-30
writing-time: 2017-03-30 08:35--16:14
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 组件生命周期

Ext 中的所有组件都扩展至 `Ext.Component`（另一个名字也叫 `Ext.AbstractComponent`)。

当创建组件时，都会经历一个叫 “组件生命周期” 的过程。基本上，生命周期分 3 个阶段：初始化过程，呈现过程，和销毁过程。

初始化阶段初始化我们的新实例，并将它登记到组件管理器中;然后，呈现阶段将在 DOM 上创建全部所需的结点;最后销毁阶段将从 DOM 上删除结点和侦听器 (listener)。

`Ext.AbstractComponent/Ext.Component` 类引导了这个生命周期过程，每个扩展至该类的组件都将自动参与这个生命周期。


## 初始化阶段

这个阶段的主要目的是基于我们的配置信息创建一个组件实例。它还将我们的组件登记到组件管理器中，以及进行其它一些操作。

![组件初始化阶段](/assets/images/learningextjs4th/comp_init_phase.png)

下面是初始化阶段每步的详细描述：

1. 第 1 步是将配置信息应用到我们要创建的类实例上。
2. 第 2 步是定义通用事件，如每个组件的 enable, disable, show 等。
3. 第 3 步是为该实例赋于一个 ID。如果在配置信息中有指定 ID 就用指定的，不然会自动生成一个。由于组件 ID 会用到 DOM 元素上，故要确保唯一性，因此最好不要指定，应自动生成。
4. 第 4 步检验是否在配置信息中定义了插件，有的话创建这些插件的实例。
5. 第 5 步运行 `initComponent` 方法。像 initComponent 等 Component 类中的模板函数都可以在子类中重载。
6. 第 6 步将实例登记到 `Ext.ComponentManager` 对象中。我们可以通过 `var panel=Ext.get("panelId")` 或 `Ext.ComponentQuery.query('xtypeValue')` 来引用组件。
7. `Component` 类有 2 个 mixin，一个用于事件管理，另一个用于状态管理。第 7 步通过调用这两个 mixin 的构造函数对它们进行初始化。
8. 如果定义有插件，那么插件在第 4 步就已经初始化了，现在将本实例作为参数，调用每个插件上的 `init(component)` 方法，进一步初始化。


如果在配置信息中指定了 `renderTo` 属性，那么接下来就开始呈现阶段。如果没有指定，也可以手动开启，如 `panel.render(Ext.getBody())`。


## 呈现阶段

呈现阶段只当组件还未呈现时才会发生。在该阶段中，会创建全部所需的结点并插入到 DOM 中，并应用 CSS 样式，创建事件侦听器。之后我们就能看到并与它进行交互。


![组件呈现阶段](/assets/images/learningextjs4th/comp_render_phase.png)


下面是呈现阶段每步的详细描述：


1. 第 1 步触发 `beforeRender` 事件。如果某个侦听器返回 false，则停止该呈现阶段。
2. 第 2 步执行 `beforeRender` 方法。并检查该组件是否是浮动组件（如 menu, window 等)，并设置正确的 CSS `z-index` 属性值。
3. 第 3 步通过设置 `container` 属性来定义本组件的容器。`container` 属性值指向一个 DOM 元素，即 Ext.dom.Element 实例。本组件将呈现到该元素中。
4. 第 4 步运行 `onRender` 方法。这会创建 `el` 属性，它包含本组件的主要结点元素。我们也可以为组件定义模板，如果这样的话，在本步中会基于模板创建结点并添加到组件的主要结点元素中。也可以重载 `onRender`，从而能添加定制的 DOM 结点。
5. 第 5 步是设置可见模式。隐藏组件元素共有 3 种模式：display, visibility, offset。
6. 第 6 步中，如果设置有 `overCls` 属性，那么会为 mouseover 和 mouseout 事件创建相应的侦听器。
7. 第 7 步运行 `render` 方法。并触发以本组件实例为参数的 `render` 事件。
8. 第 8 步是初始化内容。共有 3 种方法来设置组件内容：
    1. 通过 `html` 属性定义。
    2. 定义 `contentEl` 属性，其值是一个现有 DOM 元素的 ID。该元素将作为组件的内容。
    3. 定义 `tpl` 属性作为模板，定义 `data` 属性作为模板变量值对象，通过模板生成内容。
9. 第 9 步运行 `afterRender` 方法。如果包含有子组件，子组件也在本步中呈现。
10. 第 10 步触发 `afterRender` 事件。通过侦听该事件可以执行一些需要所有 DOM 结点都呈现后的动作。
11. 第 11 步初始化组件结点上的事件。
12. 第 12 步中，如果配置信息中设置了 `hidden:true`，则隐藏组件结点;如果设置了 `disabled:true`，则运行组件的 `disable()` 方法，这将在组件结点上添加一些 CSS 类使该结点显示为禁用状态并设置其 disabled 值为 true。


## 销毁阶段

销毁阶段的主要目的是消除 DOM，删除事件侦听器，并通过删除对象和数据来清理内存。当不再需要组件时，及时进行销毁非常重要。当窗口的属性 `closeAction` 设置为 `destroy`（默认即为该值）时，用户关闭窗口时即会触发销毁过程。

销毁过程也可以通过调用组件的方法来触发，如 `cmp.destroy()`。

![组件销毁阶段](/assets/images/learningextjs4th/comp_destroy_phase.png)


下面是销毁阶段每步的详细描述：


1. 第 1 步触发 `beforeDestroy` 事件。如果某个侦听器返回 false，则会停止销毁过程，否则，继续进行销毁，如果组件是浮动的，则将其从浮动管理器中删除。
2. 第 2 步执行 `beforeDestroy` 方法。子类通过重载该方法来删除子组件或清理内存。
3. 第 3 步中，如果本组件是某组件的子组件，则删除父组件对其的引用。
4. 第 4 步执行 `onDestroy` 方法。我们通过扩展该方法来正确的销毁组件，并确保我们添加的子组件也要销毁，以及自定义的侦听器也要清理。
5. 第 5 步销毁插件及 mixin。
6. 第 6 步中，如果组件已呈现，则将组件元素及侦听器都从 DOM 中删除。
7. 第 7 步触发 `destroy` 事件。
8. 第 8 步将本组件从组件管理器中删除，并清除其所有事件。


## 生命周期实践

```javascript
Ext.define('Myapp.sample.CustomComponent',{
    extend: 'Ext.Component',

    // 重载父类的方法
    // 一般用来配置组件属性
    initComponent: function(){
        var me = this;
        me.width = 200;
        me.height = 100;

        me.html = {
            tag: 'div',
            html: 'X',
            style: { // this can be replaced by a CSS rule
                'float': 'right',
                'padding': '10px',
                'background-color': '#e00',
                'color': '#fff',
                'font-weight': 'bold',
                'cursor': 'pointer'
            }
        };
        me.myOwnProperty = [1,2,3,4];

        //调用父类上的本方法
        me.callParent();
        console.log('Step 1. initComponent');
    },

    // 重载父类的方法
    beforeRender: function(){
        console.log('Step 2. beforeRender');
        this.callParent(arguments);
    },

    // 重载父类的方法
    onRender: function(){
        console.log('Step 3. onRender');
        // 父类中的本方法会创建组件主元素 el
        this.callParent(arguments);

        this.el.setStyle('background-color','#ccc');
    },

    // 重载父类的方法
    afterRender : function(){
        console.log('Step 4. afterRender');

        // 为该组件中的某个 DOM 元素添加 click 事件侦听
        this.el.down('div').on('click',this.myCallback,this);
        this.callParent(arguments);
    },

    // 重载父类的方法
    beforeDestroy : function(){
        console.log('5. beforeDestroy');
        this.callParent(arguments);
    },

    // 重载父类的方法
    onDestroy : function(){
        console.log('6. onDestroy');

        // 销毁时确保清理掉自定义的对象和数组，并删除侦听器
        delete this.myOwnProperty;
        this.el.down('div').un('click',this.myCallback);
        this.callParent(arguments);
    },

    myCallback : function(){
        var me = this;
        Ext.Msg.confirm('Confirmation','Are you sure you want to close this panel?',function(btn){
            if(btn === 'yes'){
                me.destroy();
            }
        });
    }
});

Ext.onReady(function(){
    Ext.create('Myapp.sample.CustomComponent',{
        renderTo : Ext.getBody()
    });
});

// 输出：
//Step 1. initComponent
//Step 2. beforeRender
//Step 3. onRender
//Step 4. afterRender
//5. beforeDestroy
//6. onDestroy
```

# 容器

容器即 `Ext.container.Container` 类（别名 Ext.AbstractContainer，Ext.Container）的实例，它用于管理子组件，并通过布局进行排列。如果我们需要我们的类能包含其它组件，则该类需要扩展至 `Ext.container.Container`，同时容器也是组件，也扩展至 `Ext.Component`，因此也有组件的全部生命周期。

所有的容器都能使用 `items` 属性（值为数组）来设置子组件，或通过 `add` 方法添加子组件。

```javascript
Ext.define("MyApp.sample.MyContainer",{
    // 扩展自容器类
    extend: "Ext.container.Container", //Step 1
    border: true,
    padding: 10,

    // 扩展父类的该方法进行一些属性设置
    initComponent: function(){
        var me = this;

        // 为每个子组件设置一些属性
        Ext.each(me.items,function(item){ //Step 2
            item.style = {
                backgroundColor:"#f4f4f4",
                border:"1px solid #333"
            };
            item.padding = 10;
            item.height = 100;
        });

        me.callParent();
    },

    onRender: function(){
        var me = this;
        me.callParent(arguments); // 生成 el 元素
        if( me.border ){ //Step 3
            me.el.setStyle( "border" , "1px solid #333" );
        }
    }
});

Ext.onReady(function(){
    Ext.create("MyApp.sample.MyContainer",{
        renderTo: Ext.getBody(),
        // 容器组件 defaults 配置对象中设置的所有属性，
        // 都将应用到每个子组件中。
        defaults: {
            xtype : "component",
            width : 100
        },
        items: [
            {
                //xtype: "component",
                html: "Child Component one"
            }, {
                //xtype: "component",
                html: "Child Component two"
            }
        ]
    });
});
```

## 容器类型

Ext 中有多个容器组件。

+ Ext.panel.Panel: 该组件扩展至 Ext.container.Container，它是最常用的容器。
+ Ext.window.Window: 该组件扩展至 Ext.panel.Panel 类，作为应用窗口使用。它是浮动组件，可以改变大小，能拖放。它也能最大化来填充整个 viewport。
+ Ext.tab.Panel: 该组件扩展至 Ext.panel.Panel 类，它能包含其它 Ext.panel.Panel 组件，在其 header 区域为每个 Panel 创建一个标签。它使用 `card` 布局来管理子组件。
+ Ext.form.Panel: 该组件扩展至 Ext.panel.Panel 类，是表单的标准容器。本质上，它是一个 Panel 容器，并创建了一个基本的表单用来管理表单项组件。
+ Ext.Viewport: 该容器表示应用程序区域（浏览器 viewport）。它将自身呈现到 document body，并将自动调整到浏览器 viewport 的大小。


同时每个容器都有一个 `layout` 属性，用来布局子组件。


## Viewport

Viewport 表示应用的可见区域，最佳实践是：网页上只创建一个 viewport。

```javascript
Ext.onReady(function(){
    Ext.create('Ext.container.Viewport',{
        padding:'5px',
        layout:'auto',
        style : {
            'background-color': '#fc9',
            'color': '#000'
        },
        html:'This is application area'
    });
});
```

## Panel

```javascript
Ext.onReady(function(){
    var MyPanel = Ext.create("Ext.panel.Panel",{
        renderTo: Ext.getBody(),
        // Panel 有 title 属性
        title: 'My first panel...',
        width: 300,
        height: 220,
        html:'<b>Here</b> goes some <i>content</i>..!'
    });
});
```

## Window

```javascript
// 是一个浮动窗口
Ext.create("Ext.window.Window",{
    title: 'My first window',
    width: 300,
    height: 200,
    maximizable: true,//可以设置是否可最大化
    closable: false, //默认为 true
    html: 'this is my first window'
}).show();
```

# 布局系统

## Border 布局

Border 布局将容器内的空间分成 5 个区域： north, south, west, east, center。每个区域都能放一个子组件，center 区域必须要放组件。

```javascript
Ext.onReady(function(){
    Ext.create('Ext.panel.Panel', {
        width: 500, height: 300,
        title: 'Border Layout',
        layout: 'border',
        items: [
            {
                xtype: 'panel',
                title: 'South Region is resizable',
                region: 'south', // region
                height: 100,
                split: true // 使该区域能调整尺寸
            }, {
                xtype: 'panel',
                title: 'West Region',
                region:'west', // region
                width: 200,
                collapsible: true, // 使该区域可折叠
                layout: 'fit',
                split: true // 使该区域能调整尺寸
            },{
                title: 'Center Region',
                region: 'center',
                layout: 'fit',
                margin: '5 5 0 0',
                html:'<b>Main content</b> goes here'
            }
        ],
        renderTo: Ext.getBody()
    });
});
```

## Fit 布局

用来只显示一个子组件，如果 `items` 属性中设置了多个组件，只显示第一个子组件。该子组件将占据容器的全部可用空间，并且会跟随容器改变自己的尺寸。


```javascript
Ext.onReady(function(){
    var win = Ext.create("Ext.window.Window",{
        title: "My first window",
        width: 300,
        height: 200,
        maximizable: true,
        // 实际上 layout 属性值也可以是一个对象，用来定义布局的配置信息
        layout: "fit",
        defaults: {
            xtype: "panel",
            height: 60,
            border: false
        },
        items: [
            // 虽然定义了 2 个子组件，但是
            // fit 布局只会显示第 1 个子组件
            {title: "Menu", html: "The main menu"},
            {title: "Content", html: "The main content!"}
        ]
    });
    win.show();
});
```

## Card 布局

Card 布局扩展至 Fit 布局，因此一次也只显示 1 个组件。但是通过 setActiveItem(index)，next(), prev() 等方法可以切换显示其它的子组件。

```javascript
Ext.onReady(function(){
    var win = Ext.create("Ext.window.Window",{
        title: "My first window",
        width: 300,
        height: 200,
        maximizable: true,
        layout: "card",//Step 1
        defaults:{ xtype: "panel", height: 60, border: false },
        items: [
            {
                title: "Menu",
                html: "The main menu"
            },{
                title: "Content",
                html: "The main content!"
            }
        ]
    });
    win.show();

    var index = 1;
    setInterval(function(){
       // win.getLayout() 获取布局对象
        win.getLayout().setActiveItem( index % 2); //Step 2
        index += 1;
    },3000);
});
```

## Accordion 布局

类似 Card 布局，每次也只显示一个组件，并以手风琴扩展的形式展示。子组件的 header 部分都会显示，可以点击子组件的标题栏进行扩展/收缩。

```javascript
var win = Ext.create("Ext.window.Window",{
    title: "My first window",
    width: 300,
    height: 600,
    maximizable: true,
    layout: "accordion",
    defaults: { xtype: "panel" },
    items:[
        {title: "Menu", html: "The main menu" },
        {title: "Content", html: "The main content!" },
        {title: "3rd Panel", html: "Content here...!" }
    ]
}).show();
```

## Anchor 布局

子组件会相对容器的尺寸调整尺寸。

```javascript
Ext.onReady(function(){
    var win = Ext.create("Ext.window.Window",{
        title: "My first window",
        width: 300,
        height: 300,
        maximizable : true,
        layout: "anchor",
        defaults: {xtype: "panel", height: 60, border: false},
        items: [
            {
                title: "Menu", html: "panel at 100% - 10 px",
                anchor:'-10' // 一个值则针对宽度，数字表示 100% 容器宽度 - 10px
            },{
                title: "Content", html: "panel at 70% of anchor",
                anchor:'70%' // 表示 70% 容器宽度
            },{
            title: "3rd Panel",
            html: "panel at 50% width and 40% height of anchor",
            anchor:'50% 40%', // 50% 宽度， 40% 容器宽度
            bodyStyle:'background-color: #fc3;'
        }
        ]
    });
    win.show();
});
```

## 更多布局

还有 Hbox, VBox, Table 等。


# 参考 

+ [Chapter3: Components and Layouts](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
