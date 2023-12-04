---
title: 小程序框架基础
date: 2018-04-03
writing-time: 2018-04-03
categories: programming
tags: Programming miniprogram
---

小程序包含一个描述整体程序的 app 和多个描述各自页面的 page。

`app.json` 中 `window` 对象中的配置顶：

+ navigationBarBackgroundColor: 导航栏背景色，HexColor，默认为 #000000， 黑色。
+ navigationBarTextStyle: 导航栏标题颜色，默认为 white，仅支持 white/black
+ navigationBarTitleText: 导航栏标题文字内容
+ navigationStyle: 导航栏样式，仅支持 default/custom。默认为 default，当为 custom 模式时可自定义导航栏，只保留右上角胶囊状的按钮， V6.6.0 起。
+ backgroundColor: 窗口背景色，默认为 #ffffff，白色。
+ backgroundTextStyle: 下拉 loading 的样式，仅支持 dark/light, 默认为 dark。
+ backgroundColorTop: 顶部窗口的背景色，仅 iOS 支持，默认为 #ffffff，自 v6.5.16。
+ backgroundColorBottom: 底部窗口的背景色，仅 iOS 支持，默认为 #ffffff，自 v6.5.16。
+ enablePullDownRefresh: 是否开启下拉刷新，默认为 false。
+ onReachBottomDistance: 页面上拉后触发触底事件时距页面底部距离，整型，默认为 50,单位为 px。


`app.json` 中 `tabBar` 对象中的配置顶：

+ color: tab 上的文字默认颜色。
+ selectedColor: tab 上的文字选中时的颜色。
+ backgroundColor: tab 的背景色。
+ borderStyle: tabbar 边框的颜色，仅支持 black/white，默认为 black。
+ list: tab 的列表，为一个 Array，最小 2 个，最多 5 个 tab。
+ position: 可选值为 bottom, top，默认为 bottom，当为 top 时，将不会显示 icon。

list 中的列表元素配置顶：

+ pagePath: 页面路径，必须在 pages 中先定义。
+ text: tab 上按钮文字。
+ iconPath: 图片路径，icon 大小限制为 40kb，建议尺寸为 81x81 px，不支持网络图片。
+ selectedIconPath: 选中时的路径。


每个页面的 page.json 配置文件用来配置本页面的窗体 UI，里面的配置项将覆盖 `app.json` 中的 window 对象中的相同配置项。

其中新增的配置项有：

+ `disableScroll`: 设置页面不能上下滚动，只在 page 中有效，默认为 false。


## 逻辑层 App Service

在 JS 的基础上，有如下修改：

+ 增加 `App` 和 `Page` 方法，进行程序和页面的注册。
+ 增加 `getApp` 和 `getCurrentPages` 方法，分别用来获取 App 实例和当前页面栈。
+ 提供 API，获取微信用户数据，扫一扫，支付等微信功能。
+ 每个页面有独立的作用域，并提供模块化能力。
+ 由于框架并非运行在浏览器中，故 `document`, `window` 等无法使用。
+ 编写的所有代码最终会打包成一份 JS。


### 注册程序

#### App

`App()` 函数用来注册一个小程序。接受一个 object 参数，用来指定小程序的生命周期函数等。

+ `onLaunch`: 生命周期函数，当小程序初始化完成后，触发（全局只触发一次）
+ `onShow`: 生命周期函数，当小程序启动，或从后台进入前台显示后，触发
+ `onHide`: 生命周期函数，当小程序进入后台后，触发
+ `onError`: 错误监听函数，当小程序发生脚本错误，或者 api 调用失败时，会触发 onError 并带上错误信息
+ 其它：开发者可添加任意的函数，并通过 `this` 访问 App 实例。

例如：

```javascript
App({
  onLaunch: function(options) {
    // Do something initial when launch.
  },
  onShow: function(options) {
      // Do something when show.
  },
  onHide: function() {
      // Do something when hide.
  },
  onError: function(msg) {
    console.log(msg)
  },
  globalData: 'I am global data'
})
```

`onLaunch`, `onShow` 的参数有：

+ `path`: 打开小程序的来源路径, String
+ `query`: 打开小程序的 query 信息，Object
+ `scene`: 打开小程序的场景值，Number
+ `shareTicket`: String
+ `referrerInfo`: Object, 当小程序是通过另一个小程序、或公众号或 App 打开时，返回该字段
+ `referredInfo.appId`: 来源小程序、或公众号或 App的 appid
+ `referredInfo.extraData`: 来源小程序传来的数据，当 scene=1037 或 1038 时支持

#### getApp()

全局的 `getApp()` 函数返回小程序实例对象：

```javascript
// other.js
var appInstance = getApp()
console.log(appInstance.globalData) // I am global data
```

