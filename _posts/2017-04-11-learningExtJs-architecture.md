---
title: ExtJS 的应用结构--Learning ExtJS(4th)
date: 2017-04-11
writing-time: 2017-04-11 09:06--16:16
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

Ext JS 4 开始引入 MVC，Ext JS 5 开始引入 MVVM。

MVVM 中引用 VM(view model) 来管理视图的数据。

# MVC 和 MVVM 模式

+ Model: 数据项与数据的集合。
+ View: 与用户交互的可视部分。
+ Controller: 应用逻辑（事件处理器和方法）都放在这些特殊类中，它像是 Model 和 View 之间的中介者。
+ ViewController: 这是一种只关联到某个特定 View 实例的 Controller，用来管理该特定的视图及其子组件。每当视图创建时，对应该视图的一个新 ViewController 实例会随之创建。
+ ViewModel: 这个类管理有一个数据对象，我们能将它的数据和某个视图绑定。ViewModel 与 ViewController 类似，当有新视图实例创建时，新的 ViewModel 实例也会随之创建。


## Model-View-Controller (MVC)

这种模式分成 3 部分。

![MVC 模式](/assets/images/learningextjs4th/mvc_pattern.png)


## Model-View-ViewModel (MVVM)

这种模式引用了数据绑定。这种方式下，基于尽量减少视图处理代码的思想，Model 与框架本身在内部进行了更多的交互。

尽管名字是 Model-View-ViewModel (MVVM)，但也会用到 Controller，因此这种模式也叫 MVC + VM。

![MVVM 模式](/assets/images/learningextjs4th/mvvm_pattern.png)

以表单为例，使用 ViewModel 的目的是将其数据与表单上的表单项绑定，从而无需为各表单项设置值，只需将表单项与数据项绑定即可。


# 应用举例

## 创建应用

```bash
$ sencha -sdk /path/to/ext generate app MyApp /path/to/myapp/
```

## 视图

```javascript
//file: app/view/MyViewport.js
// 类名必须和文件目录结构匹配
Ext.define('MyApp.view.MyViewport', {
	extend: 'Ext.container.Viewport',
	alias: 'widget.myviewport',
	requires: [
		'MyApp.view.AppZone',
		'Ext.panel.Panel'
	],
	layout: 'border',
	items: [{
		xtype: 'panel', 
		region: 'north',
		height: 76,            
		itemId: 'appHeader',
		bodyPadding:0, 
		cls:'appheaderbg', 
		title: '', 
		header:false,
		html: '<div class="appheader appheaderbg"><img src="resources/images/myapp_logo.png"/></div>'
	},{
		xtype: 'appzone',
		region: 'center',
		itemId: 'myappZone'
	}]
});
```

```javascript
//file: app/view/AppZone.js
Ext.define('MyApp.view.AppZone', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.appzone',
    // Alias property let us define the xtype to appzone on the viewport previously
    requires: [
		'MyApp.store.ModulesTreeDs', 
        'Ext.tab.Panel',
        'Ext.tab.Tab',
        'Ext.tree.Panel',
		'Ext.tree.View'
    ],
    layout: 'border',
    header: false,
    title: '',
    items: [
        {
            xtype: 'tabpanel',
            region: 'center',
            itemId: 'mainZone',
            header: false,
            title: '',
            items: [{
                xtype: 'panel',
                itemId: 'startappPanel',
                title: 'Dashboard',
                bodyPadding: 5, 
                html:'MyApp Dashboard', 
                region: 'center'
            }]
        },{
            xtype: 'panel',
            itemId: 'accessPanel',
            region: 'west',
            split: true,
            width: 180,
            layout: 'fit',
            title: 'App modules',
            items: [{
                xtype: 'treepanel',
                header: false,
                title: 'My Tree Panel',
                store: Ext.create( 'MyApp.store.ModulesTreeDs', { 
                    storeId: 'accessmodulesDs'
                }), //'ModulesTreeDs'
                rootVisible: false
            }]
        }
    ]
});
```

## Model

