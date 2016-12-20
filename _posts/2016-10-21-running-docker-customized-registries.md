---
title: 运行定制的 Docker 注册中心
date: 2016-10-21
writing-time: 2016-10-21 20:56--2016-12-20 14:40
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
+ notifications: 在该段可以用 Webhook 方式与其它项目整合
+ redis: 配置 Redis


# 增加集中式的注册中心

集中式的注册中心适合多人访问，故要将它发布到网上，这可以用 `docker run ... -p 80:5000 ...` 将主机 80 端口映射到容器的 5000 端口来实现。同时也要实现认证机制。

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

```nginx
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

```nginx
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
      auth_basic_user_file /etc/nginx/conf.d/registry.password;
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
      "./registry.password", \
      "/etc/nginx/conf.d/"]
```

至此，可以创建并运行这个基于 TLS 和 HTTP basic 的注册中心了。

在你的个人注册中心上添加 TLS 和 HTTP basic 认证很有用，但是生产环境下更适合将 TLS 连接中断到 Proxy 层。


下面的配置文件(tls-auth-registry.yml) 在默认的注册中心容器上添加了 TLS 和 HTTP basic 认证：

```yaml
version: 0.1
log:
    level: debug
    fields:
        services: registry
        environment: development
storage:
    filesystem:
        rootdirectory: /var/lib/registry
    cache:
        layerinfo: inmemory
    maintenance:
        uploadpurging:
            enabled: false
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    tls:
        certificate: /localhost.crt # TLS configuration
        key: /localhost.key
    debug:
        addr: localhost:5001
auth:  # Authentication configuration
    htpasswd:
        realm: registry.localhost
        path: /registry.password
```

包含该配置文件的 Dockerfile 文件：

```conf
# Filename: tls-auth-registry.df
FROM registry:2
LABEL source=dockerinaction
LABEL category=infrastructure
# Set the default argument to specify the config file to use
# Setting it early will enable layer caching if the 
# tls-auth-registry.yml changes.
CMD ["/tls-auth-registry.yml"]
COPY ["./tls-auth-registry.yml", \
    "./localhost.crt", \
    "./localhost.key", \
    "./registry.password", \
    "/"]
```

特别要注意的是，在生产环境中绝对不能将 Key 等文件复制到映像文件中，应该使用 Volumn 实现。

构建并运行：

```bash
$ docker build -t dockerinaction/secure_registry -f tls-auth-registry.df .

$ docker run -d --name secure_registry \
    -p 5443:5000 --restart=always \
    dockerinaction/secure_registry
```

若在注册中心本身上使用 TLS，再安装使用反向代理就会出现问题。这是因为应用层上的代理软件（如 NGINX, Apache httpd) 运行于 HTTP 协议上，它需要检查请求包来路由，但是由于注册中心使用了 TLS，那么请求流量都是密文了。因此，更好的方式是在代理层上使用 TLS。


## 客户端的兼容性

以下实现根据不同的请求，路由到不同的版本（未实现安全认证功能）。

反向代理配置文件 dual-client-proxy.conf

```nginx
upstream docker-registry-v2 {
    server registry2:5000
}
upstream docker-registry-v1 {
    server registry1: 5000;
}

server {
    listen 80;
    server_name localhost;

    client_max_body_size 0;
    chunked_transfer_encoding on;

    # V1 upstream routing
    location /v1/ {
      proxy_pass                            http://docker-registry-v1;
      proxy_set_header Host                 $http_host;
      proxy_set_header X-Real-IP            $remote_addr;
      proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto    $scheme;
      proxy_read_timeout                    900;
    }

    # V2 upstream routing
    location /v2/ {
      proxy_pass                            http://docker-registry-v2;
      proxy_set_header Host                 $http_host;
      proxy_set_header X-Real-IP            $remote_addr;
      proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto    $scheme;
      proxy_read_timeout                    900;
    }
}
```

Dockerfile dual-client-proxy.df:

```conf
FROM nginx:latest
LABEL source=dockerinaction
LABEL category=infrastructure
COPY ./dual-client-proxy.conf /etc/nginx/conf.d/default.conf
```

创建并运行：

```bash
$ docker build -t dual_client_proxy -f dual-client-proxy.df . # create image

$ docker run -d --name registry_v1 registry:0.9.1 # start registry v1

