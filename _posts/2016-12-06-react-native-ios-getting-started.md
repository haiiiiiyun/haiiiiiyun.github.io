---
title: React Native IOS 入门
date: 2016-12-06
writing-time: 2016-12-06 23:00
categories: programming ios
tags: Programming React&nbsp;Native
---

# 系统环境

+ macOS Sierra v 10.12.1

# 安装依赖

通过 `brew install node` 方式当前在本系统上安装失败，转至 [https://nodejs.org/](https://nodejs.org/) 下载最新版本 v6.9.1 LTS 手动安装。

安装 watchman:

```
$ brew install node
```

安装 React Native CLI:

```
$ sudo npm install -g react-native-cli
```

测试是否安装成功：

```
$ cd workspace
$ react-native init AwesomeProject
$ cd AwesomeProject
$ react-native run-ios
```

如果一切顺利，会在 iOS 模拟器中开启一个新的 APP。如果出现类似 **ould not parse the simulator list output** 等错误，可以是 XCode 没有更新引起的。

修改应用：

+ 打开 **index.ios.js** 文件，对其进行修改。
+ 在 iOS 模拟器中，按 Command + R 重新加载 App，可以看到修改的结果。

参考：[https://facebook.github.io/react-native/docs/getting-started.html](https://facebook.github.io/react-native/docs/getting-started.html)
