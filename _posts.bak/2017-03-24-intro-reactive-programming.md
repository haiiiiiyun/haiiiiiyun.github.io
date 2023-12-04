---
title: 响应式编程(Reactive Programming) 入门
date: 2017-03-24
writing-time: 2017-03-24 10:10--2017-03-27 10:39
categories: Programming
tags: Programming JavaScript Reactive&nbsp;Programming RX Design&nbsp;Pattern Observable RxJS
---

# 概述

学习响应式编程最难部分在于用响应式思维。

# 什么是响应式编程

## 响应式编程就是用异步数据流进行编程

这不是新理念。即使是最典型的点击事件也是一个异步事件流，从而可以对其进行侦测（observe）并进行相应操作。

可以基于任何东西创建数据流。流非常轻便，并且无处不在，任何东西都可以是一个流：变量，用户输入，属性，缓存，数据结构等等。例如，想象一下微博推文也可以是一个数据流，和点击事件一样。你可以对其进行侦听，并作相应反应。

**除些之外，我们有很多功能强大的函数，可以对这些流进行合并、过滤、转变等**。这就是 “函数式编程” 的强大之处。流可以作为另一个流的输入。甚至多个流也可以作为另一个流的输入。你也可以合并流，从流中过滤出你感兴趣的事件。你也可以将流中的数据值映射转换成另一个流。

流是响应式的核心，下面是 "在按钮上点击" 事件流。

