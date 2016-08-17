---
title: Django 部署：PaaS
date: 2016-08-16
writing-time: 2016-08-17 08:41--09:32
categories: programming
tags: Database Ubuntu Postgresql programming
---

永远不要将你的项目绑死到一个 PaaS 上，不要使用 PaaS 的很个性化的功能。

支持 Django 的 PaaS：

+ [Heroku](http://heroku.com)： 在 Python 社区用得较多，有很好的文档和插件系统。必读资料： http://www.theherokuhackersguide.com/ 

+ [PythonAnywhere](https://www.pythonanywhere.com) : 对新手来说易于使用。

# 评估一个 PaaS

## 是否符合相关法律规定

## 价格

一般会是阶梯价格，先预估随着网站的扩展，后续的价格变动。

## 在线时间

一般这些服务提供商都是租用的 AWS 和 Rackspace 等的服务器。

## 员工情况

是否有足够的员工来提供 24x7 服务，在评估时可发一条 ticket 去测试服务水平和响应速度。

## 是否容易扩展（升配和降配）

## 文档

## 性能下降

一些项目在运行一段时间后性能会开始下降，当出现这种情况时的工作流程：

1. 检查项目的最近代码修改提交历史，确定是否是修改或 BUG 引起性能下降
2. 查找项目中未发现性能瓶颈
3. 针对该问题向 PaaS 寻求支持
4. 该项目所使用的低层服务器硬件可能有问题了，比如过旧，那么开启一个新的项目实例，看是否解决问题
5. 向 PaaS 寻求更多支持
6. 考虑在其它 PaaS 或者自己的服务器上测试，看问题是否存在。

## 地理位置

## 公司的稳定性

PaaS 很费钱，如果一个 PaaS 公司在 beta 版或初期促销后还不考虑利润，那么这个公司可能不会长久。


# 部署到 PaaS 的最佳实践

## 开发环境和生产环境要尽可能接近

## 自动化所有事情

+ Makefile: 对小项目很有用
+ Invoke: 是 Fabric 的后续版本

## 维护一个 Staging 实例

## 通过备份和回滚为灾难预案

+ 从备份中还原数据库和用户上传的文件
+ 回滚到前的代码版本

## 备份外部依赖数据

如数据库和用户上传的文件，数据可以保存到 Dropdox, Crashplan, Amazon S3 和 Rackspace Cloud 等上。

 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
