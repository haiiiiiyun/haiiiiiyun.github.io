---
title: webpack 实践 9： 按需加载
date: 2017-12-14
writing-time: 2017-12-12
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

本文在代码分割的基础上，实现当用户交互时，进行按需加载。

创建新的模块 `src/print.js`:

```javascript
console.log('The print.js module has loaded! See the network tab in dev tools...');

export default () => {
  console.log('Button Clicked: Here\'s "some text"!');
}
```

`src/index.js` 调整为根据用户交互进行动态加载：

```javascript
import _ from 'lodash';

function component() {
    var element = document.createElement('div');
    var button = document.createElement('button');
    var br = document.createElement('br');

    button.innerHTML = 'Click me and look at the console!';
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    element.appendChild(br);
    element.appendChild(button);

    // Note that because a network request is involved, some indication
    // of loading would need to be shown in a prod-level site/app.
    button.onclick = e => import(/* webpackChunkName: "print" */ './print').then(module => {
        var print = module.default;
        print();
    });

    return element;
}

document.body.appendChild(component());
```

注意当 `import()` ES6 模块时，必须使用 `module` 对象的 `default` 属性值，它是当 promise resolved 时的返回值。


webpack.conf.js:

```javascript
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
      title: 'Lazy Loading'
    }),
    new CleanWebpackPlugin(['dist'])
  ]
};
```

运行 `yarn run build` 进行打包测试。

React 等框架都有自己的动态加载方法，见 [Code Splitting and Lazy Loading](https://reacttraining.com/react-router/web/guides/code-splitting)。


# 参考

+ https://webpack.js.org/guides/lazy-loading/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
