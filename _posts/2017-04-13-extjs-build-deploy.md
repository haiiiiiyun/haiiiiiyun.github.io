---
title: ExtJS 应用的构建和部署
date: 2017-04-13
writing-time: 2017-04-13 08:47
categories: Programming
tags: Programming 《Learning&nbsp;ExtJS&nbsp;4th&nbsp;Edition》 Sencha ExtJS Javascript
---

# 概述

自 Ext JS 4 开始，可以使用 Sencha CMD 来编译应用。编译过程包括提取所需的 JS 文件和必需的资源文件，对文件进行压缩、混淆和优化。


+ app.json: 包含应用的配置信息， Sencha CMD 首先会处理该文件。
+ build.xml: 该文件包含一个小型的 Ant 初始化脚本，它将加载位于 `.sencha/app/build-impl.xml` 文件中的任务 (task)。
+ sencha: 该目录包含许多与构建过程有关的文件。


# app.json

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

# Sencha CMD

```bash
$ path_of_app\sencha app build  # 构建 APP
$ path_of_app\sencha app build classic # 构建桌面版本
```

构造的所有文件都在 path_of_app/build/production/ 下，可以看到，serverside 目录及里面的 JSON 文件没有包含进 production 目录。


# 定制 build.xml 文件

在 `</project>` 前加入：

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

# 代码压缩

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

再要修改 JS 压缩器，可在 production.properties 文件中设置：

```ini
# 使用 closure 作为 JS 压缩器
build.embedded.microloader.compressor=-closure 
build.compression.yui=0
build.compression.closure=1
build.compression=-closure
```

# 部署

将 path_of_app\build\production 下的文件进行部署。



# 参考 

+ [Chapter14: Finishing the Application](https://www.amazon.com/Learning-ExtJS-Fourth-Carlos-Mendez/dp/1784394386/)