注意：

+ `App()` 必须在 app.json 中注册，且不能注册多个。
+ 不要在定义于 `App()` 内的函数中调用  `getApp()`，使用 `this` 就可拿到 app 实例。
+ 不要在 `onLaunch` 中调用 `getCurrentPages()`，此时 page 还没有生成。
+ 通过 `getApp()` 获取实例后，不要私自调用生命周期函数。

### 注册页面

`Page()` 函数用来注册一个页面。接受一个 object 参数，指定页面的初始数据，生命周期函数，事件处理函数。

object 参数有：

+ `data`: 页面原初始数据，Object。
+ `onLoad`: 生命周期函数，监听页面加载。一个页面只会调用一次，可在其中获取打开当前页所调用的 query 参数。
+ `onUnload`: 生命周期函数，监听页面卸载。当 `redirectTo` 或 `navigateBack` 时调用。
+ `onReady`: 生命周期函数，监听页面初次渲染完成。一个页面只会调用一次，代表页面已经准备妥当，可以和视图层进行交互。对界面的设置如 `wx.setNavigationBarTitle` 请在 `onReady` 之后设置。
+ `onShow`: 生命周期函数，监听页面显示。
+ `onHide`: 生命周期函数，监听页面隐藏。当 `navigateTo` 或 tab 切换时调用。
+ `onPullDownRefresh`: 页面相关事件处理函数，监听用户下拉动作。需开启 `enablePullDownRefresh`。当处理完数据刷新后， `wx.stopPullDownRefresh` 可停止当前页面的下拉刷新（关闭刷新动画）。
+ `onReachBottom`: 页面上拉触底事件的处理函数。在触发距离内滑动期间，本事件只会被触发一次。
+ `onShareAppMessage`: 用户点击右上角转发时调用。只有定义了此事件处理函数，右上角菜单才会显示 “转发” 按钮。此事件需返回一个 Object,用于自定义转发内容。
+ `onPageScroll`: 页面滚动事件的处理函数。参数为一 Object，字段有 `scrollTop`，表示页面在垂直方面已滚动的距离(px)。
+ `onTabItemTap`: 当前是 tab 页时，点击 tab 时触发。
+ 其它: 开发者可添加任意的其它函数，用 `this` 可访问本对象。

object 的内容在页面加载时会进行一次深拷贝，故需考虑数据大小对加载的影响，例如：

```javascript
//index.js
Page({
  data: {
    text: "This is page data."
  },
  onLoad: function(options) {
    // Do some initialize when page load.
  },
  onReady: function() {
    // Do something when page ready.
  },
  onShow: function() {
    // Do something when page show.
  },
  onHide: function() {
    // Do something when page hide.
  },
  onUnload: function() {
    // Do something when page close.
  },
  onPullDownRefresh: function() {
    // Do something when pull down.
  },
  onReachBottom: function() {
    // Do something when page reach bottom.
  },
  onShareAppMessage: function () {
   // return custom share data when user share.
  },
  onPageScroll: function() {
    // Do something when page scroll
  },
  onTabItemTap(item) {
    console.log(item.index)
    console.log(item.pagePath)
    console.log(item.text)
  },
  // Event handler.
  viewTap: function() {
    this.setData({
      text: 'Set some data for updating view.'
    }, function() {
      // this is setData callback
    })
  },
  customData: {
    hi: 'MINA'
  }
})
```

#### 初始化数据

作为页面的第一次渲染使用，data 中的数据必然能 JSON 化，如有字符串、数字、布尔值、对象、数组等。 这些数据要在模板中进行绑定：

```javascript
//初始化数据
Page({
  data: {
    text: 'init data',
    array: [{msg: '1'}, {msg: '2'}]
  }
})
```

模板中绑定：


```html
<view>{{text}}</view>
<view>{{array[0].msg}}</view>
```

### 自定义转发字段

`onShareAppMessage()` 返回一个 Object,用于自定义转发内容。自定义转发字段有：

+ title: 转发标题，默认值为当前小程序名称。
+ path: 转发路径，默认值为当前页面 path，必须是以 `/` 开头的完整路径。

例如：

```javascript
Page({
  onShareAppMessage: function () {
    return {
      title: '自定义转发标题',
      path: '/page/user?id=123'
    }
  }
})
```

`Page.prototype.route` 字段可以获取到当前页面的路径。

### setData()

数据绑定功能类似 React，data 中的数据项绑定到视图，当用 setData() 更新 data 后，视图中的绑定的对应部分也自动更新。

`Page.prototype.setData()` 函数用于将数据从逻辑层发送到视图层（异步），同时改变对应的 `this.data` 的值（同步）。

`setData()` 参数：

