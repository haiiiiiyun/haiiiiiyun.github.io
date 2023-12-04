---
title: Docker 中通过 Volume 实现持久化存储和数据共享
date: 2016-10-10
writing-time: 2016-10-10 14:52--2016-10-11 11:00
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# Volume 简介

主机或容器中的目录树是由一组挂载点创建的，这些挂载点描述了如何对一个或多个文件系统进行拼接。

一个 *Volume* 就是主机目录树上的一部分挂载到容器目录树上的一个挂载点。下图中，一个 Volume 挂载到了 /data 目录，故对 `/` 的写操作会导向到已挂载的 UFS，而对 `/data` 的写操作，通过 Volume，会直接在主机的文件系统上操作。

![容器通过 Volume 直接写到主机文件系统上](/assets/images/dockerinaction/docker-container-mounted-volume.png)


## Volume 提供了独立于容器的数据管理功能

Volume 能用来保存和共享数据，其所属领域和生命周期都独立于单个容器。

类似的数据有：

+ 数据库软件 VS 数据库数据
+ Web 应用 VS 日志
+ 数据处理应用 VS 输入和输入数据
+ Web 服务器 VS 静态内容
+ 产品 VS 支撑的工具

Volume 有助于架构组件的模块化。映像适合打包和分发相对静态的文件，比如程序; 而 Volume 用来保存动态数据或定制内容。这种区别使得能复用映像。

例如，MySQL 程序都是相同的，可以只在一个容器中运行，而不同的数据库内容可以使用 Volume 来注入。

## 使用 Volume 来操作一个 NoSQL 数据库

Apache Cassandra 是一个列数据库 (column database)，它内置有聚类 (clustering)， 最终一致性(eventual consistency) 和线性写入可扩展性(linear write scalability) 等功能。该数据库也将数据保存在硬盘的文件上。

在本节中，我们先用其官方的映像创建一个单节点的 Cassandra 簇，创建一个 keyspace，删除容器，再在另一个容器中将原来的 keyspace 恢复到一个新的节点上。

先创建一个随带 Volume 的容器，这种定义了 Volume 的容器叫 volume container：

```bash
$ docker run -d \
    --volume /var/lib/cassandra/data \  # 指定容器内的 Volume 挂载点
    --name cass-shared \
    alpine echo Data Container
```

该容器会立即中止。先不要删除，下面开启的 Cassandra 容器要使用该容器创建的 Volume：

```bash
$ docker run -d \
    --volumes-from cass-shared \
    --name cass1 \
    cassandra:2.2
```

该 Cassandra 容器会从 cass-shared 容器复制 Volume 的定义。之后，这两个容器的 Volume 都会挂载到容器的 `/var/lib/cassandra/data`，并且都指向主机目录树上的相同位置。

再基于 cassandra:2.2 映像开启一个新的容器，并在其中运行一个 Cassandra 客户端工具，并连接到运行的服务器：

```bash
$ docker run -it --rm \
    --link cass1:cass \
    cassandra:2.2 csqlsh cass
```

现在，可以在 CQLSH 命令行中对 Cassandra 数据库进行操作了。首先查找一个名为 docker_hello_world 的 keyspace:

```sql
cqlsh> select * from system.schema_keyspaces WHERE keyspace_name = 'docker_hello_world';

 keyspace_name | durable_writes | strategy_class | strategy_options
 ---------------+----------------+----------------+------------------

 (0 rows)
 cqlsh> 
```

Cassandra 应该返回一个空列，表示数据库还没有被修改。接着再创建该 keyspace：

```sql
create keyspace docker_hello_world
with replication = {
    'class' : 'SimpleStrategy',
    'replication_factor': 1
};
```

现在再用上面的查询语句查询应该会返回一条记录：

```sql
h> select * from system.schema_keyspaces WHERE keyspace_name = 'docker_hello_world';     
 keyspace_name      | durable_writes | strategy_class                              | strategy_options
 --------------------+----------------+---------------------------------------------+----------------------------
  docker_hello_world |           True | org.apache.cassandra.locator.SimpleStrategy | {"replication_factor":"1"}

  (1 rows)
  cqlsh> 
```

