---
title: 使用 Docker Compose 定义环境
date: 2016-10-24
writing-time: 2016-10-24 09:07--2016-12-21 13:20
categories: programming Docker
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》 Docker&nbsp;Compose docker-compose.yml
---

# Docker Compose

Compose 是一个用来定义、启动和管理服务的工具，而一个或多个 Docker 容器的组合被定义为一个服务。服务定义在 YAML 文件中，并被 docker-compose 程序管理。

Compose 能用来描述整合的环境及所有服务组件间的交互。

## 简单操作

本例用 Compose 管理一个 WordPress 环境。

新建一个目录 wp-example，在其中创建 docker-compose.yml:

```yaml
wordpress: # defines service named wordpress
  image: wordpress:4.2.2
  links:
    - db:mysql # Models link dependency on db service
  ports:
    - 8080:80 #Maps port 80 on container to port 8080 on host

db: # defines service named db
  image: mariadb
  environment:
    MYSQL_ROOT_PASSWORD: example # Sets administrative db password through env variable
```

在 wp-example 目录下使用 `docker-compose up` 来开启所有服务 :

```bash
$ docker-compose up

Creating wpexample_db_1...
Creating wpexample_wordpress_1...
```

可以使用的命令或快捷键：

+ 用 `Ctrl-C` 关闭全部服务
+ `docker-compose ps` 只列出本目录下的 docker-compose.yml 管理的容器
+ `docker-compose stop [name]` 或 `docker-compose kill [name]` 停止管理的容器或某个特定容器
+ `docker-compose rm [name]` 删除管理的所有容器或某个特定容器, 其中 `-f` 选项不是强制删除的意思，而是不显示验证阶段, `-v` 选项将一并删除其 Volume
+ `docker-compose logs [name1 [name2] [...] ]` 显示所管理的容器的日志
+ `docker-compose build [name1 [name2] [...] ]` 重新构建已更新的容器
+ `docker-compose pull` 下载所有映像


## 一个复杂的结构：注册中心和 Elasticsearch 集成

