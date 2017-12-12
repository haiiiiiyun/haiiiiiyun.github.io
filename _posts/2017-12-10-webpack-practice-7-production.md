---
title: webpack 实践 7： 生产环境
date: 2017-12-10
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---


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

+ https://webpack.js.org/guides/production/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