退出 CQLSH，从而结束该容器。由于该容器创建时有 `--rm` 选项，故当其结束时会自动被删除。接着再删除掉之前创建的 Cassandra 节点：

```bash
$ docker stop cass1
$ docker rm -vf cass1
```

这里，删除 cass1 容器后，由于数据是通过 Volume 直接保存到主机上的，故数据应该还在。

下面通过创建一个新的 Cassandra 节点，查询该 keyspace 来验证：

```bash
$ docker run -d \
    --volumes-from cass-shared \
    --name cass2 \
    cassandra:2.2

$ docker run -it --rm \
    --link cass2:cass \
    cassandra:2.2 \
    cqlsh cass
```

```sql
cqlsh> SELECT * FROM system.schema_keyspaces WHERE keyspace_name ='docker_hello_world';

 keyspace_name      | durable_writes | strategy_class                              | strategy_options
--------------------+----------------+---------------------------------------------+----------------------------
 docker_hello_world |           True | org.apache.cassandra.locator.SimpleStrategy | {"replication_factor":"1"}

(1 rows)
```

以上查询返回了之前保存的 keyspace。

退出并删除这些测试的容器：

```bash
$ docker rm -vf cass2 cass-shared
```

# Volume 类型

共有两种 Volume 类型。每种 Volume 都是主机目录树的一个位置对应到容器内的目录树上的一个挂载点，其不同只在于主机上的位置。

+ 第 1 种叫绑定挂载的 Volume (bind mount volume)：用户指定将主机上的某个目录或文件挂载到容器中的目录树上。
+ 第 2 种叫受管理的 Volume (managed volume)：所使用的主机上的位置是由 Docker daemon 创建并管理的，这些位置称为 Docker managed space。


## 绑定挂载的 Volume (Bind mount volumes)

+ 适用于将主机上的一些文件或目录挂载到容器内的目录树上的某个特定位置。
+ 适用于实现容器与容器外的程序共享数据。

例如，可在容器中运行 Apache2 服务，并将主机上的一个目录挂载到容器中的 `/usr/local/apache2/htdocs/`，这样当项目内容修改后，无需重新创建或开启 Apache2 容器。这种使用方式最适合用于开发阶段。

```bash
$ docker run -d --name bmweb \
    -v ~/example-docs:/usr/local/apache2/htdocs \
    -p 80:80 http:latest
```

上面的 `-v ~/example-docs:/usr/local/apache2/htdocs` 创建了一个绑定的 Volume。`-v` 的规则是 `-v path_on_host:path_in_container[:ro]`，如果选项最后加上 `:ro`，则表示这个 Volume 是只读的，容器不可对其进行修改。

+ 当 path_on_host 是目录时，如果不存在，Docker 会自动创建，不过最好自己来创建，这样可以更好地对目录的所有者和权限进行控制。
+ 当 path_on_host 是文件时，必须要先存在，不然 Docker 会根据上面的规则，按目录处理。


Bind mount volumes 存在的问题：

+ 由于绑定到了特定主机上的特定位置，影响了 Docker 的可移植性
+ 当多个容器绑定到同一个主机位置时，对其同时读写可能会出现冲突


## 受管理的 Volume (Docker-managed volumes)

绑定时使用的主机上的位置都是由 Docker 创建并管理的，例子：

```bash
$ docker run -d \
    -v /var/lib/cassandra/data \
    --name cass-shared \
    alpine echo Data Container
```

由于 `-v` 没有指定主机位置，这就创建了一个 Docker-managed volume。如果要找出这个 Volume 绑定到主机上的确切哪个位置，可以用 `docker inspect` 命令：

```bash
$ docker inspect -f "{{json .Volumes}}" cass-shared

{"/var/lib/cassandra/data":"/mnt/sda1/var/lib/docker/vfs/dir/632fa59c..."}

```

