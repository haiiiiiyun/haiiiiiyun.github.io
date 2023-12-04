---
title: Sencha Cmd 命令及 ExtJs 应用的调试工具
date: 2017-02-07
writing-time: 2017-02-07 09:24--09:56
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---


# Sencha Cmd

## 命令格式

`sencha [category] [command] [option...] [arguments...]`

## 帮助信息

`sencha help` 会列出所有的分类，顶层命令和选项等。要想了解更细的帮助信息，可以在 `sencha help` 后跟 `category`, `command` 等，如 `sencha help app`, `sencha help app clean`。

## 升级 Sencha Cmd

`sencha upgrade --check` 只检查，不带 `--check` 将进行实际升级操作。

## 创建应用

Sencha Cmd 支持 Ext JS 4.1.1a, Sencha Touch 2.1 及以上版本。可以在机器上使用多个版本的 SDK。

使用指定版本的 SDK 来创建应用：

```bash
$ sencha -sdk /path/to/sdk generate app [--modern/classic] MyApp /path/to/myapp
```

## 构建应用

`sencha app build` 将构建 HTML, JS, SASS 等。

在 Sencha Cmd 6 和 Ext JS 6 中，可以指定构建相应类型的应用：

```bash
$ sencha app build modern
$ sencha app build classic
```

相应的构建配置信息都在 `app.json` 中，可以进行相应的修改。

## 开启应用

`sencha app watch` 将重新构建并开启应用，同时它还监控文件的修改，以便进行刷新。

在 Sencha Cmd 6 和 Ext JS 6 中，可以指定运行相应类型的应用：

```bash
$ sencha app watch modern
$ sencha app watch classic
```

## 代码的生成

能生成 view, controller, model 等代码：

```bash
$ sencha generate view MyApp.MyView
$ sencha generate model MyModel id:int,fname,lname
$ sencha generate controller MyController
```

在创建 Model 时，如果某项没有指定类型，默认将采用 `string` 类型。

## 应用升级

```bash
$ sencha app upgrade [path-to-new-framework]
```


# 调试 Ext JS 应用

## Firefox 中的 Illumination（注：是收费插件）

Illumination 插件依赖 Firebug。它的功能有：

+ 能识别 Ext JS 组件
+ 鼠标放在 Illumination 窗口中的对象上，会高亮页面中的相应组件


## Chrome 中的 App Inspector 插件

该插件由 Sencha 开发，它提供了 Illumination 的所有功能。

它的功能有：

+ component inspector
+ store inspector
+ layout profile


## 在线执行环境 Sencha Fiddle

地址 [fiddle.sencha.com](https://fiddle.sencha.com/)，可以在上面直接编写和运行 Ext JS 代码。


参考： 

+ [Exploring Sencha Cmd commands](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
