---
title: Docker 容器的网络功能
date: 2016-08-23
writing-time: 2016-08-23 16:12--17:12
categories: programming
tags: Docker Programming Utility
---

# 对容器进行命名

启动容器时，如果没有命名，Docker 会将容器取一个随机的名字。容器的名字必须是唯一的。

通过 `--name` 进行命名：

```shell
$ docker run -d -P --name web training/webapp python app.py
```

通过 `docker ps` 命令来检查命名：

```shell
$ docker ps -l

CONTAINER ID  IMAGE                  COMMAND        CREATED       STATUS       PORTS                    NAMES
aed84ee21bde  training/webapp:latest python app.py  12 hours ago  Up 2 seconds 0.0.0.0:49154->5000/tcp  web
```

`docker inspect` 命令可以接受容器的名字为参数：

```shell
$ docker inspect web

[
   {
       "Id": "3ce51710b34f5d6da95e0a340d32aa2e6cf64857fb8cdb2a6c38f7c56f448143",
       "Created": "2015-10-25T22:44:17.854367116Z",
       "Path": "python",
       "Args": [
           "app.py"
       ],
       "State": {
           "Status": "running",
           "Running": true,
           "Paused": false,
           "Restarting": false,
           "OOMKilled": false,
  ...
```

由于容器名必须唯一，如果之前命名过，必须用 `docker rm` 先删除容器，然后才能重用：

```shell
$ docker stop web

web

$ docker rm web

web
```

# 在默认网络上启动容器

Docker 通过 **network drivers** 来实现容器的网络功能。Docker 默认提供两种网络驱动， bridge 和 overlay，当然，也可以自己编写新的网络驱动。

安装 Docker 引擎后，会自动生成 3 个默认网络：

```shell
$ docker network ls

NETWORK ID          NAME                DRIVER
18a2866682b8        none                null                
c288470c46f6        host                host                
7b369448dccb        bridge              bridge  
```

名字为 bridge 的网络是一个很特殊的网络，如果没有特别指定，Docker 总是默认在该网络上启动容器。

先启动命名为 networktest 的容器：

```shell
$ docker run -itd --name=networktest ubuntu

74695c9cea6d9810718fddadc01a727a5dd3ce6a69d09752239736c030599741
```

通过检查 bridge 网络可以看到 networktest 容器的 IP 地址：

```shell
$ docker network inspect bridge

[
    {
        "Name": "bridge",
        "Id": "f7ab26d71dbd6f557852c7156ae0574bbf62c42f539b50c8ebde0f728a253b6f",
        "Scope": "local",
        "Driver": "bridge",
        "IPAM": {
            "Driver": "default",
            "Config": [
                {
                    "Subnet": "172.17.0.1/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Containers": {
            "3386a527aa08b37ea9232cbcace2d2458d49f44bb05a6b775fba7ddd40d8f92c": {
                "EndpointID": "647c12443e91faf0fd508b6edfe59c30b642abb60dfab890b4bdccee38750bc1",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "74695c9cea6d9810718fddadc01a727a5dd3ce6a69d09752239736c030599741": {
                "EndpointID": "b047d090f446ac49747d3c37d63e4307be745876db7f0ceef7b311cbba615f48",
                "MacAddress": "02:42:ac:11:00:03",
                "IPv4Address": "172.17.0.3/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "9001"
        }
    }
]
```

将容器从某个网络断开连接：

```shell
$ docker network disconnect bridge networktest
```

重新连接：

```shell
$ docker network connect bridge networktest
```

网络是对主机上的容器进行隔离的最自然的方法。

# 创建自己的 bridge 网络

bridge 网络只能在一台主机上使用，而 overlay 网络可以包括多台主机。

创建 bridge 网络：

```shell
$ docker network create -d bridge my-bridge-network
```

+ `d` 即 driver，指定网络驱动


创建后可以查看现有网络:

```shell
$ docker network ls

NETWORK ID          NAME                DRIVER
7b369448dccb        bridge              bridge              
615d565d498c        my-bridge-network   bridge              
18a2866682b8        none                null                
c288470c46f6        host                host
```

如果现在查看新建的网络，里面将没有内容：

```shell
$ docker network inspect my-bridge-network

[
    {
        "Name": "my-bridge-network",
        "Id": "5a8afc6364bccb199540e133e63adb76a557906dd9ff82b94183fc48c40857ac",
        "Scope": "local",
        "Driver": "bridge",
        "IPAM": {
            "Driver": "default",
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1/16"
                }
            ]
        },
        "Containers": {},
        "Options": {}
    }
]
```

# 将容器连接到指定网络

```shell
$ docker run -d --network=my-bridge-network --name db training/postgres
```

这时再查看网络，会看到关联了一个容器：

```shell
$ docker inspect --format='{{json .NetworkSettings.Networks}}'  db

{"my-bridge-network":{"NetworkID":"7d86d31b1478e7cca9ebed7e73aa0fdeec46c5ca29497431d3007d2d9e15ed99",
"EndpointID":"508b170d56b2ac9e4ef86694b0a76a22dd3df1983404f7321da5649645bf7043","Gateway":"172.18.0.1","IPAddress":"172.18.0.2","IPPrefixLen":16,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"MacAddress":"02:42:ac:11:00:02"}}
```

再在默认的网络上启动一个容器：

```shell
$ docker run -d --name web training/webapp python app.py
```

获取 web 容器的 IP 地址：

```shell
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web

172.17.0.2
```

打开 db 容器中的一个 shell,  ping web 容器的 IP:

```shell
$ docker exec -it db bash

root@a205f0dd33b2:/# ping 172.17.0.2
ping 172.17.0.2
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
^C
--- 172.17.0.2 ping statistics ---
44 packets transmitted, 0 received, 100% packet loss, time 43185ms
```

因为 db 容器已经在后台运行，要打开 db 容器中的 shell，不能用 `run` 命令，应该用 `exec` 命令。

在 db 容器中，会发现无法 Ping 通 web 容器的 IP，这是因此这两个容器在不同的网络中。

Docker 允许一个容器关联到多个网络，将 web 容器也一并关联到 my-bridge-network 网络，再 Ping 测试：

```shell
$ docker network connect my-bridge-network web
$ docker exec -it db bash

root@a205f0dd33b2:/# ping web
PING web (172.18.0.3) 56(84) bytes of data.
64 bytes from web (172.18.0.3): icmp_seq=1 ttl=64 time=0.095 ms
64 bytes from web (172.18.0.3): icmp_seq=2 ttl=64 time=0.060 ms
64 bytes from web (172.18.0.3): icmp_seq=3 ttl=64 time=0.066 ms
^C
--- web ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2000ms
rtt min/avg/max/mdev = 0.060/0.073/0.095/0.018 ms
```

由于现在这两个容器处于同一个网络中，故已经可以 Ping 通了。


> 参考文献： 
> [Docker docs: Network containers](https://docs.docker.com/engine/tutorials/networkingcontainers/)