Docker-managed volume 解耦了 volume 和主机上具体文件系统位置，很适合在大型系统中用于组织数据。


# 共享 Volume

## 依赖于主机的共享

多个容器通过 Volume 绑定到主机上的相同位置：

```bash
$ mkdir ~/web-logs-example

$ docker run --name plath -d \
    -v ~/web-logs-example:/data \
    dockerinaction/ch4_write_a # 容器日志写到该目录

$ docker run --rm \
    -v ~/web-logs-example:/reader-data \
    alpine:latest \
    head /reader-data/logA # 绑定到相同的位置，进行读操作

$ cat ~/web-logs-example/logA # 直接在主机上查看

$ docker stop plath
```

下面这个例子中，4 个容器的 Volume 都绑定到主机上的相同位置，2 个读，2 个写：

```bash
$ docker run --name woolf -d \
    --volume ~/web-logs-example:/data \
    dockerinaction/ch4_write_a

$ docker run --name alcott -d \
    --volume ~/web-logs-example:/data \
    dockerinaction/ch4_write_b

$ docker run --rm --entrypoint head \
    -v ~/web-logs-example:/towatch:ro \
    alpine:latest \
    /towatch/logA

$ docker run --rm \
    -v ~/web-logs-example:/toread:ro \
    alpine:latest \
    head /towatch/logB
```

这种类型的共享方式维护成本较高。

## 普遍采用的共享方式以及 volumes-from 选项

`docker run` 参数的 `volumes-from` 选项可以将一个或多个其它容器上的 volume 定义直接复制到当前新建的容器上，例如：

```bash
$ docker run --name fowler \
    -v ~/example-books:/library/PoEAA \
    -v /library/DSL \
    alpine:latest \
    echo "Fowler collection created."

$ docker run --name knuth \
    -v /library/TAoCP.vol1 \
    -v /library/TAoCP.vol2 \
    -v /library/TAoCP.vol3 \
    -v /library/TAoCP.vol4.a \
    alpine:latest \
    echo "Knuth collection created."

$ docker run --name reader \
    --volumes-from fowler \
    --volumes-from knuth \
    alpine:latest ls -l /library/ # 会列出 fowler 和 knuth 的所有 Volume


$ docker inspect --format "{{json .Volumes}}" reader # 检查 reader 的 Volume
```

也可以先将要整合的 Volume 先集合到一个单一容器，再从该容器复制：

```bash
$ docker run --name aggregator \
    --volumes-from fowler \
    --volumes-from knuth \
    alpine:latest \
    echo "Collection Created." # Create an aggregaton

$ docker run --rm \
    --volumes-from aggregator \
    alpine:latest ls -l /library/ # 会列出 fowler 和 knuth 的所有 Volume
```

通过 `-volumes-from` 选项进行的是完全一致的复制，不可对绑定位置、ro 只读权限等进行配置或修改， 并且当多个 Volume 定义中绑定的位置相同时，会有覆盖情况发生。

# Docker-managed volume 的生命周期

它们的生命周期独立于任何的容器，并且只能通过使用它的容器才可对其进行引用。

## Volume 的所有权

Managed volumes 是二等实体 (second-class entities)，无法共享或删除某个特定的 managed volume，因为无法对其进行标识 （只能通过使用它的容器进行引用）。

最可靠的方式是对应每个 Managed volume 开启一个容器。当多个容器使用同一个 Managed volume 时，volume 的引用计数会增加，这种操作和编程语言中的变量引用类似。只有当引用计数到 0 时，才会删除该 Managed volume。


## 清理 Volume

Docker 不会自己删除 Managed volume。当删除容器时，`docker rm -v` 会尝试一并删除它的 Managed volume，如果该 Volume 也被其它容器使用，则不会删除，只会减少对它的引用计数。

没有被使用的 Managed volume 为孤儿 Volume，可以使用一些脚本来清理。因此，在删除容器时使用 `-v` 选项是一个好习惯。同时，还建议使用下节介绍的 Volume 容器模式。