+ data: Object 类型，必填，为这次要改变的数据。
+ callback: Function 类型，可选填，在 setData 对界面渲染完毕后回调。

object 中以 key, value 形式表示。其中 key 可非常灵活，以数据路径的形式给出，如 `array[2].message`, `a.b.c.d`，并且不需要在 `this.data` 中预先定义。

注意：

+ 直接修改 `this.data` 而不调用 `this.setData` 是无法改变页面的状态的，还会造成数据不一致。
+ 单次设置的数据不能超过 1024k，尽量避免一次设置过多数据。
+ 不要将 data 中任何一项的 value 设为 undefined。

示例：

```html
<!--index.wxml-->
<view>{{text}}</view>
<button bindtap="changeText"> Change normal data </button>
<view>{{num}}</view>
<button bindtap="changeNum"> Change normal num </button>
<view>{{array[0].text}}</view>
<button bindtap="changeItemInArray"> Change Array data </button>
<view>{{object.text}}</view>
<button bindtap="changeItemInObject"> Change Object data </button>
<view>{{newField.text}}</view>
<button bindtap="addNewField"> Add new data </button>
```

```javascript
//index.js
Page({
  data: {
    text: 'init data',
    num: 0,
    array: [{text: 'init data'}],
    object: {
      text: 'init data'
    }
  },
  changeText: function() {
    // this.data.text = 'changed data'  // bad, it can not work
    this.setData({
      text: 'changed data'
    })
  },
  changeNum: function() {
    this.data.num = 1
    this.setData({
      num: this.data.num
    })
  },
  changeItemInArray: function() {
    // you can use this way to modify a danamic data path
    this.setData({
      'array[0].text':'changed data'
    })
  },
  changeItemInObject: function(){
    this.setData({
      'object.text': 'changed data'
    });
  },
  addNewField: function() {
    this.setData({
      'newField.text': 'new data'
    })
  }
})
```

Page 的生命周期：

![mina-lifecycle.png](/assets/images/miniprogram/mina-lifecycle.png)

### 路由

所有页面的路由都由框架统一管理，并以栈形式维护当前的所有页面。当发生路由切换时，页面栈操作如下：

路由方式          | 页面栈表示
:-----------------|:--
xx                |
初始化            | 新页面入栈
打开新页面        | 新页面入栈
页面重定向        | 当前页面出栈，新页面入栈
页面返回          | 页面不断出栈，直到目标返回页，新页面入栈
Tab 切换          | 页面全部出栈，只留下新的 Tab 页面
重加载            | 页面全部出栈，只留下新的页面


`getCurrentPages()` 获取当前页面栈的实例，以数组形式按栈的顺序给出，第一个是首页（栈尾），最后一个为当前页面（栈顶）。

路由的触发方式：

路由方式           | 触发时机                                                                                           | 路由前页面回调 | 路由后页面回调
:----------------- | :---------                                                                                         | :---------     | :-------
xx                 |
初始化             | 小程序打开的第一个页面                                                                             |                | onLoad, onShow
打开新页面         | 调用 `wx.navigateTo()` 或使用组件 `<navigator open-type="navigateTo"/>`                            | onHide         | onLoad, onShow
页面重定向         | 调用 `wx.redirectTo()` 或使用组件 `<navigator open-type="redirectTo"/>`                            | onUnload       | onLoad, onShow
页面返回           | 调用 `wx.navigateBack()` 或使用组件 `<navigator open-type="navigateBack"/>` 或用户按左上角返回按键 | onUnload       | onShow
Tab 切换           | 调用 `wx.switchTab()` 或使用组件 `<navigator open-type="switchTab"/>` 或用户切换 Tab               |                |
重加载             | 调用 `wx.reLaunch()` 或使用组件 `<navigator open-type="reLaunch"/>`                                | onUnload       | onLoad,onShow


+ `navigateTo`, `redirectTo` 只能打开非 tabBar 页面
+ `switchTab` 只能打开 tabBar 页面
+ `reLaunch` 可打开任意页面
+ 页面底部的 tabTab 由页面决定，即只要是定义为 tabBar 的页面，底部都有 tabBar。
+ 调用页面路由带的参数可在目标页面的 `onLoad` 中提取。


### 模块化

#### 文件作用域

变量和函数只在本文件中有效。通过全局函数 `getApp()` 可获取全局的应用实例，并将全局数据设置其中，如：

```javascript
// app.js
App({
  globalData: 1
})

// a.js
// The localValue can only be used in file a.js.
var localValue = 'a'
// Get the app instance.
var app = getApp()
// Get the global data and change it.
app.globalData++


// b.js
// You can redefine localValue in file b.js, without interference with the localValue in a.js.
var localValue = 'b'
// If a.js it run before b.js, now the globalData shoule be 2.
console.log(getApp().globalData)
```