```javascript
//file: app/model/ModulesModel.js
Ext.define('MyApp.model.ModulesModel', {
    extend: 'Ext.data.Model',
    requires: [
        'Ext.data.field.String',
        'Ext.data.field.Boolean',
        'Ext.data.field.Integer'
    ],
    fields: [
        {type: 'string', name: 'description'},
        {type: 'boolean', name: 'allowaccess'},
        {type: 'int', name: 'level'},
        {type: 'string', name: 'moduleType',  defaultValue: ''},
		{type: 'string', name: 'moduleAlias', defaultValue: ''},
        {type: 'string', name: 'options'}
    ]
});
```

创建 Store:

```javascript
//file: app/store/ModulesTreeDs.js
Ext.define('MyApp.store.ModulesTreeDs', {
    extend: 'Ext.data.TreeStore',
    requires: [
        'MyApp.model.ModulesModel',
		'Ext.data.proxy.Ajax'
    ],
    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'mymodulesTreeDs',
			autoLoad: true,
            model: 'MyApp.model.ModulesModel',
            proxy: {
                type: 'ajax',
                url: 'serverside/data/menu_extended.json'
            }
        }, cfg)]);
    }
});
```

```javascript
// file: app.js
Ext.Loader.setConfig({
    MyApp: 'app'
});

Ext.application({
    name: 'MyApp', // 必须是自定义组件的首个命名空间
    controllers: [
        'App' // 对应 'MyApp.controller.App'
    ],
    views: [
            'MyViewport', // 对应 'MyApp.view.MyViewport'
            'AppZone' // 对应 'MyApp.view.AppZone'
    ],

    // the application's main entry
    launch: function(){
        Ext.create('MyApp.view.MyViewport');
    }
});
```

## 控制器

使用 MVC 模式，在树面板上添加交互代码。当点击树叶子结点时，根据结点配置内容，进行相应操作，如打开新的面板，打开窗口，或访问新链接。

```javascript
//file: app/controller/App.js
Ext.define('MyApp.controller.App', {
    extend: 'Ext.app.Controller',	
    requires:[
        'MyApp.view.AppZone',
        'MyApp.view.MyViewport'	
    ],
    config:{
        // 定义引用
        refs: {
            // 定义该引用后，要在本 Controller 中
            // 获取该组件的实例，只需用其相应的 get 函数，
            // 即 this.getMyappzone()
            myappzone: {
                selector: 'appzone', // 对应 alias: 'widget.appzone'
                xtype: 'appzone',
                autoCreate: false
            }
        }
    },

    // 该控制器的初始化函数，
    // 每当创建该控制器实例时会
    // 首先调用该函数。
    // 一般在这里定义一些事件侦听处理
    init: function() {
        console.log('app controller init');
        var me = this;
        this.control({
            // appzone, treepanel 是基于 xtype 选择
            // #accessPanel 是基于组件的 itemId 属性值选择
            'appzone #accessPanel treepanel': {
                // 树叶子结点双击事件
                itemdblclick: me.handleAccess	
            }
        });
    },

    handleAccess:function(cmpView, record, itemx, index, evt, eOpts){
        console.log('handle access for: ' + record.data.text);
        var me = this, moduleData = record.data;

        // 基于 moduleType 值进行不同操作
        if (moduleData.hasOwnProperty('moduleType')){
            var typeModule = moduleData.moduleType;
            if (typeModule == ''){
                return;
            } else if (typeModule == 'link'){
                me.executeLink(moduleData);
            } else if (typeModule == 'window'){
                me.runWindow(moduleData);
            } else if (typeModule == 'module'){
                me.addModule(moduleData);
            }
        }
    },

    addModule: function(data){
        console.log('Adding Module: ' + data.options);
        var me = this;
        var myZone = me.getMyappzone();
        var modulesTab = myZone.query('tabpanel#mainZone')[0];
        var existModule = false;
        for (var i=0; i<modulesTab.items.items.length; i++){
            if (modulesTab.items.items[i].xtype == data.moduleAlias){
                existModule = true;
                break;
            }
        }
        if (existModule){
            modulesTab.setActiveTab(i);
            return;
        }
        else {
            var mynewModule = Ext.create(data.options);
            modulesTab.add(mynewModule);
            modulesTab.setActiveTab(modulesTab.items.items.length - 1);
            return;
        }
    },

    runWindow: function(data){
        console.log('Execute window: ' + data.options);
        Ext.Msg.alert("Window module", "here we show window: <b>" +
            data.text + "</b>");
    },

    executeLink: function(data){
        console.log('Launch Link: ' + data.options);
        window.open(data.options);
    }
});
```

