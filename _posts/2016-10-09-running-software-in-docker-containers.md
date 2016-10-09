---
title: 在 Docker 容器中运行应用程序
date: 2016-10-09
writing-time: 2016-10-09 09:23
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 案例说明

运行 3 个容器，共同实现对一个网站的监控。

三个容器的说明:

+ 容器 `web`: 创建自 nginx 映像，使用 80 端口，运行于后台，实现 web 服务。
+ 容器 `mailer`: 该容器中运行一个 mailer 程序，运行于后台，当接收到事件后会向管理员发送邮件。
+ 容器 `agent`: 该容器运行一个 watcher 程序，运行于交互式模式，用于不断地监测 web 服务的运行服务，一旦出现故障会立即向 `mailer` 容器发送消息。

# 创建容器

## 创建并运行 web 容器

```bash
$ docker run --detach --name web nginx:latest
```

命令执行后，docker 会从 Docker Hub 上下载 `nginx:latest` 映像文件，根据该映像文件开启一个容器，并在容器中运行 nginx 程序。

运行后，会输出一行字符串，该字符串为该容器的唯一标识符，类似如 `7cb5d2b9a7eab87f07182b5bf58936c9947890995b1b94f412912fa822a9ecb5`。通常我们可以将该标识符保存到一个变量里，以便于在其它命令中使用。

`--detach` 选项使得该容器在后台运行，也可以用其缩写版本 `-d`。

`--name web` 将当前容器命名为 `web`，以便之后引用。

## 创建并运行 mailer 容器

```bash
$ docker run -d --name mailer dockerinaction/ch2_mailer
```

## 创建并运行一个交互式的容器 agent

一个交互式的程序可以从用户获取输入或将输出显示到终端中。在 Docker 中运行交互式程序需要将你的终端绑定到容器的输入或输出上。

运行一个交互式容器如下:

```bash
$ docker run --interactive --tty \
    --link web:myweb \
    --name web_test \
    busybox:latest /bin/sh
```

`--interactive` 或 `-i` 选项告诉 Docker 为该容器开启标准输入 (stdin)。 `--tty` 或 `-t` 选项告诉 Docker 为该容器分配一个虚拟终端，以便于向容器发送信号。通常这两个选项是一起使用的，合记为 `-it`。

`--link web:web` 选项使得当前容器能用 `myweb` 来引用 容器 web。

最后，`/bin/sh` 是指定在该容器中运行的程序，运行后，可以在 sh 中运行 `wget -O - http://myweb:80/` 来检测容器 web 的运行情况。这里的 `wget` 命令实现向 nginx 服务器发送请求，并将获取的页面内容输出到终端上。

通用 `--tty` 开启的交互式容器，可以使用 `Ctrl-P Q` 来使其转入后台运行。

### 运行 agent 容器

```bash
$ docker run -it \
    --name agent \
    --link web:insideweb \
    --link mailer:insidemailer \
    dockerinaction/ch2_agent
```

该容器会每 1 秒对容器 web 检测一次，并输出类似 `System up.` 等信息。当看到这些信息后，可以用 `Ctrl-P Q` 来使其转入后台运行。


# 容器命令

## docker ps

`docker ps` 会列出每个正在运行的容器的下面信息:

+ 容器 ID
+ 使用的映像文件
+ 在容器中运行的命令
+ 自容器创建后的时间
+ 容器已运行的时间
+ 容器使用的端口号
+ 容器的名称


## 重启容器

```bash
$ docker restart web
$ docker restart mailer
$ docker restart agent
```

## 查看容器的日志

```bash
$ docker logs web
```

由于容器 agent 对容器 web 进行了多次请求，故上面的命令会输出一长串的 `GET / HTTP/1.0" 200`。

容器运行是的每条输出（或错误输出）都会保存到容器的日志文件中，因此，只要容器一直在运行，它的日志文件会不断的变大。由于没有截断的手段，因而最好用 volume 来处理日志数据。

```bash
$ docker logs mailer
```

mailer 的日志会像： `CH2 Example Mailer has started.`

`docker logs` 命令添加 `--follow` 或 `-f` 选项时，会一直保持运行，并持续显示最新的日志。可以用 `Ctrl C` 中断。


## 关闭容器

```bash
$ docker stop web
```

以上命令将中止容器中的 PID #1 程序的运行。

