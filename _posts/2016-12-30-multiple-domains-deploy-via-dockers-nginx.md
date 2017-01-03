---
title: 单机上通过 Nginx 反向代理部署多个域名（子域名）的 Docker 应用
date: 2016-12-30
writing-time: 2016-12-30 11:04
categories: programming Docker
tags: Docker Programming nginx domain
---

# 目标

在一台主机上运行多个 Web 应用，每个 Web 应用通过 docker-compose 管理，运行在各自的容器组内。

每个 Web 应用有各自的域名或子域名，通过在浏览器中输入域名，实现对各 Web 应用的访问。

# 方案 1

在单主机上运行一个真实的 Nginx（不在容器时运行），作为反向代理服务器。它针对不同的域名请求，转发给相应的容器。

# 方案 2

在单主机上运行一个容器 Nginx 作为代理服务，在启动该代理服务容器时，必须通过 `--link` 将所有的 Web 应用容器关联过来。由于 Docker 容器关联的实现方式，每次 Web 应用容器重启上，都必须要重启代理服务容器，这将影响到其它 Web 容器的可用性。因此不考虑使用这种方案。

# 具体实现

实验环境是阿里云 ECS Ubuntu 16.04。

## 安装最新版的 nginx:

在 `/etc/apt/sources.list` 中添加源：

```bash
$ sudo vi /etc/apt/sources.list

# add the lines below
deb http://nginx.org/packages/ubuntu/ xenial nginx
deb-src http://nginx.org/packages/ubuntu/ xenial nginx
```

安装：

```bash
$ sudo apt-get update 
$ sudo apt-get install nginx
```

配置文件，nginx.conf:

```conf
user nginx;
worker_processes 1;
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;
worker_rlimit_nofile 65535;
events {
    use epoll;
    worker_connections 65535;
}

http {
    include mime.types;
    default_type application/octet-stream;
    # include /etc/nginx/conf.d/*.conf;
    # include /etc/nginx/sites-enabled/*;
    include /etc/nginx/conf.d/reverse-proxy.conf;
    sendfile on;
    keepalive_timeout 65;
    gzip on;
    client_max_body_size 50m; #缓冲区代理缓冲用户端请求的最大字节数,可以理解为保存到本地再传给用户
    client_body_buffer_size 256k;
    client_header_timeout 3m;
    client_body_timeout 3m;
    send_timeout 3m;
    proxy_connect_timeout 300s; #nginx跟后端服务器连接超时时间(代理连接超时)
    proxy_read_timeout 300s; #连接成功后，后端服务器响应时间(代理接收超时)
    proxy_send_timeout 300s;
    proxy_buffer_size 64k; #设置代理服务器（nginx）保存用户头信息的缓冲区大小
    proxy_buffers 4 32k; #proxy_buffers缓冲区，网页平均在32k以下的话，这样设置
    proxy_busy_buffers_size 64k; #高负荷下缓冲大小（proxy_buffers*2）
    proxy_temp_file_write_size 64k; #设定缓存文件夹大小，大于这个值，将从upstream服务器传递请求，而不缓冲到磁盘
    proxy_ignore_client_abort on; #不允许代理端主动关闭连接
    server {
        listen 80;
        server_name localhost;
        location / {
            root html;
            index index.html index.htm;
        }
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root html;
        }
    }
}
```

反向代理服务器配置文件 `reverse-proxy.conf`：

```conf
server
{
    listen 80;
    server_name hello.atjiang.com;
    location / {
        proxy_redirect off;
        proxy_set_header host $host;
        proxy_set_header x-real-ip $remote_addr;
        proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:9100;
        # proxy_pass http://192.168.10.40:9100; # 如果是转发到其它主机
    }
    access_log /var/log/nginx/hello.atjiang.com_access.log;
}

server
{
    listen 80;
    server_name world.atjiang.com;
    location / {
        proxy_redirect off;
        proxy_set_header host $host;
        proxy_set_header x-real-ip $remote_addr;
        proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:9101;
        # proxy_pass http://192.168.10.50:9101; # 如果是转发到其它主机
    }
    access_log /var/log/nginx/world.atjiang.com_access.log;
}
```

设置并启动 nginx：
 
```bash
$ sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak  # backup
$ sudo cp ./nginx.conf /etc/nginx/nginx.conf
$ sudo cp ./reverse-proxy.conf /etc/nginx/conf.d/reverse-proxy.conf
$ sudo nginx -t # test
$ sudo service nginx start
```

启动生效后，对 `hello.atjiang.com` 的访问就会导向到服务器的 9100 端口，对 `world.atjiang.com` 的访问就会导向到服务器的 9102 端口。

由于请求都是由反向代理器转发到后端的机器，后端的访问日志里记录的都会是反向代理的 IP。如果要想记录真实的 IP 地址，后台（假设也是 nginx）的日志格式需要修改为：

```conf
log_format access '$HTTP_X_REAL_IP - $remote_user [$time_local] "$request" '
'$status $body_bytes_sent "$http_referer" '
'"$http_user_agent" $HTTP_X_Forwarded_For';
```

具体流程可参见 [nginx 安装文档](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)。



参考文献： 

+ [一台服务器，两个部署了nginx的容器，解析了两域名，想分别访问这两个容器不添加端口？](https://segmentfault.com/q/1010000007004630)
+ [搭建nginx反向代理用做内网域名转发](http://www.ttlsa.com/nginx/use-nginx-proxy/)
