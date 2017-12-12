---
title: webpack 实践 3：输出管理
date: 2017-12-08
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# 指定多个入口文件

本文的代码基于 [webpack 实践 1：安装与初始化](http://www.atjiang.com/webpack-practice-1-getting-started/) 中的代码。

先添加 `src/print.js`:

```javascript
export default function printMe() {
    console.log("I get called from print.js!");
}
```

在 `src/index.js` 中使用 printMe 方法：

```javascript
import printMe from './print.js';

var btn = document.createElement('button');
btn.innerHTML = 'Click me and check the console!';
btn.onclick = printMe;
element.appendChild(btn);
```

在 `dist/index.html` 中手工填入两个依赖的包文件 print.bundle.js 和 app.bundle.js：

```html
<html>
  <head>
    <title>Output Management</title>
    <script src="print.bundle.js"></script>
  </head>
  <body>
    <script src="app.bundle.js"></script>
  </body>
</html>
```

在 webpack.config.js 中创建两个 entry，并配置输出：

```javascript
  entry: {
      app: './src/index.js',
      print: './src/print.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  }
```

运行 `yarn run build` 进行打包测试。

# 使用 HtmlWebpackPlugin 插件自动创建 index.html

使用 HtmlWebpackPlugin 插件能在输出目录下自动创建 `index.html` 文件，并根据 webpack 配置文件自动插入依赖的打包文件。这样我们无需再手动创建 `dist/index.html` 文件了。使用 [html-webpack-template](https://github.com/jaketrent/html-webpack-template) 可以改变 HtmlWebpackPlugin 创建 index.html 文件时的模板。

先安装插件：

```bash
$ yarn add html-webpack-plugin --dev
```

在 webpack.config.js 中使用 HtmlWebpackPlugin 插件：

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    plugins: [
        new HtmlWebpackPlugin({
            title: 'Output Management by HtmlWebpackPlugin'
        })
    ]
}
```

删除 `dist/index.html`，打包并测试。

# 使用 clean-webpack-plugin 插件在每次构建前自动清空输出目录

先安装插件：

```bash
$ yarn add clean-webpack-plugin --dev
```

在 webpack.config.js 中使用：

```javascript
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  plugins: [
      new CleanWebpackPlugin(['dist'])
  ]
}
```

# Manifest

Webpack 通过 manifest 数据文件将打包的模块映射到输出的包中。

使用 [WebpackManifestPlugin](https://github.com/danethurber/webpack-manifest-plugin) 插件可以将 manifest 数据抽取成为一个 json 文件，方便使用。

# 参考

+ https://webpack.js.org/guides/output-management/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
