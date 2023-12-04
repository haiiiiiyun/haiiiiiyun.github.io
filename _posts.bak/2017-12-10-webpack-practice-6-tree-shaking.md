---
title: webpack 实践 6： 去除无用代码 Tree Shaking
date: 2017-12-10
writing-time: 2017-12-08
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

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

运行 `yarn run build` 后检查 `dist/bundle.js`：

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

# 使用 UglifyJSPlugin 混淆并去除无用代码

先安装：

```bash
$ yarn add uglifyjs-webpack-plugin --dev
```

在 webpack.config.js 中使用：

```javascript
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

//...
plugins: [
    new UglifyJSPlugin()
]
```

此后构建的包中将不再包含 square 代码。

在运行 webpack 时，添加 `--optimize-minimize` 命令行选项也能插入 UglifyJSPlugin 插件。

webpack 使用第三方工具实现 tree-shaking, 工具有 [UglifyJS](https://webpack.js.org/plugins/uglifyjs-webpack-plugin/)， [webpack-rollup-loader](https://github.com/erikdesjardins/webpack-rollup-loader) 和  [Babel Minify Webpack Plugin](https://webpack.js.org/plugins/babel-minify-webpack-plugin)。


# 参考

+ https://webpack.js.org/guides/tree-shaking/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
