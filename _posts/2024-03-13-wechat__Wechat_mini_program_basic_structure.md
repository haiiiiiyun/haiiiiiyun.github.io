---
title: Wechat mini program basic structure
date: 2024-03-13
tags: wechat mini-program
categoris: Programming
---

## Project config file project.config.json

Put project settings such as `appid`.

## App global config file app.json

Include all page pathes and navigation bar style:

```json
{
	"pages": [
		"pages/index/index",
		"pages/logs/logs"
	],
	"window": {
		"navigationBarTitleText": "WeChat"
	}
}
```

## App global style file app.wxss

Same as CSS file.

## Define the app logic with App() in the app.js file

```js
App({
	onLaunch: function(){},
	onShow: function(options){},
	onHide: function(){},
	globalData: {
		userInfo: null,
		myData: {}
	}
})
```

## Page files

Every page constitutes of  3 files,  js file, wxml file and wxss file, corresponds to js file, html file and css file.

### Define page  logic with Page() in pages's js file

Define data and event handlers in js file:

```js
// pages/index/index.js
Page({
    data: { msg: 'Hello' }, // Page initial data
	myData: '123',
	onLoad: function(options){},
	handleBtnTap: function() {},
	changeData: function(){
		this.setData({today: '2024-03-13'})
	}
})
```

### wxml file

Page object's `data` value is available in wxml file:

```html
<view>{{msg}}</view>
```

We can bind event handler to a component with `bind<evnet>`

```html
<button bindtap="handleBtnTap">..</button>
```

### Refresh with setData()

Just like React's setData or setState, `setData()` will update the Page's data and then will trigger a page refresh. See `changeData()`.