#### 模块化

可将公用代码抽离成为一个单独 js，作为一个模块。模块只有通过 `module.exports` 或 `exports` 才能对外暴露接口。其中 `exports` 其实是对 `module.exports` 的一个引用，故不能更改其指向。

例如：

```javascript
// common.js
function sayHello(name) {
  console.log(`Hello ${name} !`)
}
function sayGoodbye(name) {
  console.log(`Goodbye ${name} !`)
}

module.exports.sayHello = sayHello
exports.sayGoodbye = sayGoodbye
```

在需要使用该模块的文件中，用 `require()` 引入：

```javascript
var common = require('common.js')
Page({
  helloMINA: function() {
    common.sayHello('MINA')
  },
  goodbyeMINA: function() {
    common.sayGoodbye('MINA')
  }
})
```

`require()` 暂不支持绝对路径。

## 视图层

### 模板语言 WXML

Mustache 语法（`{{}}`) 不仅进于绑定数据，还用于表达式值，因此还用在 `wx:for`, `wx:if` 等语句中。


**数据绑定**

```
<!--wxml-->
<view> {{message}} </view>

// page.js
Page({
  data: {
    message: 'Hello MINA!'
  }
})
```

**列表渲染**

```
<!--wxml-->
<view wx:for="{{array}}"> {{item}} </view>

// page.js
Page({
  data: {
    array: [1, 2, 3, 4, 5]
  }
})
```

**条件渲染**

```
<!--wxml-->
<view wx:if="{{view == 'WEBVIEW'}}"> WEBVIEW </view>
<view wx:elif="{{view == 'APP'}}"> APP </view>
<view wx:else="{{view == 'MINA'}}"> MINA </view>

// page.js
Page({
  data: {
    view: 'MINA'
  }
})
```

**模板**

```
<!--wxml-->
<template name="staffName">
  <view>
    FirstName: {{firstName}}, LastName: {{lastName}}
  </view>
</template>

<template is="staffName" data="{{...staffA}}"></template>
<template is="staffName" data="{{...staffB}}"></template>
<template is="staffName" data="{{...staffC}}"></template>



// page.js
Page({
  data: {
    staffA: {firstName: 'Hulk', lastName: 'Hu'},
    staffB: {firstName: 'Shang', lastName: 'You'},
    staffC: {firstName: 'Gideon', lastName: 'Lin'}
  }
})
```

**事件**

事件可以绑定在组件上，当达到触发事件，就会执行逻辑层中对应的事件处理函数。事件对象可以携带额外信息，如 id, dataset, touches。

例如：


```
//wxml 中
<view id="tapTest" data-hi="WeChat" bindtap="tapName"> Click me! </view>

//js 中
Page({
  tapName: function(event) {
    console.log(event)
  }
})
```

事件处理函数的参数是 event, 可以看到 Log 出来的信息大致为：

```json
{
"type":"tap",
"timeStamp":895,
"target": {
  "id": "tapTest",
  "dataset":  {
    "hi":"WeChat"
  }
},
"currentTarget":  {
  "id": "tapTest",
  "dataset": {
    "hi":"WeChat"
  }
},
"detail": {
  "x":53,
  "y":14
},
"touches":[{
  "identifier":0,
  "pageX":53,
  "pageY":14,
  "clientX":53,
  "clientY":14
}],
"changedTouches":[{
  "identifier":0,
  "pageX":53,
  "pageY":14,
  "clientX":53,
  "clientY":14
}]
}
```

#### 事件分类

1. 冒泡事件：当一个组件上的事件被触发后，会向父节点传递。
2. 非冒泡事件：不会向父节点传递。

冒泡事件有：

+ touchstart: 表示手指触摸动作开始
+ touchmove: 表示手指触摸后移动
+ touchcancel: 手指触摸动作被打断，如来电提醒，弹窗
+ touchend: 手指触摸动作结束
+ tap: 手指触摸后马上离开
+ longpress: 手指触摸后，超过 350ms 后再离开，若指定了该事件回调，则 tap 事件将不被触发
+ longtap: 推荐使用 longpress 代替
+ tansitionend: 会在 WXSS transition 或 wx.createAnimation 动画结束后触发
+ animationstart: 会在一个 WXSS animation 动画开始时触发
+ animationiteration: 会在一个 WXSS animation 一次迭代结束时触发
+ animationend: 会在一个 WXSS animation 动画完成时触发
+ touchforcechange: 在支持 3D Touch 的 iPhone 设备中，重按时触发

