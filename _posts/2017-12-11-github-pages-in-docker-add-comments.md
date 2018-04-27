---
title: 在本机以 docker 方式运行 github pages 及添加评论系统 isso
date: 2017-12-11
writing-time: 2017-12-11
categories: blog
tags: github&nbsp;pages isso docker
---

# 在 docker 中运行 github-pages

使用 docker hub 中现存的映像文件 [starefossen/github-pages](https://hub.docker.com/r/starefossen/github-pages/)，这是它对应的 [Dockerfile](https://github.com/Starefossen/docker-github-pages/blob/master/Dockerfile)。

需要将 github page 乃至的各种插件 gem 及 github pages 的仓库地址都配置在 `_config.yml` 文件中，例如：

```yaml
# in _config.yml
repository: haiiiiiyun/haiiiiiyun.github.io
plugins:
- jekyll-paginate
- jekyll-github-metadata
- jekyll-mentions
- jekyll-redirect-from
- jekyll-sitemap
- jemoji
```

在本机运行的例子：

```bash
$ docker run \
  --name atjiang \
  -t \
  --restart always \
  -v "/home/hy/workspace/haiiiiiyun.github.io":/usr/src/app \
  -e JEKYLL_GITHUB_TOKEN=your_github_token \
  -p "9900:4000" starefossen/github-pages &
```


# 运行评论系统 isso

[isso](https://posativ.org/isso/) 是一个类似于 Disqus 的评论系统，支持匿名评论，可以将它集成到静态网站中。它的 github 地址是 [github.com/posativ/isso](https://github.com/posativ/isso)。

使用 docker hub 上现有的映像文件 [wonderfall/isso](https://hub.docker.com/r/wonderfall/isso/)，这是它对应的 [Dockerfile](https://github.com/Wonderfall/dockerfiles/tree/master/isso)。

## 配置

为 isso 创建配置文件 `isso.conf`:

```ini
[general]
; database location, check permissions, automatically created if not exists
dbpath = /db/comments.db
; your website or blog (not the location of Isso!)
; you can add multiple hosts for local development
; or SSL connections. There is no wildcard to allow
; any domain.
host = 
    http://www.atjiang.com/
    http://atjiang.com/
    http://fullstackpython.atjiang.com/
    http://localhost:8080
log-file = /db/logs
notify = smtp

[server]
listen = http://0.0.0.0:8080

[guard]
enabled = true
ratelimit = 2
direct-reply = 3
reply-to-self = true
require-author = true
require-email = false

[smtp]
; send email notification when receiving comments
host = smtp.sina.com
port = 465
security = ssl
username = your_name@sina.com
password = your_password
to = your_admin_account@gmail.com
from = your_name@sina.com
timeout = 10
```

配置文件中指定了数据库文件(sqlite 3) 及日志文件的位置。同时指定的需要使用该评论系统的域名。

这里使用新浪的 SMTP 服务来发送提醒，因此要注意 `[smtp]` 下的 `username` 和 `from` 的值必须一致。


在本机上为 isso 创建目录:

```bash
$ mkdir  -p ~/workspace/isso_comments
$ cd ~/workspace/isso_comments
```

将上面的配置文件 `isso.conf` 移到 `~/workspace/isso_comments` 目录下。

运行：

```bash
$ docker run \
  --name isso_comments \
  --restart always \
  -v "/home/hy/workspace/isso_comments":/config \
  -v "/home/hy/workspace/isso_comments":/db \
  -p "9902:8080" \
  wonderfall/isso &
```

访问 `http://localhost:9902/js/embed.min.js` 检测是否运行 isso 成功。

将上面的 isso 系统运行到服务器上，假设绑定的域名 "comments.my_isso.com"。

## 集成

在 github pages 的模板中加入：

```html
<script data-isso="//comments.my_isso.com/"
        data-isso-css="true"
        data-isso-lang="zh"
        data-isso-reply-to-self="false"
        data-isso-require-author="true"
        data-isso-require-email="false"
        data-isso-max-comments-top="10"
        data-isso-max-comments-nested="5"
        data-isso-reveal-on-click="5"
        data-isso-avatar="true"
        data-isso-avatar-bg="#f0f0f0"
        data-isso-avatar-fg="#9abf88 #5698c4 #e279a3 #9163b6 ..."
        data-isso-vote="true"
        data-vote-levels=""
        src="//comments.my_isso.com/js/embed.min.js"></script>
<section id="isso-thread"></section>
<noscript>请开启 JavaScript 查看 <a href="https://posativ.org/isso/" rel="nofollow">isso 评论系统的内容</a>。</noscript>
```

完成。

# 参考

+ [github pages docker 映射](https://hub.docker.com/r/starefossen/github-pages/)
+ [github pages docker 映射 Dockerfile](https://github.com/Starefossen/docker-github-pages/blob/master/Dockerfile)
+ [isso 评论系统 docker 映射文件](https://hub.docker.com/r/wonderfall/isso/)
+ [isso 评论系统 docker 映射 Dockerfile](https://github.com/Wonderfall/dockerfiles/tree/master/isso)
+ [isso github](https://github.com/posativ/isso)
+ [用ISSO自建静态博客的评论系统](https://www.jianshu.com/p/205f2fce3051)