$ docker run -d --name dual_client_proxy \ # start reverse proxy
    -p 80:80 \
    --link personal_registry:registry2 \
    --link registry_v1:registry1 \
    dual_client_proxy

$ docker run --rm -u 1000:1000 \ # test v1 from host
    --net host \
    dockerinaction/curl -s http://localhost:80/v1/_ping

$ docker run --rm -u 1000:1000 \ # test v2 from host
    --net host \
    dockerinaction/curl -Is http://localhost:80/v2/
```

## 投入生产环境之前

生产环境与开发测试环境在以下方面有区别：安全管理、日志调优、Debug 及可靠的存储。

私钥等密码信息绝对不能提交到映像中：文件应通过 bind-mounting Volume 方式注入，而信息可通过环境变量注入。

注册中心会用于下面这些安全信息：

+ TLS private key
+ SMTP 用户名和密码
+ Redis secret
+ 各种远程存储帐号和 key pairs
+ client state signature key


以 `REGISTRY_` 为前缀的环境变量会覆盖配置文件中的对应项，如，配置文件中的：

```conf
http:
    secret: somedefaultsecret
```

可以通过 `REGISTRY_HTTP_SECRET` 环境变量来覆盖。

通过 `REGISTRY_LOG_LEVEL` 降低日志登记级别为 `error` 或 `warn`:

```bash
$ docker run -d -e REGISTRY_LOG_LEVEL=error registry:2
```

将 `debug` 设置为空串关闭调试：

```bash
$ docker run -d -e REGISTRY_HTTP_DEBUG='' registry:2
```

# 持久的 blob 存储

注册中心目前支持 4 种存储：

+ filesystem
+ azure
+ s3
+ rados


默认是 `filesystem`, 它只有一属性 `rootdirectory`，如：

```yaml
storage:
    filesystem:
            rootdirectory: /var/lib/registry
```

## 托管的远程存储 Microsoft Azure

使用 [Azure storage](http://azure.microsoft.com/services/storage/) 对应的配置文件：

```yaml
# filename: azure-config.yml
version: 0.1
log:
    level: debug
    fields:
        service: registry
        environment: development
storage:
    azure:
        accountname: your_account_name
        accountkey: your_base64_encoded_account_key
        container: your_container
        realm: core.windows.net
    cache:
        layerinfo: inmemory
    maintenance:
        uploadpurging:
            enabled: false
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
```

通过 Dockerfile 文件将上面的配置文件与原始映像文件整合：

```conf
# Filename: azure-config.df
FROM registry:2
LABEL source=dockerinaction
LABEL category=infrastructure
# Set the default argument to specify the config file to use
# Setting it early will enable layer caching if the 
# azure-config.yml changes.
CMD ["/azure-config.yml"]
COPY ["./azure-config.yml", "/azure-config.yml"]
```

## 托管的远程存储 Amazon Simple Storage Service

Amazon Simple Storage Service(S3) 比 AZure 更成熟，有加密、版本控制、访问审计、CDN 等功能。

```yaml
# Filename: s3-config.yml
version: 0.1
log:
    level: debug
    fields:
        service: registry
        environment: development
storage:
    cache:
        layerinfo: inmemory
    s3:
        accesskey: your_awsaccesskey
        secretkey: your_awssecretkey
        region: your_bucket_region
        bucket: your_bucketname
        encrypt: true
        secure: true
        v4auth: true
        chunksize: 5242880 # 5G
        rootdirectory: /s3/object/name/prefix
    maintenance:
        uploadpurging:
            enabled: false
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
```

```conf
# Filename: s3-config.df
FROM registry:2
LABEL source=dockerinaction
LABEL category=infrastructure
# Set the default argument to specify the config file to use
# Setting it early will enable layer caching if the 
# d3-config.yml changes.
CMD ["/s3-config.yml"]
COPY ["./d3-config.yml", "/d3-config.yml"]
```

## 通过 RADOS(Ceph) 使用网络远程存储

[Ceph](http://ceph.com) 这个项目提供了 Reliable Autonomic Distributed Object Store(RADOS)。可以用 Ceph 来创建你自己的 Azure Storage 或 AWS S3。使用这种方式时，配置文件如下：

```yaml
version: 0.1
log:
    level: debug
    fields:
        service: registry
        environment: development
