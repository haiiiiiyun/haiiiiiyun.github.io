---
title: webpack 2.x 简介
date: 2017-12-04
writing-time: 2017-12-04
categories: programming
tags: JS javascript webpack
---

## 概念

webpack 是一个 JS 应用的模块打包工具。它会将你的应用所需的每一个模块用递归方式构建成依赖图 (dependency graph)，然后打包成一个或多个 bundle。

## Entry

可在配置文件中用 `entry` 设置入口点，用来表示从哪个模块开始构建依赖图。例如：

```javascript
//webpack.config.js
module.exports = {
    entry: "./path/to/my/entry/file.js"
};
```

### 单入口语法

形式为 `entry: string|Array<string>`。

`entry: string` 形式的写法实际上是以下的简写：

```javascript
entry: {
    main: "./path/to/my/entry/file.js"
}
```

也可以传入数组的形式，表示 "multi-main entry"，用来实现将多个文件整合成一个依赖包 (dependency chunk)。

### 对象形式的语法

形式为 `entry: {[entryChunkName: string]: string|Array<string>}`。

可以指定多组 chunk 的入口：

```javascript
module.exports = {
    entry: {
        app: "./src/app.js",
        vendors: "./src/vendors.js"
    }
};
```

上例中将为本应用及第三方库创建两个各自独立的依赖图。在单页应用中，这样设置后，可以利用 `CommonsChunkPlugin` 从应用的 bundle 中抽取出第三方库的引用，并放入 vendor bundle 中,并使用 `__webpack_require__()` 调用来代替这些引用。

在多页应用中，可设置为：

```javascript
module.exports = {
    entry: {
        page1: "./src/page1/index.js",
        page2: "./src/page2/index.js",
        page3: "./src/page3/index.js"
    }
};
```

这样可为每页打包一个独立的 bundle。同时可利用 `CommonsChunkPlugin` 抽出每页的共享的代码创建一个共享的 bundle。


## Output

可用 `output` 设置打包文件的输出目录和文件名等，例如：

```javascript
//webpack.config.js
const path = require("path");

module.exports = {
    entry: "./path/to/my/entry/file.js"
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: 'my-first-webpack.bundle.js"
    }
};
```

`__dirname` 是 node.js 中的一个环境变量，用来表示当前执行脚本所有目录。

虽然 `entry` 可以设置多个入口，但是只能有一个 `output` 设置，因此需要使用代替法实现输出文件名的唯一性，如：

```javascript
{
  entry: {
    app: './src/app.js',
    search: './src/search.js'
  },
  output: {
    filename: '[name].js',
    path: __dirname + '/dist'
  }
}

// writes to disk: ./dist/app.js, ./dist/search.js
```

下面是将 CDN 上的资源文件通过其 hash 定位输出到项目中的例子：

```javascript
output: {
  path: "/home/proj/cdn/assets/[hash]",
  publicPath: "http://cdn.example.com/assets/[hash]/"
}
```

## Loader

webpack 本身只能处理 js 文件，但是 loader 能将其它文件转变成 webpack 能处理的模块形式，从而使它们也能被 webpack 打包进 bundle 中。

在 `import` 或加载某类型的文件中，若该类型文件有设置了 loader，则该类型文件会先通过该 loader 进行预处理后再进行加载。

使用 Loader 可实现压缩、打包、编程语言翻译等功能。

配置 Loader:

+ 用 `test` 项中的正则表达式匹配要处理的文件。
+ 用 `use` 项设置这些文件要使用的 loader。


例如：

```javascript
//webpack.config.js
const path = require("path");

module.exports = {
    entry: "./path/to/my/entry/file.js"
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: 'my-first-webpack.bundle.js"
    },
    module: {
        rules: [
            { test: /\.txt$/, use: 'raw-loader' }
        ]
    }
};
```

上面的 Loader 配置信息写在 `module.rules` 属性中。

本例实现了将应用中用 `require()` 或 `import` 语句加载的 `.txt` 文件都会先通过 `raw-loader` 处理，再通过 webpack 打包。

### Loader 的使用

Loader 一般是一些 npm 库，故要先安装：

```bash
$ npm install --save-dev css-loader # css -> javascript
$ npm install --save-dev ts-loader  # typescript -> javascript
```

有 3 种使用 Loader 的方法：

+ 在 webpack.config.js 配置文件中指定（推荐）
+ 在 `import` 语句中显式指定，inline 方式
+ 在命令行中指定


