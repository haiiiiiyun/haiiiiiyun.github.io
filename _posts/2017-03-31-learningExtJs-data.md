---
title: ExtJS 数据--Learning ExtJS(4th)
date: 2017-03-31
writing-time: 2017-03-31 09：01
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

所有需要显示信息的组件都通过 Store 来管理数据。

# Ajax

Ext 的单例对象 `Ext.Ajax` 用于 Ajax 请求。

```javascript
// 用 request 方法进行 Ajax 请求
Ext.Ajax.request({
    url:"serverside/myfirstdata.json",

    // 请求成功时的回调函数，
    // 即当服务端应答码为 200-299 时运行。

    // 函数参数 response 是服务器返回的应答对象，
    // 可以从中抽取出应答文体 responseText 和应答头信息。
    // 函数参数 options 就是我们传入 Ajax request 方法的所有信息，
    // 这里即 url, success, failure, callback。
    success: function(response,options){
        // 从应答对象中提取出应答文本 response.responseText
        // 并用 Ext.decode 方法将 JSON 文件转成 JS 对象
        // 假设返回的 JSON 为：
        // {
        //  "success": true,
        //  "msg": "This is a success message..!"
        // }
        var data = Ext.decode(response.responseText);
        Ext.Msg.alert("Message", data.msg);
    },

    // 请求失败时的回调函数，
    // 即当服务端应答码为 403, 404, 500, 503 等时运行。
    // 参数与 success 回调函数的相同
    failure: function(response,options){
        Ext.Msg.alert("Message",
            'server-side failure with status code ' + response.status);
    },

    // 该回调函数无论请求成功还是失败都会运行

    // 函数参数 options 就是我们传入 Ajax request 方法的所有信息，
    // 函数参数 success 是布尔值，表示请求返回是否成功，
    // 函数参数 response 是一个 XMLhttpRequest 对象，包含有应答信息
    callback: function( options, success, response ){
        console.log('Callback executed, we can do some stuff !');
        // 从应答对象中提取出应答文本 response.responseText
        // 并用 Ext.decode 方法将 JSON 文件转成 JS 对象
        if(success) {
            var data = Ext.decode(response.responseText);
            Ext.Msg.alert("Message", data.msg);
        }
    }
});
```

下面是请求返回 XML 时的情况：

```javascript
Ext.Ajax.request({
    url: "serverside/myfirstdata.xml",
    success: function(response,options){
        // 假设返回的 XML 为：
        //<?xml version="1.0" encoding="UTF-8"?>
        //<response success="true">
        //  <msg>This is a success message in XML format</msg>
        //</response>
        var data = response.responseXML;
        var node = xml.getElementsByTagName('msg')[0];
        Ext.Msg.alert("Message", node.firstChild.data );
    },
    failure: function(response,options){
        Ext.Msg.alert("Message",
            'server-side failure with status code ' + response.status);
    }
});
```

## 向 Ajax 请求中传入请求参数，设置请求超时毫秒数

```javascript
Ext.Ajax.request({
    url: "serverside/myfirstparams.php",
    method: 'POST', // 设置请求方式，转为为 'GET'
    params: { // 通过 params 属性可传入多个参数
        x:200,
        y:300
    },
    // 设置请求超时为 50000 毫秒，即 50 秒
    // 默认为 30 秒，超时后将放弃等待应答
    timeout: 50000, 
    success: function(response,options){
    },
    failure: function(response,options){
    }
});
```

# 数据模型 Model

一个 Model 代表一个对象或实体，如 客户 Client，收据 Invoice 等。而 Model 会被 Store 使用。

一个 Model 可含有多个数据项，验证器信息，以及与其它 Model 的关联。还可通过设置一个代理来获取或存储数据。

