---
title: 管理 Docker 容器中的数据
date: 2016-08-24
writing-time: 2016-08-24 08:31--10:44
categories: programming
tags: Docker
---

# 管理容器中的数据

主要有两种方法：

+ Data volumes
+ Data volume 容器


# Data volume 方法

一个 data volume 容器中的一个特殊目录，它能绕过 UFS 系统的限制。Data volume 为数据的持久化和共享提供如下功能：

+ Volumes 在容器创建时初始化。如果容器的映像文件中的那个对应挂载点本来就有数据，那么这些数据会在初始化过程中复制到 Volume 上（如果挂载的是主机上的目录则不复制）
+ Data volumes 可以在容器间共享共用
+ 能对 Data volumes 中的数据直接进行修改
+ 当更新映像文件时，不会包含进 Data volumes 中的更新内容
+ 即便容器删除了，Data volumes 也不会被删除


Data volumes 是用来持久化数据的，它不依赖容器的生命周期。因此，当删除容器时，Docker 不会自动地删除 Data volumes。

## 添加一个 Data volume

```shell
$ docker run -d -P --name web -v /webapp training/webapp python app.py
```

上面的命令会在容器的 `/webapp` 上挂载一个新的 Data volume。

`-v` 选项即 volume，指定 Data volume 的挂载点。可以在 `docker create` 和 `docker run` 命令中使用 `-v`，在命令中多次使用 `-v` 可以指定多个 Data volumes。

同时，在 Dockerfile 文件中可以用 `VOLUME` 指令来添加 Data volume。

## 定位 Data volume

通过 `docker inspect` 可以查出 volume 在主机上的具体位置：

```shell
$ docker inspect web
```

输出中会有 Volume 的相关信息，类似：

```conf
...
"Mounts": [
    {
        "Name": "fac362...80535",
        "Source": "/var/lib/docker/volumes/fac362...80535/_data",
        "Destination": "/webapp",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    }
]
...
```

可以看到， Destination 是容器内的挂载点，而 Source 是主机上的对应目录。

## 指定主机上的一个目录为 Data volume

```shell
$ docker run -d -P --name web -v /src/webapp:/opt/webapp training/webapp python app.py
```

上面的命令将主机上的 `/src/webapp` 挂载到容器中的 `/opt/webapp`。如果容器中原来就有 `/opt/webapp` 目录，那么现在新挂载的目录将隐藏原来的目录，这和 `mount` 命令的行为一致。

容器中的目录必须用绝对路径，而主机目录即可以用绝对路径，也可以用 `name` 值。

当用 `name` 值时，Docker 会根据 `name` 值创建一个命名 Volume。`name` 值必须以字母开头，其它可以包含的字符为`0-9_.-`。

挂载一个主机目录对测试非常有用。例如你可以将源码目录挂载到容器中，然后当源码修改后可以实时看到实现的修改效果。指定的主机目录如果不存在，Docker 会自动创建。

Data volumes 默认是以读写模式挂载的，但是我们可以手动进行设置：

```shell
$ docker run -d -P --name web -v /src/webapp:/opt/webapp:ro training/webapp python app.py
```

由于主机目录是和主机类型关联的，而 Docker 映像文件是可移植的，因此不能在 Dockerfile 中指定挂载主机目录。

## 将共享存储器挂载为 Data volume

通过 [一些 Docker volume 插件](https://docs.docker.com/engine/extend/plugins_volume/) 可以挂载 iSCSI, NFS 或 FC 等共享存储器。

共享存储器的好处是它们与主机无关。

下面的命令通过 `flocker ` volume 驱动，创建了一个命名 volume `my-named-volume`，然后将其挂载到 `/opt/webapp`:

```shell
$ docker run -d -P \
  --volume-driver=flocker \
  -v my-named-volume:/opt/webapp \
  --name web training/webapp python app.py
```

也可以先通过 `docker volume create` 命令创建一个命名 volume，再挂载：

```shell
$ docker volume create -d flocker --name my-named-volume -o size=20GB

$ docker run -d -P \
  -v my-named-volume:/opt/webapp \
  --name web training/webapp python app.py
```

## Volume labels

像 SELinux 等都要求挂载到容器中的 volume 必须有适当的标签。Docker 默认不会修改 OS 设置的标签。要想在容器中修改，在加载 volume 时可以添加 `:z` 或 `:Z` 这两个后缀来实现。`z` 生成共享的标签，它使得所有的容器都能对 Volume 的内容进行读写，而 `Z` 生成私有不共享的标签，只有当前容器可以使用。

## 将主机文件挂载为 Data volume

```shell
$ docker run --rm -it -v ~/.bash_history:/root/.bash_history ubuntu /bin/bash
```

挂载后，在容器中的 Bash 命令历史会和主机共享。

不推荐这种方式，要想实现这种功能，可挂载其父目录。

# 创建并挂载一个 Data volume 容器

如果想在多个容器间共享持久化数据，最好创建一个命名的 Data Volume 容器，然后再对其进行挂载。


先创建一个含有共享 volume 的命名容器 dbstore：

```shell
$ docker create -v /dbdata --name dbstore training/postgres /bin/true
```

之后，可以通过 `--volumes-from` 将 dbstore 中的共享 volume `/dbdata` 挂载到新的容器中：

```shell
$ docker run -d --volumes-from dbstore --name db1 training/postgres

$ docker run -d --volumes-from dbstore --name db2 training/postgres
```

如果 postgres 映像中原来就有 /dbdata 目录，那么原来的目录会被隐藏。

指定多个 `--volumes-from` 参数可以加载多个容器 volume。

也可以扩展这个共享挂载链：

```shell
$ docker run -d --volumes-from db1 --name db3 training/postgres
```

这些共享 Volume 相当于程序设计中的对象引用。因此，即使 dbstore 被删除了， db1, db2, db3 中的共享 volume 也不会删除，因为对象引用数还没有到 0。如果要删除这个共享 Volume, 在删除最后一个挂载它的容器时用 `docker rm -v` 。

当共享 Volume 没有被任何容器挂载时，就会成为无主 Volumes。查看并删除这些 Volumes：

```shell
$ docker volume ls -f dangling=true

$ docker volume rm <volume_name>
```

## 对 Data Volumes 进行备份、恢复和数据迁移

将共享 Volume **/dbdata** 上的数据备份到主机当前目录下的 backup.tar 文件中：

### 打包备份

```shell
$ docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```

+ `--rm` 指定当容器被删除时，一同删除其匿名的 Volumes
+ `--volumes-from dbstore` 将容器 dbstore 中的 /dbdata 共享挂载过来
+ `-v $(pwd):/backup` 将主机上的当前目录挂载为容器中的 /backup 目录
+ `tar cvf /backup/backup.tar /dbdata` 将 /dbdata 目录进行打包备份


### 数据恢复

```shell
$ docker run -v /dbdata --name dbstore2 ubuntu /bin/bash

$ docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"
```

### 删除 Volumes

当容器删除时，Data Volume 不会被删除。命名 Volume 有指定的数据源（名称如 awesome:/bar），而匿名 Volume 没有指定的数据源。当启动容器时，应该通过 `--rm` 指定在删除容器时同时删除匿名的 Volume（命名 Volume 不会被删除）：

```shell
$ docker run --rm -v /foo -v awesome:/bar busybox top
```

## 共享 Volumes 时的重要提示

当多个容器同时对其进行写操作时，存在数据损坏的可能。


> 参考文献： 
> [Docker docs: Manage data in containers](https://docs.docker.com/engine/tutorials/dockervolumes/)