除以上之外的其它组件自定义事件一般都是非冒泡事件，如 `<form/>` 的 `submit` 事件， `<input/>` 的 `input` 事件， `<scroll-view/>` 的 `scroll` 事件。

#### 事件绑定的写法

类型属性绑定，以 key, value 形式完成。

key 以 `bind` 或 `catch` 开头，然后跟事件类型，如 `bindtap`, `catchtouchstart`。自基础库 1.5.0 起，`bind` 和 `catch` 后可紧跟一个 `:`，如 `bind:tap`, `catch:touchstart`。

value 是一个字符串，表示在 `Page` 中定义的函数名。

`bind` 事件绑定不会阻止冒泡事件向上冒泡，而 `catch` 会。

#### 事件对象

`BaseEvent` 对象属性列表：

+ type: 事件类型，String
+ timeStamp: 事件生成时的时间戳，为页面打开到触发事件所经过的毫秒数，Integer
+ target: 触发事件的组件的一些属性值集合，Object，属性值有事件源组件 `id`，当前组件的标签名 `tagName`，事件源组件上由 `data-` 开头自定义属性组成的集合 `dataset`
+ currentTarget: 当前组件的一些属性值集合，值或同 target, 或为其父组件（冒泡时）

`CustomEvent` 自定义事件对象属性列表（继承 BaseEvent):

+ detail: 额外的信息，Object，如表单组件提交事件会携带用户的输入。

`TouchEvent` 触摸事件对象属性列表（继承 BaseEvent):

+ touches: 当前停留在屏幕中的触摸点信息的数组，Array
+ changedTouches: 当前变化的触摸点信息的数组， Array

`Touch` 对象属性：

+ identifier: 触摸点的标识符，Number
+ pageX, pageY: 距离文档左上角的距离
+ clientX, clientY: 距离页面可显示区域（屏幕除去导航条）左上角距离。

`CanvasTouch` 对象属性：

+ identifier: 触摸点的标识符，Number
+ x, y: 距离 Canvas 左上角的距离

`changedTouches` 数据格式同 `touches`，表示变化的触点，如从无变有 touchstart, 位置变化  touchmove，从有变无 touchend, touchcancel。






### 脚本语言 WXS

是小程序的一套脚本语言，结合 WXML 可创建出页面的结构。

+ wxs 不依赖于运行时的基础库版本，可以在所有版本的小程序中运行
+ wxs 与 js 是不同的语言，有自己的语法，并不和 js 一致。
+ wxs 的运行环境和 js 代码是隔离的， wxs 中不能调用其它 js 文件中定义的函数，也不能调用小程序提供的 API。
+ wxs 函数不能作为组件的事件回调。

WXS 页面渲染示例：

```
<!--wxml-->
<wxs module="m1">
var msg = "hello world";

module.exports.message = msg;
</wxs>

<view> {{m1.message}} </view>
```

输出：

```
hello world
```

WXS 数据处理示例：

```
// page.js
Page({
  data: {
    array: [1, 2, 3, 4, 5, 1, 2, 3, 4]
  }
})

<!--wxml-->
<!-- 下面的 getMax 函数，接受一个数组，且返回数组中最大的元素的值 -->
<wxs module="m1">
var getMax = function(array) {
  var max = undefined;
  for (var i = 0; i < array.length; ++i) {
    max = max === undefined ? 
      array[i] : 
      (max >= array[i] ? max : array[i]);
  }
  return max;
}

module.exports.getMax = getMax;
</wxs>

<!-- 调用 wxs 里面的 getMax 函数，参数为 page.js 里面的 array -->
<view> {{m1.getMax(array)}} </view>
```

页面输出： 5


## 自定义组件

基础库版本自 1.6.3 起，小程序支持组件化编程。自定义组件在使用时与基础组件相似。

类似页面，一个自定义组件由 `json`, `wxml`, `wxss`, `js` 4 个文件组件。并且 `json` 中要定义： `{ "component": true }`。

**代码示例**:

```html
!-- 这是自定义组件的内部WXML结构 -->
<view class="inner">
  {{innerText}}
</view>
<slot></slot>
```

```css
/* 这里的样式只应用于这个自定义组件 */
.inner {
  color: red;
}
```

注意在组件的 wxss 中不应使用 ID 选择器、属性选择器和标签名选择器。

在自定义组件的 js 中，需使用 `Component()` 来注册组件，并提供组件的属性定义、内部数据和自定义方法。

组件的属性值和内部数据将被用于组件 wxml 的渲染，其中属性值可由组件外部传入。

例如：

```javascript
Component({
  properties: {
    // 这里定义了innerText属性，属性值可以在组件使用时指定
    innerText: {
      type: String,
      value: 'default value',
    }
  },
  data: {
    // 这里是一些组件内部数据
    someData: {}
  },
  methods: {
    // 这里是一个自定义方法
    customMethod: function(){}
  }
})
```