一类文件可以指定多个 Loader，并加入 Loader 参数。

配置文件中的例子：

```javascript
module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          { loader: 'style-loader' },
          {
            loader: 'css-loader',
            options: {
              modules: true
            }
          }
        ]
      }
    ]
  }
```

Inline 的例子：

```javascript
import Styles from 'style-loader!css-loader?modules!./styles.css';
```

其中资源与 Loader 之间用 `!` 分隔，Loader 参数可用 query parameter 形式传入，如 `?key=value&foo=bar`，也可以 JSON 对象传入，如 `?{"key":"value","foo": "bar"}`。


命令行中的例子：

```bash
$ webpack --module-bind jade-loader  --module-bind 'css=style-loader!css-loader'
```

### Loader 功能

+ 多个 Loader 可以串联，中间的 Loader 返回值不限制，但最后一个 Loader 必须返回一个 webpack 可用的 JS 对象
+ 可异步/同步使用
+ 普通模块在其 `package.json` 中可通过 `loader` 项导出一个 Loader



## Plugin

Loader 只用来将各种文件转变成 webpack 可处理的模块。而插件可实现 bundle 优化，代码混淆等其它任务。

插件有 [插件接口](https://webpack.js.org/api/plugins)，可用来实现自己的插件。

插件是 webpack 的骨架，webpack 本身就构造在相同的插件系统上。

一个 webpack 插件就是具有 `apply` 属性的 JS 对象。webpack 编译器会调用每个插件的 `apply` 属性，从而使插件能访问整个编译生命周期。

### 一个简单的插件

```javascript
//ConsoleLogOnBuildWebpackPlugin.js

function ConsoleLogOnBuildWebpackPlugin() {};

ConsoleLogOnBuildWebpackPlugin.prototype.apply = function(compiler) {
  compiler.plugin('run', function(compiler, callback) {
    console.log("The webpack build process is starting!!!");

    callback();
  });
};
```

由于有 `Function.prototype.apply` 方法，因此所有的 JS 函数都可以作为插件传入，此时，其 `this` 会指向 `compiler`。

### 插件的使用

由于插件能接收参数，因此必须通过 `new` 实例化时传入。

在配置文件中一个插件可能要使用多次：

```javascript
const HtmlWebpackPlugin = require('html-webpack-plugin'); //installed via npm
const webpack = require('webpack'); //to access built-in plugins
const path = require('path');

const config = {
  entry: './path/to/my/entry/file.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'my-first-webpack.bundle.js'
  },
  module: {
    rules: [
      { test: /\.txt$/, use: 'raw-loader' }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new HtmlWebpackPlugin({template: './src/index.html'})
  ]
};

module.exports = config;
```

插件实例放在 `plugins` 属性中。webpack 提供了[多个插件](https://webpack.js.org/plugins)。

## 配置文件

webpack 的配置文件是一个 JS 文件，并且是一个 CommonJS 模块，它通过 `module.exports` 导出配置对象供 webpack 使用。

由于是一个 CommonJS 模块，故可以用 `require(...)` 加载到其它地方使用。

## webpack 模块

webpack 模块可以通过如下方式表达：

+ ES2015 `import` 语句
+ CommonJS `import` 语句
+ AMD 的 `define` 和 `require` 语句
+ css/sass/less 文件中的 `@import` 语句
+ 样式文件中的 `url(...)` 或 html 文件中的 `<img src=...>`


通过 Loader，webpack 可支持如下用不同语言实现的模块：

+ CoffeeScript
+ TypeScript
+ ESNext (Babel)
+ Sass
+ Less
+ Stylus


### 模块定位

webpack 在打包时对于 `require/import` 语句中的模块，使用 [enhanced-resolve](https://github.com/webpack/enhanced-resolve) 来定位模块。

`enhanced-resolve` 可以解析 3 种类型的路径：

**绝对路径**

例如：

```javascript
import "/home/me/file";
import "C:\\Users\\me\\file";
```

**相对路径**

相对于当前 `import/require` 语句所有的文件目录，例如：

```javascript
import "../src/file1";
import "./file2";
```

**模块路径**

在配置项 `resolve.modules` 中指定的各目录中查找模块。可以通过 `resolve.alias` 将模块路径替换成另一个别名。

使用这种规则时，resolver 会先确定路径指向的是文件还是目录。

如果指向的是一个文件，则：

+ 如果有后缀名，则该文件直接打包
+ 如果没有，则通过 `resolve.extensions` 配置项中的设定来解析，可确定可接受的后缀名（如 .js, .jsx）


如果指向的是一个目录，则：

+ 如果目录中有 `package.json` 文件，则根据其中的 `resolve.mainFields` 中依次查找各子项，使用首个找到的文件路径
+ 如果没有 `package.json` 文件，或 `resolve.mainFields` 没有返回有效路径，则在 `resolve.mainFields` 中依次查找文件名，看是否与 `import/required` 目录下的文件匹配
+ 文件后缀名也使用 `resolve.extensions` 解析


### 缓存

模块访问后都会被缓存。

## Target

JS 代码可用于服务端和浏览器端，故可用 `target` 指示打包部署的目标。

下面是将一个库打包成多个目标包的配置文件：

```javascript
//webpack.config.js
ar path = require('path');
var serverConfig = {
  target: 'node', //the bundle weill be loaded by `require()` in node
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'lib.node.js'
  }
  //…
};

var clientConfig = {
  target: 'web', // <=== can be omitted as default is 'web'
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'lib.js'
  }
  //…
};

module.exports = [ serverConfig, clientConfig ];
```

会打包成 `lib.js` 和 `lib.node.js` 两个文件。

## Manifest

使用 webpack 构建的应用中一般有 3 种代码：

1. 自己写的代码
2. 依赖的库代码，即第三方或 vendor 代码
3. webpack 运行时及用来指导所有模块间交互的 *manifest*

### 运行时

webpack Runtime + manifest 数据，用来联结你的模块化应用。它还包含加载逻辑和路径解析逻辑，用来连接模块间的交互及按需加载等。

### Manifest

你的应用代码被 webpack 解析和打包后，你的所有模块的所有详细信息都会保存到一个 Manifest 数据文件中。运行时利用 Manifest 数据文件来解析和加载打包块中的模块。

无论之前你的代码中使用什么样的模块加载语法，这些 `import` 和 `require` 语句在打包块的模块中都替换成了 `__webpack_require__` 方法。

### 用处

使用 Manifest，结合将文件内容的 hash 加入打包块文件名中，可以优化文件的浏览器缓存。详细见 [manifest 文档](https://webpack.js.org/concepts/manifest/)。


## 热模块替换 (Hot Module Replace)

HMR 能在应用运行过程中对模块进行交换、添加和删除。

下面从几个不同角度说明其基本原理。

### 应用程序的角度

1. 应用请求 HMR 运行时去检测是否有更新
1. HMR 运行时异步下载更新并通知应用
1. 应用要求 HMR 运行时应用更新
1. HMR 运行时同步应用更新

### 编译器的角度

编译器需要触发 “更新数据” 进行更新：

“更新数据” 有两部分：

1. 更新后的 manifest (JSON)，包含新的编译 hash
1. 一个或多个更新块（JS），包含更新模块的新代码


### 模块的角度

模块只按需实现 HMR 代码。一个例子是通过 `style-loader` 修改样式。`style-loader` 需实现 HMR 接口，当从 HMR 接收到更新消息时，用新数据替换旧样式。

类似地，在模块中实现 HMR 接口时，要描述当模块更新时要进行什么操作，接口见 [HMR API page](https://webpack.js.org/api/hot-module-replacement)。

### 模块系统运行时的角度

运行时会触发对模块的父模块及子模块的跟踪操作。

运行时支持两个方法： `check` 和 `apply`。

`check` 通过 HTTP 请求更新的 manifest。如果请求失败，则无需更新。如果成功，一列更新块会与当前加载的块(chunk)进行比较。对于第一个加载的块来说，其对应的更新块将被下载。所有的模块更新都存储在运行时中。当所有的更新块下载完毕后，运行时切换到 `ready` 状态。

`apply` 方法会先将所有已更新模块标识为无效。对于每个无效的模块，本模块或其父模块中需要有一个更新处理器(update handler)，进行相应的处理并将取消模块的无效标记，本模块没有更新处理器的依次上浮到父模块处理。

之后，所有还是无效的模块都被通过 dispose handler 进行处置，并卸载。模块的 hash 进行更新，调用所有的 `accept handler`。运行时此时切换回 `idle` 状态。


## 参考

+ https://webpack.js.org/concepts/
