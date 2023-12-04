---
title: 在 Docker 中运行 WordPress 服务
date: 2017-05-09
writing-time: 2017-05-09 15:04
categories: blog
tags: docker docker-compose wordpress mysql mariadb nginx
---

# 概述

运行一个 wordpress 容器和 mariadb 容器。wordpress 系统文件保存到主机的 `./wordpress/html` 目录，数据库文件保存到主机的 `./wordpress/db/` 目录。

wordpress 容器中的 80 端口映射到主机的 9999 端口。主机上可使用 nginx 设置反向代理。

# docker-compose 文件

docker-compose.yml 文件如下：

```yaml
version: '2'

services:

  wordpress:
    image: wordpress
    ports:
      - 9999:80
    links:
      - db
    volumes:
      - ./wordpress/html:/var/www/html
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
    restart: always

  db:
    image: mariadb
    ports:
      - 3306:3306
    volumes:
      -  ./wordpress/db:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: wordpress
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    restart: always
```

该 docker-compose 可在 [github](https://github.com/haiiiiiyun/wordpress_docker_composer) 上获取。

# 运行

在 docker-compose.yml 所在目录下，运行 `docker-compose up -d` 即可。运行后通过 `http://host-ip:9999` 访问。