```javascript
// 创建一个 Model
Ext.define('Myapp.model.Client',{
    extend:'Ext.data.Model', // 自定义 Model 都扩展至 Ext.data.Model

    // 指定 JSON 应答中，每条记录中
    // 作为 ID 项的属性名
    // 如果没有指定，Model 会在每条记录中
    // 自动创建一个 `id` 属性
    idProperty:'clientId ',
    fields:[
        // 数据项的类型 type 值可为：
        //    string
        //    int
        //    float
        //    boolean
        //    date（记得设置 dataFormat 属性）
        //    auto（表示不对接收到的数据进行任何转换）
        {name: 'clientId', type: 'int'},
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},
        {name: 'website' , type: 'string'},
        {name: 'status' , type: 'string'},
        {name: 'clientSince', type: 'date', dateFormat:'Y-m-d H:i'}
    ],

    // 设置数据项的验证规则
    // type 定义使用哪个规则，
    // Ext 内置有常用的验证规则，如：
    //   inclusion, exclusion, presence, length, format, e-mail 等
    //   针对各种验证规则，可能还需要额外的参数，如 length 的 min 和 max。
    // type 值实际上对应于 Ext.data.Validator 子类中的一个函数。
    validators:{
        name:[
            { type:'presence'}
        ],
        website:[
            { type:'presence', allowEmpty:true},
            { type:'length', min: 5, max:250 }
        ]
    }
});

// 创建一个 Model 实例
var myclient = Ext.create('Myapp.model.Client',{
    clientId:10001,
    name:'Acme corp',
    phone:'+52-01-55-4444-3210',
    website:'www.acmecorp.com',
    status:'Active',
    clientSince:'2010-01-01 14:35'
});

// GET 方法
var nameClient = myclient.get('name'); // 'Acme Corp'
var websiteClient = myclient.get('website'); // 'ww.acmecorp.com'

// SET 方法
myclient.set('phone','+52-01-55-0001-8888'); // 设置一个值
myclient.set({ // 设置多值
    name: 'Acme Corp of AMERICA LTD.',
    website:'www.acmecorp.net'
});

// 实际上在 Model 实例中，所有的数据项信息都保存在 `data` 属性中，
// 因此可以直接通过 data 属性进行读写
// 读:
console.log(myclient.data.name); // 'Acme Corp'
// 写：
myclient.data.website = "www.acmecorp.biz";

// 但是最好通过 get 和 set 方法进行读写。因为 set 除了
// 设置值外，还会执行一些重要的操作，如：将 model 状态
// 设置为 dirty，保存旧数据以备恢复等。


// 验证器
// isValid() 方法返回布尔值
console.log(myclient.isValid()); // true
myclient.set('name', '');
console.log(myclient.isValid()); // false，因为 name 不能为空

// 显示验证错误信息
// validate() 方法错误集，即 Ext.data.ErrorCollection （扩展
// 至 Ext.util.MixedCollection）实例。
var errors = myclient.validate();
errors.each(function(error){
    console.log(error.field,error.message); // name Name must be present (custom message)
});
```

## 映射

如果应答中的数据项名与 Model 中的数据项中不相同时，可以进行映射。例如返回的 JSON 为：

```javascript
{
    "success" :"true",
    "id":"id",
    "records":[
        {
            "id": 10001,
            "name": "Acme corp2",
            "phone": "+52-01-55-4444-3210",
            "x0001":"acme_file.pdf"
        }
    ]
}
```

要将应答中的数据名 `x0001` 映射到 Model 的 `contractFileName` 数据项，如下：

```javascript
Ext.define('Myapp.model.Client',{
    extend: 'Ext.data.Model',
    idProperty: 'clientId ',
    fields:[
        {name: 'clientId', type: 'int' },
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},

        // 应答包记录中的 x0001 项对应到本 Model 的 contractFileName 项
        {name: 'contractFileName', type: 'string', mapping:'x0001'}
    ]
});
```

## 自定义数据项类型

从 Ext JS 5 开始，推荐创建自定义的数据项类型，用来替代自定义验证器。

