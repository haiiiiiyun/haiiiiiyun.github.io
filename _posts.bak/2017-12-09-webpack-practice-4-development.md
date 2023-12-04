---
title: webpack 实践 4：开发环境
date: 2017-12-09
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# 使用 source maps

当将多个文件 a.js, b.js, c.js 打包成一个 bundle.js 文件后，定位错误时会成问题。JS 中可使用 [source maps](http://blog.teamtreehouse.com/introduction-source-maps) 将编译后的代码映射回源代码。此时，当 b.js 中出错时，source maps 会提供正确的位置。

webpack 中有 [多种 source maps](https://webpack.js.org/configuration/devtool)，本文使用 `inline-source-map`。

在 webpack.config.js 中启用：

```javascript
devtool: 'inline-source-map'
```

将 `src/print.js` 代码中的 `console` 改成 `cnosole`，产生错误。

编译后测试，会出现如下错误提示：

```
Uncaught ReferenceError: cnosole is not defined
    at HTMLButtonElement.printMe (print.js:2)
```

从而能确定出错源。


# 使用 Watch 模式自动编译

webpack 开启 watch 模式后，当依赖树中的文件有修改时，会自动编译。

先在 `package.json` 中添加一个开启 webpack watch 模式的命令：

```javascript
"scripts": {
    "watch": "webpack --watch"
}
```

运行 `yarn run watch` 后，当文件有修改时，会自动编译。


# 使用 webpack-dev-server 自动重编译和重加载页面

watch 模式中重编译后，页面还是要手工刷新。

webpack-dev-server 包提供了一个简单的 Web 服务器，并且也侦测文件的修改，一旦有修改，自动重编译，并重新刷新页面。

先安装：

```bash
$ yarn add webpack-dev-server --dev
```

在 webpack.config.js 中配置使用开发服务器，并指定根目录：

```javascript
devServer: {
    contentBase: './dist'
}
```

在 `package.json` 中添加一个开启该开发服务器的命令：

```javascript
  "scripts": {
    "start": "webpack-dev-server --open"
  }
```

运行 `yarn run start` 开启并调试，默认的端口是 8080，更多参数见 [文档](https://webpack.js.org/configuration/dev-server)。

# 参考

+ https://webpack.js.org/guides/development/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
