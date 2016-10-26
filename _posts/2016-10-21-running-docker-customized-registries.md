---
title: 运行定制的 Docker 注册中心
date: 2016-10-21
writing-time: 2016-10-21 20:56
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

实现了 Registry API (目前是 v2) 的程序都叫注册中心。Docker Hub 使用的注册中心的代码项目就保存为 registry 映像库。

## 运行一个个人的注册中心

```bash
$ docker run -d --name personal_registry \ # launch the registry container
    -p 5000:5000 --restart=always \
    registry:2
```

该注册中心容器通过受管理的 Volumes，将映像的数据都保存在容器的 /var/lib/registry。

将 registry:2 映像以 distribution:2 的标签存入该注册中心：

```bash
$ docker tag registry:2 localhost:5000/distribution:2
$ docker push localhost:5000/distribution:2
```

从该注册中心获取映像：

```bash
$ docker rmi localhost:5000/distribution:2
$ docker pull localhost:5000/distribution:2
```

## 注册中心的 V2 API

V2 Registry API 是 RESTful 的，其标准在 [docs.docker.com/registry/spec/api/](https://docs.docker.com/registry/spec/api/)。

下面的例子中，先创建一个包含 curl 的映像，再利用该映像来测试 V2 API。

映像的 Dockerfile 文件 curl.df:

```
FROM gliderlabs/alpine:latest
LABEL source=dockerinaction
LABEL category=utility
RUN apk --update add curl
ENTRYPOINT ["curl"]
CMD ["--help"]
```


创建映像：

```bash
$ docker build -t dockerinaction/curl -f curl.df .
```

验证个人的注册中心是否运行 V2 API：

```bash
$ docker run --rm --net host dockerinaction/curl -Is \
    http://localhost:5000/v2/
```

如果是 V2 API，会返回：

```
HTTP/1.1 200 OK
Content-Length: 2
Content-Type: application/json; charset=utf-8
Docker-Distribution-Api-Version: registry/2.0
```

如果不是 V2 API，会返回：

```
HTTP/1.1 404 NOT FOUND
Server: gunicorn/19.1.1
Connection: keep-alive
Content-Type: text/html
Content-Length: 233
```

获取 `distribution` 这个映像的所有标签列表：

```bash
$ docker run --rm -u 1000:1000 --net host \
    dockerinaction/curl -s http://localhost:5000/v2/distribution/tags/list

{"name":"distribution","tags":["2"]}
```

为 `distribution` 添加一个标签，再获取其所有标签列表：

```bash
$ docker tag \
    localhost:5000/distribution:2 \
    localhost:5000/distribution:two

$ docker push localhost:5000/distribution:two

$ docker run --rm -u 1000:1000 --net host \
    dockerinaction/curl -s http://localhost:5000/v2/distribution/tags/list

{"name":"distribution","tags":["2", "two"]}
```

## 定制注册中心的 registry 映像

Docker Hub registry 映像的基本信息：

+ 基于 Debian，里面的依赖包都已经更新了
+ 其主程序名为 `registry`，路径包含在 `PATH` 中，并被作为容器的 entrypoint
+ 默认的配置文件为 config.yml


config.yml 配置文件包含 9 个最高层配置段：

+ version: 必须，指定配置的版本
+ log: 控制 registry 项目的日志输出
+ storage: 控制映像保存在哪里，用何种方式
+ auth: 控制注册中心的认证机制
+ middleware: 可选，用来对用于 storage, registry, repository 的中间件的配置
+ reporting: 该项目已整合了一些报表工具，如 Bugsnag 和 NewRelic，该段用来配置这些工具
+ http: 配置该项目的网络功能
+ notifications: 在该段可以 Webhook 方式与其它项目整合
+ redis: 配置 Redis


# 增加集中式的注册中心

集中式的注册中心适合多人访问，故要将它发发页到网上，这可以用 `docker run ... -p 80:5000 ...` 将主机 80 端口映射到容器的 5000 端口来实现。同时也要实现认证机制。

## 使用反向代理

客户端向服务器的 80 端口发送请求，服务器上的反向代理（如 NGINX) 接受请求，并将前缀为 `/v2/` 的所有请求转发到 `registry` 容器进一步处理。