```javascript
// 创建自定义数据项类型
Ext.define('Myapp.fields.Status',{

    // 扩展至内置的 String 数据项类型
    extend: 'Ext.data.field.String',

    // 数据项类型的别名以 'data.field' 为前缀
    alias: 'data.field.status',

    // 设置该数据项的验证器
    validators: {
        type: 'inclusion',
        list: [ 'Active', 'Inactive'],
        message: 'Is not a valid status value, please select the proper options[Active, Inactive]'
    }
});

// 在 Client Model 中使用自定义的数据项类型 status
Ext.define('Myapp.model.Client',{
    extend:'Ext.data.Model',
    idProperty:'clientId ',
    fields:[
        {name: 'clientId', type: 'int' },
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},
        {name: 'website' , type: 'string'},

        // type: 'status'，从而会引用别名为 `data.field.status` 的
        // 数据项类型
        {name: 'status' , type: 'status'},
        {name: 'clientSince' , type: 'date', dateFormat: 'Y-m-d H:i'}
    ],
    validators:{
    // ...
    }
});

// 测试自定义数据项类型
var myclient = Ext.create('Myapp.model.Client',{
    clientId: '10001',
    name: 'Acme corp',
    phone: '+52-01-55-4444-3210',
    website: 'www.acmecorp.com',
    status: 'Active',
    clientSince: '2010-01-01 14:35'
});

myclient.isValid(); // true

myclient.set('status','No longer client');
if (!myclient.isValid(){
    var errors = myclient.validate();
    errors.each(function(error){
        console.log(error.field, error.message); //status Is not a valid status value, please select the proper options[Active, Inactive]
    });
}
```

自定义数据项类型时，可用的基类有：

+ Ext.data.field.Field
+ Ext.data.field.Boolean
+ Ext.data.field.Date
+ Ext.data.field.Integer
+ Ext.data.field.Number
+ Ext.data.field.String


## Model 间的关联

### 一对多关联

```javascript
// 先定义一个 Employee Model
// file:appcode/model/Employee.js
Ext.define('Myapp.model.Employee',{
    extend:'Ext.data.Model',
    idProperty:'id ',
    fields:[
        {name: 'id', type: 'int' },

        // 该数据项用来关联 Client Model
        {name: 'clientid' , type: 'int'},
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},
        {name: 'email' , type: 'string'},
        {name: 'gender' , type: 'string'}
    ]
});

// 定义 ClientWithContacts Model，
// file:appcode/model/ClientWithContacts.js
// Client 与 Employee 有一对多关联，
// 即一个客户可能需要多个员工来提供服务。
Ext.define('Myapp.model.ClientWithContacts',{
    extend:'Ext.data.Model',

    // 会动态加载相关的依赖
    requires: ['Myapp.model.Employee'],
    idProperty:'id ',
    fields:[.... ],

    // 通过 hasMany 属性定义一对多关联
    hasMany:{
        // model 指定关联的 Model
        model:'Myapp.model.Employee',

        // 指定用来返回关联项（实际上返回的是一个 Store）的函数名，
        // 如果未指定，Ext 默认会使用关联 Model 名的复数形式，
        // 例如本例中会是 'Employees'，
        name:'employees',
        associationKey: 'employees'
    }
});

// 创建一个实例
var myclient = Ext.create('Myapp.model.ClientWithContacts',{
    id: 10001,
    name: 'Acme corp',
    phone: '+52-01-55-4444-3210',
    website: 'www.acmecorp.com',
    status: 'Active',
    clientSince: '2010-01-01 14:35'
});

// myclient.employees() 返回的是一个 Ext.data.Store 实例。
myclient.employees().add(
    {
        id:101,
        clientId:10001, // 这个是关联 Client 的 ID
        name:'Juan Perez',
        phone:'+52-05-2222-333',
        email:'juan@test.com',
        gender:'male'
    },
    {
        id:102,
        clientId:10001,
        name:'Sonia Sanchez',
        phone: '+52-05-1111-444',
        email:'sonia@test.com',
        gender:'female'
    }
);

myclient.employees().each(function(record){
    console.log(record.get('name') + ' - ' + record.get('email') );
});
```

### 一对一关联