[运行定制的 Docker 注册中心](http://www.atjiang.com/running-docker-customized-registries/) 这篇文章中，将注册中心和 Elasticsearch 集成的例子，对应的 docker-compose.yml 如下：

```yaml
registry:
    build: ./registry
    ports:
        - "5555:5000" # map registry to port 5555 on host
    links:
        - pump:webhookmonitor # link registry to pump service

pump:
    build: ./pump
    expose:
        - "8000" # export port 8000 to dependent services
    links:
        - elasticsearch:esnode # link pump to elasticsearch service

elasticsearch:
    image: elasticsearch:1.6 # use official elasticsearch image
    ports:
        - "9200:9200"
    command: "-Des.http.cors.enabled=true" # pass flag to ElasticSearch that enables cross origin calls

calaca:
    build: ./calaca # use local sources for calaca service
    ports:
        - "3000:3000"
```

当使用 `docker-compose up` 来重启某个容器时，其相关的容器也必会被删除再重新构建开启，如果已经确保了相关容器无需重启，可加 `--no-dep`，如： `docker-compose up --no-dep -d registry`。

# docker-compose 环境的迭代

下面的例子中使用的容器及其关系如下：

![容器的依赖关系](/assets/images/dockerinaction/docker-compose-example.png)

本例的代码可以通过 `git clone https://github.com/dockerinaction/ch11_coffee_api.git` 获取，是一个有关咖啡店的元数据的 API 应用。

## 构建、开启和重构服务

```bash
$ docker-compose build # 构建相关映像, 由于大部分都使用了映像，只有 Coffee API 需要构建
```

coffee 应用的 Dockerfile 文件如下：

```conf
FROM python:2-onbuild
CMD [ "./entrypoint.sh" ]
```

而 `python:2-onbuild` 基映像对应的 Dockerfile 为：

```conf
FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN pip install --no-cache-dir -r requirements.txt

ONBUILD COPY . /usr/src/app
```

使用这种 python 基映像无法加入 pip 的镜像设置，构建时通过 pip 安装较慢。因此，先在 coffee 目录下创建一个 pip 镜像配置文件 pip.conf:

```conf
[global]
trusted-host =  mirrors.aliyuncs.com
index-url = http://mirrors.aliyuncs.com/pypi/simple
```

再将 coffee 的 Dockerfile 修改为：

```conf
FROM python:2.7

COPY ./pip.conf /etc/pip.conf

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "./entrypoint.sh" ]
```

之后再 `docker-compose build` 会快很多。


```bash
$ docker-compose pull # 下载用到的映像

$ docker-compose up -d db # 开启 db 服务

$ docker-compose up -d # 全部重新开启，可以看到即便 db 已经开启了，也会进行重启

$ docker-compose up --no-dep -d proxy # 重建并重启 proxy，使用 --no-dep 保证其依赖服务不重启
```

运行后，通过 http://localhost:8080/api/coffeeshops/ 访问，应该可以看到类似 `{"coffeeshops": []}` 的 JSON 内容。

通过 curl 添加内容：

```bash
$ curl -H "Content-Type: application/json" \
    -X POST \
    -d '{"name":"Albina Press", "address": " 5012 Southeast Hawthorne
        Boulevard, Portland, OR", "zipcode": 97215, "price": 2,
        "max_seats": 40, "power": true, "wifi": true}' \
    http://localhost:8080/api/coffeeshops/
```

刷新 /api/coffeeshops/ 页面，现可看到：

```json
{
  "coffeeshops": [
    {
      "address": " 5012 Southeast Hawthorne Boulevard, Portland, OR", 
      "id": 1, 
      "max_seats": 40, 
      "name": "Albina Press", 
      "power": true, 
      "price": 2, 
      "wifi": true, 
      "zipcode": 97215
    }
  ]
}
```

现在为该应用添加一个 ping 功能，以便负载均衡器能方便检查应用的可用性。

先核实当前 /api/ping 还没有实现，然后在 `./coffee/app/api.py` 中添加：

```python
@api.route('/ping')
def ping():
    return os.getenv('HOSTNAME')
```

重构重启后就能使用 ping 功能了：

```bash
$ docker-compose build coffee
$ docker-compose up -d
```

## 扩容和删除服务

假设现在要扩展 coffee 服务，即并行运行多个 coffee 服务。先查看当前运行的情况：

```bash
$ docker-compose ps coffee
         Name                Command       State            Ports          
--------------------------------------------------------------------------
ch11coffeeapi_coffee_1   ./entrypoint.sh   Up      0.0.0.0:32770->3000/tcp 
```

可以看到，当前只有一个 coffee 服务运行，并且主机的 32770 端口映射到了容器的 3000 端口。

进行扩容：

```bash
$ docker-compose scale coffee=5 # 扩展到共 5 个服务
WARNING: The "coffee" service specifies a port on the host. If multiple containers for this service are created on a single host, the port will clash.
Creating and starting ch11coffeeapi_coffee_2 ... done
Creating and starting ch11coffeeapi_coffee_3 ... done
Creating and starting ch11coffeeapi_coffee_4 ... done
Creating and starting ch11coffeeapi_coffee_5 ... done


$ docker-compose ps coffee # 可看到当前共有 5 个服务在运行
         Name                Command       State            Ports          
--------------------------------------------------------------------------
ch11coffeeapi_coffee_1   ./entrypoint.sh   Up      0.0.0.0:32770->3000/tcp 
ch11coffeeapi_coffee_2   ./entrypoint.sh   Up      0.0.0.0:32771->3000/tcp 
ch11coffeeapi_coffee_3   ./entrypoint.sh   Up      0.0.0.0:32772->3000/tcp 
ch11coffeeapi_coffee_4   ./entrypoint.sh   Up      0.0.0.0:32774->3000/tcp 
ch11coffeeapi_coffee_5   ./entrypoint.sh   Up      0.0.0.0:32773->3000/tcp 
```

可以这样进行扩容是因为 coffee 容器的 3000 指定被绑定到了主机的 0 端口，因此会被动态分配，不会出现端口冲突的问题。

缩放回只运行一个 coffee 服务：

```bash
$ docker-compose scale coffee=1
Stopping and removing ch11coffeeapi_coffee_2 ... done
Stopping and removing ch11coffeeapi_coffee_3 ... done
Stopping and removing ch11coffeeapi_coffee_4 ... done
Stopping and removing ch11coffeeapi_coffee_5 ... done

$ docker-compose ps coffee
         Name                Command       State            Ports          
--------------------------------------------------------------------------
ch11coffeeapi_coffee_1   ./entrypoint.sh   Up      0.0.0.0:32770->3000/tcp 
```

## 迭代与持久化状态

当 Compose 重构服务时，其关联的受管理 Volumes 不会被删除，当服务重构后，它们会被重新关联到该服务。这也意味着迭代更新时数据不会丢失。受管理 Volumes 只在使用 `docker-compose rm -v` 后，删除最后一个容器时才会被清除。

最大的问题是保持环境的状态，比如在环境配置文件修改后也能保持。比如当 coffee 服务运行后，在 docker-compose.yml 中将该服务名改为了 api，那么重构后，Compose 将不会了解旧的 coffee 服务和新的 api 服务的关联性。

## 关联问题与网络

Docker 在构建容器关联时，是通过新建防火墙规则，并将 service discovery info 相关信息注入到依赖容器的环境变量和 /etc/hosts 文件中来实现的。

在上面的例子中， proxy 依赖 coffee 服务，当只重构 coffee 服务后，coffee 服务的 IP 可能会改变，那么 proxy 可能无法访问 coffee 服务。解决此问题的最好方法是重构所有的服务。


# 开启一个新项目： Compose YAML 的三个例子

## 构建、环境、metadata、网络

`coffee` 服务在 docker-compose.yml 中的定义：

```yaml
coffee:
    build: ./coffee # Build from Dockerfile located under ./coffee
    user: 777:777
    restart: always
    expose: # Expose and map ports for containers
        - 3000
    ports:
        - "0:3000" # 3000 in container-> dynamic port on host
    links:
        - db:db
    environment: # Set environment to use a database
                 # 环境变量也可以通过一个或多个 env_file 键指定，指定的文件中可包含多个环境变量定义
        - COFFEEFINDER_DB_URI=postgresql://postgres:development@db:5432/po..
        - COFFEEFINDER_CONFIG=development
        - SERVICE_NAME=coffee
    labels: # Label the service，使用 label 来保持映像和容器的 metadata
        com.dockerinaction.chapter: "11"
        com.dockerinaction.example: "Coffee API"
        com.dockerinaction.role: "Application Logic"
```

## 已知的组件与 bind-mount volumes

使用第三方映像时，要先测试，再引用 content-addressable 的映像，确保使用的就是测试的那个版本。

proxy 和 db 服务都使用了 content-addressable 的映像：

```yaml
db:
    image: postgres@sha256:66ba100bc635be17... # Use content-addressable images for trusted version
    volumes_from:
        - dbstate # use a data container pattern
    environment:
        - PGDATA=/var/lib/postgresql/data/pgdata
        - POSTGRES_PASSWORD=development
    labels:
        com.dockerinaction.chapter: "11"
        com.dockerinaction.example: "Coffee API"
        com.dockerinaction.role: "Database"

proxy:
    image: nginx@sha256:a2b8bef333864317... # use content-addressable image
    restart: always
    volumes:
        - ./proxy/app.conf:/etc/nginx/conf.d/app.conf # inject conf via volume
    ports:
        - "8080:8080"
    links:
        - coffee
    labels:
        com.dockerinaction.chapter: "11"
        com.dockerinaction.example: "Coffee API"
        com.dockerinaction.role: "Load Balancer"
```

docker-compose.yml 中可用的鍵，可查看 https://docs.docker.com/compose/yml/。

## Volume 容器和扩展的服务

Compose 服务也有类似类的继承功能。例如，本例子中，先定义一个服务 data:

```yaml
data:
    image: gliderlabs/alpine
    command: echo Data Container
    user: 999:999
    labels:
        com.dockerinaction.chapter: "11"
        com.dockerinaction.example: "Coffee API"
        com.dockerinaction.role: "Volume Container"
```

这个服务没有定义 Volume，只是定义了一个原型，待子服务 dbstate 扩展：

```yaml
dbstate:
    extends:
        file: docker-compose.yml # Reference to parent service via file/service keys
        service: data
    volumes:
        - /var/lib/postgresql/data/pgdata
```

扩展相当于在 Dockerfile 中使用了 `FROM` 命令，即 dbstate 将 data 作为它的基映像，data 的所有属性都被dbstate 继承。


参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Declarative environments with Docker Compose](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
