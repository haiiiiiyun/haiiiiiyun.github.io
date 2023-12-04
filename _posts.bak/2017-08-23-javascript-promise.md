---
title: Javascript Promise
date: 2017-08-23
writing-time: 2017-08-23
categories: programming
tags: javascript promise
---

# 概述

`Promise` 对象用来表示一个异步操作的最终结果情况，当操作成功时是一个值，操作失败时是一个错误对象。使用 `Promise` 后，异步函数也像同步函数一样返回值：不是立即返回最终值，而是返回一个 Promise，该 Promise 在未来的某个时间点会提供一个值。

`Promise` 可通过其构造器创建。但是一般是使用从函数调用中返回的 `Promise` 对象。

一个 `Promise` 对象本质上就是可以将回调函数与它关联的返回对象。

一个 Promise 有 3 种状态：

+ pending: 初始状态
+ fulfilled: 操作已成功完成
+ rejected: 操作失败


Promise 的初始状态是 pending，操作成功完成后，变成 fulfilled 并产生一个值，操作失败后变成 rejected 并附带一个错误原由。无论操作成功还是失败后，通过 Promise `.then()` 添加的关联回调函数都会被调用。

传统上，一般通过传入两个回调函数来使用异步操作：

```javascript
function successCallback(result) {
  console.log("It succeeded with " + result);
}

function failureCallback(error) {
  console.log("It failed with " + error);
}

doSomething(successCallback, failureCallback);
```

而现在的做法是：函数立即返回一个 `Promise` 对象，然后将回调函数关联进来：

```javascript
let promise = doSomething(); 
promise.then(successCallback, failureCallback);

// or
doSomething().then(successCallback, failureCallback);
```

相比旧方法，使用 Promise 有以下优点：

+ 回调函数不会在当前 Javascript 事件循环执行完毕前执行，即回调函数总是先放在一个队列中，稍后执行
+ 通过 `.then()` 添加的回调函数，即使是在异步操作完成后添加的，也会被调用
+ 可多次调用 `.then()`，添加多个回调函数，它们的执行顺序与添加顺序无关。


# Promise 构造器

## 语法

```javascript
new Promise( /* executor */ function(resolve, reject){ ... });
```

## 参数

`executor` 参数是一个函数，该函数有两个参数 `resolve` 函数对象和 `reject`函数对象。executor 函数在创建 Promise 实例时会立即执行（在 Promise 构造器返回创建的对象前执行）。executor 通常初始化一些异步任务，然后，当完成后，如果成功，则调用 `resolve`，如果失败，则调用 `reject`。

## 属性

`Promise.length` 表示其构造器的参数个数，值总是为 1。

## 方法

`Promise.all(iterable)`: 若参数列表中所有 Promise 都成功操作完成，则返回一个 fulfilled 的 Promise，关联的返回值是一个数组，元素是参数中各 Promise 的关联返回值，值顺序与参数顺序相同。 若其中有一个 Promise 失败，则返回一个 reject 的 Promise，关联的返回值是第一个 rejected Promise 的关联返回值。

`Promise.race(iterable)`: 一旦参数列表中某个 Promise 操作完成时，则立即返回一个 Promise，关联值是参数中操作完成的 Promise 的返回关联值。

`Promise.reject(reason)`: 立即返回一个 rejected 状态的 Promise 对象。

`Promise.resolve(value)`: 一般返回一个 fulfilled 状态的  Promise 对象。但如果 value 是 thenable 的（即有 then 函数），则返回的 Promise 将 "follow" 该 thenable，并采用其最终状态。

`Promise.prototype.catch(onRejected)`: 添加一个 onRejected 关联回调函数。

`Promise.prototype.then(onFullfilled, onRejected)`: 添加 onFullfilled 和 onRejected 两个关联回调函数。


# 链式

当需要按顺序执行多个异步操作时，可创建一个 Promise 链：

```javascript
const promise = doSomething();
const promise2 = promise.then(successCallback, failureCallback);

//or
//let promise2 = doSomething().then(successCallback, failureCallback);
```

promise2 不仅只表示 doSomething() 的完成情况，还表示传入的 successCallback 或 failureCallback 的完成情况（它们也可以是一个返回 Promise 的异步函数）。而每个 Promise 对象基本上表示链中这个异步操作步骤的操作结果。

