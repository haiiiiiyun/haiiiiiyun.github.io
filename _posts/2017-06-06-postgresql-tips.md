---
title: Postgresql Tips
date: 2017-06-06
writing-time: 2017-06-06
categories: Programming
tags: Programming database postgresql
---

# 修改数据库的所有者

```sql
ALTER DATABASE name OWNER TO new_owner;
```

参考：https://stackoverflow.com/questions/4313323/how-to-change-owner-of-postgresql-database

# 修改数据库用户密码

```sql
ALTER USER username WITH PASSWORD 'password';
```