容器 web 中止后，容器 agent 将触发对容器 mailer 的请求，进而可以看到容器 mailer 中相关日志 `Sending email: To: admin@work Message: The service is down!`

# 已解决的问题及 PID 命名空间

PID 命令空间是可用于标识进程的一个数集。Linux 可创建多个 PID 命令空间，每个命名空间中使用的 PID 相互独立，即每个命名空间都各自使用使用 1, 2, 3 等而故不干扰。

Docker 默认为每个容器都会创建一个 PID 命名空间:

```bash
$ docker run -d --name namespaceA \
    busybox:latest /bin/sh -c "sleep 30000"
$ docker run -d --name namespaceB \
    busybox:latest /bin/sh -c "nc -l -p 0.0.0.0:80"
```

运行之后两个容器后，

```bash
$ docker exec namespaceA ps

PID   USER     TIME   COMMAND
    1 root       0:00 /bin/sh -c sleep 30000
    6 root       0:00 sleep 30000
    7 root       0:00 ps


$ docker exec namespaceB ps

PID   USER     TIME   COMMAND
    1 root       0:00 /bin/sh -c nc -l -p 0.0.0.0:80
    5 root       0:00 nc -l -p 0.0.0.0:80
    6 root       0:00 ps
```

可以看到，每个容器中使用的 PID 都是独立的，例如都有 PID #1。

要使容器不创建自己的 PID 命名空间，在运行 `docker create` 或 `docker run` 时要加上 `--pid host` 选项：

```bash
$ docker run --pid host busybox:latest ps
```

以上命令将列出机器上的所有运行中的进程。

## Docker 解决的问题

Docker 基于 Linux namespace, file system roots, virtualized network components 实现的容器隔离性解决了如下的冲突问题:

+ 多个程序想绑定到相同的端口
+ 多个程序想使用相同的临时文件名
+ 各程序想使用全局安装的代码库的不同版本
+ 同个程序的不同进程想使用相同的 PID 文件
+ 多个程序同时修改环境变量


# 消除 metaconflicts：创建一个网站集群

metaconflicts 即容器间的冲突。

继续上面的例子，这次开启多组 web + agent 容器对，然后只开启一个 mailer 容器，所有的 agent 都将事件发送给容器 mailer。

## 灵活的容器标识

当执行 `docker run -d --name webid nginx` 时，生成的容器的名称为 webid，容器的名称不能重复。当没有使用 `--name` 选项时，Docker 会自动为我们创建一个易读的唯一容器名。也可以重命名容器：

```bash
$ docker rename webid webid-old
```

每个容器还有一个 1024 位的十六进制编码的唯一 ID，如 `7cb5d2b9a7eab87f07182b5bf58936c9947890995b1b94f412912fa822a9ecb5`。可以通过这个 ID 对该容器进行引用。如：

```bash
docker stop \
    7cb5d2b9a7eab87f07182b5bf58936c9947890995b1b94f412912fa822a9ecb5 
```

该 ID 值是完全唯一的，即永远不会冲突，若要想在同一台机器上保持唯一性，只需取其前 12 个字符长的字符串即可，因此，上面的命令也可以这样：

```bash
```bash
docker stop \
    7cb5d2b9a7ea
```

容器 ID 值不适合人读，但可用于脚本处理或自动化程序中使用。

### 如果获取容器 ID

当开启一个在后台运行的容器时，容器 ID 会自动输出到终端，因此可以获取。但如果开启的是交互式的容器，就不能获取 ID。这种情况下可以先用 `docker create` 命令先创建一个容器（不立即运行），该命令和 `docker run` 的格式完成一样，同样也会输出容器的 ID。

将 ID 值保存到一个 Shell 变量中：

```bash
CID=$(docker create nginx:latest)
echo $CID
```

这种方式获取的 ID 只能在一个脚本或程序中使用，不能在多个程序间共享。如果要在多个程序间共享该容器 ID 值，可以将值保存在 container ID(CID) 文件中。`docker run` 和 `docker create` 命令都可以用 `--cidfile` 选项指定 CID 文件的位置，如：

```bash
$ docker create --cidfile /tmp/web.cid ngix
```

然后用 `cat /tmp/web.cid` 来获取该值。用这种方式时， CID 文件可能会冲突。幸运的是，当指定的 CID 冲突时（即该文件已经存在），Docker 会报错，不会创建该容器。 CID 文件可以在多个容器时共享，并且可以通过 Volume 功能进行重命名。

另一个获取 ID 的方式是使用 `docker ps`:

```bash
CID=$(docker ps --latest --quiet) # or CID=$(docker ps -l -q)
echo $CID
```

这种方式获取的是截取的 12 字节长的 ID，要想获取整个 ID，要加 `--no-trunc` 选项。

容器 ID 不适合人使用，应该 Docker 还会被容器自动创建一个可读的唯一的名字，名字的结构是： 一个形容词_某个名人的名字，如 `hungry_swartz`, `distracted_turing` 等。

## 容器的状态及其依赖

用脚本加载容器：

```bash
MAILER_CID=$(docker run -d dockerinaction/ch2_mailer)
WEB_CID=$(docker create nginx)

