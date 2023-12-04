---
title: webpack 实践 12： 打包发布自己的库
date: 2017-12-19
writing-time: 2017-12-18
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

# 新建一个库

文件有：

```
  |- webpack.config.js
  |- package.json
  |- /src
    |- index.js
    |- ref.json
```

初始化：

```bash
$ npm init -y
$ npm install --save-dev webpack lodash
```

`src/ref.json`:

```javascript
[{
  "num": 1,
  "word": "One"
}, {
  "num": 2,
  "word": "Two"
}, {
  "num": 3,
  "word": "Three"
}, {
  "num": 4,
  "word": "Four"
}, {
  "num": 5,
  "word": "Five"
}, {
  "num": 0,
  "word": "Zero"
}]
```

`src/index.js`:

```javascript
import _ from 'lodash';
import numRef from './ref.json';

export function numToWord(num) {
  return _.reduce(numRef, (accum, ref) => {
    return ref.num === num ? ref.word : accum;
  }, '');
};

export function wordToNum(word) {
  return _.reduce(numRef, (accum, ref) => {
    return ref.word === word && word.toLowerCase() ? ref.num : accum;
  }, -1);
};
```

# 实现目标

+ 不打包进 `lodash`，让用户自行添加依赖
+ 库包设置为 `webpack-numbers`
+ 将库导出为一个叫 `webpackNumbers` 的变量
+ 能在 Node.js 中访问该库


同时用户能用如下方式访问库：

+ ES2015 模块中： `import webpackNumbers from 'webpack-numbers'`
+ CommonJS 模块中：`require('webpack-numbers')`
+ 使用 `<script>` 加载时通过全局变量访问


# 配置文件

```javascript
//webpack.config.js
var path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'webpack-numbers.js'
  }
};
```

# 指定外部依赖

不打包进 `lodash`，只将它指定为是一个依赖，需要用户自行安装：

```javascript
//webpack.config.js
var path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'webpack-numbers.js'
  },
  externals: {
    lodash: {
      commonjs: 'lodash',
      commonjs2: 'lodash',
      amd: 'lodash',
      root: '_'
    }
  }
};
```

也可以用正则表达式来指定多个外部依赖，例如对于依赖：

```javascript
import A from 'library/one';
import B from 'library/two';
//...
```

可以在 webpack.config.js 中指定为：

```javascript
externals: [
    'library/one',
    'library/two',
    // Everything that starts with "library/"
    /^library\/.+$/
]
```

# 导出库

导出库要能在多个环境下使用，如 CommonJS, AMD, Node.js 和作为全局变量等。

通过 `output.library` 属性设置导出的库名：

```javascript
//webpack.config.js
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'webpack-numbers.js',
    library: 'webpackNumbers'
  }
```

这将我们的库作为一个名为 `webpackNumbers` 的全局变量导出。通过 `output.libraryTarget` 属性设置以何种方式导出库。

导出方式有：

+ `libraryTarget: 'var'`： 通过 `<script>` 标识引用，作为一个全局变量使用，默认方式，通过 `libraryTarget: { var: 'varname' }`，还同时指定导出的全局变量名
+ `libraryTarget: 'this'`: 导出到 `this`，通过 `this` 访问
+ `libraryTarget: 'window'`: 导出到浏览器的 `window` 对象中
+ `libraryTarget: 'umd'`: 通过 `require` 加载使用


# 优化

可根据 [webpack 实践 7： 生产环境](http://www.atjiang.com/webpack-practice-7-production/) 进行优化。

在 package.json 中设置：

```javascript
{
    "main": "dist/webpack-numbers.js",
}
```

以指向库的最终的包文件。

同时根据 [这篇文章](https://github.com/dherman/defense-of-dot-js/blob/master/proposal.md#typical-usage) 添加:

```javascript
{
    "module": "src/index.js",
}
```

从而保持在非 ES2015 模块环境的兼容性。

运行 ` ./node_modules/.bin/webpack` 进行打包，将打包输出文件 [作为一个 npm 包发布](https://docs.npmjs.com/getting-started/publishing-npm-packages)。


# 参考

+ https://webpack.js.org/guides/author-libraries/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