使用自定义组件前，首先要在页面的 json 文件中进行引用声明，将自定义组件的文件路径对应为一个组件标签名，例如：

```json
{
  "usingComponents": {
    "component-tag-name": "path/to/the/custom/component"
  }
}
```

之后在模板中就要像使用基础组件一样使用了：

```html
<view>
  <!-- 以下是对一个自定义组件的引用 -->
  <component-tag-name inner-text="Some text"></component-tag-name>
</view>
```

### 自定义组件 wxml 中的 slot

`<slot/>` 节点用于承载组件引用时提供的子节点。例如：

```html
<!-- 组件模板 -->
<view class="wrapper">
  <view>这里是组件的内部节点</view>
  <slot></slot>
</view>

<!-- 引用组件的页面模版 -->
<view>
  <component-tag-name>
    <!-- 这部分内容将被放置在组件 <slot> 的位置上 -->
    <view>这里是插入到组件slot中的内容</view>
  </component-tag-name>
</view>
```

组件 wxml 中默认只能有一个 slot，需要多个时，要在组件  js 中声明启用：

```javascript
Component({
  options: {
    multipleSlots: true // 在组件定义时的选项中启用多slot支持
  },
  properties: { /* ... */ },
  methods: { /* ... */ }
})
```

此时多个 slot 用 `name` 来区分：

```html
<!-- 组件模板 -->
<view class="wrapper">
  <slot name="before"></slot>
  <view>这里是组件的内部细节</view>
  <slot name="after"></slot>
</view>


<!-- 引用组件的页面模版,使用时，用 slot 属性来将节点插入到不同的slot上。 -->
<view>
  <component-tag-name>
    <!-- 这部分内容将被放置在组件 <slot name="before"> 的位置上 -->
    <view slot="before">这里是插入到组件slot name="before"中的内容</view>
    <!-- 这部分内容将被放置在组件 <slot name="after"> 的位置上 -->
    <view slot="after">这里是插入到组件slot name="after"中的内容</view>
  </component-tag-name>
</view>
```


### 自定义组件样式

只对组件 wxml 内的节点有效。

自定义组件中不能使用以下的选择器：

```css
#a { } /* 在组件中不能使用 id 选择器 */
[a] { } /* 在组件中不能使用属性选择器*/
button { } /* 在组件中不能使用标签名选择器 */
.a > .b { } /* 除非 .a 是 view 组件节点，否则不一定会生效 */
```

可以使用 `:host` 选择器给托管组件定义样式。

组件中可以通过 `externalClasses` 指定一些外部样式类名，并在组件中使用这些样式名，而使用者在使用时可以为该样式名赋值，从而实现从外部传入样式的效果，例如：

```
/* 组件 custom-component.js 中声明外部样式类名*/
Component({
  externalClasses: ['my-class']
})

<!-- 组件 custom-component.wxml 模板中使用该外部样式类名 -->
<custom-component class="my-class">这段文本的颜色由组件外的 class 决定</custom-component>
这样，组件的使用者可以指定这个样式类对应的 class ，就像使用普通属性一样。


<!-- 使用者的 WXML 中为外部样式赋值，并在样式文件中定义具体样式-->
<custom-component my-class="red-text" />


.red-text {
  color: red;
}
```

### Component 构造器

用于定义自定义组件，可以定义组件的属性，数据和方法等。


+ `properties`: Object Map, 组件的对象属性，是属性名到属性设置的映射表，属性设置中可包含三个字段， type 表示属性类型，value 表示属性初始值，observor 表示属性值被修改时的响应函数
+ `data`: Object，组件的内部数据，和 `properties` 一起用于组件的模板渲染
+ `methods`: Object, 组件的方法，包括事件响应函数和任意的自定义方法。
+ `hehaviors`: String Arrary, 类似于 mixins 和 traits 的组件间代码利用机制
+ `created`: Function，组件生命周期函数，在组件实例进入页面节点树时执行，注意此时不能调用 `setData`
+ `attached`: Function，组件生命周期函数，在组件实例关联页面节点树时执行
+ `ready`: Function，组件生命周期函数，在组件布局完成后执行，此时可用 `SelectorQuery` 获取节点信息
+ `moved`: Function，组件生命周期函数，在组件实例从页面节点树删除时执行
+ `detached`: Function，组件生命周期函数，在组件实例进入页面节点树时执行，注意此时不能调用 `setData`
+ `relations`: Object, 组件间关系定义
+ `externalClasses`: String Array, 组件接受的外部样式类名
+ `options`: Object Map，一些组件选项

