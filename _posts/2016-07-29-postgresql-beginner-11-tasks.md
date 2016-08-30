---
title: PostgreSQL 初学者应该学会的 11 个任务
date: 2016-07-29
writing-time: 2016-07-29 15:50--17:07
categories: programming
tags: Database Ubuntu Postgresql programming
---

# 一、安装

以 Ubuntu 为例，如果无需安装最新版本，只需用：

```sh
sudo apt-get install postgresql
```

如果要安装最新版本，以 Ubuntu Trusty(14.04) 为例。

1) 先从 [PostgreSQL 下载页](https://www.postgresql.org/download/linux/ubuntu/) 获取相应的 Apt 仓库信息，然后创建文件 **/etc/apt/sources.list.d/pgdg.list**， 命令为：

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
```

2) 加载仓库的 GPG Key：

```sh
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
```

3) 安装

```sh
sudo apt-get update && sudo apt-get install postgresql postgresql-contrib
```

# 二、打开命令行创建数据库

安装 PostgreSQL 后，会在数据库系统里自动创建名为 **postgres** 的用户名和角色名，同时在 Linux 系统中创建一个相同用户名的用户。

切换到 **postgres** 用户：

```sh
sudo su - postgres
```

开启 **psql** 终端：

```sh
psql
```

由于数据库系统中的 **postgres** 用户密码是随机产生的，如果想修改，在由 `psql` 打开的终端窗口中执行：

```sql
ALTER USER postgres WITH PASSWORD 'postgres';
```

如果想修改 Linux 系统中的 postgres 用户密码：

1. 删除旧密码：

```sh
sudo passwd -d postgres
```

2. 设置新密码：

```sh
sudo su - postgres
passwd
```

## 创建数据库

剧情设定： 蝙蝠侠想创建一个登记混蛋的数据库：

```sql
CREATE DATABASE villains;
```

创建数据库时也可以指定编码：

```sql
CREATE DATABASE villains ENCODING 'UTF-8';
```

# 三、创建用户

为确保安全，为每个数据库创建一个专门用户：

```sql
CREATE USER batman WITH PASSWORD 'Extremly-Secret-Password';
```

# 四、为用户授权权限

授权全部的权限：

```sql
GRANT ALL PRIVILEGES ON DATABASE villains to batman;
```

或者也可以授权指定的权限：

```sql
GRANT SELECT ON DATABASE villains to alfred;
```

能够授权的权限有：

+ SELECT
+ INSERT
+ UPDATE
+ DELETE
+ RULE
+ REFERENCES
+ TRIGGER
+ CREATE
+ TEMPORARY
+ EXECUTE
+ USAGE


对于上面的创建数据库、创建用户和授权三步操作，其实可以用一步来完成：

```sql
CREATE DATABASE villains OWNER batman;
```

# 五、创建表

创建一个超级混蛋数据表：

```sql
CREATE TABLE super_villains (id serial PRIMARY KEY, name character varying(100), super_power character varying(100), weakness character varying(100));
```

再创建一个装备数据表：

```sql
CREATE TABLE equipment (id serial PRIMARY KEY, name character varying(100), status character varying(100), special_move character varying(100));
```

# 六、显示表的信息

查看表的列名、列类型等表描述信息：

```sql
\d+ equipment;
```

如果想在 PgAdmin 上查询的话：

```sql
SELECT *
FROM information_schema.columns
WHERE table_name = 'equipment';
```

该命令会显示关于表的更加详细的信息。


如果想列出当前数据库中有哪些表：

```sql
\d
```

该命令会列出数据库中全部的表，包括由系统创建的一些控制表，如 equipment_id_seq 等。


# 七、修改表格，使其序号能自增

系统已经为表格序号的自增创建了相应的控制表，如对应 equipment 表有 equipment_id_seq 表。

修改表格使得每次插入时无需填写 id 值，id 值能自动递增：

```sql
ALTER TABLE equipment ALTER id set default nextval('equipment_id_seq');
ALTER TABLE super_villains ALTER id set default nextval('super_villains_id_seq');
```

# 八、插入数据

```sql
INSERT INTO equipment(name, status, special_move) VALUES('Utility Belt', 'Nice and yellow', 'All kind of cool stuff in your waist');
INSERT INTO super_villains(name, super_power, weakness) VALUES('The Joker', 'Extra Crazy', 'Super punch');
```

# 九、查询

```sql
SELECT * from equipment;  
SELECT * from super_villains;
SELECT weakness from super_villains;
SELECT special_move, name from equipment;
```

# 十、基本管理操作

## 允许远程访问

找到数据库的配置文件 **postgresql.conf**， Ubuntu 14.04 上的位置是 **/etc/postgresql/9.5/main/postgresql.conf**。

找到含有 `#listen_address = 'localhost'` 的行，修改成允许访问的远程 IP 地址，如： `listen_addresses = '10.0.0.3'`，或者允许所有地址： `listen_addresses = '*'`。

## 重启数据库服务器

在 Ubuntu 上：

```sh
sudo service postgresql restart
```

# 十一、备份与恢复

## 备份

```shell
$ sudo su - postgres

$ pg_dump dbname > backup.sql
```

## 还原

```shell
$ sudo su - postgres
$ dropdb dbname # 先删除原来的数据库
$ psql # 打开 psql 界面
#postgres# CREATE DATABASE dbname OWNER owername;
# \q
$ psql -d dbname -f backup.sql
```

参考文献： 

+ [How to Install PostgreSQL 9.5 on Ubuntu (12.04 - 15.10)](http://www.tuicool.com/articles/Ir6vmmn)
+ [修改postgres密码](http://www.cnblogs.com/kaituorensheng/p/4735191.html)
+ [10 beginner's PostgreSQL tasks you should know](https://eye.raze.mx/10-beginner-postgresql-tasks-you-should-know/)