而树 Store 结点的 JSON 内容如下：

```json
{
	"text": "My app",
	"expanded": true,
	"allowaccess":true,
	"description":"Main application",
	"level":1,
	"children": [
		{
			"text": "Modules",
			"expanded": true,
			"allowaccess":false,
			"description":"Main modules for administrate information",
			"level":2,
			"children": [
				{
					"leaf": true,
					"text": "Customers",
					"allowaccess":false,
					"description":"Customer administration",
					"level":3,
					"iconCls":"customer-16",
					"moduleType":"module",
					"moduleAlias":"customersmodule",
					"options":"MyApp.view.modules.Customers"
				}
			]
		}, {
			"text": "Support",
			"description":"Support modules",
			"level":2,
			"expanded": true,
			"children": [
				{
					"leaf": true,
					"text": "Submit a ticket",
					"allowaccess":false,
					"description":"Submit support tickets",
					"level":3,
					"moduleType":"window",
					"iconCls":"support-16",
					"options":"MyApp.view.Ticket"	
				}, {
					"leaf": true,
					"text": "Forum",
					"allowaccess":false,
					"description":"Go to Forum",					
					"level":3,					
					"moduleType":"link",
					"iconCls":"link-16",
					"options":"http://www.sencha.com/forum/"	
				}, {
					"leaf": true,
					"text": "Visit our web site",
					"allowaccess":false,
					"description":"Go to website",	
					"level":3,					
					"moduleType":"link",
					"iconCls":"link-16",
					"options":"http://www.sencha.com/"	
				}
			]
		}
	]
}
```

## 创建 Customer 模块

```javascript
// file: app/model/Customer.js
Ext.define('MyApp.model.Customer',{
	extend:'Ext.data.Model',
	idProperty:'id', 
	fields:[
		{name: 'id'		 , type: 'int'},
		{name: 'name'    , type: 'string'},
		{name: 'phone'   , type: 'string'},
		{name: 'website' , type: 'string'},
		{name: 'status'  , type: 'string'},
		{name: 'clientSince' , type: 'date', dateFormat: 'Y-m-d'}, 
		{name: 'country' , type: 'string'},
		{name: 'sendnews', type: 'boolean'},		
		{name: 'employees', type: 'int'}
	]
});
```

```javascript
// file: app/store/CUstomers.js
Ext.define('MyApp.store.Customers', {
    extend: 'Ext.data.Store',
    requires: [
        'MyApp.model.Customer',
        'Ext.data.proxy.Ajax',
        'Ext.data.reader.Json'
    ],
    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'Customers',
            autoLoad: true,
			pageSize: 25,
            model: 'MyApp.model.Customer',
            proxy: {
                type: 'ajax',
                url: 'serverside/data/customers.json',
                actionMethods:{read:"POST"},
                reader: { 
					type: 'json', 
					rootProperty: 'records', 
					useSimpleAccessors: true 
				}
            }
        }, cfg)]);
    }
});
```

创建一个 Customer Grid。

