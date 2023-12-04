---
title: 在 Ubuntu 上搭建 thingsboard 开发环境
date: 2019-11-20
writing-time: 2019-11-20
categories: java thingsboard iot
tags: java thingsboard iot
---

# 1. 工具

# 1.1 Java

Thingsboard 2.4 需要 Java 8.

```bash
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```

# 1.2 多个 Java 版本间的切换

`apt-get` 不会覆盖系统上现有的 Java 版本。

要在已安装的多个 Java 版本间进行切换，使用 Debian 的 [alternatives system](https://wiki.debian.org/DebianAlternatives) 系统:

```bash
# List all versions
update-java-alternatives --list

# Set java version as default (needs root permissions):
sudo update-java-alternatives --set /path/to/java/version

java -version
```

# 1.3 Maven

Thingsboard 2.4 需要 Maven 3.1.0+.

```bash
sudo apt-get install maven

mvn -version
```

# 1.4 NodeJS

见 http://www.atjiang.com/javascript-es2015-basic/.

```bash
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install -y nodejs
npm -v
```

# 2. 构建

# 2.1 安装 npm 依赖包

```bash
sudo npm install -g cross-env
sudo npm install -g webpack
```

# 2.2 构建

在将项目导入到 IDE 前，先执行 `mvn clean install` 以创建 IDE 编译所需的 protobuf 文件。

```bash
git clone git@github.com:thingsboard/thingsboard.git

# checkout latest release branch
git checkout release-2.4

mvn clean install -DskipTests
```

再以 `Maven 项目`的方式导入 IDEA 中。


# 3. 数据库

2.4 版本默认使用 postgresql 数据库，创建 thingsboard 数据库:

```bash
psql -U postgres -d postgres -h 127.0.0.1 -W
CREATE DATABASE thingsboard;
\q
```

创建表并导入测试数据:

```bash
cd application/target/bin/install
chmod +x install_dev_db.sh
sudo ./install_dev_db.sh
```

# 4. 运行

以热部署方式 (hot redploy mode) 运行 UI 容器，完成后可通过 127.0.0.1:3000 访问:

```bash
cd ui
mvn clean install -P npm-start
```

运行服务端容器，完成后可通过 127.0.0.1:8080 访问：

```bash
java -jar application/target/thingsboard-2.4.1-boot.jar
```


在 IDE 中，可通过执行 `org.thingsboard.server.ThingsboardServerApplication` 类的主方法来启动服务端窗口。


测试用户: tenant@thingsboard.org
密码: tenant

其它的测试账号、测试设备 Tokens 见 [Demo Account](https://thingsboard.io/docs/samples/demo-account/)。

# 5. 错误

1. 在执行 `mvn clean install` 时出错: `Failed to execute goal org.fortasoft:gradle-maven-plugin:1.0.8:invoke (default) on project http: org.gradle.tooling.BuildException: Could not execute build using Gradle distribution 'https://services.gradle.org/distributions/gradle-2.13-bin.zip'. -> [Help 1]`。

有可能是因为设置了 gradle 代理，而代理不能访问导致的，尝试在 `~/.gradle/grade.properties` 文件中注释掉代理信息，关闭所有的 java 进程并重新运行。

```
## For more details on how to configure your build environment visit
# http://www.gradle.org/docs/current/userguide/build_environment.html
#
# Specifies the JVM arguments used for the daemon process.
# The setting is particularly useful for tweaking memory settings.
# Default value: -Xmx1024m -XX:MaxPermSize=256m
# org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8
#
# When configured, Gradle will run in incubating parallel mode.
# This option should only be used with decoupled projects. More details, visit
# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects
# org.gradle.parallel=true
#Thu May 31 15:01:45 CST 2018
#systemProp.https.nonProxyHosts=10.0.2.*
#systemProp.https.proxyPort=1090
#systemProp.http.proxyHost=127.0.0.1
#systemProp.http.nonProxyHosts=10.0.2.*
#org.gradle.daemon=true
#systemProp.https.proxyHost=127.0.0.1
#systemProp.http.proxyPort=1090
```

2. 在执行 `java -jar application/target/thingsboard-2.4.1-boot.jar` 时出错： ` ERROR 17201 --- [           main] o.a.velocity.runtime.log.Log4JLogChute   : Problem instantiating the template loader: org.thingsboard.server.conf
ig.ThingsboardMessageConfiguration$SpringResourceLoader.
Look at your properties file and make sure the
name of the template loader is correct.

java.lang.IllegalAccessException: Class org.apache.velocity.util.ClassUtils can not access a member of class org.thingsboard.server.config.ThingsboardMessageConfiguration$
SpringResourceLoader with modifiers ""
`。

见 [issue 1625](https://github.com/thingsboard/thingsboard/issues/1625)


# Resources
+ https://thingsboard.io/docs/user-guide/contribution/how-to-contribute/
+ https://thingsboard.io/docs/user-guide/install/ubuntu/
+ https://askubuntu.com/questions/740757/switch-between-multiple-java-versions
