---
title: 在 Ubuntu 16.04 上配置 SSR 客户端并通过 Privoxy 转换为 HTTP 代理
date: 2018-01-31
writing-time: 2018-01-31
categories: programming
tags: Programming SSR Sock5 Privoxy HTTP proxy VPN Ubuntu android&nbsp;amulator&nbsp;proxy
---

# Ubuntu SSR 客户端

在 [github](https://github.com/the0demiurge/CharlesScripts/blob/master/charles/bin/ssr) 上下载最新的 SSR 客户端脚本，下载为 `~/opt/ssr.sh`。

设置权限，安装和配置：

```bash
$ cd ~/opt
$ chmod 766 ./ssr.sh
$ ./ssr.sh install
$ ./ssr.sh config
```

配置信息格式为:

```json
{
  "server": "x.x.x.x",
  "server_ipv6": "::",
  "server_port": 2333,
  "local_address": "127.0.0.1",
  "local_port": 1080,
  "password": "xxx",
  "group": "xxx",
  "obfs": "tls1.2_ticket_auth",
  "method": "aes-192-ctr",
  "ssr_protocol": "auth_sha1_v4",
  "obfsparam": "",
  "protoparam": "",
  "udpport": "0",
  "uot": "0"
}
```

可以在 https://ssssssssjshhd.herokuapp.com/ 等网站上获取免费 SSR 信息。

# 安装配置 Privoxy

```bash
$ sudo apt-get install privoxy
```

配置文件位置： `/etc/privoxy/config`。

+ 将 `# listen-address localhost:8118` 这行注释去掉。
+ 在配置文件最后添加两行：
    - `forward-socks5 / 127.0.0.1:1080 .`
    - `listen-address 127.0.0.1:8118`

运行 `sudo service privoxy start` 即可。

日志文件位置： `/var/log/privoxy/logfile`。

# Android Studio 3.0.1 模拟器中使用代理

模块器中设置代理的方式：

+ 在模拟器设置页中设置为使用 Android Stuido 的代理，或者手动设置为 `http://127.0.0.1:8118` 的代理。
+ 在 Android Terminal 中使用 `cd ~/Android/Sdk/tools && emulator -avd Nexus_5X_API_23 -http-proxy http://127.0.0.1:8118 -debug-proxy` 开启模块器并设置代理。


再 2 种方法都没有尝试成功，虽然在 Privoxy 的日志文件中都有连接记录，但是模拟器的浏览器中访问被墙网站都 TIMED_OUT，但是访问未被墙网站正常。

最后尝试直接在 Java 网络连接代码中使用代理，尝试成功：

```java
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.Proxy;

//in class ...
public byte[] getUrlBytes(String urlSpec) throws IOException {
    URL url = new URL(urlSpec);
    Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("10.0.2.2", 8118));
    HttpURLConnection connection = (HttpURLConnection) url.openConnection(proxy);

    try {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        InputStream in = connection.getInputStream();

        if (connection.getResponseCode() != HttpURLConnection.HTTP_OK) {
            throw new IOException(connection.getResponseMessage() +
                ": with " + urlSpec );
        }

        int bytesRead = 0;
        byte[] buffer = new byte[1024];
        while ((bytesRead = in.read(buffer)) > 0) {
            out.write(buffer, 0, bytesRead);
        }
        out.close();
        return out.toByteArray();
    } finally {
        connection.disconnect();
    }
}
```

其中 `10.0.2.2` 地址为 Android 模拟器中访问开发机的地址。

# 参考

+ [ubuntu安装ssr客户端](http://blog.csdn.net/Martind/article/details/78951425)
+ [shadowsocsR+privoxy liunx下使用SSR全局代理](https://kinoko3.github.io/2017/10/18/shadowsocsR-privoxy-liunx%E4%B8%8B%E4%BD%BF%E7%94%A8SSR%E5%85%A8%E5%B1%80%E4%BB%A3%E7%90%86/)
