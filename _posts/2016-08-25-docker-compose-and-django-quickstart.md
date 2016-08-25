---
title: Docker Compose 和 Django 入门
date: 2016-08-25
writing-time: 2016-08-25 08:44--09:43
categories: programming
tags: Docker
---

# 定义项目组件

本项目中，需要创建 Dockerfile、Python 依赖描述文件和一个 docker-compose.yml 文件。

1. 创建空的项目目录，该目录应该只包含构建 Docker 映像所需的资源。
2. 在项目目录中创建 Dockerfile 文件，文件中包含构建 Docker 映像的指令。
3. Dockerfile 中的内容如下：

```conf
# 基于 python 2.7 基映像文件
FROM python:2.7

# 相当于设置 python 命令行的 -u 选项
# 不缓冲stdin、stdout和stderr，默认是缓冲的。
ENV PYTHONUNBUFFERED 1 

# 映像中创建 /code 目录
RUN mkdir /code

# 将映像中的工作目录切换到 /code
WORKON /code

# 将项目目录下的 requirements.txt 挂载到映像中的 /code/ 下
ADD requirements.txt /code/

RUN pip install -r requirements.txt

# 将项目目录挂载到映像中的 /code
ADD . /code/
```

4. 在项目目录中创建 requirements.txt，内容如下：

```conf
Django
psycopg2
```

5. 在项目目录下创建 docker-compose.yml 文件，用来描述应用所需的依赖服务。本例中只有 Web 服务器和数据库两个服务。本文件还描述了哪个映像对应哪个服务、各服务的连接关系、容器内的挂载点及端口映射等。内容如下：

```yaml
version: '2'
services:
  db:
    image: postgres
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
```

# 创建一个 Django 项目

1. 创建 Django 项目目录，即在当前项目目录下运行：

```sheell
$ docker-compose run web django-admin.py startproject composeexample
```

由于 web 服务的映像还没有生成，Docker 会先构建出该映像，然后再启动容器，并在容器中执行 `django-admin.py startproject composeexample`。

2. 当命令完成后，查看项目文件：

```shell
$ ls -l
drwxr-xr-x 2 root   root   composeexample
-rw-rw-r-- 1 user   user   docker-compose.yml
-rw-rw-r-- 1 user   user   Dockerfile
-rwxr-xr-x 1 root   root   manage.py
-rw-rw-r-- 1 user   user   requirements.txt
```

可以看到生成的 composeexample 的所有者是 root，这是因为容器是以 root 身份运行的。因此要修改所有权：

```shell
sudo chown -R $USER:$USER .
```

由于 Django 1.8 等后续版本修改了项目目录结构，以上命令生成的 Django 项目目录结构会是：

```
composeexample/
    composeexample/
    manage.py
```

因此，当使用较新版本的 Django 时，docker-compose.yml 中的运行命令也应该由 `python manage.py runserver 0.0.0.0:8000` 调整为 `python composeexample/manage.py runserver 0.0.0.0:8000`。


# 连接数据库

1. 编辑 `composeexample/settings.py` 文件，数据库连接部分修改为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

# 开启所有服务

```shell
$ docker-compose up
Starting composepractice_db_1...
Starting composepractice_web_1...
Attaching to composepractice_db_1, composepractice_web_1
...
db_1  | PostgreSQL init process complete; ready for start up.
...
db_1  | LOG:  database system is ready to accept connections
db_1  | LOG:  autovacuum launcher started
..
web_1 | Django version 1.8.4, using settings 'composeexample.settings'
web_1 | Starting development server at http://0.0.0.0:8000/
web_1 | Quit the server with CONTROL-C.Starting composepractice_db_1...
Starting composepractice_web_1...
Attaching to composepractice_db_1, composepractice_web_1
...
db_1  | PostgreSQL init process complete; ready for start up.
...
db_1  | LOG:  database system is ready to accept connections
db_1  | LOG:  autovacuum launcher started
..
web_1 | Django version 1.8.4, using settings 'composeexample.settings'
web_1 | Starting development server at http://0.0.0.0:8000/
web_1 | Quit the server with CONTROL-C.
```


> 参考文献： 
> [Docker docs: Quickstart: Docker Compose and Django](https://docs.docker.com/compose/django/)