以前完成多个异步操作时，代码会变成倒金字塔形状：

```javascript
doSomething(function(result) {
  doSomethingElse(result, function(newResult) {
    doThirdThing(newResult, function(finalResult) {
      console.log('Got the final result: ' + finalResult);
    }, failureCallback);
  }, failureCallback);
}, failureCallback);
```

使用 Promise 后变为：


```javascript
doSomething()
.then(result => doSomethingElse(result))
.then(newResult => doThirdThing(newResult))
.then(finalResult => {
  console.log(`Got the final result: ${finalResult}`);
})
.catch(failureCallback);
```

这里每一步的回调函数都返回一个 Promise。

## 当某步操作失败后（即执行 catch后），也可以继续链下去：

```javascript
new Promise((resolve, reject) => {
    console.log('Initial');

    resolve();
})
.then(() => {
    throw new Error('Something failed');
        
    console.log('Do this');
})
.catch(() => {
    console.log('Do that');
})
.then(() => {
    console.log('Do this whatever happened before');
});
```

将输出：

```
Initial
Do that
Do this whatever happened before
```

## 错误处理

一般地，当 Promise 链中出现异常时将停止，并查询链中接下来的 catch 处理函数：

```javascript
doSomething()
.then(result => doSomethingElse(value))
.then(newResult => doThirdThing(newResult))
.then(finalResult => console.log(`Got the final result: ${finalResult}`))
.catch(failureCallback);
```

这种处理方式是根据同步操作代码的工作模式建模的：

```javascript
try {
  let result = syncDoSomething();
  let newResult = syncDoSomethingElse(result);
  let finalResult = syncDoThirdThing(newResult);
  console.log(`Got the final result: ${finalResult}`);
} catch(error) {
  failureCallback(error);
}
```

这种与同步操作代码的对称性在 ECMAScript 2017 版中演化成了 [async/await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) 语法糖，如：

```javascript
async function foo() {
  try {
    let result = await doSomething();
    let newResult = await doSomethingElse(result);
    let finalResult = await doThirdThing(newResult);
    console.log(`Got the final result: ${finalResult}`);
  } catch(error) {
    failureCallback(error);
  }
}
```

## 将旧的回调函数 API 封闭成一个 Promise

```javascript
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

wait(10000).then(() => saySomething("10 seconds")).catch(failureCallback);
```

## 组合

`Promise.all()` 和 `Promise.race()` 是并行运行异步操作的两个组合工具。

`Promise.resolve()` 和 `Promise.reject()` 是手工创建 fulfilled 或 rejected Promise 的方法。

顺序执行异步操作的组合，可以通过 `Array.reduce` 实现。

`Array.reduce(callback[, initialValue])` 将 callback 应用于数组中的每个元素，最终生成一个值。而 callback 是一个接收 2 个参数的函数。

按顺序组合：

```javascript
[func1, func2].reduce((p, f) => p.then(f), Promise.resolve());
```

即将一组异步函数 reduce 成如下等价的 Promise 链：

```javascript
Promise.resolve().then(func1).then(func2);
```

这可以发展一个通用的组合函数（在函数式编程中很常见）：

```javascript
let applyAsync = (acc,val) => acc.then(val);
let composeAsync = (...funcs) => x => funcs.reduce(applyAsync, Promise.resolve(x));
```

然后这样使用：

```javascript
let transformData = composeAsync(func1, asyncFunc1, asyncFunc2, func2);
transformData(data);
```

在 ECMAScript 2017 中，顺序组合可以简单地用 async/await 完成：

```javascript
for (let f of [func1, func2]) {
  await f();
}
```

# 延时

通过 `then()` 添加的回调函数不会同步执行：

```javascript
Promise.resolve().then(() => console.log(2));
console.log(1); // 1, 2
```

即它们都会先被放到一个任务队列中，不会立即执行：

```javascript
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

wait().then(() => console.log(4));
Promise.resolve().then(() => console.log(2)).then(() => console.log(3));
console.log(1); // 1, 2, 3, 4
```


# 参考

+ [MDN Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
+ [Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
