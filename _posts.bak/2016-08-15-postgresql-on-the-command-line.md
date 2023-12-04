---
title: 高效使用 PostgreSQL 命令行
date: 2016-08-15
writing-time: 2016-08-15 22:36--2016-08-19 16:29
categories: programming
tags: Database Ubuntu Postgresql programming
---

# 配置 psql

psql 默认使用表格形式显示 SELECT 结果，如：

```sql
db=# SELECT 'hello' AS foo, bar FROM generate_series(1, 2) AS bar;
  foo  | bar
-------+-----
 hello |   1
 hello |   2
(2 rows)
```

但是当查询项的内容过长时，会很难阅读，如：

```sql
db=# SELECT 'really long string messing with the output' AS foo, bar, 
'another long string making things worse' AS baz FROM generate_series(1,
 2) AS bar;
                    foo                     | bar |                   ba
z
--------------------------------------------+-----+---------------------
--------------------
 really long string messing with the output |   1 | another long string 
making things worse
 really long string messing with the output |   2 | another long string 
making things worse
(2 rows)
```

此时，通过开通 **扩展显示模式**，查询内容将不再以表格形式显示，而是以键值对的形式显示。

开通 **扩展显示模式** ：

```sql
db=# \x
Expanded display is on.
```

扩展显示模式下的显示例子：

```sql
db=# SELECT 'really long string messing with the output' AS foo, bar, 
'another long string making things worse' AS baz FROM generate_series(1,
 2) AS bar;
-[ RECORD 1 ]-----------------------------------
foo | really long string messing with the output
bar | 1
baz | another long string making things worse
-[ RECORD 2 ]-----------------------------------
foo | really long string messing with the output
bar | 2
baz | another long string making things worse
```

通过 `\x auto` 设置后，如果水平空间足够，查询结果会以表格形式显示，而当水平空间不足时，会以键值对形式显示。

第二个配置项是指定 **NULL** 如何显示。默认显示下， **NULL** 与空字符串无法区别出来：

```sql
db=# SELECT '', NULL;
 ?column? | ?column?
----------+----------
          |
(1 row)
```

通过运行 `\pset null ¤`，就能显示出 **NULL** 了：

```sql
db=# SELECT '', NULL;
 ?column? | ?column?
----------+----------
          | ¤
(1 row)
```

psql 默认支持 Tab 命令补全，要想使补全的所有 SQL 关键词都用大写形式，可以设置 `\set COMP_KEYWORD_CASE upper`。

psql 支持从配置文件  *~/.psqlrc* 中读取配置值，因此可以将以上的设置值保存到 *~/.psqlrc* 文件中，内容如下：

```sql
\set COMP_KEYWORD_CASE upper
\x auto
\pset null ¤
```

# 获取帮助

`\h` 命令列出所有的 SQL 命令信息，在列出的页面中可以使用 vi 按键进行移动和查询。

`\h alter` 命令列出所有 ALTER 命令相关的帮助信息。

`\?` 命令列出 PostgreSQL 元命令的帮助信息。

# 玩转数据库

当连接数据库时，psql 能非常智能地自动填写缺少的值，如 localhost, 标准端口等。因此，当连接本地的一个数据库时，只需:

```shell
psql db_name
```

没有指定数据库名时， psql 会进入一个以当前用户名命名的数据库中。

```shell
$ psql
psql: FATAL: database "phil" does not exist
$ createdb `whoami`
$ psql
phil=#
```

这个数据库对于平时学习和测试很有用。


# 探索数据库

## 列举

+ 列出表：  `\dt`
+ 列出索引： `\di`
+ 列出视图： `\dv`


上面的这些命令还能接受一个模式参数，类似在命令行中模糊查询文件，可以用来过滤信息，例如，想列出以 **user** 开头的表： `\dt user*`

## schema

PostgreSQL 中的 schema 相当于表的命名空间。默认的命名空间是 **public**。如果你没有指定命名空间，当创建 **foo** 表时，实际上创建了 **public.foo**。一般地，可以为每个客户（公司）创建一个独立的命名空间。

如果不考虑命名空间，只想找到所有的表名为 **users** 的表：

```sql
db=# \dt *.users
         List of relations
  Schema  | Name  | Type  | Owner
----------+-------+-------+-------
 apple    | users | table | phil
 google   | users | table | phil
 facebook | users | table | phil
(3 rows)
```

## 显示对象详细信息

要想列出单个对象（如表或视图）的详细信息，使用 `\d obj_name` 命令，它将显示对象的所有详细信息，包括：

+ 列名及其类型，是否有 **NOT NULL**，其默认值
+ 索引
+ 检测约束
+ 外键约束
+ 通过外键引用了当前表的所有表格
+ 触发器


```sql
db=# \d users
                          Table "public.users"
  Column  |  Type   |                     Modifiers
----------+---------+----------------------------------------------------
 id       | integer | not null default nextval('users_id_seq'::regclass)
 name     | text    | not null
 email    | text    | not null
 group_id | integer | not null
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
    "users_email_key" UNIQUE CONSTRAINT, btree (email)
Check constraints:
    "users_email_check" CHECK (email ~ '.@.'::text)
    "users_name_check" CHECK (name <> ''::text)
Foreign-key constraints:
    "users_group_id_fkey" FOREIGN KEY (group_id) REFERENCES groups(id)
Referenced by:
    TABLE "posts" CONSTRAINT "posts_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
```

## 查找函数名

`\df` 可用来列出函数列表，但是该命令和上面的 `\dt` 等命令不同，没有加参数不会列出任何信息，这是因为函数太多了。

