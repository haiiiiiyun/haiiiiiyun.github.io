---
title: webpack 实践 10： 环境变量
date: 2017-12-16
writing-time: 2017-12-12
categories: programming
tags: JS javascript webpack webpack2 yarn webpack&guides
---

`webpack` 命令可以通过 `--env` 加入多个环境变量值，例如 `webpack --env.production --env.NODE_ENV=local` 等，这些环境变量值可以在 `webpack.config.js` 中引用。

传入的环境变量没有用 `=` 给定值时，默认值为 `true`，例如 `webpack --env.production`。

webpack 的配置文件中的 `module.exports` 通过是指向一个 `{}` 对象，但是要引用环境变量 `env` 时，需要将 `module.exports` 指向一个函数，例如：

```javascript
//webpack.config.js
module.exports = env => {
  // Use env.<YOUR VARIABLE> here:
  console.log('NODE_ENV: ', env.NODE_ENV) // 'local'
  console.log('Production: ', env.production) // true

  return {
    entry: './src/index.js',
    output: {
      filename: 'bundle.js',
      path: path.resolve(__dirname, 'dist')
    }
  }
}
```


# 参考

+ https://webpack.js.org/guides/environment-variables/
+ [测试代码 github 仓库](https://github.com/haiiiiiyun/webpack-practice)
