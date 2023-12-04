---
title: webpack 实践 1：安装与初始化
date: 2017-12-05
writing-time: 2017-12-05
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# 安装

## 局部安装

本系统例子使用 [yarn](www.atjiang.com/yarn-intro/) 来管理 node 包。


```bash
$ mkdir -p ~/workspace/webpack-practice/getting-started
$ cd ~/workspace/webpack-practice/getting-started
$ yarn init # create package.json
$ yarn add webpack --dev
#$ yarn add webpack@version --dev  # add special version
```

webpack 程序一般放在 "node_modules/.bin/" 下。


# 初始化

添加文件 `index.html`, `src/index.js`。

```javascript
//src/index.js
function component() {
  var element = document.createElement('div');

  // Lodash, currently included via a script, is required for this line to work
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

```html
<!--index.html-->
<html>
  <head>
    <title>Getting Started</title>
    <script src="https://unpkg.com/lodash@4.16.6"></script>
  </head>
  <body>
    <script src="./src/index.js"></script>
  </body>
</html>
```

现在 `src/index.js` 通过 `<script>` 标签依赖于 `lodash`。

## 使用 webpack 创建一个 Bundle

创建 `dist` 目录用来存放分发的代码，将 `index.hmtl` 移到 `dist/` 下。`src/index.js` 中显式 `import _ from 'lodash'`。同时去除 `dist/index.html` 中的 `lodash` 链接。

由于现在是 `import _ from 'lodash`，因此需要手动下载安装 lodash:

```bash
$ yarn add lodash
```

现在的文件内容：

```javascript
//src/index.js
import _ from 'lodash';
function component() {
  var element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

```html
<!--dist/index.html-->
<html>
  <head>
    <title>Getting Started</title>
  </head>
  <body>
    <script src="bundle.js"></script>
  </body>
</html>
```

运行 webpack 进行打包：

```bash
$ yarn run webpack src/index.js  dist/bundle.js

Hash: b78ba88800fb17fdfd02
Version: webpack 3.10.0
Time: 301ms
    Asset    Size  Chunks                    Chunk Names
bundle.js  544 kB       0  [emitted]  [big]  main
   [0] ./src/index.js 256 bytes {0} [built]
   [2] (webpack)/buildin/global.js 509 bytes {0} [built]
   [3] (webpack)/buildin/module.js 517 bytes {0} [built]
    + 1 hidden module
```

这里将 `src/index.js` 作为入口，`dist/bundle.js` 作为输出打包文件。

## 使用配置文件

创建 webpack 的打包配置文件 `webpack.config.js`:

```javascript
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  }
};
```

再运行打包：

```bash
$ yarn run webpack --config webpack.config.js

hash: b78ba88800fb17fdfd02
Version: webpack 3.10.0
Time: 306ms
    Asset    Size  Chunks                    Chunk Names
bundle.js  544 kB       0  [emitted]  [big]  main
   [0] ./src/index.js 256 bytes {0} [built]
   [2] (webpack)/buildin/global.js 509 bytes {0} [built]
   [3] (webpack)/buildin/module.js 517 bytes {0} [built]
    + 1 hidden module
Done in 0.72s.
```

由于默认的配置文件名为 `webpack.config.js`，故上面命令可简写为:

```bash
$ yarn run webpack
```

## NPM 脚本

在 `package.json` 中添加 webpack 的自定义命令：

```json
{
    "scripts": {
        "build": "webpack"
    }
}
```

再用 `yarn run build` 运行。

# 参考

+ https://webpack.js.org/guides/installation/
+ https://webpack.js.org/guides/getting-started/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
