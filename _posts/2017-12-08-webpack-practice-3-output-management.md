---
title: webpack 实践 3：输出管理
date: 2017-12-08
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

本文的代码基于 [webpack 实践 1：安装与初始化](http://www.atjiang.com/webpack-practice-2/

添加 `src/print.js`:

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

## 使用 HtmlWebpackPlugin 插件自动创建 index.html

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

## 使用 clean-webpack-plugin 插件在每次构建前自动清空输出目录

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

## Manifest

Webpack 通过 manifest 数据文件将打包的模块映射到输出的包中。

使用 [WebpackManifestPlugin](https://github.com/danethurber/webpack-manifest-plugin) 插件可以将 manifest 数据抽取成为一个 json 文件，方便使用。


# 开发环境

## 使用 source maps

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


## 使用 Watch 模式自动编译

webpack 开启 watch 模式后，当依赖树中的文件有修改时，会自动编译。

先在 `package.json` 中添加一个开启 webpack watch 模式的命令：

```javascript
"scripts": {
    "watch": "webpack --watch"
}
```

运行 `yarn run watch` 后，当文件有修改时，会自动编译。


## 使用 webpack-dev-server 自动重编译和重加载页面

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


# Hot Module Replacement

HRM 适合在开发环境中使用，不适合不生产中使用。

## 开启 HMR

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

## 通过 Node.js API 使用 Webpack Dev Server

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

## 使用 HMR 时的陷井

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

## 样式的 HMR

`style-loader` 加载器会通过 `module.hot.accept` 自动更新依赖的 CSS。

因此修改 css 样式后，会在页面上立即体现。

# Tree Shaking

webpack 2 内置对 *unused module export* 的检测。而 Tree Shaking 就是在打包时将没有用到的导出对象排除到包外。

先添加一个工具库 `src/math.js`，并导出两个函数：

```javascript
export function square(x) {
    return x*x;
}

export function cube(x) {
    return x*x*x;
}
```

`src/index.js` 修改为：

```javascript
import { cube } from './math.js';

function component() {
  var element = document.createElement('pre');

  element.innerHTML = [
      'Hello webpack!',
      '5 cubed = ' + cube(5)
  ].join('\n\n');

  return element;
}

document.body.appendChild(component());
```

由于没有从 `src/math.js` 中导入 `square` 方法，因此该函数为 *dead code*。

运行 `yarn run build` 后检查 `dist/app.bundler.js`：

```javascript
/***/ "./src/math.js":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export square */
/* harmony export (immutable) */ __webpack_exports__["a"] = cube;
function square(x) {
    return x*x;
}

function cube(x) {
    return x*x*x;
}


/***/ })

/******/ });
```

`square` 函数上加入了 `unused harmony export square` 的注释，并且该函数在打包后没有导出。

## 使用 UglifyJSPlugin 混淆并去除无用代码

先安装：

```bash
$ yarn add uglifyjs-webpack-plugin --dev
```

在 webpack.config.js 中使用：

```javascript
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')

//...
plugins: [
    new UglifyJSPlugin()
]
```

此后构建的包中将不再包含 square 代码。

在运行 webpack 时，添加 `--optimize-minimize` 命令行选项也能插入 UglifyJSPlugin 插件。

webpack 使用第三方工具实现 tree-shaking, 工具有 [UglifyJS](https://webpack.js.org/plugins/uglifyjs-webpack-plugin/)， [webpack-rollup-loader](https://github.com/erikdesjardins/webpack-rollup-loader) 和  [Babel Minify Webpack Plugin](https://webpack.js.org/plugins/babel-minify-webpack-plugin)。


# 生产环境

将 webpack 配置文件分成 3 个文件，共用部分 `webpack.common.js`，开发环境用 `webpack.dev.js`，生产环境下用 `webpack.prod.js`，然后用 `webpack-merge` 工具组合。

先安装 `webpack-merge`:

```bash
$ yarn add webpack-merge --dev
```

```javascript
//webpack.common.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
      app: './src/index.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
      new CleanWebpackPlugin(['dist']),
      new HtmlWebpackPlugin({
          title: 'Production'
      })
  ],
  module: {
      rules: [
          {
              test: /\.css/,
              use: [
                  'style-loader',
                  'css-loader'
              ]
          },
          {
              test: /\.(png|svg|jpg|gif|)$/,
              use: [
                  'file-loader'
              ]
          },
          {
              test: /\.(woff|woff2|eot|ttf|otf)$/,
              use: [
                  'file-loader'
              ]
          },
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
      ]
  }
};
```

```javascript
//webpack.dev.js
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    devtool: 'inline-source-map',
    devServer: {
        contentBase: './dist'
    }
});
```

```javascript
//webpack.prod.js
const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = merge(common, {
    plugins: [
        new UglifyJSPlugin()
    ]
});
```

## 自定义命令

在 `package.json` 中定义 `start` 命令用于开发环境下的测试，而 `build` 命令用于生产环境下的构建：

```javascript
"scripts": {
    "start": "webpack-dev-server --open --config webpack.dev.js",
    "build": "webpack --config webpack.prod.js"
},
```

## 混淆和最小化代码

可以用 [UglifyJSPlugin](https://webpack.js.org/plugins/uglifyjs-webpack-plugin)，还有一些更加流行的工具，如：

+ [BabelMinifyWebpackPlugin](https://github.com/webpack-contrib/babel-minify-webpack-plugin)
+ [ClosureCompilerPlugin](https://github.com/roman01la/webpack-closure-compiler)


## Source Mapping

建议在生产环境中也启用 source map, 以便于定位错误。在开发环境中一般用 `inline-source-map`，而在生产环境中避免用 `inline-***` 或 `eval-***` 的 source-map，它们会增大打包后的文件大小，并影响性能。

生产环境中可以使用 `source-map`，并在 UglifyJSPlugin 中也启用 souce map:

```javascript
module.exports = merge(common, {
    devtool: 'source-map',
    plugins: [
        new UglifyJSPlugin({
            sourceMap: true
        })
    ]
});
```

## 指定环境

`process.env.NODE_ENV` 这个变量值可以用来检测当前是生产环境还是开发环境。

可以使用 webpack 内置的 `DefinePlugin` 插件来定义这个变量值：

```javascript
//webpack.prod.js
const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const webpack = require('webpack');

module.exports = merge(common, {
    devtool: 'source-map',
    plugins: [
        new UglifyJSPlugin({
            sourceMap: true
        }),
        new webpack.DefinePlugin({
            'process.env.NODE_ENV': JSON.stringify('production')
        })
    ]
});
```

如果使用 react，可以看到这样定义后，打包文件会显著变小。

可以在源码的任何地方使用该变量：

```javascript
//src/index.js
if (process.env.NODE_ENV !== 'production') {
    console.log('Looks like we are in devel mode!');
}
```

## 用命令行传入

上面提到的这些插件也可以用 webpack 的命令行选项传入。

+ `--optimize-minimize` 将自动加入 UglifyJSPlugin 插件。
+ `--define process.env.NODE_ENV="'production'"` 会自动加入 DefinePlugin 实例并定义值。



# 参考

+ https://webpack.js.org/guides/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