storage:
    cache:
        layerinfo: inmemory
storage:
    rados: # RADOS configuration
        poolname: radospool
        username: radosuser
        chunksize: 4194304
    maintenance:
        uploadpurging:
            enabled: false
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
```

Ceph 将 blobs 存储在 pool 中。Chunk 对 Ceph 的内部数据表示很重要，见 [Ceph architecture]( http://ceph.com/docs/master/architecture/)。默认 chunksize 是 4M。

# 扩展访问及延时改善

通过使用反向代理和持久的后端存储，现在可以对注册中心进行水平扩展了。但是这样又会增加延时。

### 集成 metadata cache 来降低延时

可以使用 in-memory 或 [Redis](http://redis.io)。in-memory 适合小型的注册中心。如果用 Redis 的话，必须保证 Redis 服务器与本容器的网络的联通（如使用 joined network 的容器来运行 Redis）。以下配置文件中的 Redis 运行在 redis-host:6379 上：

```yaml
# Filename: redis-config.yml
version: 0.1
log:
    level: debug
    fields:
        service: registry
        environment: development
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
storage:
    cache: # cache configuration
        blobdescriptor: redis
    s3:
        accesskey: your_awsaccesskey
        secretkey: your_awssecretkey
        region: your_bucket_region
        bucket: your_bucketname
        encrypt: true
        secure: true
        v4auth: true
        chunksize: 5242880 # 5G
        rootdirectory: /s3/object/name/prefix
    maintenance:
        uploadpurging:
            enabled: false
redis: # Redis-specific details
    addr: redis-host:6379
    password: asecret
    dialtimeout: 10ms # connect timeout
    readtimeout: 10ms
    writetimeout: 10ms
    pool: # connection pool
        maxidle: 16 # minimum pool size
        maxactive: 64 # maximum pool size
        idletimeout: 300s
```

运行：

```bash
$ docker run -d --name redis redis
$ docker build -t dockerinaction/redis-registry -f redis-config.df .
$ docker run -d --name redis-registry \
    --link redis:redis-host -p 5001:5000 \
    dockerinaction/redis-registry
```

使用 cache 只能改善与 metadata 服务有关的延时。

## 使用 storage middleware 进行文件传输

使用 CDN 和 registry middleware 能提高下载速度。目前只支持使用一种 storage middle，即将你的注册中心、S3 存储后端与 AWS CloundFront 整合，CloundFront 是一种 CDN。

![注册中心 storage middle 与 AWS CloudFront 整合](/assets/images/dockerinaction/docker-registry-middleware.png)

下面的配置文件使用了 CloudFront:

```yaml
# Filename: scalable-config.yml
version: 0.1
log:
    level: debug
    fields:
        services: registry
        environment: development
http:
    addr: :5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
storage:
    cache: # cache configuration
        blobdescriptor: redis
    s3:
        accesskey: your_awsaccesskey
        secretkey: your_awssecretkey
        region: your_bucket_region
        bucket: your_bucketname
        encrypt: true
        secure: true
        v4auth: true
        chunksize: 5242880 # 5G
        rootdirectory: /s3/object/name/prefix
    maintenance:
        uploadpurging:
            enabled: false
redis: # Redis-specific details
    addr: redis-host:6379
    password: asecret
    dialtimeout: 10ms # connect timeout
    readtimeout: 10ms
    writetimeout: 10ms
    pool: # connection pool
        maxidle: 16 # minimum pool size
        maxactive: 64 # maximum pool size
        idletimeout: 300s
middleware: # Middleware configuration
    storage:
        - name: cloudfront
          options:
                baseurl: https://my.cloudfronted.domain.com/
                privatekey: path_to_pem
                keypairid: cloudfrontkeypairid
                duration: 3000