AGENT_CID=$(docker create --link $WEB_CID:insideweb \
    --link $MAILER_CID:insidemailer \
    dockerinaction/ch2_agent)
```

以上命令只是创建容器，还没有运行，因此 `docker ps` 默认不会列出 web, agent 这两个容器，要想查看所有状态的容器，使用 `docker ps -a`。

容器的所有状态为： running, paused, restarting, exited 等。各状态相互转化如下：

![Docker 容器状态转换图](/assets/images/docker-state-transition-diagram.png)

容器创建后，再开启：

```bash
docker start $AGENT_CID
docker start $WEB_ID
```

运行以上的命令会出错：

```
Error response from daemon: Cannot start container
03e65e3c6ee34e714665a8dc4e33fb19257d11402b151380ed4c0a5e38779d0a: Cannot
link to a non running container: /clever_wright AS /modest_hopper/
insideweb
FATA[0000] Error: failed to start one or more containers
```

这是因为 agent 容器依赖于 web 容器，故要先启动 web 容器，如下：

```bash
docker start $WEB_ID
docker start $AGENT_CID
```

# 创建环境无关的系统

安装软件和维护的工作量主要在于对计算环境的定制。这种定制工作有：

+ 全局依赖（如主机上的文件系统位置）
+ 硬编码的部署架构（如在代码和或配置中检测检测变量值）
+ 数据的存储位置（如数据保存在一个特定的机器上）


Docker 可以利用以下 3 个特性来帮助实现环境无关的系统，从而减少维护量：

+ 只读文件系统
+ 环境变量注入
+ Volume


本次实现的案例是使用 Docker 运行多个 WordPress 博客。每个博客共享 WordPress 程序，只是博客内容不同。

## 只读文件系统

使用 `--read-only` 选项开启一个只读的 WordPress 容器:

```bash
$ docker run -d --name wp --read-only wordpress:4
```

`--read-only` 使得该容器的内容不可修改。

执行后，再使用 `docker inspect --format "{{.State.Running}}" wp` 来查看容器是否已经开启了，输出 true 和 false。

这里会输出 false，用 `docker logs wp` 查看日志：

```
error: missing required WORDPRESS_DB_PASSWORD environment variable
  Did you forget to -e WORDPRESS_DB_PASSWORD=... ?

  (Also of interest might be WORDPRESS_DB_USER and WORDPRESS_DB_NAME.)
```

可见，WordPress 依赖 MySQL。

使用 docker 运行一个 Mysql 容器：

```bash
$ docker run -d --name wpdb \
    -e MYSQL_ROOT_PASSWORD=ch2demo \
    mysql:5
```

上面命令中的 `-e` 选项向容器注入了一个环境变量值，以便容器使用。

现在再开启一个新的 WordPress 容器，并与 MySQL 数据库连接起来：

```bash
$ docker run -d --name wp2 \
    --link wpdb:mysql \
    -p 80 --read-only \
    wordpress:4
```

再查看该容器是否已正常运行：

```bash
$ docker inspect --format "{{.State.Running}}" wp2
```

发现还是没有启动，用 `docker logs wp2` 再次检查，可看到类似以下的日志:

```
...  Fatal Error Unable to create lock file: Bad file descriptor (9)
```

可以看到因为 WordPress 容器是只读的，从而无法生成一个 lock 文件，而导致该容器启动失败。

因此，需要通过挂载 Volume 使该只读容器中的某些目录可写：

```bash
# start the container with specific volumes for read only exceptions
$ docker run -d --name wp3 --link wpdb:mysql -p 80 \
    -v /run/lock/apach2/ \
    -v /run/apache2/ \
    --read-only wordpress:4
