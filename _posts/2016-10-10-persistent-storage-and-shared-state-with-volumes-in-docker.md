---
title: Docker 中通过 Volume 实现持久化存储和共享状态
date: 2016-10-10
writing-time: 2016-10-10 14:52
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# Volume 简介

主机或容器中的目录树是由一组挂载点创建的，这些挂载点描述了如何拼命一个或多个文件系统。

一个 *Volume* 就是主机目录树上的一部分挂载到容器目录树上的一个挂载点。下图中，一个 Volume 挂载到了 /data 目录，故对 `/` 的写操作会导向到已挂载的 UFS，而对 `/data` 的写操作，通过 Volume，会直接在主机的文件系统上操作。

![容器通过 Volume 直接写到主机文件系统上](/assets/images/container-monted-volume.png)


## Volume 提供了独立于容器的数据管理功能

Volume 这个工具能保存和共享的数据，它们的领域或生命周期都独立于单个容器。

类似的数据有：

+ 数据库软件 VS 数据库数据
+ Web 应用 VS 日志
+ 数据处理应用 VS 输入和输入的数据
+ Web 服务器 VS 静态内容
+ 产品 VS 支撑的工具

Volume 有助于架构组件的模块化。映像适当打包和分发相对静态的文件，比如程序; 而 Volume 用来保存动态数据或定制内容。这种区别使得映像可被复用。

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

再退出 CQLSH，从而结束该容器。由于该容器创建时有 `--rm` 选项，故当其结束时会自动被删除。接着再删除掉之前创建的 Cassandra 节点：

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

上面的查询返回了之前保存的 keyspace。

退出并删除这些测试的容器：

```bash
$ docker rm -vf cass2 cass-shared
```

# Volume 类型

共有两种 Volume 类型。每种 Volume 都是主机目录树的一个位置到容器内的目录树上的一个挂载点，其不同在于主机上的位置。











参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Persistent storage and shared state with volumes](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