下面的命令可以删除所有已关闭的容器，并清理掉它们的 Managed Volume：

```bash
$ docker rm -v $(docker ps -aq)
```

# 容器使用 Volume 的常用模式

## Volume container 模式

创建一个容器（假设容器名为 vc_data）专门用于定义 Volumes，这个 vc_data 容器可以不运行（在上面的例子中可看也，这种容器只运行了下 `echo "Container Created"`），因为停止的容器也会保留对 Volume 的引用。然后其它的容器在创建或运行时通过 `--volumes-from` 从 vc_data 容器复制 Volume 定义。

使用这种模式要注意：


+ 一般容器名加前缀 `vc_`，表示 volume container
+ 涉及的各容器对于 Volume 绑定的目录位置及命名规范都必须协同一致

这种模式中，vc 容器保持了一个对数据的引用，从而便于进行备份、恢复和数据迁移操作。

用例：假设要升级一个数据库软件，如果数据库容器将数据写入到了一个 Volume，而该 Volume 是由一个 vc 容器定义的，那么在数据迁移时，只需关闭原来的数据库容器，然后再将原来的 vc 容器作为 Volume 源，再开启新的数据库容器即可。

## Data-packed volume container 模式

这种模式扩展至 Volume container 模式。Data-packed volume container 不仅定义 Volume，而且将从本容器的映像中的一些数据（如静态文件、配置数据、代码等）复制到这个定义的 Volume 中，从而可与其它容器共享。

```bash
$ docker run --name dpvc \
    -v /config \
    dockerinaction/ch4_packed \
    /bin/sh -c 'cp /packed/* /config/' # copy image content into a volume

$ docker run --rm --volumes-from dpvc \
    alpine:latest ls /config # list shared material

$ docker run --rm --volumes-from dpvc \
    alpine:latest cat /config/packedData

$ docker rm -v dpvc # remember to use -v when clean up
```
 
## Polymorphic container pattern

多态模式下，只提供一个统一的接口，但是能有不同的实现。具体到 Volume，可以在不对映像进行修改的情况下，注入不同的行为。

一个多态容器中的一些功能可以通过 Volumes 来替代。例如，假设一个 Node.js 映像默认会执行命令 `/app/app.js`，该映像中的默认实现是输出 `This is a Node.JS application`。

要修改该容器的行为，在创建该容器时，只需将自己的 `app.js` 实现通过 Volume 注入到 `/app/app.js` 即可。这种方式的适合使用情况：

+ 在开发时，避免每次迭代都要新建映像
+ 在运行一些事件处理任务时


可以将一些工具做成一个 data-packed volume container，然后和其它容器共享，在其它容器中使用这些工具来进行一些事件处理操作，例如：

```bash
$ docker run --name tools \
    dockerinaction/ch4_tools # create data-packed volume container with tools

$ docker run --rm \
    --volumes-from tools \
    alpine:latest \
    ls /operations/* # list shared tools

$ docker run -d --name important_app \
    --volumes-from tools \
    dockerinaction/ch4_ia # start another container with shared tools

$ docker exec important_app \
    /operations/tools/someTool # use shared tool in running container

$ docker rm -vf important_app
$ docker rm -v tools
```

也可以将文件注入到只读的容器中。通常会用多态容器来注入应用的配置信息。

开发阶段：

```bash
$ docker run --name devConf \
    -v /config \
    dockerinaction/ch4_packed_config:latest \
    /bin/sh -c 'cp /development/* /config/'

$ docker run --name devApp \
    --volumes-from devConf \
    dockerinaction/ch4_polyapp
```

生产环境中：

```bash
$ docker run --name prodConf \
    -v /config \
    dockerinaction/ch4_packed_config:latest \
    /bin/sh -c 'cp /production/* /config/'

$ docker run --name prodApp \
    --volumes-from prodConf \
    dockerinaction/ch4_polyapp
```


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Persistent storage and shared state with volumes](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