```javascript
//file app/view/modules.Customers.js
Ext.define('MyApp.view.modules.Customers', {
    extend: 'Ext.grid.Panel',
    requires: [		
		'Ext.grid.column.Number',
        'Ext.grid.column.Date',
        'Ext.grid.column.Boolean',
        'Ext.view.Table',
        'Ext.button.Button',
        'Ext.toolbar.Fill',
        'Ext.toolbar.Paging',
		'MyApp.view.modules.CustomersController',		
		'MyApp.view.forms.CustomerWindow'
    ], 
	xtype: 'customersmodule',
    alias: 'widget.customersmodule',	

    // 定义 view controller
	controller: 'customersmodule',  // ViewController, 对应 alias: 'controller.customersmodule
    frame: false,
    closable: true,
    iconCls: '',
    title: 'Customers...',
	forceFit:true,
	listeners:{
        // 侦听函数都在本视图的 ViewController 中定义
		afterrender:{fn:'myafterrender'}, 
		render:{fn:'myrenderevent'}
	},
	initComponent: function() {
		var me=this;
		var myStore= me.createCustomersStore();  
		me.store   = myStore; 		
		me.columns =[{ 
				xtype: 'rownumberer',  
				width: 50, 
				align:'center'
			},{ 
				xtype: 'numbercolumn',
				width: 70, 
				dataIndex: 'id',
				text: 'Id', 
				format: '0'
			},{
				xtype: 'templatecolumn',
				text: 'Country',
				dataIndex: 'country',			
				tpl: '<div> <div class="flag_{[values.country.toLowerCase()]}">&nbsp</div> &nbsp;&nbsp;{country}</div>'
			},{
				xtype: 'gridcolumn',
				width: 210,
				dataIndex: 'name',
				text: 'Customer name'
			},{
				xtype: 'datecolumn',
				dataIndex:'clientSince',
				width: 120,
				text: 'Client Since',
				format: 'M-d-Y',
				align:'center'
			},{
				xtype: 'booleancolumn',
				dataIndex:'sendnews',
				width: 100,	
				align:'center',
				text: 'Send News?',
				falseText: 'No',
				trueText: 'Yes'
			}
		]; 
		me.dockedItems=[{
				xtype: 'toolbar', dock: 'top',

                // 侦听函数都在本视图的 ViewController 中定义
				items: [{
						xtype: 'button', text: 'New...',  iconCls:'addicon-16', action:'newrecord', listeners: {click:'bntactionclick' }    
					},{
						xtype: 'button', text: 'Edit...', iconCls:'editicon-16', action:'editrecord', listeners: {click:'bntactionclick' } 
					},{
						xtype: 'button', text: 'Delete...', iconCls:'deleteicon-16', action:'deleterecord', listeners: {click:'bntactionclick' } 
					},{
						xtype: 'tbfill'
					},{
						xtype: 'button', text: 'Help.', iconCls:'help-16', action:'showhelp' //, listeners: {click:'bntactionclick' } 
					}
				]
			}
//			,{
//				xtype: 'pagingtoolbar', dock: 'bottom',
//				store: myStore , 
//				displayInfo: false, displayMsg: 'Displaying {0} - {1} of {2} customer(s)'				
//			}
		];
		me.callParent();
	},
	createCustomersStore:function(){ 		
		return Ext.create('MyApp.store.Customers'); 
	}
});
```

## ViewController

在 MVC 模式中，只用一个控制器来处理所有的视图逻辑，会使代码难以维护。而 ViewController 只处理一个具体视图实例的逻辑，它只关联个某个特定的视图。

创建 Customers 的 ViewController：