因此反向代理设置需要两个容器，一个运行 NGINX 反向代理，另一个运行注册中心 registry。反向代理容器通过 registry 别名与注册中心容器关联起来。

反向代理 NGINX 的配置文件 basic-proxy.conf:

```nginx
upstream docker-registry {
    server registry:5000; # Link alias requirement
}

server {
    listen 80; # container port requirement
    # Use the localhost name for testing purposes
    server_name localhost;
    # A real deployment would use the real hostname where is it deployed
    # server_name mytotallyawesomeregistry.com;

    client_max_body_size 0;
    chunked_transfer_encoding on;

    # We're going to forward all traffic bound for the registry
    location /v2/ { # Note /v2 prefix
      proxy_pass                            http://docker-registry;
      proxy_set_header Host                 $http_host;
      proxy_set_header X-Real-IP            $remote_addr;
      proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto    $scheme;
      proxy_read_timeout                    900;
    }
}
```

反向代理的 Dockerfile 文件 basic-proxy.df:

```
FROM nginx:latest
LABEL source=dockerinaction
LABEL category=infrastruction
COPY ./basic-proxy.conf /etc/nginx/conf.d/default.conf
```

这里由于使用了 Nginx 的 upstream 指令，它可以检测到关联的容器是否已正常运行，故无需创建启动脚本了。

创建映像：

```bash
$ docker build -t dockerinaction/basic_proxy -f basic_proxy.df .
```

运行反向代理容器，关联到之前的 personal_registry，并测试 V2 API:

```bash
$ docker run -d --name basic_proxy -p 80:80 \
    --link personal_registry:registry \
    dockerinaction/basic_proxy

$ docker run --rm -u 1000:1000 --net host \
    dockerinaction/curl \
    -s http://localhost:80/v2/distribution/tags/list

{"name":"distribution","tags":["2", "two"]}
```

## 在反向代理上配置 HTTPS(TLS)

传输层安全性 (Transport layer security, TLS) 能标识端点、确保消息的完整性和私密性，它在 HTTP 的下一层实现，它即为 HTTPS 中的 S。

Docker daemon 不会连接没有配置 TLS 的注册中心（除非运行在同一主机上），因此，必须要为集中式的注册中心配置 TLS。

HTTPS 端点与 HTTP 端点的不同：

+ 监听于 TCP 443 端口
+ 需要签名证书和私有 key 文件
+ 主机名、代理配置文件中的配置、以及用于创建证书的主机名必须匹配


下面举例创建一个主机名为 localhost，自签名的证书。

### 创建公密钥对及一个自签名的证书

通过 centurylink/openssl 映像创建：

```bash
$ docker run --rm -e COMMON_NAME=localhost -e KEY_NAME=localhost \
    -v "$(pwd)":/certs centurylink/openssl
```

这将创建一个 4096 位的 RSA 密钥对，并保存在一个 key 文件中，还有一个自签名的证书。


### 创建 TLS 版的反向代理

反向代理的配置文件 tls-proxy.conf:

```
upstream docker-registry {
    server registry:5000; # Link alias requirement
}

server {
    listen 443 ssl;
    # Use the localhost name for testing purposes
    server_name localhost;
    # A real deployment would use the real hostname where is it deployed
    # server_name mytotallyawesomeregistry.com;

    client_max_body_size 0;
    chunked_transfer_encoding on;

    # Note SSL configuration
    ssl_certificate /etc/nginx/conf.d/localhost.crt; 
    ssl_certificate_key /etc/nginx/conf.d/localhost.key; 

    # We're going to forward all traffic bound for the registry
    location /v2/ { # Note /v2 prefix
      proxy_pass                            http://docker-registry;
      proxy_set_header Host                 $http_host;
      proxy_set_header X-Real-IP            $remote_addr;
      proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto    $scheme;
      proxy_read_timeout                    900;
    }
}
```

Dockerfile 文件 tls-proxy.df:

