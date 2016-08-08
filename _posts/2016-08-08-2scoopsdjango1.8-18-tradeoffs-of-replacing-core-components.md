---
title: 权衡替换 Django 核心组件
date: 2016-08-08
writing-time: 2016-08-08 17:03--17:33
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

尽量不要替换 Django 核心组件，除非你了解：

+ 可能无法使用一些或全部的第三方应用包
+ 不能使用 Django admin 应用
+ 你已花费大量时间使用核心组件来创建你的应用，但是发现这些核心组件是主要问题所有
+ 你已对代码进行了分析，找出了主要的问题所在
+ 你已尝试了其它所有的可能方案，包括缓存等
+ 你的项目是一个实时的，有大量用户的网站。即不是在没有根据的情况下进行预优化
+ 你已评估了 SOA 模式，发现不适合
+ 你了解 Django 升级后，代码的相应修改会很难

# 非关系型数据库和关系型数据库

使用关系型数据库来持久化数据的项目也会使用一些非关系型数据库，如使用 Memcached 来缓存，或使用 Redis 实现队列。但是用非关系型数据库完全取代关系型数据库需要考虑清楚。

## 不是所有的非关系型数据库都兼容 ACID

ACID 含义：

**Atomicity** 原子性指一个事务要么全部成功要么全部失败。
**Consistency** 一致性指所有事务会使数据保存在一个有效状态。
**Isolation** 独立性指并行处理的数据不会在事务间有关联或发生冲突。
**Durability** 持续性指一旦事务提交，它的结果即便在数据库服务器关闭后还会保存完好。

没有这些特性，数据都有破坏的可能。

## 不要使用非关系型数据库处理关系型任务
## 不随大流，要自己做研究评估


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