```javascript
//file: view/modules/CustomersController.js
Ext.define('MyApp.view.modules.CustomersController', {
    extend: 'Ext.app.ViewController',

    // 定义别名后，可用 controller: 'customersmodule' 来引用
    alias: 'controller.customersmodule',
	config: {
         control: { // Other alternative on how to listen some events 
             // customersmodule 和 button 是基于 xtype 选择
             // [action=showhelp] 基于属性值选择
             'customersmodule button[action=showhelp]': {
                 click:'bntactionclick'
             }
          }
    },
	init: function() {
		console.log('customers view controller init'); 
	},
	myrenderevent:function(cmpx, eOpts){
		console.log('Grid - module customers render event'); 		
	},
	myafterrender:function(cmpx, eOpts){
		console.log('Grid - module customers afterrender event'); 
	}, 
	bntactionclick:function(btnx, evt, eOpts){
	console.log('Button clicked : ' + btnx.action);
		if (btnx.action=='newrecord'){	
			var mywindow = Ext.create('MyApp.view.forms.CustomerWindow',{
				action:'add',
				record:null, 
				gridModule:this.view // 关联的视图
			}); 
			mywindow.show();
			
		} else if (btnx.action=='editrecord'){ 
			var hasSelection = this.view.getSelectionModel().hasSelection(); 
			if (!hasSelection){
				Ext.Msg.alert('Error..', 'please select a record for edit..!');	
				return; 
			}
			var selectedRecords = this.view.getSelectionModel().getSelection();
			if  (selectedRecords.length<=0 || selectedRecords.length>1){ 
				Ext.Msg.alert('Error..', 'please select only one record for edit..!');	
				return; 		
			}
			var myrecord = selectedRecords[0]; 
			var mywindow = Ext.create('MyApp.view.forms.CustomerWindow',{
				action: 'edit',
				record: myrecord.data, 
				gridModule:this.view 			
			}); 
			mywindow.show();	
		
		} else if (btnx.action=='deleterecord'){ 
			var hasSelection = this.view.getSelectionModel().hasSelection(); 
			if (!hasSelection){
				Ext.Msg.alert('Error..', 'please select a record for delete..!');	
				return; 
			}
			var selectedRecords = this.view.getSelectionModel().getSelection();
			if  (selectedRecords.length<=0 || selectedRecords.length>1){ 
				Ext.Msg.alert('Error..', 'please select only one record for delete..!');	
				return; 		
			}
			var myrecord = selectedRecords[0]; 
			Ext.Msg.show({
				title:'Delete customer...?',
				message: 'Are you sure to delete customer:<br><b>' + myrecord.data.name + ' </b>...?',
				buttons: Ext.Msg.YESNO,
				icon: Ext.Msg.QUESTION,
				fn: function(btn) {
					if (btn === 'yes') {
						var test=11;
						this.view.getStore().remove(myrecord);	
						this.view.getView().refresh();						
						Ext.Msg.alert('Ok', 'Customer has been deleted..!');							
						//Usually we place an ajax request , send data and check response to make the proper actions												
					} else if (btn === 'no') {
						return; 
					} 
				},
				scope:this 
			});
			
		} else if (btnx.action=='showhelp'){ 
					
			Ext.Msg.alert('Help..', 'show customers help');	
				
		}
		
	}
});
```

## ViewModel

ViewModel 类用来管理数据。它能侦听数据的改动，并和与其绑定的组件（及其子组件）进行交互。

从 Ext JS 5 开始，所有的组件都有一个 bind 配置对象，用于将属性与 ViewModel 中的数据进行绑定。

当某个视图实例创建时，与其关联的 ViewModel 也会对应创建一个新的实例。


```javascript
// file: app/view/forms/CustomerFormViewModel.js
// 定义一个 ViewModel
Ext.define('MyApp.view.forms.CustomerFormViewModel', {
    extend:'Ext.app.ViewModel',
    alias: 'viewmodel.customerform',

    // 默认的数据对象，这些数据会与视图绑定
	data:{
		action:'add',
		ownerCmp:null, 		
		rec:null		
	},

    // 定义命名值，这些值通过函数来管理
    // 通过执行函数还可以完成其它额外操作
    // 传入的参数 get 可用来获取 data 中的数据值
	formulas:{
		readOnlyId:function(get){
			return (get('action')!=='add'); //?true:false;
//			if (get('action')!='add'){ //Edit action
//				return true; 
//			} else { 
//				return false;
//			} 						
		},
		ownerNotNull:function(get){
			var cmpx = get('ownerCmp'); 
			return (cmpx!==null && cmpx!==undefined); // ?false:true; 
		},
		refName:function(get){
			var value='';
			if (get('action')!=='add'){ //Edit action
				var id = get('rec.id'), custname =get('rec.name'); 
				if (custname===''){ custname ='(not defined)'; } 
				value = 'Editing : ' +  id + ' - ' + custname + "..." ; 									
			} else { 
				value = 'New customer...';
			} 
            
            // this.getView() 可获取关联的视图实例
			var xtypeOwner = this.getView().ownerCt.getXType(); 
			if (xtypeOwner=="customerwindow"){ 
				this.getView().ownerCt.setTitle(value);
			}
			return value; 
		}
	}
});
```

