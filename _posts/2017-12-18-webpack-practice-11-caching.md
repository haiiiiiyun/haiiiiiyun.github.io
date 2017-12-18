---
title: webpack 实践 11： 缓存
date: 2017-12-18
writing-time: 2017-12-18
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# 输出文件中放入 hash

浏览器会根据资源的文件名进行缓存。

在 webpack 配置文件中，将 `[hash]` 替换变量设置在 `output.filename` 中，能实现针构建时相关的信息作为一个 hash 放入输出文件名中，例如：

```javascript
output: {
    filename: '[name].[hash].js‘
}
```

而 `[chunkhash]` 替换变量可以将 chunk 内容相关的信息作为一个 hash 放入输出文件名中。


```javascript
output: {
    filename: '[name].[chunkhash].js‘
}
```

`src/index.js` 文件：

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

`webpack.config.js` 文件：

```javascript
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: '[name].[chunkhash].js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Caching'
    }),
    new CleanWebpackPlugin(['dist'])
  ]
};
```

运行 `yarn run build` 产生打包文件 `main.15b52867804efb130452.js`：

```
Hash: 5b7a1b5a7365ee461d6a
Version: webpack 3.10.0
Time: 526ms
                       Asset       Size  Chunks                    Chunk Names
main.15b52867804efb130452.js     544 kB       0  [emitted]  [big]  main
                  index.html  197 bytes          [emitted]         
   [0] ./src/index.js 255 bytes {0} [built]
   [2] (webpack)/buildin/global.js 509 bytes {0} [built]
   [3] (webpack)/buildin/module.js 517 bytes {0} [built]
    + 1 hidden module
Child html-webpack-plugin for "index.html":
     1 asset
       [2] (webpack)/buildin/global.js 509 bytes {0} [built]
       [3] (webpack)/buildin/module.js 517 bytes {0} [built]
        + 2 hidden modules
Done in 1.07s.
```

运行 `yarn run build` 产生打包文件 `main.15b52867804efb130452.js`：

```
Hash: 5b7a1b5a7365ee461d6a
Version: webpack 3.10.0
Time: 535ms
                       Asset       Size  Chunks                    Chunk Names
main.15b52867804efb130452.js     544 kB       0  [emitted]  [big]  main
                  index.html  197 bytes          [emitted]         
   [0] ./src/index.js 255 bytes {0} [built]
   [2] (webpack)/buildin/global.js 509 bytes {0} [built]
   [3] (webpack)/buildin/module.js 517 bytes {0} [built]
    + 1 hidden module
Child html-webpack-plugin for "index.html":
     1 asset
       [2] (webpack)/buildin/global.js 509 bytes {0} [built]
       [3] (webpack)/buildin/module.js 517 bytes {0} [built]
        + 2 hidden modules
Done in 1.07s.
```

可见虽然代码没有修改，但是打包文件中的 hash 变了。

这是因为 webpack 会将运行时和 manifest 等一些样板信息放入 entry chunk 中，而这些信息在每次构建时会有变动。

# 抽出样板信息

利用 `CommonsChunkPlugin` 插件可以将 manifest 等样板信息抽出，生成一个独立的 bundle。

`webpack.config.js`:

```javascript
const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
        name: 'manifest'
    })
  ]
}
```

再次运行 `yarn run build` 会看到抽出会生成了独立的 `manifest.e949286afc215d459d57.js`。

最好将第三方库 `loadash`, `react` 等代码统一打包在一个独立的 `vendor` 包，因为这些内容一般不会变动。设置如下：

```javascript
//webpack.config.js
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
      main: './src/index.js',
      vendor: [
          'lodash'
      ]
  },
  output: {
    filename: '[name].[chunkhash].js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Caching'
    }),
    new CleanWebpackPlugin(['dist']),
    new webpack.optimize.CommonsChunkPlugin({
        name: 'vendor'
    }),
    new webpack.optimize.CommonsChunkPlugin({
        name: 'manifest'
    })
  ]
};
```

配置文件中的 CommonsChunkPlugin 实例的放置位置很重要，`vendor` 的必须放在 `manifest` 之上。


# 模块 标识

添加另一个模块 `src/print.js`:

```javascript
export default function print(text) {
  console.log(text);
}
```

`src/index.js` 修改为：

```javascript
import _ from 'lodash';
import Print from './print';

function component() {
  var element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = _.join(['Hello', 'webpack'], ' ');
  element.onclick = Print.bind(null, 'Hello webpack!');

  return element;
}

document.body.appendChild(component());
```

这次只是新增加了一个模块，并且只修改了 index.js，再次运行 `yarn run build`，会发现 manifest, vendor, main 这 3 个包文件名都变动了，与预期只有 main 会变动不符。

这是因为 `module.id` 是基于使用该模块的时间，其值是递增的，即删减模块后，其它模块的 ID 也可能会变化。


+ `main` 包名变动是因为它的内容有修改。
+ `vendor` 包名变动是因为它内部模块的 `module.id` 有变动。
+ `manifest` 包名变动是因为它包含了一个新的模块的引用。


添加 `NamedModulesPlugin` 插件后，webpack 会使用模块的路径名作为其标识，因而删减模块后，模块标识不会变动。但因其性能原因，最好只用在开发环境下。而生产环境中可使用 `HashedModuleIdsPlugin` 插件：

```javascript
//webpack.config.js
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
      main: './src/index.js',
      vendor: [
          'lodash'
      ]
  },
  output: {
    filename: '[name].[chunkhash].js',
    path: path.resolve(__dirname, 'dist')
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'Caching'
    }),
    new CleanWebpackPlugin(['dist']),
    new webpack.HashedModuleIdsPlugin(),
    new webpack.optimize.CommonsChunkPlugin({
        name: 'vendor'
    }),
    new webpack.optimize.CommonsChunkPlugin({
        name: 'manifest'
    })
  ]
};
```

之后运行 `yarn run build` 的结果会如预期。


# 参考

+ https://webpack.js.org/guides/caching/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
