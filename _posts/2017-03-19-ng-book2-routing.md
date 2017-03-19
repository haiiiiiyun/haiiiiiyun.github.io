---
title: Angular2 的路由功能
date: 2017-03-19
writing-time: 2017-03-19 17:54
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 概述

Web 开发中，路由通常是指根据浏览器中的当前 URL，根据某种规则将应用分割成不同的部分。例如，当访问 `/` 时，路由到主页面，而当访问 `/about` 时，则可路由到关于页面等。

在应用中定义路由的好处：

+ 能将应用分割成不同的部分
+ 能维护应用的状态
+ 能基于某种规则保护应用的各部分


## 客户端的路由如何运作

服务端的路由很简单，只需根据进入的 URL 调用不同的控制器来呈现。

而客户端路由中，当每次 URL 修改时，我们无需向服务端请求。这种应用称为 "Single Page Pages"(SPA)，因为服务端只提供一个页面，然后由 JavaScript 呈现不同的页面。

客户端的路由主要有 2 种实现方法。

### 老办法：使用 anchor 标签

比如，在页面中，为 a 标签加 `name`，如：

```html
<a name="about"><h1>About</h1></a>
```

然后通过 `http://something/#about`，浏览器值直接跳到该标签。SPA 用的相同的原则，但是对标签名就个小小改进，使它们看起来更像路径，例如，`about` 路由可能为 `http://something/#/about`。这种路由叫 *hash-based routing*。


### 新办法：HTML5 客户端路由

续...









# 参考 

+ [Routing](https://www.ng-book.com/2/)
