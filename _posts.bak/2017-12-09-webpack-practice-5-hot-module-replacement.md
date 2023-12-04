---
title: webpack 实践 5：模块热更新 HMR
date: 2017-12-09
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

HRM 适合在开发环境中使用，不适合不生产中使用。

# 开启 HMR

只需在 webpack.config.js 中为 webpack-dev-server 添加 `hot: true`，并使用 webpack 的内置 HMR 插件即可，同时修改为一个 entry:

```javascript
const webpack = require("webpack");

module.exports = {
  entry: {
      app: './src/index.js'
  },
  devServer: {
    contentBase: './dist',
    hot: true
  },
  plugins: [
      new webpack.NamedModulesPlugin(),
      new webpack.HotModuleReplacementPlugin()
  ]
}
```

使用 `NamedModulesPlugin` 插件可以看出哪个依赖库打了补丁。

使用 `yarn run start` 开启开发服务器。在命令行中使用 `webpack-dev-server --hotOnly` 开启开发服务器也可以传入参数。

在 `src/index.js` 中添加接收模块更新的代码，从而当 `print.js` 有更新时，运行相关的回调函数：

```javascript
if (module.hot) {
    module.hot.accept('./print.js', function(){
        console.log("Accepting the updated printMe module!");
        printMe();
    })
}
```

将 `src/print.js` 修改为：

```javascript
export default function printMe() {
    console.log("Updating print.js...");
}
```

可在浏览器的 console 中看到：

```
[HMR] Waiting for update signal from WDS...
main.js:4395 [WDS] Hot Module Replacement enabled.
+ 2main.js:4395 [WDS] App updated. Recompiling...
+ main.js:4395 [WDS] App hot update...
+ main.js:4330 [HMR] Checking for updates on the server...
+ main.js:10024 Accepting the updated printMe module!
+ 0.4b8ee77….hot-update.js:10 Updating print.js...
+ main.js:4330 [HMR] Updated modules:
+ main.js:4330 [HMR]  - 20
+ main.js:4330 [HMR] Consider using the NamedModulesPlugin for module names.
```

# 通过 Node.js API 使用 Webpack Dev Server

此时不要把开发服务器的配置项放在 webpack 的配置对象中，而要在创建时将它作为第 2 个参数传入：

```javascript
new WebpackDevServer(compiler, options)
```

在开启 HMR，需要修改 webpack 配置对象，以加入 HMR 入口点，而 `webpack-dev-server` 包中的一个叫 `addDevServerEntrypoints` 的方法能添加 HMR 入口点。下面是一个例子：

```javascript
//dev-server.js
const webpackDevServer = require('webpack-dev-server');
const webpack = require('webpack');

const config = require('./webpack.config.js');
const options = {
  contentBase: './dist',
  hot: true,
  host: 'localhost'
};

webpackDevServer.addDevServerEntrypoints(config, options);
const compiler = webpack(config);
const server = new webpackDevServer(compiler, options);

server.listen(5000, 'localhost', () => {
  console.log('dev server listening on port 5000');
});
```

# 使用 HMR 时需注意

上例中，当通过 HMR 更新完 `printMe` 函数后，button 上绑定的 `onclick` 处理函数还是旧的 printMe。要绑定更新后的函数， `src/index.js` 需修改为：

```javascript
let element = component(); // Store the element to re-render on print.js changes
document.body.appendChild(element);

if (module.hot) {
    module.hot.accept('./print.js', function(){
        document.body.removeChild(element);
        element = component(); // re-render the "component" to update the click handler
        document.body.appendChild(element);
    });
}
```

# 样式的 HMR

`style-loader` 加载器会通过 `module.hot.accept` 自动更新依赖的 CSS。

因此修改 css 样式后，会在页面上立即体现。

# 参考

+ https://webpack.js.org/guides/hot-module-replacement/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
