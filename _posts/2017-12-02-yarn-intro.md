---
title: Yarn 入门
date: 2017-12-02
writing-time: 2017-12-02
categories: programming
tags: yarn npm node nodejs webpack
---

# 简介

Yarn 是一个 JS 包依赖管理器。

特点：

+ 快速。每个包都会被缓存，故只会下载一次。并行操作提速安装过程。
+ 安全。使用检验和对每个已安装的包进行完全性检验，之后才会运行。
+ 可靠。相同的依赖，无论安装次序，在所有的机器上都按同样方式安装。


# 安装

在 Ubuntu 上：

```bash
$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

$ sudo apt-get update && sudo apt-get install yarn
```

如果安装失败，可以先尝试删除 cmdtest: `sudo apt remove cmdtest`。

安装好后：

```bash
$ yarn --version
```

# 使用

## 创建一个项目

```bash
$ yarn init
```

## 添加依赖

```bash
$ yarn add package
$ yarn add package@version
$ yarn add package@tag
```

## 将依赖添加到不同的依赖目录

例如添加到 `devDependencies`, `peerDependencies`, `optionalDependencies` 等。

```bash
$ yarn add package --dev
$ yarn add package --peer
$ yarn add package --optional
```

## 升级依赖包

```bash
$ yarn upgrade package
$ yarn upgrade package@version
$ yarn upgrade package@tag
```

## 删除依赖

```bash
$ yarn remove package
```

## 安装项目中的所有依赖

```bash
$ yarn  # or
$ yarn install
```

# 包配置文件

每个包都有一个配置文件 `package.json`，Yarn 据该文件识别每个包，并进行处理。

Yarn 会在项目的根目录下创建一个 `yarn.lock` 文件，用于管理依赖关联，我们无需修改该文件，并需要将该文件包含进代码库中。


## package.json

`name` 和 `version` 项组合成一个唯一的标识。

开发和生产环境下都需要的依赖放在 `dependencies` 下，如：

```json
{
  "dependencies": {
    "package-1": "^3.1.4"
  }
}
```

可以指定精确的版本，最小版本 `>=`，一个版本区间 `>= ... <`。

开发环境下的依赖放在 `devDependencies` 中：

```json
{
  "devDependencies": {
    "package-2": "^0.4.2"
  }
}
```

`peerDependencies` 可用来声明你的包与其它包的兼容性：

```json
{
  "peerDependencies": {
    "package-3": "^2.7.18"
  }
}
```

`optionalDependencies` 中的包若没有找到，安装过程也会继续：

```json
{
  "optionalDependencies": {
    "package-5": "^1.6.1"
  }
}
```

`bundledDependencies` 中的包，当你的包发布时，会一起打包进来：

```json
{
  "bundledDependencies": [
    "package-4"
  ]
}
```


# Yarn 工作流

## 创建 Yarn 工程

一般在项目的根目录下运行 `yarn init` 命令，回答一些项目相关的问题，之后创建一个 `package.json` 文件，用来保存项目及其依赖信息。

## 管理依赖

使用 Yarn 的 add, upgrade, remove 等命令来管理依赖，这些命令会自动更新 `package.json` 及 `yarn.lock` 文件的内容。

## 安装依赖包

使用 `yarn install` 来安装项目的全部依赖包，依赖包信息从 `package.json` 中提取，并保存到 `yarn.lock` 文件中。

安装方式：

1. 安装全部依赖： `yarn` 或 `yarn install`
1. 每个包只安装一个版本： `yarn install --flat`
1. 强制重装下载安装全部包： `yarn install --force`
1. 只安装生产环境下的依赖： `yarn install --production`


## 版本控制

必须将以下 2 个文件加入代码库中。

+ `package.json`： 包含当前的所有依赖信息。
+ `yarn.lock`： 保存了每个已安装的依赖包的信息。


# 从 npm 迁移到 Yarn

Yarn 和 Npm 基本上是兼容的，Yarn 可以使用 npm 创建的 `package.json`，可以安装 npm registry 中的任何包。一般只需运行 `yarn`，将生成的 `yarn.lock` 文件加入代码库即完成迁移。见 https://yarnpkg.com/en/docs/migrating-from-npm。


# 参考

+ https://yarnpkg.com/
+ https://yarnpkg.com/en/docs/install
+ https://yarnpkg.com/en/docs/yarn-workflow
+ https://yarnpkg.com/en/docs/migrating-from-npm
+ https://yarnpkg.com/en/docs/configuration