进行数据绑定：

```javascript
// file: app/view/forms/CustomerForm.js
Ext.define('MyApp.view.forms.CustomerForm', {
    extend: 'Ext.form.Panel',
    alias: 'widget.customerform',
	xtype: 'customerform', 
    requires:[
        'Ext.form.field.Number', 
		'Ext.form.field.Date',
        'Ext.form.field.ComboBox',
        'Ext.toolbar.Toolbar', 
		'Ext.toolbar.Fill',
        'Ext.button.Button',
		'MyApp.view.forms.CustomerFormViewController',		
        'MyApp.view.forms.CustomerFormViewModel',
		'MyApp.model.Customer'		
    ],
	controller: 'customerform',  // ViewController
    viewModel: {type: 'customerform' }, // 对应 alias: 'viewmodel.customerform'
    bodyPadding: 6, 
	header: false, title:'Customer...',

    // 从 ExtJS 5 开始，每个组件都有 bind 设置项。
    // 用来绑定 ViewModel 中的值
    // 值可以是 ViewModel 中 data 对象中的值，
    // 也可以是来自 formulas 对象中的命名名
	bind:{title:'{refName}'},
	defaults:{labelAlign: 'right',labelWidth: 110,msgTarget: 'side', anchor: '-18'},
    items: [{
            xtype: 'numberfield',fieldLabel: 'Customer ID',
			name:'id', 
            anchor: '100%', maxWidth: 200, minWidth: 200, hideTrigger: true,			
			bind:{
				value:'{rec.id}', 
				readOnly:'{readOnlyId}'
			}
        },{
            xtype: 'textfield',
            fieldLabel: 'Name',
			name:'name',
			bind:'{rec.name}'
        },{
            xtype: 'textfield',
            fieldLabel: 'Phone',
			name:'phone',
			bind:'{rec.phone}'
        },{
            xtype: 'textfield',
            fieldLabel: 'Web site',
			name:'website',
			bind:'{rec.website}'
        },{
            xtype: 'datefield',
            anchor: '60%',
            fieldLabel: 'Client since',
			name:'clientSince',
			submitFormat : 'Y-m-d', 
			bind:'{rec.clientSince}'
        },{
            xtype: 'combobox',
            fieldLabel: 'Country',
			name:'country',
			store: Ext.create('Ext.data.Store', {
			    fields: ['id', 'name'],
			    data : [
					{"id": "USA","name": "United States of America"},
					{"id": "Mexico","name": "Mexico"}
			    ]			
			}),
			valueField:'id', 
			displayField:'name',
			bind:'{rec.country}'
        },{
            xtype: 'combobox',
            fieldLabel: 'Status',
			name:'status',
			store: Ext.create('Ext.data.Store', {
			    fields: ['id', 'name'],
			    data : [
					{"id": "Active","name": "Active"},
					{"id": "Inactive","name": "Inactive"},	
					{"id": "Suspended","name": "Suspended"},
					{"id": "Prospect","name": "Prospect"}
			    ]			
			}),
			valueField:'id', 
			displayField:'name',
			bind:'{rec.status}'
        },{
            xtype: 'numberfield',
            anchor: '60%',
            fieldLabel: '# Employees',
			name:'employees',
			bind:'{rec.employees}'
        },{
			xtype:'checkbox', 
			fieldLabel: 'Send news ?',
			boxLabel:'check if yes/uncheck if no...!', 
			name:'sendnews', 
			inputValue:1,
			bind:'{rec.sendnews}'
		}
    ],
    dockedItems: [{
		xtype: 'toolbar', dock: 'bottom',
		items: [{
				xtype: 'tbfill'
			},{
				xtype: 'button',
				iconCls: 'save-16',
				text: 'Save...', action:'savecustomer'
			},{
				xtype: 'button',
				iconCls: 'cancelicon-16',
				text: 'Close / Cancel', action:'closeform', 
				bind:{ hidden:'{ownerNotNull}'}
		}]
	}], 
	initComponent: function() { //step 4 
		var me=this;
		var test=this; 
		me.callParent();
	}, 
	listeners:{
		'titlechange':{
			fn:function( panelx, newtitle, oldtitle, eOpts){
				if (panelx.rendered){ 
					panelx.ownerCt.setTitle(newtitle);					
				}
			}	
		}, 
		'afterrender':{
			fn:function( panelx, eOpts ){
				panelx.ownerCt.setTitle(panelx.title);
			},
			single:true		
		}
	}
});
```