![按钮点击事件流](https://camo.githubusercontent.com/36c0a9ffd8ed22236bd6237d44a1d3eecbaec336/687474703a2f2f692e696d6775722e636f6d2f634c344d4f73532e706e67)

流就是一个按时间顺序正在进行的事件序列(A stream is a sequence of ongoing events ordered in time)。

它可以发送 3 种不同的事物：

+ 一个值（类型不限）
+ 一个错误
+ 或一个已完成(completed) 信号


例如，当包含该按钮的视图或窗口关闭时，流会发送 "completed" 信号。

我们只能异步捕获这些发送的事件，即定义：

+ 一个函数，用于当一个值发送出来时再执行
+ 定义另一个函数，用于当错误发送出来时执行
+ 再定义一个函数，用于当 'completed' 信号发送出来时执行

有时可只定义第一个函数，而忽略定义后两个函数。

对流的 “侦听” 又称为 **订阅(subscribing)**，而定义的函数即为 **观察者(observer)**，流就是 **主题(subject, observable)**。这是一个典型的观察者模式。

也可以用 ASCII 来画示意图：

```
--a---b-c---d---X---|->

a, b, c, d 都是发送出的值
X 是错误
| 是 'completed' 信号
---> 是时间线
```

下面演示将原始的点击事件流转变成一个新的流。

首先，创建一个计数流来指示一个按钮的点击次数。在常见的响应式库中，每个流都会绑定很多的函数，如 map, filter, scan 等。当你调用这些函数时，如 `clickStream.map(f)`，会基于 clickStream 返回一个新流。但它不会修改原来的 clickStream 流。这是响应式流的一个核心特性： **不变性(immutability)**。因而它能让我们进行函数串联，如 `clickStream.map(f).scan(g)`:

```
  clickStream: ---c----c--c----c------c-->
               vvvvv map(c becomes 1) vvvv
               ---1----1--1----1------1-->
               vvvvvvvvv scan(+) vvvvvvvvv
counterStream: ---1----2--3----4------5-->
```

map(f) 函数根据提供的 f 函数将发送出的值转换到另一个新流中，这里是将每次点击映射成数据  1。scan(g) 函数聚合流中所有之前的值，产生值 x = g(accumulated, current)，这里 g 是一个简单的加函数。最后，counterStream 每当点击事件发生时就发送出一个代表总点击数的值。

要显示响应式的真正强大之处，假设现想创建一个 “双击” 事件流，为使更有趣，该流可以将多击（多于 2 次）都认为是双击。

在响应式中，这非常简单。画示意图进行思考是理解和创建流的最好方式，无论你是新手还是专家。

![多击事件流](https://camo.githubusercontent.com/995c301de2f566db10748042a5a67cc5d9ac45d9/687474703a2f2f692e696d6775722e636f6d2f484d47574e4f352e706e67)

灰框表示将流转换成另一个流的函数。首先将点击积累成事件列表，这里 throttle(250ms) 将 250ms 内的点击都合并在一个列表中。现得到了一个列表流，再应用 map() 将每个列表映射成其对应的列表长度。最后，使用 filter(x>=2) 将长度 1 过滤掉。我们用 3 个操作来产生我们需要的流。然后我们可以侦听（订阅）它，进而进行相应的响应。


# 为什么要采用 RP？

响应式编程提高了代码的抽象水平，因此能专注于那些定义业务逻辑的事件的依存关系，而无需摆弄大量的实现细节。用 RP 写的代码会更加简洁。

现在的 Webapp 和移动 App，都会和与数据事件相关的 UI 事件进行大量交互，因此使用 RP 的优点会更明显。App 已经进化成了更加实时：修改一个表单项会自动触发保存到后台的操作，“点赞” 会实时反应到其他连接的用户，等等。现在的应用含有大量的各种类型的实时事件，以向用户提供高度交互体验。我们需要能处理这些情况的工具，而响应式编程就是答案。

# 用 RP 思维

现使用一个实例来一步步引导如何使用 RP 思维。本例使用 JavaScript 和 [RxJS](https://github.com/Reactive-Extensions/RxJS)。

## 实现一个 “关注谁” 推荐框

界面类似 Twitter 的账号关注推荐 UI：

![Twitter Who to follow](https://camo.githubusercontent.com/81e5d63c69768e1b04447d2e246f47540dd83fbd/687474703a2f2f692e696d6775722e636f6d2f65416c4e62306a2e706e67)

本例实现以下核心功能：

+ 启动时，根据 [Github User API](https://developer.github.com/v3/users/#get-all-users) 获取账号数据，并显示 3 个推荐
+ 点击 “刷新” 后，将另外 3 个推荐导入推荐框中的 3 行中
+ 当在账号行上点击 'x' 按钮时，清除该账号并显示另一个
+ 每行显示账号的头像及页面链接


## 请求与应答

如何用 Rx 解决这个问题？ **（几乎）任何事务都可以是一个流**，这是 Rx 的口头禅。

先实现 “启动时，根据 API 获取账号数据，并显示 3 个推荐” 的功能。这里没有特殊的，只需 ：

1. 发送一个请求
2. 获取一个应答
3. 显示应答


先将请求表示为一个流。启动时，只需进行一次请求，因此将它建模成数据流时，该流将只会发送出一个值。

```
--a------|->

这里 a 是字符串 'https://api.github.com/users'
```

这是我们需要进行请求的 URL 流。每当一个请求事件发生时，它都会告诉我们两件事：何时和什么。事件发送出值的时间就是 “何时” 应用执行请求的时间，而发送出来的值（URL 字符串）就是应该请求的 “什么”。

在 Rx* 中创建这样的一个单值流很简单。流的官方术语是 "Observable"，这是基于它是可被观测的事件命名。

```javascript
var requestStream = Rx.Observable.just('https://api.github.com/users');
```

但是现在，它只是一个字符串流，没有做其它任何操作，因此我们需要为当值发送出来时定义一些操作。这通过 [订阅](https://github.com/Reactive-Extensions/RxJS/blob/master/doc/api/core/observable.md#rxobservableprototypesubscribeobserver--onnext-onerror-oncompleted) 该流完成。

```javascript
requestStream.subscribe(function(requestUrl) {
    // 执行请求操作
    jQuery.getJSON(requestUrl, function(reponseData){
        //...
    });
})
```

这里使用 jQuery Ajax 回调函数来处理异步请求操作，但 Rx 就是用来处理异步数据流的。该请求在以后某个时间返回的应答可以用流表示吗？当然可以：

```javascript
requestStream.subscribe(function(requestUrl) {
    // 执行请求操作
    var responseStream = Rx.Observable.create(function (observer) {
        jQuery.getJSON(requestUrl)
            .done(function(response) { 
                observer.onNext(response);
            })
            .fail(function(jqXHR, status, error){
                observer.onError(error);
            })
            .always(function() {
                observer.onCompleted();
            });
    });

    responseStream.subscribe(function(response){
        // ...
    });
});
```

`Rx.Observable.create` 创建了一个自定义流，该流显式地通知每个观察者（或者说订阅者）有关数据事件 (onNext()) 或错误 (onError())。这里只封装了 jQuery Ajax 的 Promise。因为 **Promise 也是一个可观察对象(Observable)**。

Observable 是 Promise 的超集。在 Rx 中可以通过 `var stream = Rx.Observable.fromPromise(promise)` 将一个 Promise 转成 Observable。但是 Observable 不能转成 Promise。一个 Promise 简单来说就是一个只发送单个值的 Observable，而 Rx 流却可以返回多个值。

上面的例子中，使用了回调函数。但在 Rx 中有一些简单机制，能基于流转换创建出新的流。

map(f) 函数，能从流 A 中抽取出每个值，用 f() 进行处理后，将新值插入到流 B。如果在请求和应答流上使用，就可以将请求 URL 映射成应答 Promise(类似流）：

```javascript
var responseMetaStream = requestStream
    .map(function(requestUrl) {
        return Rx.Observable.fromPromise(jQuery.getJSON(requestUrl));
    });
```

responseMetaStream 是一个流的流，即发送出的值还是一个流。

![应答 metastream](https://camo.githubusercontent.com/2a8a9cc75acd13443f588fd7f386bd7a6dcb271a/687474703a2f2f692e696d6775722e636f6d2f48486e6d6c61632e706e67)

我们需要的是发送出一个 JSON 对象的流。因此可以用 [flatMap](https://github.com/Reactive-Extensions/RxJS/blob/master/doc/api/core/observable.md#rxobservableprototypeflatmapselector-resultselector) 将流的流扁平化成流：

```javascript
var responseMetaStream = requestStream
    .flatMap(function(requestUrl) {
        return Rx.Observable.fromPromise(jQuery.getJSON(requestUrl));
    });
```

![应答流](https://camo.githubusercontent.com/0b0ac4a249e1c15d7520c220957acfece1af3e95/687474703a2f2f692e696d6775722e636f6d2f4869337a4e7a4a2e706e67)

因为应答流是对应请求流的，如果之后在请求流上发生更多事件，那么在应答流上也会出现对应的应答事件：


```
requestStream:  --a-----b--c------------|->
responseStream: -----A--------B-----C---|->

(小写是请求，大写是应答)
```

现在有了应答流，故可以呈现接收到的数据了：

```javascript
responseStream.subscribe(function(response){
    // 将应答呈现在 DOM 中
});
```

合并目前所有代码：

```javascript
var requestStream = Rx.Observable.just('https://api.github.com/users');

var responseStream = requestStream
    .flatMap(function(requestUrl) {
        return Rx.Observable.fromPromise(jQuery.getJSON(requestUrl));
    });
    
responseStream.subscribe(function(response){
    // 将应答呈现在 DOM 中
});
```

## 刷新按钮

每个 JSON 应答中都含 100 个用户信息。该 API 只允许指定页偏移，不能指定页大小，故只使用了 3 个数据对象并浪费了 97 个。

每次当点击刷新按钮时，请求流应该发送出一个新 URL，从而能获得一个新应答。需要 2 样东西：刷新按钮上的点击事件流，并将请求流修改成依赖于刷新点击流。RxJS 有将事件转成流的工具：

```javascript
var refreshButton = document.querySelector('.refresh');
var refreshClickStream = Rx.Observable.fromEvent(refresh, 'click');
```

由于刷新点击事件自己不带 API URL，我们需要将每次点击映射成一个实际的 URL。现将请求流修改成由刷新点击流通过将事件映射成一个 API URL 得到。

```javascript
var requestStream = refreshClickStream
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    });
```

但是这样破坏了原来的功能，现在在启动时不会有请求发出，只有当点击刷新时才会请求。需要在点击刷新和打开页面时都要进行请求。

我们知道这两种情况分开时的流：

```javascript
var requestStream = refreshClickStream
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    });

var startupRequestStream = Rx.Observable.just('https://api.github.com/users');
```

可以用 `merge()` 函数将两者合并。

```
stream A: ---a--------e-----o----->
stream B: -----B---C-----D-------->
          vvvvvvvvv merge vvvvvvvvv
          ---a-B---C--e--D--o----->
```

合并后的代码为：

```javascript
var requestOnRefreshStream = refreshClickStream
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    });

var startupRequestStream = Rx.Observable.just('https://api.github.com/users');

var requestStream = Rx.Observable.merge(
    requestOnRefreshStream, startupRequestStream
);
```

也可以简写为：

```javascript
var requestStream = refreshClickStream
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    })
    .merge(RequestStream = Rx.Observable.just('https://api.github.com/users'));
);
```

再进一步简写为：

```javascript
var requestStream = refreshClickStream
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    })
    .startWith('https://api.github.com/users');
```

`startWith()` 和你想像的功能一样。无论将 startWith 放在代码的哪个位置，startWith(x) 中的 x 总会在结果流的最前面。

为达到更好的直观效果，这里是要实现在启动时模拟点击刷新按钮，故可以改代码改成：

```javascript
var requestStream = refreshClickStream.startWith('startup click')
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    })
```

## 用流来建模 3 个推荐

现在有个问题：当你点击刷新时，当前的 3 个推荐不能先清空掉。新推荐只有当应答到达后才会显示，但要使 UI 更好看，需要在点击刷新时就清空掉当前的推荐。

```javascript
refreshClickStream.subscribe(function()
    // clear the 3 suggestion DOM elements
});
```

但是这样也不好，因为现在有 **两个** 订阅者可以影响推荐的 DOM 元素（另一个是 responseStream.subscribe())，而这不太符合 [责任分离原则](https://en.wikipedia.org/wiki/Separation_of_concerns)。

响应式的口头禅是任何事务都可以是一个流。

[Everything is a stream](https://camo.githubusercontent.com/e581baffb3db3e4f749350326af32de8d5ba4363/687474703a2f2f692e696d6775722e636f6d2f4149696d5138432e6a7067)

因此可以将推荐也建模成流，流中发送的每个值都是包含推荐数据的 JSON 对象。对这 3 个中的每个都分开处理。下面是推荐 #1：

```javascript
var suggestion1Stream = responseStream
    .map(function(listUsers){
        // 从列表中抽取一个随机用户
        return listUsers[Math.floor(Math.random()*listUsers.length)];
    });

suggestion1Stream.subscribe(function(suggestion){
    // 将推荐 1 显示到 DOM 上
});

// 推荐 #2 和 #3 也类似
```

回到 “刷新时清除全部推荐”，可以简单地将刷新点击映射成一个数据为 null 的推荐：

```javascript
var suggestion1Stream = responseStream
    .map(function(listUsers){
        // 从列表中抽取一个随机用户
        return listUsers[Math.floor(Math.random()*listUsers.length)];
    })
    .merge(
        refreshClickStream.map(function(){ return null; });
    );

// 呈现，将 null 解析为 “无数据”，因而隐藏 UI
suggestion1Stream.subscribe(function(suggestion){
    if (suggestion === null){
        // 隐藏推荐的 DOM 元素
    }
    else {
        // 显示推荐的 DOM 元素，并显示数据
    }
});

// 推荐 #2 和 #3 也类似
```

现在的示意图如下：

```
refreshClickStream: ----------o--------o---->
     requestStream: -r--------r--------r---->
    responseStream: ----R---------R------R-->   
 suggestion1Stream: ----s-----N---s----N-s-->
 suggestion2Stream: ----q-----N---q----N-q-->
 suggestion3Stream: ----t-----N---t----N-t-->

N 表示 null
```

进一步，还可以在启动时显示 “空” 推荐。只需在推荐流中添加 startWith(null) 即可：

```javascript
var suggestion1Stream = responseStream
    .map(function(listUsers){
        // 从列表中抽取一个随机用户
        return listUsers[Math.floor(Math.random()*listUsers.length)];
    })
    .merge(
        refreshClickStream.map(function(){ return null; });
    )
    .startWith(null);
```

从而示意图变为：

```
refreshClickStream: ----------o---------o---->
     requestStream: -r--------r---------r---->
    responseStream: ----R----------R------R-->   
 suggestion1Stream: -N--s-----N----s----N-s-->
 suggestion2Stream: -N--q-----N----q----N-q-->
 suggestion3Stream: -N--t-----N----t----N-t-->
```

## 关闭一个推荐并使用缓存应答

在每个推荐上点击 'x' 按钮时，就关闭该推荐并重新加载一个。如果简单地当在点击 'x' 按钮时发送一个请求，如下：

```javascript
var close1Button = document.querySelector('.close1');
var close1ClickStream = Rx.Observable.fromEvent(close1Button, 'click');

var requestStream = refreshClickStream.startWith('startup click')
    .merge(close1ClickStream)
    .map(function(){
        var randomOffset = Math.floor(Math.random()*500);
        return 'https://api.github.com/users?since=' + randomOffset;
    });
```

但是上面的效果会是关闭当前推荐并重新加载所有推荐，而不仅仅加载点击的推荐。我们复用之前的应答来解决这个问题，因为之前的每个应答页共有 100 个用户，而只使用了 3 个，因此无需再次请求。

再次使用流思维，当点击 'x' 时，想在 responseStream 流上最近发送出的应答用户列表中获取一个随机用户：

```
    requestStream: --r--------------->
   responseStream: ------R----------->
close1ClickStream: ------------c----->
suggestion1Stream: ------s-----s----->
```

Rx* 的 [combineLatest](https://github.com/Reactive-Extensions/RxJS/blob/master/doc/api/core/observable.md#rxobservableprototypecombinelatestargs-resultselector) 函数以两个流 A 和 B 作为输入，当其中任一个流发送出一个值时，combineLatest 将从两个流中抽取最近发送的值 a 和 b，组合并输出一个值 c=f(a, b)。示意图如下：

```
stream A: --a-----------e--------i-------->
stream B: -----b----c--------d-------q---->
          vvvvvvvv combineLatest(f) vvvvvvv
          ----AB---AC--EC---ED--ID--IQ---->

这里 f 是一个大写转换函数
```

因此使用 combineLatest 将 close1ClickStream 和 responseStream 组合，从而当点击某个 'x' 按钮时，就能获取最近的应答，并在 suggestion1Stream 上发送出一个新值。同时，combineLatest 还是对称的：当 responseStream 上有新应答时，应答会与最近的 'x' 点击事件组件来产生一个新推荐：

```javascript
var suggestion1Stream = close1ClickStream
    .combineLatest(responseStream,
        function(click, listUsers) {
        // 从列表中抽取一个随机用户
        return listUsers[Math.floor(Math.random()*listUsers.length)];
    })
    .merge(
        refreshClickStream.map(function(){ return null; });
    )
```

combineLatest 需要使用两个数据源，因此如果某个源一直没有发送数据，combineLatest 不会产生数据。我们可以在启动时模拟一个 'close 1' 点击来解决该问题：

```javascript
var suggestion1Stream = close1ClickStream.startWith('startup click')
    .combineLatest(responseStream,
        function(click, listUsers) {
        // 从列表中抽取一个随机用户
        return listUsers[Math.floor(Math.random()*listUsers.length)];
    })
    .merge(
        refreshClickStream.map(function(){ return null; });
    )
    .startWith(null);
```

## 全部代码

```javascript
var refreshButton = document.querySelector('.refresh');
var refreshClickStream = Rx.Observable.fromEvent(refreshButton, 'click');

var closeButton1 = document.querySelector('.close1');
var close1ClickStream = Rx.Observable.fromEvent(closeButton1, 'click');
// and the same logic for close2 and close3

var requestStream = refreshClickStream.startWith('startup click')
  .map(function() {
    var randomOffset = Math.floor(Math.random()*500);
    return 'https://api.github.com/users?since=' + randomOffset;
  });

var responseStream = requestStream
  .flatMap(function (requestUrl) {
    return Rx.Observable.fromPromise($.ajax({url: requestUrl}));
  });

var suggestion1Stream = close1ClickStream.startWith('startup click')
  .combineLatest(responseStream,             
    function(click, listUsers) {
      return listUsers[Math.floor(Math.random()*listUsers.length)];
    }
  )
  .merge(
    refreshClickStream.map(function(){ return null; })
  )
  .startWith(null);
// and the same logic for suggestion2Stream and suggestion3Stream

suggestion1Stream.subscribe(function(suggestion) {
  if (suggestion === null) {
    // hide the first suggestion DOM element
  }
  else {
    // show the first suggestion DOM element
    // and render the data
  }
});
```

运行效果见 http://jsfiddle.net/staltz/8jFJH/48/。


# 参考 

原文来自 [@andrestaltz](https://twitter.com/andrestaltz) 的 [The introduction to Reactive Programming you've been missing](https://gist.github.com/staltz/868e7e9bc2a7b8c1f754)，可能需要翻墙阅读。

