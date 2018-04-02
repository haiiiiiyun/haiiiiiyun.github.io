---
title: 小程序基础
date: 2018-04-02
writing-time: 2018-04-02
categories: programming
tags: Programming miniprogram
---


## 代码构成

1. `.json` 配置文件
2. `.wxml` 页面模板文件，相当于 HTML
3. `.wxss` 页面样式文件，相当于 CSS
4. `.js` 脚本文件

### JSON 配置

####  app.json

根目录下的 `app.json` 文件用来保存小程序的全局配置信息，如页面路径信息、窗体 UI 配置、网络超时时间、底部 tab 等。例如：

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "window": {
    "navigationBarTitleText": "Demo"
  },
  "tabBar": {
    "list": [{
      "pagePath": "pages/index/index",
      "text": "首页"
    }, {
      "pagePath": "pages/logs/logs",
      "text": "日志"
    }]
  },
  "networkTimeout": {
    "request": 10000,
    "downloadFile": 10000
  },
  "debug": true
}
```

`pages` 中定义的第一项将是小程序的默认首页。

#### project.config.json

根目录下的 `project.config.json` 保存项目及开发工具的配置信息。

#### 每个页面都可以有自己的配置文件

例如 `pages/logs/logs` 页面对应的配置文件为 `pages/logs/logs.json`


### WXML 模板

每个页面有一个模板文件，例如 `pages/index/index` 页对应模板文件 `pages/index/index.wxml`，例如：

```html
<view class="container">
  <view class="userinfo">
    <button wx:if="{{!hasUserInfo && canIUse}}"> 获取头像昵称 </button>
    <block wx:else>
      <image src="{{userInfo.avatarUrl}}" background-size="cover"></image>
      <text class="userinfo-nickname">{{userInfo.nickName}}</text>
    </block>
  </view>
  <view class="usermotto">
    <text class="user-motto">{{motto}}</text>
  </view>
</view>
```
WXML 模板的使用模式，总体上和 Angular 类似。

+ 模板中使用封装了的组件，如 view, button, image, text, block 等。
+ 组件支持 `wx:if`, `wx:else`, `wx:for` 等 `wx:` 开头的属性，用来控制组件的呈现。
+ 支持使用 `{{var}}` 表达式将变量值呈现在页面中。

### WXSS 样式

具有 CSS 大部分功能。

+ 新增了尺寸单位 rpx (responsive pixel),可以根据屏幕宽度进行自适应，规定所有屏幕宽为 750rpx。
+ 全局样式放在根目录下的 app.wxss 中，每个页面的修改化样式放在各自对应的 page.wxss 中。
+ 仅支持部分 CSS 选择器。

### JS 交互逻辑

在模板中为组件添加事件响应绑定，例如：

```html
<button bindtap="clickMe">点击我</button>
```

在页面对应的 page.js 中定义方法：

```javascript
Page({
  clickMe: function() {
    this.setData({ msg: "Hello World" })
  }
})
```

从而当点击 button 时，调用 `clickMe` 方法。其数据的绑定也类似 React，即每个 Page 对象中都有 data，data 中的数据会更新到模板中，通过 JS 的 `Page.setData()` 更新 data。

## 小程序的启动

1. 打开前，会把整个小程序的代码包下载到本地。
2. 紧接着将 `app.json` 文件中的 pages 中的第一项作为首页地址。
3. 加载首页的代码，通过小程序的一些机制，渲染该页面。

小程序启动后，在 `app.js` 定义的 `App` 实例（整个小程序只有一个该实例，全部页面共享）的 `onLaunch` 回调会被执行：

```javascript
App({
  onLaunch: function () {
    // 小程序启动之后 触发
  }
})
```

### 页面

每个页面都包含有 4 种文件，例如 `pages/logs/logs` 页面有文件 `logs.json`, `logs.wxml`, `logs.wxss`, `logs.js`。

1. 微信客户端会先根据  `logs.json` 配置生成一个界面、颜色、文字等信息。
2. 加载页面的 WXML 结构和 WXSS 样式。
3. 最后加载  logs.js，内容例如：

```javascript
Page({
  data: { // 参与页面渲染的数据
    logs: []
  },
  onLoad: function () {
    // 页面渲染后 执行
  }
})
```

`Page` 是一个页面构造器，它生成一个页面实例。在生成页面时，小程序框架会将 Page.data 中的数据和 wxml 模板结构结合起来，最终呈现出页面。

在页面渲染完成后，页面实例会执行 `Page.onLoad` 回调。

# 参考

+ [小程序简易教程](https://developers.weixin.qq.com/miniprogram/dev/)

