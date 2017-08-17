---
title: Angular docs-入门
date: 2017-06-09
writing-time: 2017-08-17
categories: programming
tags: angular node Angular&nbsp;docs
---

# 入门

## 安装 Angular CLI


```bash
$ sudo npm install -g @angular/cli
```

详细见 http://www.atjiang.com/ubuntu_reinstall/

## 创建新项目

```bash
$ cd worksapce
$ ng new startup  # 创建一个 startup 的项目目录
```

## 开启服务

```bash
$ cd startup
$ ng server --open
```

`ng server` 会开启服务端进程，并监测文件的修改，有修改时自动重构。

`--open` 或 `-o` 选项自动在浏览器中打开 `http://localhost:4200/`。

## 编辑 Angular 组件

CLI 已为我们创建了首个 Angualar 组件，它即为 root component, 名为 `app-root`，定义在 `src/app/app.component.ts` 文件中。

修改组件的 title 属性：

```ts
// file: src/app/app.component.ts
export class AppComponent {
  title = 'Startup App';
}
```

保存后，服务端要自动重构，浏览器端会自动刷新。

在 src/app/app.component.css 中为组件设置样式：

```css
/* file: src/app/app.component.css */
h1 {
  color: #369;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 250%;
}
```

## 项目中的文件

### src 目录

应用代码全部在 src 目录中，即所有的组件、模板、样式、图片等等。该目录以外的所有文件都是用来辅助应用构建的。

```
$ sudo apt-get install tree
$ tree src

src
├── app
│   ├── app.component.css
│   ├── app.component.html
│   ├── app.component.spec.ts
│   ├── app.component.ts
│   └── app.module.ts
├── assets
├── environments
│   ├── environment.prod.ts
│   └── environment.ts
├── favicon.ico
├── index.html
├── main.ts
├── polyfills.ts
├── styles.css
├── test.ts
├── tsconfig.app.json
├── tsconfig.spec.json
└── typings.d.ts

3 directories, 16 files
```


文件 | 目的
-----|
`app/app.component.{ts,html,css,spec.ts}` | 定义 `AppComponent` 及其 HTML 模板，CSS，单元测试。这是根组件。
`app/app.module.ts` | 定义 `AppModule`，即根模块 root module，用来告诉 Angular 如何组装应用。里面会声明所有用到的组件。
`assets/*` | 资源文件
`environments/*` | 里面的每个文件对应一种环境配置，如开发环境、生产环境等。
`favicon.ico` | 网站收藏夹图标
`index.html` | 应用的主 HTML 页，CLI 在构建时会自动更新里面的 js 和 css 文件，故一般无需手动修改
`main.ts` | 应用的主入口点。调用 [JIT compiler](https://angular.io/guide/glossary#jit) 进行编译，通过应用的根模块 `AppModule` 启动，最后在浏览器中运行。要使用 [AOT compiler](https://angular.io/guide/glossary#ahead-of-time-aot-compilation) 编译，只需将 `--aot` 传给 `ng build` 或 `ng serve` 即可。
`polyfills.ts` | 规整化所有浏览器的标准支持度。
`styles.css` | 放置全局样式。组件一般在本地存储样式。
`test.ts` | 单元测试的主入口。
`tsconfig.{app|spec}.json` | TypeScript 编译器的配置文件，`tsconfig.app.json` 针对 Angular 应用，`tsconfig.spec.json` 针对单元测试。


### 根目录

```
startup
├── e2e
│   ├── app.e2e-spec.ts
│   ├── app.po.ts
│   └── tsconfig.e2e.json
├── node_modules/...
├── src/...
├── .angular-cli.json
├── .editorconfig
├── karma.conf.js
├── package.json
├── protractor.conf.js
├── README.md
├── tsconfig.json
└── tslint.json
```

文件 | 目的
-----|
`e2e` | 里面都是 end-to-end tests。e2e 测试程序实际也是一个独立的应用，有自己的编译器配置信息 `tsconfig.e2e.json`，只不过它恰好是用来测试我们的应用的。因此不放在 `src` 中。
`node_modules/` | `Node.js` 将 `package.json` 中列出的第三方模块全部安装在这里。
`.angular-cli.json` | Angular CLI 配置文件，除了设置默认值外，还能设置构建时包含进哪些文件。
`.editorconfig` | 通用的编辑器配置文件。VIM 等多数编辑器都支持。
`karma.conf.js` | 使用 [Karma test runner](https://karma-runner.github.io/) 时的单元测试配置文件，当运行 `ng test` 时使用。
`package.json` | npm 依赖包列表，也可在里面添加自定义脚本。
`protractor.conf.js` | 使用 [Protractor](http://www.protractortest.org/) 时的 e2e 测试配置文件，当运行 `ng e2e` 时使用。
`tsconfig.json` | 使用 IDE 时所需的 TypeScript 编译器配置文件，IDE 可基于它提示帮助。
`tslint.json` | [TSLint](https://palantir.github.io/tslint/) 和 [Codelyzer](http://codelyzer.com/) 的 Linting 配置文件。


## 参考

+ https://angular.io/guide/quickstart
+ [对应的 jupyter notebook](https://github.com/haiiiiiyun/angular-docs-notebook/blob/master/quickstart.ipynb)
