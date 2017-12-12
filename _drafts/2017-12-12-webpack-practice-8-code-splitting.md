---
title: webpack 实践 8： 代码分割
date: 2017-12-12
writing-time: 2017-12-12
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

webpack 的代码分割功能能将代码分成多个 bundle，从而实现按需加载或并行加载。

有 3 种常用的代码分割方法：

+ 入口点：在配置文件中通过 `entry` 手动指定分割
+ 去重：使用 `CommonsChunkPlugin` 插件抽取重复模块
+ 动态加载：通过模块中的内联函数调用实现


# 入口点方法

这是最直观最简单的方法，缺点是需要手动配置分割，并且重复的模块可能会打包进多个 bundle 中，无法去重。


添加另一个模块 `src/another-module.js`：

```javascript
import _ from 'lodash';

console.log(
    _.join(['Another', 'module', 'loaded!'], ' ')
);
```

`webpack.config.js`:

```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
    index: './src/index.js',
    another: './src/another-module.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Code Splitting'
    }),
    new CleanWebpackPlugin(['dist'])
  ]
};
```

`src/index.js`:

```javascript
import _ from 'lodash';

function component() {
  var element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

运行 `yarn run build` 会打包出两个文件 `dist/index.bundle.js` 和 `dist/another.bundle.js`。由于 `src/index.js` 和 `src/another-module.js` 这两个源文件中都加载了 `lodash`，两个结果包中也都有包含了 `lodash`，没有去重。

# 去重

[CommonsChunkPlugin](https://webpack.js.org/plugins/commons-chunk-plugin) 插件可以将通用的依赖模块抽取出来，保存到现有的 entry chunk 或一个新的 chunk 中。

先在 `webpack.config.js` 中使用该插件：

```javascript
const webpack = require('webpack');

module.exports = {
  //...
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
        name: 'common' // Specify the common bundle's name.
    })
  ]
};
```

运行 `yarn run build` 可以多出了一个打包文件： `dist/common.bundle.js`。即将原来两个包文件中重复的 `lodash` 模块抽取了出来并单独保存为了一个新的打包文件。

使用该插件可以将第三方库 (vendor) 代码抽取并打包为一个独立包。

可用于分割代码的其它插件和加载器：

+ [ExtractTextPlugin](https://webpack.js.org/plugins/extract-text-webpack-plugin)：可用于将 CSS 从主程序中分割出来
+ [bundle-loader](https://webpack.js.org/loaders/bundle-loader): 可用来分割代码并按需加载模块
+ [promise-loader](https://github.com/gaearon/promise-loader): 和 bundle-loader 类似，但使用 promises


# 动态加载

这里会有 2 种方法：

+ 使用 `import()` 语法（内部使用了 promises 实现，因此老浏览器上需使用 [es6-promise](https://github.com/stefanpenner/es6-promise) 或 [promise-polyfill](https://github.com/taylorhakes/promise-polyfill)
+ 另一个老方法，即使用 webpack 的 `require.ensure`

先在 `webpack.config.js` 中去除 CommonsChunkPlugin 插件，入口设置为一个，`output` 中添加 `chunkFilename` 配置：

```javascript
//webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
    index: './src/index.js',
  },
  output: {
    filename: '[name].bundle.js',
    chunkFilename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Code Splitting'
    }),
    new CleanWebpackPlugin(['dist'])
  ]
};
```

`chunkFilename` 配置项用来确定 `non-entry chunk` 文件的名字，详细见 [output doc](https://webpack.js.org/configuration/output/#output-chunkfilename)。


将 `src/index.js` 修改成动态加载 `lodash`：

```javascript
function getComponent() {
    return import(/* webpackChunkName: "lodash" */ 'lodash').then(_ => {
        var element = document.createElement('div');
        element.innerHTML = _.join(['Hello', 'webpack'], ' ');
        return element;
    }).catch(error => 'An error occurred while loading the component');
}

getComponent().then(component => {
    document.body.appendChild(component);
});
```

注意 `import` 语句中的 `webpackChunkName: "lodash"` 注释，它将使动态加载的模块打包为 `lodash.bundle.js`。关于 webpackChunkName 和其它选项，见 [import doc](https://webpack.js.org/api/module-methods#import-)。

打包后可看到生成了 `dist/lodash.bundle.js` 和 `dist/index.bundle.js`。


# Bundle 分析工具

+ [官方工具](https://github.com/webpack/analyse)
+ [webpack-chart](https://alexkuz.github.io/webpack-chart/)： 以交互式的饼图显示 webpack stat
+ [webpack-visualizer](https://chrisbateman.github.io/webpack-visualizer/)：可视化并分析你的 bundle，以查看模块都占用多少空间，是否有重复
+ [webpack-bundle-analyzer](https://github.com/th0r/webpack-bundle-analyzer)： 即是一个插件，也是一个命令行工具，能以便捷的交互式的可绽放的 treemap 方式呈现 bundle 的内容。


# 参考

+ https://webpack.js.org/guides/code-splitting/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
