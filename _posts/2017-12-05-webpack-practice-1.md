---
title: webpack 2.x 实践（一）
date: 2017-12-05
writing-time: 2017-12-05
categories: programming
tags: JS javascript webpack yarn
---

# 安装

## 局部安装

```bash
$ cd ~/workspace/webpack-practice
$ yarn init # create package.json
$ yarn add webpack --dev
$ yarn add webpack@version --dev  # add special version
$ yarn  install
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

# 资源文件管理

使用 webpack 可以完成 grunt 或 gulp 的工作。

## 加载 CSS

要使 JS 中能 `import` CSS，需要安装 `style-loader` 和 `css-loader`:

```bash
$ yarn add style-loader css-loader --dev
```

再在 webpack.config.js 中为 css 文件配置加载器：

```javascript
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
      rules: [
          {
              test: /\.css/,
              use: [
                  'style-loader',
                  'css-loader'
              ]
          }
      ]
  }
};
```

现在可以在 JS 模块中 `import './style.css'`，然后当模块运行时，一个带有 `style.css` 内容的 `<style>` 标签将插入到 html 文件中的 `<head>` 中。

创建 `src/style.css` 文件：

```css
.hello {
    color: red;
}
```

在 `src/index.js` 中加载并使用 CSS:

```javascript
import _ from 'lodash';
import './style.css'

function component() {
  var element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');
  element.classList.add('hello');

  return element;
}

document.body.appendChild(component());
```

运行 `yarn run build` 打包并测试效果。

通过 loader, 还可以直接将 sass, less 文件翻译后再加载进 JS 模块中。

## 加载图片

使用 `file-loader` 来加载图片。

安装加载器：

```bash
$ yarn add file-loader --dev
```

在 webpack.config.js 中为图片应用加载器：

```javascript
//...
    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|gif|)$/,
                use: [
                    'file-loader'
                ]
            }
        ]
    }
//...
```


现在，当 `import MyImage from './my-image.png'` 时，该图片经过处理后将添加到配置文件中 `output` 指定的目录中，而 `MyImage` 变量中将表示处理后的图片 URL。

当使用 `css-loader` 时，其中的 `url('./my-image.png')` 等的图片引用也会经历上面类似的图片加载处理过程，并将 `url` 值更新为处理后的 URL 值。

`html-loader` 在处理 `<img src="./my-image.png" />` 等图片引用也，处理同上。

在 `src/index.js` 中加载和使用图片：

```javascript
import Icon from './icon.png';
//...
var myIcon = new Image();
myIcon.src = Icon;

element.appendChild(myIcon);
```

在 `src/style.css` 中使用背景图片：

```css
.hello {
    color: red;
    background: url('./icon.png');
}
```

打印处理后，`icon.png` 将输出到 `dist` 目录下，并改为了 `86375d934477a20aaf0f446b12a17cfb.png` 类似的名字。

## 加载字体

字体的加载和图片加载一样，也是用 `file-loader` 加载器，同时，字体文件的 url 处理也和图片的一样。

下载字体 [aclonica-font](http://www.1001fonts.com/aclonica-font.html)，将字体文件 Aclonica.ttf 放在 `src` 下。

在 webpack.config.js 中添加针对字体文件的 loader:

```javascript
{
    test: /\.(woff|woff2|eot|ttf|otf)$/,
    use: [
        'file-loader'
    ]
}
```

在 `src/styles.css` 中通过 url 引用字体文件：

```css
@font-face {
    font-family: 'Aclonica';
    src: url('./Aclonica.ttf') format('truetype');
    font-weight: 600;
    font-style: normal;
}

.hello {
    color: red;
    font-family: 'Aclonica';
    background: url('./icon.png');
}
```

## 加载数据文件

和 Node 一样，webpack 内置也直接支持导入 json 文件，如 `import Data from './data.json`。而 CSV, TSV，XML 等数据文件则要 `csv-loader` 和 `xml-loader` 加载器加载。

安装加载器：

```bash
$ yarn add csv-loader xml-loader --dev
```

webpack.config.js 中加入加载器使用规则：

```javascript
{
    test: /\.(csv|tsv)$/,
    use: [
        'csv-loader'
    ]
},
{
    test: /\.xml$/,
    use: [
        'xml-loader'
    ]
}
```

添加 xml 数据文件 `src/data.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Mary</to>
  <from>John</from>
  <heading>Reminder</heading>
  <body>Call Cindy on Tuesday</body>
</note>
```

现在可以在 `src/index.js` 中加载和使用 JSON, CSV, TSV, XML 数据了：

```javascript
import Data from './data.xml';

console.log(Data);
```

可以看到，Data 变量即为一个解析了的 JSON 对象。

## 全局资源目录

通过 webpack 的资源打包方式，我们可以将组件所需的资源放在组件目录下，无需放在一个全局目录下，从而提高可复用性。


# 参考

+ https://webpack.js.org/guides/
