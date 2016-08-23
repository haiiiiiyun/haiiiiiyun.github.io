---
title: 在 Docker 容器中运行一个简单的应用
date: 2016-08-23
writing-time: 2016-08-23 13:35--14:19
categories: programming
tags: Docker
---

# 学习使用 Docker 客户端

语法：

```shell
# Usage: [sudo] docker [subcommand] [flags] [arguments] ..
# Example:
$ docker run -i -t ubuntu /bin/bash
```

通过 `docker version` 命令可以查看 Docker 服务器、客户端 及 GO 语言的版本信息。

```shell
$ docker version
Client:
 Version:      1.12.1
 API version:  1.24
 Go version:   go1.6.3
 Git commit:   23cf638
 Built:        Thu Aug 18 05:33:38 2016
 OS/Arch:      linux/amd64

Server:
 Version:      1.12.1
 API version:  1.24
 Go version:   go1.6.3
 Git commit:   23cf638
 Built:        Thu Aug 18 05:33:38 2016
 OS/Arch:      linux/amd64
 ```

# 获取 Docker 命令的帮助信息

列出所有的命令: 

```shell
$ docker --help
```

要查看指定子命令的帮助信息，例如：

```shell
$ docker attach --help

Usage: docker attach [OPTIONS] CONTAINER

Attach to a running container

  --help              Print usage
  --no-stdin          Do not attach stdin
  --sig-proxy=true    Proxy all received signals to the process
```

# 在 Docker 中运行一个 Web 应用

```shell
$ docker run -d -P training/webapp python app.py
```

+ `-d` 选项使 Docker 在后台运行
+ `-P` 选项将 Docker 内的 5000 端口映射到主机的某个随机端口
+ `training/webapp`  是 Docker Hub 上的一个测试 Flask Web App
+ `python app.py` 指定在容器中启动 Web App


# 查看我们的 Web 应用容器

```shell
$ docker ps -l

CONTAINER ID  IMAGE                   COMMAND       CREATED        STATUS        PORTS                    NAMES
bc533791f3f5  training/webapp:latest  python app.py 5 seconds ago  Up 2 seconds  0.0.0.0:49155->5000/tcp  nostalgic_morse
```

+ `-l` 即 last - 列出最近启动的容器信息


查看上面的端口信息：

```
PORTS
0.0.0.0:49155->5000/tcp
```

由于使用了 `-P` 选项，从而使得容器内的 5000 端口映射到了主机的 49155 端口。`-P` 选项是 `-p 5000` 选项的简写，它实现将容器内的 5000 端口映射到主机的一个高位端口（从 32768 到 61000）。当然，通过 `-p` 选项也可以指定要映射的主机端口号，比如要将容器内的 5000 端口映射到主机的 80 端口：

```shell
$ docker run -d -p 80:5000 training/webapp python app.py
```

# 查看端口映射信息

通过  `docker ps` 查看比较麻烦，可以通过 `docker port container_name in_container_port` 进行：

```shell
$ docker port nostalgic_morse 5000

0.0.0.0:49155
```

# 查看 Web 应用的日志

```shell
$ docker logs -f nostalgic_morse

* Running on http://0.0.0.0:5000/
10.0.2.2 - - [23/May/2014 20:16:31] "GET / HTTP/1.1" 200 -
10.0.2.2 - - [23/May/2014 20:16:31] "GET /favicon.ico HTTP/1.1" 404 -
```

+ `-f` 选项使得可以像 `tail -f` 命令一样看到容器标准输出上的内容。


# 列出容器中的进程

```shell
$ docker top nostalgic_morse

PID                 USER                COMMAND
854                 root                python app.py
```

# 查看容器的详细信息

通过 `docker inspect` 可以查看容器的配置及状态等详细信息，并以 JSON 格式返回。

```shell
$ docker inspect nostalgic_morse

[{
    "ID": "bc533791f3f500b280a9626688bc79e342e3ea0d528efe3a86a51ecb28ea20",
    "Created": "2014-05-26T05:52:40.808952951Z",
    "Path": "python",
    "Args": [
       "app.py"
    ],
    "Config": {
       "Hostname": "bc533791f3f5",
       "Domainname": "",
       "User": "",
. . .
```

还可以指定要返回的信息项：

```shell
$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nostalgic_morse

172.17.0.5
```

# 关闭容器

```shell
$ docker stop nostalgic_morse

nostalgic_morse
```

# 重启容器

刚关闭后，还可以重新启动。

```shell
$ docker start nostalgic_morse

nostalgic_morse
```

要先关闭再启动，可以用 `docker restart container_name`。

# 删除容器

容器没有关闭时不能删除：


```shell
$ docker rm nostalgic_morse

Error: Impossible to remove a running container, please stop it first or use -f
2014/05/24 08:12:56 Error: failed to remove one or more containers
What happened? We can’t actually remove a running container. This protects you from accidentally removing a running container you might need. You can try this again by stopping the container first.
```

```shell
$ docker stop nostalgic_morse

nostalgic_morse

$ docker rm nostalgic_morse

nostalgic_morse
```

> 参考文献： 
> [Docker docs: Run a simple application](https://docs.docker.com/engine/tutorials/usingdocker/)
