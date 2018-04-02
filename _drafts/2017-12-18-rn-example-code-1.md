---
title: React Native 官方文档示例 1
date: 2017-12-18
writing-time: 2017-12-18
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# Shimming

webpack 编译器能处理用 ES2015，CommonJS 或 AMD 编写的模块。

使用 Shimming 技术，使得能在 webpack 中处理 “非模块化” 的代码(例如 `jQuery` 库依赖一个全局的 `$` 变量)。

Shimming 的另一个使用场景是用在 [polyfill](https://en.wikipedia.org/wiki/Polyfill) 浏览器的功能上。


## Shimming 全局变量的场景

假设 `lodash` 包也和 `jQuery` 一样，导出为一个全局变量。

使用 `ProvidePlugin` 插件可使一个包能在每个通过 webpack 编译过的模块中作为一个变量使用。当 webpack 看到有使用该变量时，将在打包的 bundle 中加入相应的包体。

先在 `src/index.js` 中去除对 `lodash` 的 `import` 语句：

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

在 webpack.config.js 中提供 `_` 变量的定义：

```javascript
const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    plugins: [
        new webpack.ProvidePlugin({
            _: 'lodash'
        })
    ]
};
```

还可以用 `ProvidePlugin` 导出模块中的多个属性和方法，参数形式为 `[module, child1, child2, ...children?]`。

例如只导出 `lodash` 中的 `join`:

```javascript
//webpack.config.js
    plugins: [
        new webpack.ProvidePlugin({
            join: ['lodash', 'join']
        })
    ]
```


此时 `src/index.js` 中直接使用 join 函数：

```javascript
function component() {
  var element = document.createElement('div');

  // Lodash, now imported by this script
  element.innerHTML = join(['Hello', 'webpack'], ' ');

  return element;
}

document.body.appendChild(component());
```

运行 `yarn run build` 后等到的打包文件会变小，即未用 `ProvidePlugin` 导出的内容没有打包进来。


# Granular Shimming

有些旧模块会将 `this` 作为 `window` 对象。

作为模拟，将 `src/index.js` 修改为：

```javascript
function component() {
  var element = document.createElement('div');

  element.innerHTML = join(['Hello', 'webpack'], ' ');

  // Assume we are in the context of `window`
  this.alert("Hmmm, this probably isn't a great idea...");

  return element;
}

document.body.appendChild(component());
```

上面模块无法在 CommonJS 上下文中运行，因为此时的 `this` 指定 `module.exports`。

需要在 webpack.config.js 中用 `imports-loader` 加载器重载 `this`:

```javascript
const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            {
                test: require.resolve('./src/index.js'),
                use: 'imports-loader?this=>window'
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            join: ['lodash', 'join']
        })
    ]
};
```

之后 `./src/index.js` 文件中的 `this` 都指向 `window`。

安装 `imports-loader`:

```bash
$ yarn add imports-loader --dev
```

# 全局导出

假设有一个库，是以导出全局变量的形式实现的。假设库为 `src/globals.js`:

```javascript
var file = 'blah.txt';
var helpers = {
  test: function() { console.log('test something'); },
  parse: function() { console.log('parse something'); }
}
```

此时需要在 webpack.config.js 中用 `exports-loader` 将全局变量导出转换为普通的模块导出，例如将模块中的 `file` 导出为 `file`, `helpers.parse` 导出为 `pase`:

```javascript
    module: {
        rules: [
            {
                test: require.resolve('./src/globals.js'),
                use: 'exports-loader?file,parse=helpers.parse'
            }
        ]
    },
```

之后，在 `src/index.js` 中，可以用 `import { file, parse } from './globals` 的形式导入了。

安装 `exports-loader`:

```bash
$ yarn add exports-loader --dev
```

# 参考

+ https://webpack.js.org/guides/shimming/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