生成的组件实例可以在组件的方法、生命周期函数和属性的 `observer` 中通过 `this` 访问。

组件有如下一些通用的属性和方法：

+ `is` 属性: String，组件的文件路径
+ `id` 属性: String，节点 id
+ `dataset` 属性: String，节点 dataset
+ `data` 属性: Object，组件数据，包括内部数据和属性值
+ `setData` 方法：设置 data 并执行视图层渲染
+ `hasBehavior` 方法：检查组件是否有该 `behavior`
+ `triggerEvent` 方法：触发事件
+ `createSelectorQuery` 方法：创建一个 `SelectorQuery` 对象，选择器选取范围为这个组件实例内
+ `selectComponent`: 使用选择器选择组件实例节点，返回匹配的第一个组件实例对象
+ `selectAllComponents`: 返回一个匹配数组
+ `getRelationNodes`: 获取所有该关系对应的所有关联节点

示例：

```javascript
Component({

  behaviors: [],

  properties: {
    myProperty: { // 属性名
      type: String, // 类型（必填），目前接受的类型包括：String, Number, Boolean, Object, Array, null（表示任意类型）
      value: '', // 属性初始值（可选），如果未指定则会根据类型选择一个
      observer: function(newVal, oldVal){} // 属性被改变时执行的函数（可选），也可以写成在methods段中定义的方法名字符串, 如：'_propertyChange'
    },
    myProperty2: String // 简化的定义方式
  },
  data: {}, // 私有数据，可用于模版渲染

  // 生命周期函数，可以为函数，或一个在methods段中定义的方法名
  attached: function(){},
  moved: function(){},
  detached: function(){},

  methods: {
    onMyButtonTap: function(){
      this.setData({
        // 更新属性和数据的方法与更新页面数据的方法类似
      })
    },
    _myPrivateMethod: function(){
      // 内部方法建议以下划线开头
      this.replaceDataOnPath(['A', 0, 'B'], 'myPrivateData') // 这里将 data.A[0].B 设为 'myPrivateData'
      this.applyDataUpdates()
    },
    _propertyChange: function(newVal, oldVal) {

    }
  }

})
```

注意在 `properties` 定义段中，属性名用驼峰写法 propertName，而在 wxml 中指定属性值时则对应使用连字符写法 `<component-tag-name property-name="attr val" />`，应用于数据绑定时采用驼峰写法 `attr="{{propertyName}}"`。


### 自定义组件事件

组件通过 `triggerEvent` 方法触发生成事件，并指定事件名、detail 对象和事件选项，例如：

```
<!-- 在自定义组件中 -->
<button bindtap="onTap">点击这个按钮将触发“myevent”事件</button>

// 组件 js 中
Component({
  properties: {}
  methods: {
    onTap: function(){
      var myEventDetail = {} // detail对象，提供给事件监听函数
      var myEventOption = { // 触发事件的选项
          /*
          bubbles: true, //事件是否能冒泡
          composed: false, //事件是否能穿越组件边界，为 false 时，事件只能在引用组件的节点树上触发，不进入其它组件内部
          capturePhase: false //事件是否拥有捕获阶段
          */
      }
      this.triggerEvent('myevent', myEventDetail, myEventOption)
    }
  }
})
```

监听自定义组件事件的方法同监听基础组件事件的一样。


### behaviors

用于组件间代码共享，类似 mixins 或 traits。

和 Component 类似，每个 behavior 可包含一组属性、数据、生命周期函数和方法，组件引用它时，它的属性、数据和方法会被合并到组件中，而生命周期函数也会在对应时机被调用。

每个组件可引用多个 behavior，同时每个 behavior 也可引用其它 behavior。

示例：

```javascript
// my-behavior.js, behavior 需要使用 Behavior() 构造器定义。
module.exports = Behavior({
  behaviors: [],
  properties: {
    myBehaviorProperty: {
      type: String
    }
  },
  data: {
    myBehaviorData: {}
  },
  attached: function(){},
  methods: {
    myBehaviorMethod: function(){}
  }
})


// my-component.js, 组件引用时，在 behaviors 定义段中将它们逐个列出即可。
var myBehavior = require('my-behavior')
Component({
  behaviors: [myBehavior],
  properties: {
    myProperty: {
      type: String
    }
  },
  data: {
    myData: {}
  },
  attached: function(){},
  methods: {
    myMethod: function(){}
  }
})
```

#### 字段的覆盖和组件规则

+ 如果有同名的属性或方法，组件本身的属性或方法会覆盖 behavior 中的属性或方法，如果引用了多个 behavior ，在定义段中靠后 behavior 中的属性或方法会覆盖靠前的属性或方法；
+ 如果有同名的数据字段，如果数据是对象类型，会进行对象合并，如果是非对象类型则会进行相互覆盖；
+ 生命周期函数不会相互覆盖，而是在对应触发时机被逐个调用。如果同一个 behavior 被一个组件多次引用，它定义的生命周期函数只会被执行一次。

