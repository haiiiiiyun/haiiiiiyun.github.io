---
title: ExtJS 组件和布局--Learning ExtJS(4th)
date: 2017-03-30
writing-time: 2017-03-30 08:35
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 组件生命周期

Ext 中的所有组件都扩展至 `Ext.Component`（另一个名字也叫 `Ext.AbstractComponent`)。


当创建组件时，都会经历一个叫 “组件生命周期” 的过程。基本上，生命周期分 3 个阶段：初始化过程，呈现过程，和销毁过程。

初始化阶段初始化我们的新实例，并将它登记到组件管理器中;然后，呈现阶段将在 DOM 上创建全部所需的结点;最后销毁阶段将从 DOM 上删除结点和侦听器 (listener)。

`Ext.AbstractComponent/Ext.Component` 类引导了这个生命周期过程，每个扩展至该类的组件都将自动参与这个生命周期。


## 初始化阶段

这个阶段的主要目的是基于我们的配置信息创建一个组件实例。它还将我们的组件登记到组件管理器中等其它一些事情。

```
+----------------+       +----------+    +-------------+     +---------------+
| 1.Apply        |       |2.Common  |    | 3.Unique ID |     |4.Instantiate  |
|   Configuration+-----> |  e^ents  +--> |             +---> |  Plugins      |
+----------------+       +----------+    +-------------+     +------+--------+
                                                                    |
                                                                    v

 +--------------+       +------------+     +----------------+ +----------------+
 |8.Initialize  |       |7.Events &  |     |.Registration in| |5.InitComponent |
 |  Plugins     | <-----+  Stateful  | <-+ | Comp.Manager   <-+                |
 +---------+----+       +------------+     +----------------+ +----------------+
           |
 +---------v----------+
 |Render phase starts |
 |                    |
 +--------------------+
```


# 参考 

+ [Chapter3: Components and Layouts](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
