---
title: ExtJS 应用的构建和部署
date: 2017-04-14
writing-time: 2017-04-13 08:47--2017-04-14 10:25
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript 《Ext&nbsp;JS&nbsp;Application&nbsp;Development&nbsp;Blueprints》 
---

# 概述

自 Ext JS 4 开始，可以使用 Sencha Cmd 来编译应用。编译过程包括提取所需的 JS 文件和必需的资源文件，对文件进行压缩、混淆和优化。


# 文件目录结构

+ /overrides: 覆盖 Ext JS 框架中的对应功能，例如要覆盖 Ext.data.proxy.Proxy 的功能，则在该目录下的相应目录结构下创建 Ext/data/proxy/Proxy.js 来代替。另一个用法是为 Ext JS 打补丁。重载类放在 `overrides/` 下，扩展类放在 `app` 下。
+ /.sencha: 该目录包含许多 Sencha Cmd 所需的配置和构建过程有关的文件。
+ bootstrap.js, bootstrap.json, bootstrap.css: Ext 基于 `requires` 功能创建了一个强大的依赖管理系统。这些 bootstrap 文件中包含了运行应用所需的最少量 CSS 和 JS 文件信息。
+ /packages: 类似于 Node.js npm 的 packages，Sencha Cmd 也有 packages 概念。通过使用 packages 中的 bundle (包含 CSS，图片及其它资源）实现功能重用。
+ /resources, SASS: 资源文件。
+ index.html: 应用的根文件。编译时 bootstrap.js 将所需的依赖文件信息插入到文件中的 `<script id="microloader" type="text/javascript" src="bootstrap.js"></script>` 位置。
+ /build, build.xml: /build 目录放置构建的结果文件。build.xml 文件包含一个小型的 Ant 初始化脚本，它将加载位于 `.sencha/app/build-impl.xml` 文件中的任务 (task)。
+ app.js: 应用的 JS 主入口。一般推荐不修改该文件，而修改 /app/Application.js 文。
+ app.json: 包含与 Sencha Cmd 及启动有关的配置信息， Sencha Cmd 首先会处理该文件。


## app.json

```javascript
// 使用自定义主题
"theme": "my-custom-theme",

//包含入图表功能
"requires": [
    "charts"
],

// 自动生成的应用  ID 值
"id": "7833ee81-4d14-47e6-8293-0cb8120281ab",

// 支持多种语言
"locales": ["zh_CN", "en"]
```

# Sencha Cmd

Sencha Cmd 整合了多种第三方工具/功能。

+ PhantomJS: 从而无需通过浏览器界面来处理页面。
+ VCDIFF: 一个用于对比一组文件的工具。
+ Closure Compiler: 用于优化和压缩 JS 代码。
+ Jetty: 一个简单的 HTTP 服务器。


这些功能又使用可定制的 Apache Ant 来粘合。


**创建应用**

```bash
$ sencha -sdk ~/<path-to-ext-sdk> generate app MyApp ./my-app
```

**创建视图**

```bash
$ sencha generate view main.Main
```

会在 `app/view/main/` 目录下创建 Main.js (View), MainModel.js (ViewModel)，MainController.js (ViewController) 3 个文件。


**创建工作台实现多个应用共享 ext 库文件**

```bash
$ sencha generate workspace ./my-workspace
```

该命令只是简单地在工作台目录下创建一些配置文件，但当在当前工作台下创建应用时，这些应用的 ext 库文件会放在工作台目录下，而非应用目录下。

```bash
$ sencha -sdk <path-to-sdk>/ext generate app MyApp ./my-workspace/my-app
```

**创建其它组件**

```bash
# 创建 controller:
$ sencha generate controller MyController

# 创建 Model:
$ sencha generate model MyModel fullName:string,age:int
```


**构建应用**

```bash
$ path_of_app\sencha app build  # 构建 APP
$ path_of_app\sencha app build classic # 构建桌面版本
```

构造的所有文件都在 path_of_app/build/production/ 下，可以看到，serverside 目录及里面的 JSON 文件没有包含进 production 目录。


# 构建过程

Sencha Cmd 支持环境的概念，不同的环境（如开发环境、生产环境）定义了不同的变量，这些变量会被 Ant 使用，并传入构建过程。

要查看默认的构建变量，运行： 

```bash
$ sencha ant .props

[INF] [echoproperties] app.output.js=app.js
[INF] [echoproperties] app.output.js.compress=false
[INF] [echoproperties] app.output.js.enable=true
[INF] [echoproperties] app.output.js.optimize=false
```


## 代码压缩

构建过程默认使用 [YUI compressor](http://yui.github.io/yuicompressor/) 来压缩 JS 代码。

`.sencha` 目录下有很多文件，可以设置各种构建中使用到的属性值。例如：

+ production.defaults.properties: 该文件中包含有用于生产环境版本构建的默认属性/变量。
+ production.properties: 该文件中包含的属性/变量值将覆盖 production.defaults.properties 中的同名属性/变量。


production.defaults.properties 文件的内容如下：

```ini
# Comments ......
# more comments......
build.options.logger=no
build.options.debug=false
# enable the full class system optimizer
app.output.js.optimize=true
build.optimize=${build.optimize.enable}
enable.cache.manifest=true
enable.resource.compression=true
build.embedded.microloader.compressor=-closure
```

要修改 JS 压缩器，可在 production.properties 文件中设置：

```ini
# 使用 closure 作为 JS 压缩器
build.embedded.microloader.compressor=-closure 
build.compression.yui=0
build.compression.closure=1
build.compression=-closure
```


## 定制 build.xml 文件

Ant 是一个基于 XML 的构建系统。Ant 的一个重要概念是 **targets**，该术语用来描述一组任务。

> "A target is a container of tasks that cooperate to reach a desired state during the build process."


Sencha Cmd 中已经预先定义了一些 target，可直接加入到构建过程中，build.xml 文件中包含了加入这些 target 的位置。


### 在建构过程前使用 JSHint 来确保 JS 代码质量

[JSHint](https://github.com/philmander/ant-jshint) 是一个 Ant 任务，用前要下载 [Java JAR](http://git.io/VSZvRQ)。

在 `</project>` 前加入：

```xml
<!-- Expose the new task using the ant-jshint jar file -->
<taskdef name="jshint" classname="com.philmander.jshint.JsHintAntTask"
    classpath="${basedir}/ant-jshint-0.3.6-SNAPSHOT-deps.jar" />
<!-- Hook into the before-init target -->
<target name="-before-init">
    <!-- JSHint is now fully exposed via XML -->
    <!-- 注意要告诉 jshint Ext 这个全局变量。-->
    <jshint dir="${basedir}/app" includes="**/*.js" globals="Ext:true" options="strict=false">
        <!-- Output a report to a file called jshint.out -->
        <report type="plain" destFile="${basedir}/jshint.out" />
    </jshint>
</target>
```

现在使用 `sencha app build` 构建时，如果代码未通过 JSHint 检验，会将失败日志输出到 jshint.out，并停止构建过程。


### 添加复制文件任务

```xml
<target name="-after-build" depends="init">
    <copy todir="${build.out.base.path}/serverside" overwrite="false">
        <fileset dir="${app.dir}/serverside" includes="**/*"/>
    </copy>
</target>
```


上面添加的任务功能为：当构建过程结束后，如果 `Init` 过程没有出错，则将 `${app.dir}/serverside` 目录复制到 `${build.out.base.path}/serverside` 目录。

```bash
$ sencha app build classic -c # -c 表示先 clear build/production
```

## 版本数管理

### 创建版本数字

```xml
<propertyfile file="app.properties">
    <entry key="build.number" type="int" operation="+" value="1"/>
</propertyfile>
```

propertyfile 任务指定文件 app.properties 中有一条叫 build.number 的记录，每次运行该任务时都会递增该条记录的值。


### 替换结果 JS 文件中的 {VERSION}

```xml
<property file="app.properties"/>
<replace file="${build.classes.file}" token="{VERSION}" value="${build.number}"/>
```

该任务从 app.properties 文件中的 build.number 记录读取版本数字，用来替换结果 JS 文件中的 `{VERSION}` 字符串。

将以上两个任务合并到 `after-page` 任务挂钩中，从而在创建了结果 JS 文件后执行：

```xml
<?xml version="1.0" encoding="utf-8"?>
    <project name="MyApp" default=".help">
    <import file="${basedir}/.sencha/app/build-impl.xml"/>
    <target name="-after-page">
        <propertyfile file="app.properties">
            <entry key="build.number" type="int" operation="+" value="1"/>
        </propertyfile>

        <property file="app.properties"/>
        <replace file="${build.classes.file}" token="{VERSION}" value="${build.number}"/>
    </target>
</project>
```

该任务不会修改源文件。

## 部署

当构建过程完成后，使用 `after-build` 任务来完成部署过程。

```xml
<target name="-after-build">
    <input message="Please enter SFTP username:" addproperty="scp.user" />
    <input message="Please enter SFTP password:" addproperty="scp.password" />
    <scp remoteTodir="${scp.user}@sftp.mysite.com:/path/to/myapp/dir"
        password="${scp.password}">
        <fileset dir="build/production"/>
    </scp>
</target>
```


# 参考 

+ [Chapter 14: Finishing the Application](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
+ [Chapter 3: Application Structure](https://www.amazon.com/Ext-JS-Application-Development-Blueprints/dp/1784395307/)
+ [Chapter 4: Sencha Cmd](https://www.amazon.com/Ext-JS-Application-Development-Blueprints/dp/1784395307/)