#### 内置 behaviors

`wx://form-field` 使组件有类似表单控件的行为，使用：

```javascript
Component({
  behaviors: ['wx://form-field']
})
```

### 组件间的关系

定义自定义父子组件间 linked, linkChanged, unlinked 时的回调动作，例如：

```
<!-- 组件间的关系 -->
<custom-ul>
  <custom-li> item 1 </custom-li>
  <custom-li> item 2 </custom-li>
</custom-ul>

// path/to/custom-ul.js，自定义组件中定义关系
Component({
  relations: {
    './custom-li': {
      type: 'child', // 关联的目标节点应为子节点
      linked: function(target) {
        // 每次有custom-li被插入时执行，target是该节点实例对象，触发在该节点attached生命周期之后
      },
      linkChanged: function(target) {
        // 每次有custom-li被移动后执行，target是该节点实例对象，触发在该节点moved生命周期之后
      },
      unlinked: function(target) {
        // 每次有custom-li被移除时执行，target是该节点实例对象，触发在该节点detached生命周期之后
      }
    }
  },
  methods: {
    _getAllLi: function(){
      // 使用getRelationNodes可以获得nodes数组，包含所有已关联的custom-li，且是有序的
      var nodes = this.getRelationNodes('path/to/custom-li')
    }
  },
  ready: function(){
    this._getAllLi()
  }
})


// path/to/custom-li.js，自定义组件中定义关系
Component({
  relations: {
    './custom-ul': {
      type: 'parent', // 关联的目标节点应为父节点
      linked: function(target) {
        // 每次被插入到custom-ul时执行，target是custom-ul节点实例对象，触发在attached生命周期之后
      },
      linkChanged: function(target) {
        // 每次被移动后执行，target是custom-ul节点实例对象，触发在moved生命周期之后
      },
      unlinked: function(target) {
        // 每次被移除时执行，target是custom-ul节点实例对象，触发在detached生命周期之后
      }
    }
  }
})
```

注意：必须在两个组件定义中都加入relations定义，否则不会生效。


### 抽象节点

自定义组件中声明并使用一个抽象节点（相当于一个节点变量，可在使用该组件中具体赋值），例如：

```
//自定义组件的 js
Component({
  "usingComponents": {
    "custom-radio": "path/to/custom/radio",
    "custom-checkbox": "path/to/custom/checkbox"
  },
  "componentGenerics": {
    "selectable": { //声明一个抽象节点
      "default": "path/to/default/component" //一个默认值
    }
  }
})

<!-- 自定义组件模板中使用抽象节点 selectable -->
<view wx:for="{{labels}}">
  <label>
    <selectable disabled="{{false}}"></selectable>
    {{item}}
  </label>
</view>


<!-- 在使用该自定义组件时，指定抽象节点的具体值-->
<selectable-group generic:selectable="custom-radio" />
<selectable-group generic:selectable="custom-checkbox" />
```


### 多线程 Worker

一些异步处理任务，可放置在 Worker 中运行，再将运行结果返回到小程序的主线程。Worker 运行于一个单独的全局上下文与线程中，不能直接调用主线程的方法。主线程使用 `Worker.postMessage()` 发送数据，Worker 使用 `Worker.onMessage()` 接收数据，数据不是直接共享，而是被复制。

步骤为：

先在 `app.json` 中配置 Worker 代码放置的目录，目录下的代码将打包成一个文件：

```json
{
  "workers": "workers"
}
```

目录下有文件：

```
workers/request/index.js
workers/request/utils.js
workers/response/index.js
```

编写 Worker 代码：

```javascript
//在 workers/request/index.js 编写 Worker 响应代码

var utils = require('./utils')

// 在 Worker 线程执行上下文会全局暴露一个 `worker` 对象，直接调用 worker.onMeesage/postMessage 即可
worker.onMessage(function (res) {
  console.log(res)
})
```

在主线程中初始化 Worker，并发送消息

```javascript
//在主线程的代码 app.js 中初始化 Worker
var worker = wx.createWorker('workers/request/index.js') // 文件名指定 worker 的入口文件路径，绝对路径

//主线程向 Worker 发送消息
worker.postMessage({
  msg: 'hello worker'
})
```

+ Worker 最大并发数限制为 1 个，创建下一个前调用  `Worker.terminate()` 结束当前 Worker
+ Worker 内不支持 wx 系列的 API


# 参考

+ [小程序框架](https://developers.weixin.qq.com/miniprogram/dev/framework/MINA.html)