```javascript
// file: app/view/forms/CustomerFormViewController.js
Ext.define('MyApp.view.forms.CustomerFormViewController', {
    extend: 'Ext.app.ViewController' ,
    alias:  'controller.customerform',
	config: {
         control: {
             'customerform button[action=savecustomer]': {
                 click:'saveCustomer'
             },
			 'customerform button[action=closeform]': {
                 click:'formClose'
             }			 
          }
    },
	init: function() {
		//console.log('customers form view controller init'); 
	},
	formClose:function(cmpx, eOpts){
		//console.log('Closing Form'); 
		var closeCmp= this.getViewModel().get('ownerCmp');		
		if  (closeCmp!=null && closeCmp!=undefined){			
			var xtypeUsed = closeCmp.getXType(); 		
			if (xtypeUsed =='panel' || xtypeUsed =='gridpanel' || xtypeUsed =='window' || xtypeUsed =="customerwindow"){ 
				closeCmp.close(); 				
			}
		}
		return;  
	},
	saveCustomer:function(btnx, evt, eOpts){		
		var action = this.getView().getViewModel().get('action'); //: "edit";
		//console.log('Performing action in form : ' + btnx.action); 
		if (action=='add'){ 
			if  (  this.getView().getForm().isValid() ) { 
				var newCustomerData =this.getView().getForm().getValues(); 				 
				var mycustomer = Ext.create('MyApp.model.Customer', newCustomerData );				
				this.getView().gridModule.getStore().add(mycustomer); 
				Ext.Msg.alert('Ok', 'New customer added succesfully!');	
				this.formClose();											
			} else  { 
				Ext.Msg.alert('Error!', 'There are some errors in the form , please check the information!');
				return;			
			} 
		} else { //Edit action 
			if  (  this.getView().getForm().isValid() ) { 
				var newCustomerData =this.getView().getForm().getValues(); 		
				var Record = this.getView().gridModule.getStore().getById( newCustomerData.id ); 				
				var editResult = Record.set(newCustomerData); 
				if (editResult!=null){ 
					Record.commit();
					Ext.Msg.alert('Ok', 'Customer edited succesfully!');	
					this.formClose();	
				} else { 
					Ext.Msg.alert('Error!', 'Error updating customer.!');
					return;			
				}
			} else  { 
				Ext.Msg.alert('Error!', 'There are some errors in the form , please check the information!');
				return;			
			}
		} 

	}
});
```

创建编辑窗口。

```javascript
// file: app/view/forms/CustomerWindow.js
Ext.define('MyApp.view.forms.CustomerWindow', {
    extend: 'Ext.window.Window',
    alias: 'widget.customerwindow',
	xtype: 'customerwindow',
    requires: [
       'MyApp.view.forms.CustomerWindowViewController',
	   'MyApp.view.forms.CustomerForm'   
    ],
	controller: 'customerwindow', 
    height: 368, 
	width:  489, 
	iconCls: 'customer-16',
	layout:'fit', 
	closable:true, 
	minimizable:true,
	title: '',
	tools:[{
		type:'restore',
		tooltip: 'Restore window...',	
		handler: function(event, toolEl, panelHeader) {
			var cmpx=panelHeader.up('window');
			if (cmpx.collapsed){
				cmpx.expand();
			} 
		}
	}],
	initComponent: function() { //step 4 
		var me=this;
		var myForm = Ext.create('MyApp.view.forms.CustomerForm',{
			gridModule: me.gridModule,
			viewModel:{
				data:{
					action:me.action,
					ownerCmp: me, 		
					rec:  me.record || null,
					test:'test string for development'
				}			
			}
		});
		me.items=[myForm]; 
		me.callParent(arguments);	
	}
});
```