```javascript
Ext.define('Myapp.model.Contract',{
    extend:'Ext.data.Model',
    idProperty:'id ',
    fields:[
        {name: 'id', type: 'int' },
        {name: 'contractId', type: 'string'},
        {name: 'documentType', type: 'string'}
    ]
});

// 数据项中使用 reference 指定一对一关联
Ext.define('Myapp.model.Customer',{
    extend:'Ext.data.Model',
    requires: ['Myapp.model.Contract'],
    idProperty:'id ',
    fields:[
        {name: 'id', type: 'int'},
        {name: 'name' , type: 'string'},
        {name: 'phone' , type: 'string'},
        {name: 'website' , type: 'string'},
        {name: 'status' , type: 'string'},
        {name: 'clientSince' , type: 'date', dateFormat: 'Y-m-d H:i'},

        // 数据项中没有使用 type
        // 而是使用 reference 指定一对一关联
        // 即该项会指向一个 Contract Model 实例
        {name: 'contractInfo' , reference: 'Contract', unique:true}
    ]
});

var myclient = Ext.create('Myapp.model.Customer',{
    id: 10001,
    name: 'Acme corp',
    phone: '+52-01-55-4444-3210',
    website: 'www.acmecorp.com',
    status: 'Active',
    clientSince: '2010-01-01 14:35',

    // 直接通过配置信息创建关联的 Model 实例
    // 没有在创建 Customer 实例时没有指定
    // contractInfo 项的配置信息，那么 contractInfo 
    // 不会出现在 Customer 的实例中。
    contractInfo:{
        id:444,
        contractId:'ct-001-444',
        documentType:'PDF'
    }
});
```

# Store

Store 是 Model 的一个集合，它能作为客户端（如组件）的缓存工具，用来管理客户端的本地数据。例如，对本地数据进行排序、分组、过滤等。Store 也能通过代理 proxy 从服务端获取数据，解析后合并到集合中。

组件如 grid, tree, combo box, data view 等都使用 Store 来管理数据，一旦 Store 中的数据更新了，那么组件也会自动更新。


```javascript
// 自定义一个 Store 类
Ext.define('MyApp.store.Customers',{
    // Store 都扩展至 Ext.data.Store
    extend : 'Ext.data.Store', 

    // 指定本 Store 使用的 Model（即单条记录的类型）
    model : 'Myapp.model.Customer'
});

// Store 的方法

// 创建一个 Store 实例
var store = Ext.create("MyApp.store.Customers");
console.log(store.count()); // 0

// 生成一条记录，并通过 add 方法添加到 Store 中
var mynewcustomer = Ext.create('Myapp.model.Customer',{
    id: 10001,
    name: 'Acme corp',
    phone: '+52-01-55-4444-3210',
    website : 'www.acmecorp.com',
    status: 'Active',
    clientSince: '2010-01-01 14:35',
    contractInfo:{
        id:444,
        contractId:'ct-001-444',
        documentType:'PDF'
    }
});
// add 方法将记录添加到集合的最末尾
store.add(mynewcustomer);

//add 方法也可以通过 Model 配置信息添加记录，
//Ext 会根据 Store 中的 Model 定义值自动创建相应实例
store.add({
    id: 10002,
    name: 'Candy Store LTD',
    phone: '+52-01-66-3333-3895',
    website : 'www.candyworld.com',
    status: 'Active',
    clientSince: '2011-01-01 14:35',
    contractInfo:{
        id:9998,
        contractId:'ct-001-9998',
        documentType:'DOCX'
    }
});

// add 方法也可以同时添加多个记录
var mynewcustomer = Ext.create('Myapp.model.Customer', { ...});
var mynewcustomerb = Ext.create('Myapp.model.Customer', { ...});
store.add([mynewcustomer, mynewcustomerb]);

// 遍历集合中的记录
// each 方法的第 2 个参数 [context] 是可选的，
// 用作回调函数的上下文对象。
store.each(function(record, index){
    console.log(index, record.get("name"));
});

// 获取 Store 的记录

// 通过索引位置，索引从 0 开始
var modelTest = store.getAt(2);

// 首个和最后一个
var first = store.first();
var last = store.last();

// 返回一个区别记录列表，
// 和 Python 的列表不同，这里返回 [1,3] 索引的记录
var list = store.getRange(1,3);
```

// 续 ..







# 参考 

+ [Chapter4: It's All about the Data](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