```
FROM nginx
LABEL source=dockerinaction
LABEL category=infrastruction
COPY ["./tls-proxy.conf", \
      "./localhost.crt", \
      "./localhost.key", \
      "/etc/nginx/conf.d/"]
```

创建映像，开启并测试：

```bash
$ docker build -t dockerinaction/tls_proxy -f tls-proxy.df .

$ docker run -d --name tls-proxy -p 443:443 \
    --link personal_registry:registry \
    dockerinaction/tls_proxy

$ docker run --rm --net host \
    dockerinaction/curl -ks \ # Note k flag
    https://localhost:443/v2/distribution/tags/list

{"name":"distribution","tags":["2", "two"]}
```

curl 的 -k 选项会忽略请求中的所有证书错误，因此我们使用了自签名的语句，所有要使用该选项。

## 添加认证层

注册中心本身有 3 种认证机制，分别为 silly, token, htpasswd。当然，也可以在反向代理层配置认证机制。

silly 非常不安全，只能用于开发测试。

token, 使用 JSON web token(JWT)，Docker Hub 也是用的这种机制。注册中心使用这种机制，来验证调用者是否已经过第三方验证服务认证。因此，它也要求部署一个独立的认证服务。现成的几个开源 JWT 认证服务都还不适合生产环境下使用，因此建立使用 htpasswd 机制。

htpasswd 本身是 Apache 套件中的一个程序，它用于创建加密的用户名和密码对，而密码是用 bcrypt 加密的。

当采用 htpasswd 认证时，注意密码都是明文传输的，因此最好用 HTTPS。

htpasswd 认证既可以加到反向代理层，也可以加到注册中心。

先用 htpasswd 创建密码文件。创建一个安装了 htpasswd 的映像。Dockerfile 文件 htpasswd.df:

```
FROM debian:jessie
LABEL source=dockerinaction
LABEL category=utility
RUN apt-get update && \
    apt-get install -y apache2-utils
ENTRYPOINT ["htpasswd"]
```

创建映像：

```bash
$ docker build -t htpasswd -f htpasswd.df .
```

为密码文件新建一个新项：

```bash
$ docker run -it --rm htpasswd -nB <USERNAME>
```

+ <USERNAME> 写入用户名
+ -nB 选项指定使用 bcrypt 加密算法，并将结果输出到标准输出

输出结果会类似 `username:$2y$05$h2fDaJFn7nPyEMZeF4Hl2uyM9IYr9ofKIIKsrFkQbzvGC3H09ZZeW`，将这个结果复制到 registry.password 文件。

在 NGINX 中实现 HTTP Basic 认证，其配置文件 tls-auth-proxy.conf 如下：

```
upstream docker-registry {
    server registry:5000;
}

server {
    listen 443 ssl;
    # Use the localhost name for testing purposes
    server_name localhost;
    # A real deployment would use the real hostname where is it deployed
    # server_name mytotallyawesomeregistry.com;

    client_max_body_size 0;
    chunked_transfer_encoding on;

    # SSL
    ssl_certificate /etc/nginx/conf.d/localhost.crt; 
    ssl_certificate_key /etc/nginx/conf.d/localhost.key; 

    # We're going to forward all traffic bound for the registry
    location /v2/ { # Note /v2 prefix
      auth_basic "registry.localhost"; #Authentication realm
      auth_basic_user_file /etc/nginx/conf.d/registry.passwd;
      proxy_pass                            http://docker-registry;
      proxy_set_header Host                 $http_host;
      proxy_set_header X-Real-IP            $remote_addr;
      proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto    $scheme;
      proxy_read_timeout                    900;
    }
}
```

映像的 Dockerfile 文件 tls-auth-proxy.df:

```
FROM nginx:latest
LABEL source=dockerinaction
LABEL category=infrastruction
COPY ["./tls-auth-proxy.conf", \
      "./localhost.crt", \
      "./localhost.key", \
      "./registry.passwd", \
      "/etc/nginx/conf.d/"]
```

至此，可以创建并运行测试了。





















参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Running customized registries](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