```

上面 `-v /datadir` 选项使得主机上的某个临时目录挂载到容器中的 /datadir 目录。

至此，一个可用于开启 WordPress 及监控程序的脚本如下：

```bash
SQL_CID=$(docker create -e MYSQL_ROOT_PASSWORD=ch2demo mysql:5)

docker start $SQL_CID

MAILER_CID=$(docker create dockerinaction/ch2_mailer)
docker start $MAILER_CID

WP_CID=$(docker create --link $SQL_CID:mysql -p 80\
    -v /run/lock/apache2/ -v /run/apache2/ \
    --read-only wordpress:4)

docker start $WP_CID

AGENT_CID=$(docker create --link $WP_CID:insideweb \
    --link $MAILER_CID:insidemailer \
    dockerinaction/ch2_agent)

docker start $AGENT_CID
```

## 环境变量注入

很多程序可根据环境变量进行配置。而 Docker 也会利用环境变量来共享主机名、容器等信息，同时还有可向容器注入环境变量的机制。

`env` 命令可列出当前会话上下文里的所有环境变量值，向容器注入环境变量并显示：

```bash
$ docker run --env MY_ENVIRONMENT_VAR="this is a test" \
    busybox:latest env
```

上面的 `--env` 或 `-e` 选项可用来指定向容器注入的环境变量值，可以映像里已经设置了该变量，那么本次设置会覆盖原来的设置值。

WordPress 用到下面这些环境变量：

- WORDPRESS_DB_HOST
- WORDPRESS_DB_USER
- WORDPRESS_DB_PASSWORD
- WORDPRESS_DB_NAME
- WORDPRESS_AUTH_KEY
- WORDPRESS_SECURE_AUTH_KEY
- WORDPRESS_LOGGED_IN_KEY
- WORDPRESS_NONCE_KEY
- WORDPRESS_AUTH_SALT
- WORDPRESS_SECURE_AUTH_SALT
- WORDPRESS_LOGGED_IN_SALT
- WORDPRESS_NONCE_SAL- 

创建 WordPress 容器时这样注入环境变量：

```bash
$ docker create 
    --env WORDPRESS_DB_HOST=<my_database_hostname> 、
    --env WORDPRESS_DB_USER=site_admin \
    --env WORDPRESS_DB_PASSWORD=MeowMix42 \
    wordpress:4
```

要能开启多个 WordPress 容器，还需要为每个容器指定使用的数据库名：

```bash
docker create --link wpdb:mysql \
    -e WORDPRESS_DB_NAME=client_a_wp wordpress:4

docker create --link wpdb:mysql \
    -e WORDPRESS_DB_NAME=client_b_wp wordpress:4
```

至此，可以更新启动脚本了:


```bash
# 先启动 mysql 和 mailer 容器:
DB_CLD=$(docker run -d -e MYSQL_ROOT_PASSWORD=ch2demo mysql:5)
MAILER_CID=$(docker run -d dockerinaction/ch2_mailer)

# 假设 $CLIENT_ID 变量会传入脚本
if [ ! -n "$CLIENT_ID" ]; then
    echo "Client ID not set"
    exit 1
fi

WP_CID=$(docker create \
    --link $DB_CID:mysql \
    --name wp_$CLIENT_ID \
    -p 80 \
    -v /run/lock/apach2/ -v /run/apache2/ \
    -e WORDPRESS_DB_NAME=$CLIENT_ID \
    --read-only wordpress:4)

docker start $WP_CID

AGENT_CID=$(docker create \
    --name agent_$CLIENT_ID \
    --link $WP_CID:insideweb \
    --link $MAILER_CID:insidemailer \
    dockerinaction/ch2_agent)

docker start $AGENT_CID
```

# 创建可持续运行的容器

Docker 的一些选项可用于监测并自动重启容器。

## 自动重启容器

在创建容器百，可用 `--restart` 选项指定以下的重启策略：

+ 不重启（默认）
+ 当检测到某种条件后才重启
+ 不管什么情况问题重启


重启的等待时间采用 exponential backoff strategy。

采用这种方式重启会有空白时间，期间容器没有启动。


> 参考文献： 
> [《Docker in Action》by Jeff Nickoloff: Running software in containers](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
