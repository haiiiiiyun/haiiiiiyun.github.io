---
title: 高效使用 PostgreSQL 命令行
date: 2016-08-15
writing-time: 2016-08-15 22:36
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

此时，通过开通 **扩展显示模式**，显示的查询内容都不再以表格的形式显示，而是以键值对的形式显示。

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

通过 `\x auto` 设置后，如果水平空间足够，查询结构会以表格形式显示，而当水平空间不足时，会以键值对形式显示。

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

psql 默认支持 Tab 命令补全，要想使补全的所有 SQL 关键键都是大写形式，可以设置 `\set COMP_KEYWORD_CASE upper`。

psql 支持从配置文件  *~/.psqlrc* 中读取配置值，因此可以将以上的设置值保存到 *~/.psqlrc* 文件中，内容如下：

```sql
\set COMP_KEYWORD_CASE upper
\x auto
\pset null ¤
```










> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
