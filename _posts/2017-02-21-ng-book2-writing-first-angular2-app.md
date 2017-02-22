---
title: 编写首个 Angular2 应用
date: 2017-02-21
writing-time: 2017-02-21 22:29
categories: Programming
tags: Programming 《ng-book2-r49》 Angular2 Google JavaScript TypeScript Node ng2
---

# 环境设置

TypeScript 是 JavaScript ES6 的超集，它添加了对类型的支持。

Angular 2(简称 ng2) 虽然提供了 ES5 (普通 JavaScript) API，但由于其本身是用 TypeScript 编写的，因此 ng2 应用最好也应该用 TypeScript 编写。

TypeScript 依赖 Node，故要先 [安装 Node](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions)。

## 安装 angular-cli

这个命令行可以用来管理 ng 项目，如创建项目，创建控制器等常用任务。 安装 angular-cli:

```bash
$ sudo npm install -g angular-cli@1.0.0-beta.18
```

安装好后会有 ng 命令，运行该命令后会有一大串输出：

```bash
$ ng # 安装好后会有该命令
Could not start watchman; falling back to NodeWatcher for file system events.
3 Visit http://ember-cli.com/user-guide/#watchman for more info.
4 Usage: ng <command (Default: help)>
...
```

在 OSX 或 Linux 运行一般会有 'Could not start watchman ...' 的输出，这是因为我们还没有安装 [watchman](https://ember-cli.com/user-guide/#watchman)，该程序能帮助 angular-cli 监测项目中的文件修改情况。如果在 OSX 上，最好通过 Homebrew 安装它：

```bash
$ brew install watchman
```

# 一个示例项目

创建项目：

```bash
$ ng new angular2_hello_world

1 installing ng2
2 create .editorconfig
3 create README.md
4 create src/app/app.component.css
5 create src/app/app.component.html
...
33 Successfully initialized git.
34  Installing packages for tooling via npm
```

等待一段时间后，会出现 'Installing packages for tooling via npm'，说明已经创建项目成功。 ng 为该项目创建了很多的默认文件。

通过 tree 命令可以看到项目的文件和目录结构：

```bash
$ tree -F -L 1
.
├── angular-cli.json    # angular-cli 配置文件
├── e2e/                # end to end 测试
├── karma.conf.js       # 单元测试配置文件
├── node_modules/       # 安装的依赖包
├── package.json        # npm 配置
├── protractor.conf.js  # e2e 测试的配置信息
├── README.md           # README
├── src/                # 应用的源代码
└── tslint.json         # linter 配置文件

3 directories, 6 files
```

目前，只需关注源代码目录：

```bash
$ cd src
$ tree -F
.
├── app/
│   ├── app.component.css
│   ├── app.component.html
│   ├── app.component.spec.ts
│   ├── app.component.ts
│   ├── app.module.ts
│   └── index.ts
├── assets/
├── environments/
│   ├── environment.prod.ts
│   └── environment.ts
├── favicon.ico
├── index.html
├── main.ts
├── polyfills.ts
├── styles.css
├── test.ts
├── tsconfig.json
└── typings.d.ts

4 directories, 20 files
```

续...












# 参考 

+ [Writing your first Angular 2 Web Application](https://www.ng-book.com/2/)