```

相关的配置项见 [CloudFront User Documentation](http://aws.amazon.com/cloudfront)。


# 通过 notification 集成

Notifaction 是一个简单地 webhook 型的集成工具。当你在注册中心的配置文件中提供了一个端点后，每当注册中心上有 push 或 pull 事件发生时，注册中心都会发送一条 HTTP 请求并上传一个 JSON 编码的事件。

Notification 能用于收集使用度量、触发部署，触发映像构建过程，发送邮件等。

下面的例子中，将使注册中心与 [Elasticsearch](https://github.com/elastic/elasticsearch) 和 Web 界面整合，为注册中心的事件创建一个可检索的数据库。

Elasticsearch 是一个可扩展的文档索引和数据库，它提供了能用来运行自己的搜索引擎的所有功能。Calaca 是一个用于 Elasticsearch 的开源 Web 界面。 本例中，它们各自在容器中运行。

![注册中心与 Elasticsearch 集成](/assets/images/dockerinaction/docker-distribute-integrate-elasticsearch.png)

先下载相关的映像：

```bash
$ docker pull elasticsearch:1.6
$ docker pull dockerinaction/ch10_calaca
$ docker pull dockerinaction/ch10_pump
```

`dockerinaction/ch10_calaca` 中的 Calaca 已经配置为了能使用运行在 localhost 上的 Elasticsearch 结点。这里的名字很重要，因为要符合 cross-origin resource sharing(CORS) 规则。

`dockerinaction/ch10_pump` 中运行一个 Node.js 服务，它监听 notifications 并过滤将 pull 和 push 事件转发到 Elasticsearch 结点。

注册中心上的每个有效事件都会产生 notification, 包含：

+ 仓库清单的上传和下载
+ Blob metadata 请求、上传和下载


Notification 用 JSON 格式分发，每个 notification 中都含一组事件，例如：

```json
{ "events": [{
  "id": "921a9db6-1703-4fe4-9dda-ea71ad0014f1",
  "timestamp": ...
  "action": "push",
  "target": {
    "mediaType": ...
    "length": ...
    "digest": ...
    "repository": ...
    "url": ...
  },
  "request": {
    "id": ...
    "addr": ...
    "host": ...
    "method": ...
    "useragent": ...
  },
  "actor": {},
  "source": {
    "addr": ...
    "instanceID": ...
  }
}]}
```

开启 Elasticsearch 和 pump:

```bash
$ docker run -d --name elasticsearch -p 9200:9200 \
    elasticsearch:1.6 -Des.http.cors.enabled=true

$ docker run -d --name es-pump -p 8000 \
    --link elasticsearch:esnode \
    dockerinaction/ch10_pump

$ docker run -d --name calaca -p 3000:3000 \
    dockerinaction/ch10_calaca
```

运行 elasticsearch 容器时通过开启 CORS 头，从而使得该容器能与 Calaca 整合。

这里的 calaca 容器没有关联 Elasticsearch 容器，这是因为本例中的 Calaca 容器已经配置为使用 localhost 上运行的 Elasticsearch 结点了。但是如果用的是 VirtualBox，还需要一些设置，因为 VirtualBox 用户还没有将他们的 elasticsearch 容器的端口绑定到 localhost，而是绑定到 VirtualBox 虚拟杣的 IP 地址上。可以用 VirtualBox 自带的 VBoxManage 程序进行设置，用下面的两条命令创建端口转发规则，将 localhost 上的端口转发到虚拟机上：

```conf
VBoxManage controlvm "$(docker-machine active)" natpf1 \
    "tcp-port9200,tcp,,9200,,9200"
VBoxManage controlvm "$(docker-machine active)" natpf1 \
    "tcp-port3000,tcp,,3000,,3000"
```

注册中心的配置文件中添加 notifications:

```yaml
# Filename: hooks-config.yml
version: 0.1
log:
    level: debug
    formatter: text
    fields:
        service: registry
        environment: development
storage:
    filesystem:
        rootdirectory: /var/lib/registry
    maintenance:
        uploadpurging:
            enabled: false
            age: 168h
            interval: 24h
            dryrun: false
http:
    addr: 0.0.0.0:5000
    secret: asecratforlocaldevelopment
    debug:
        addr: localhost:5001
notifications:
    endpoints:
        - name: webhookmonitor
          disabled: false
          url: http://webhookmonitor:8000/
          timeout: 500
          threshold: 5
          backoff: 1000
```

运行：

```bash
$ docker run -d --name ch10-hooks-registry -p 5555:5000 \
    --link es-pump:webhookmonitor \
    -v "$(pwd)"/hooks-config.yml:/hooks-config.yml \
    registry:2 /hooks-config.yml
```

测试时，通过 `http://localhost:3000/` 访问 Calaca 容器。

pull 和 push 操作后，就可以在搜索中得到相关的结果。


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Running customized registries](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