```javascript
//file: app/view/forms/CustomerWindowViewController.js
Ext.define('MyApp.view.forms.CustomerWindowViewController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.customerwindow', 
	config: {
		control:{
			'customerwindow':{
			   'minimize':'mywindowMinimize', 
			   'expand':'myExpand'
			}
		}
	},
	mywindowMinimize:function(cmpx, eOpts){
		//console.log('customerWindow minimizing..!');
		cmpx.collapse();
        cmpx.alignTo(Ext.getBody(),'tr-tr');
	},
	myExpand:function(cmpx, eOpts){
		cmpx.center();	
	}
});
```

# 路由 (router)

Ext JS 5 开始引入了路由功能。路由基于浏览器的历史堆栈，可实现对踪应用的状态的跟踪。

当访问 `http://localhost/#basic-panels` 时， `#basic-panels` 部分叫作一个 hash 或 fragment identifier。浏览器会触发一个 `haschange` 事件，我们的应用可对该事件进行相关操作。

先在 `app.js` 的末尾添加：

```javascript
init: function(){
    // 加载应用后，如果 URL 中没有 hash 部分，则默认设置 ''
    this.setDefaultToken('');
}
```

将 `app/controller/App.js` 中的 handleAccess 改为：

```javascript
handleAccess:function(cmpView, record, itemx, index, evt, eOpts){
    console.log('handle access for: ' + record.data.text);
    var me = this, moduleData = record.data;

    // 基于 moduleType 值进行不同操作
    if (moduleData.hasOwnProperty('moduleType')){
        var typeModule = moduleData.moduleType;
        if (typeModule == ''){
            return;
        } else if (typeModule == 'link'){
            me.executeLink(moduleData);
        } else if (typeModule == 'window'){
            me.runWindow(moduleData);
        } else if (typeModule == 'module'){
            // 使用 router
            if (moduleData.options == "MyApp.view.modules.Customers") {
                // redirectTo 会更新 router 的 hash，
                // 默认如果路由的当前 hash 和传入的 hash 相同时不会
                // 进行路由操作。
                // customer 是传入的 hash
                // 第 2 个参数 true 强制进行路由 hash 更新。
                this.redirectTo('customers', true);
                return;
            }
            else {
                me.addModule(moduleData);
            }
        }
    }
}
```

在 `app/controller/App.js` 中的添加路由设置：

```javascript
config:{
        // 定义引用
        refs: {
            // 定义该引用后，要在本 Controller 中
            // 获取该组件的实例，只需用其相应的 get 函数，
            // 即 this.getMyappzone()
            myappzone: {
                selector: 'appzone', // 对应 alias: 'widget.appzone'
                xtype: 'appzone',
                autoCreate: false
            }
        },

        // 定义路由
        routes: {
            ':id': {
                // 在进行路由操作前执行
                before: 'beforeHandleRoute',

                // 进行路由操作
                action: 'handleRoute'
            }
        }
},

//...

// 在进行路由操作前执行
beforeHandleRoute: function(id, action) {
    if (id!='customers'){
        Ext.Msg.alert("Route error", "invalid action...!");
        action.stop(); // 不继续进行路由操作
    } else {
        action.resume(); //继续进行，即调用 handleRoute
    }
},

// 进行路由操作
handleRoute: function(id) {
    if (id=='customers'){
        var myStore=this.getMyappzone().query('treepanel')[0].getStore();
        // 根据结点的 text 值查找一条结点记录
        var myRecord = myStore.findNode('text', 'Customers');

        if (myRecord!=undefined){
            this.addModule(myRecord.data);
        } else {
            Ext.Msg.alert("Route error", "error getting customers data access...!");
        }
    }
}
```

# 参考 

+ [Chapter10: Architecture](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
