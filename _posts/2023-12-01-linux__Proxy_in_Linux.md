---
title: Proxy in Linux
date: 2023-12-01
tags: proxy ignore
categoris: Programming
---
curl use proxy5:

```bash
curl -x socks5h://localhost:8080 https://www.google.com
```

git command proxy5:

```bash
ALL_PROXY=socks5h://127.0.0.1:8080 git pull
```

or

```bash
git config --global http.proxy 'socks5h://127.0.0.1:8080'
git config --global --unset http.proxy
```

https://stackoverflow.com/questions/15227130/using-a-socks-proxy-with-git-for-the-http-transport

On Mac:

修改 `~/.ssh/config` 文件（不存在则新建）：

```
# 必须是 github.com
Host github.com
   HostName github.com
   User git
   # 走 HTTP 代理
   # ProxyCommand socat - PROXY:127.0.0.1:%h:%p,proxyport=8080
   # 走 socks5 代理（如 Shadowsocks）
   ProxyCommand nc -v -x 127.0.0.1:8080 %h %p
```

See https://gist.github.com/zhaozzq/9add1901333ed952561c6fd087869b37