假设要查询含有 **regexp** 的所有函数：

```sql
db=# \df *regexp*
                                    List of functions
   Schema   |         Name          | Result data type |  Argument data types   |  Type
------------+-----------------------+------------------+------------------------+--------
 pg_catalog | regexp_matches        | SETOF text[]     | text, text             | normal
 pg_catalog | regexp_matches        | SETOF text[]     | text, text, text       | normal
 pg_catalog | regexp_replace        | text             | text, text, text       | normal
 pg_catalog | regexp_replace        | text             | text, text, text, text | normal
 pg_catalog | regexp_split_to_array | text[]           | text, text             | normal
 pg_catalog | regexp_split_to_array | text[]           | text, text, text       | normal
 pg_catalog | regexp_split_to_table | SETOF text       | text, text             | normal
 pg_catalog | regexp_split_to_table | SETOF text       | text, text, text       | normal
(8 rows)
```

找到函数后，如果想查看它的具体定义或者要编辑，用 `\ef fun_name`。如果有重名函数，则加上参数，如 `\ef fun_name(arg1,arg2)`。命令执行后会在 $EDITOR 指定的编辑器中打开一个文件，里面的内容是包含在 **CREATE OR REPLACE FUNCTION** 中的函数定义体。保存并关闭该文件后，里面的代码即被执行。

当只想查看函数体，退出编辑器后不想执行里面的代码，则要在退出编辑器时使编辑器返回一个非 0 值。psql 只有当编辑器退出返回为 0 时（表示没有出错）才执行里面的代码。当使用 vim 时，用 `:cq` 使退出返回一个非 0 值。


# 构建查询语句

在 psql 命令行中适合输入较短的查询语句。如果语句较长，可以使用 `\e` 命令。`\e` 命令会在 $EDITOR 指定的编辑中打开 psql 中的最后一条查询语句。当保存退出编辑器后，psql 将执行里面的语句。

同时，在编辑器中，为保存查询语句，也可以将文件另存到其它位置。

在 psql 中也可以直接执行文件中的查询语句，用 `\i filename`。

`\e` 命令也可以接受一个文件名参数，使得文件在编辑器中打开： `\e filename`。但是这种方式下只支持已存在的文件，不能新建。

工作流程：

一、在 psq 中输入查询语句，用 `\e` 在编辑器中打开，保存到一个文件中，以后要再运行时，用 `\e filename` 再次打开，编辑并退出后 psql 自动运行里面的语句。

二、在同一个 tmux 窗口中打开两个 pane，一个打开 foo.sql，编辑查询语句;另一个打开 psql，运行 `\e foo.sql`。


# 输出内容比较

psql 中的命令默认输出到终端，但是通过 `\o filename` 命令可以将输出追加到 filename 上，然后再次运行 `\o`（不加参数），之后的命令又会恢复输出到终端中。

这个命令不适合用于导出数据，但是适合用于对输出数据进行比较：

```sql
db=# \o a.txt
db=# EXPLAIN SELECT * FROM users WHERE id IN (SELECT user_id FROM groups WHERE name = 'admins');
db=# \o b.txt
db=# EXPLAIN SELECT users.* FROM users LEFT JOIN groups WHERE groups.name = 'admins';
db=# \! vimdiff a.txt b.txt
```

# 克隆数据库

当在数据库上试验 migration 时，有可能会破坏原来的数据，而重建数据库会很费时间。

工作流程：

先创建一个克隆数据库，再在当前数据库上试验，一旦出错，删除当前数据库，从克隆数据库恢复，再重新试验。

创建克隆数据库 app_db_backup，并指定克隆的模板为 app_db:

```shell
$ createdb -T app_db app_db_backup
```

删除当前数据库，并恢复：

```shell
$ dropdb app_db
$ createdb -T app_db_backup app_db
```

# 提取数据

假设要将数据保存为 CSV 文件。可以使用 SQL 的 COPY 命令，或者元命令 `\copy`。

## COPY 命令

使用 COPY 命令导出数据为 CSV：

```
COPY (SELEC ...)
TO '/absolute/path/export.csv'
WITH (FORMAT csv, HEADER true);
```

该命令有一些限制，如只能指定绝对路径。只能保存到本地文件系统，即当你打开远程数据库时，保存的文件只能在远程服务器上。

## \copy 命令

```sql
\copy (SELECT ...) TO export.csv WITH (FORMAT csv, HEADER true)
```

\copy 命令可以指定相对路径，甚至可以不用引号，但是语句只能写在一行中，因为元命令是通过回车触发的，而不是通过 ; 触发。

\copy 本质上调用的也是 COPY 命令，但是它将输出写到 STDOUT 上，然后 psql 再将输出重定向到本地文件中。

导出文件的默认编码是 *UTF-8*，但是 Excel 对其支持不好，如果要想在 Excel 使用，使用 *latin1*:

```sql
\copy (SELECT ...) TO export.csv WITH (FORMAT csv, HEADER true, ENCODING 'latin1')
```

如果经常要执行这个命令，可以安装 [psql2csv](https://github.com/fphilipe/psql2csv)

使用方法：

```shell
$ psql2csv dbname "select * from table" > data.csv

$ psql2csv dbname < query.sql > data.csv

$ psql2csv --no-header --delimiter=$'\t' --encoding=latin1 dbname <<sql
> SELECT *
> FROM some_table
> WHERE some_condition
> LIMIT 10
> sql
```

> 参考文献： [comfortable with the command-line interface](http://phili.pe/posts/postgresql-on-the-command-line/)
