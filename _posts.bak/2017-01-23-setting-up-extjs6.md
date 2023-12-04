---
title: 设置 Ext JS 6 开发环境
date: 2017-01-23
writing-time: 2017-01-23 09:20--10:26
categories: Programming
tags: Programming 《Ext&nbsp;JS&nbsp;6&nbsp;By&nbsp;Example》 Sencha ExtJS Javascript
---

# 安装 JRE

Sencha Cmd 依赖 JRE。

到 [Oracle 网站上](http://www.oracle.com/technetwork/cn/java/javase/downloads/jdk8-downloads-2133151-zhs.html) 下载相应版本的 JRE 或 JDK。

以在 Ubuntu 16.04 上为例，先将下载的包解压到 `~/opt/`，生成如 `~/opt/jdk1.8.0_111` 目录。

在 `~/.bashrc` 中添加以下行，用来设置 JAVA 环境变量：

```bash
export JAVA_HOME=~/opt/jdk1.8.0_111
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
```

使用 `source ~/.bashrc` 命令使刚才的配置生效。


```bash
$ source ~/.bashrc
$ java -version
java version "1.8.0_111"
Java(TM) SE Runtime Environment (build 1.8.0_111-b14)
Java HotSpot(TM) Server VM (build 25.111-b14, mixed mode)
```

# 安装 Sencha Cmd

到 [Sencha 网站](https://www.sencha.com/products/extjs/cmd-download/) 上下载相应的版本。

以在 Ubuntu 16.04 上为例，先将下载的包解压，再运行安装脚本：

```bash
$ bash ./SenchaCmd-6.2.1.29-linux-i386.sh
```

根据安装向导将 Sencha Cmd 安装到 `~/opt/Sencha/Cmd/6.2.1.29`。

验证是否安装成功：

```bash
$ sencha which
Sencha Cmd v6.2.1.29
/home/hy/opt/Sencha/Cmd/6.2.1.29/
```

# 使用 Sencha Cmd 创建 Ext JS 应用

```bash
$ sencha generate app -ext MyApp ./myapp
```

上面的命令将下载并使用最新的 ExtJS 框架，在目录 `./myapp` 中创建一个名为 `MyApp` 的应用。默认会包含 `classic` 和 `modern` 两份代码。可以手动指定只生成一份代码：

```bash
$ sencha generate app -ext -modern MyApp ./myapp
```

如果已经下载了 ExtJS 框架包，不需要 Sencha Cmd 自动下载，可以用 `-sdk` 指定：

```bash
$ sencha -sdk /path/to/sdk generate app MyApp /path/to/myapp
```

测试生成的应用：

```bash
$ cd myapp/
$ sencha app watch

Sencha Cmd v6.2.1.29
[INF] Processing Build Descriptor : classic
[INF] Starting server on port : 1841
[INF] Mapping http://localhost:1841/~cmd to /home/hy/opt/Sencha/Cmd/6.2.1.29...
...
[INF] Writing content to /home/hy/workspace/book_exercises/ExtJS6ByExample/chap1/myapp/classic.json
[INF] Waiting for changes...
```

`sencha app watch` 会启动一个 HTTP 测试服务器，并且监视代码的修改情况。现在可以通过 http://localhost:1841 来访问刚创建的应用了。

应用默认会检测访问的浏览器，桌面浏览器和移动端浏览器分别会使用 `classic` 或 `modern` 工具集。不过要想在桌面上查看 `modern` 应用，只需在 URL 后添加 `profile=modern` 即可，如 http://localhost:1841?profile=modern。


> 参考： 

+ [Setting up Ext JS](https://www.amazon.com/Ext-JS-Example-Anand-Dayalan/dp/178355049X/)
