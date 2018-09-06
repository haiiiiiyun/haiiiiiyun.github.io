---
title: 在 Windows 上安装 Shadowsocks 并注册为服务运行
date: 2018-09-06
writing-time: 2018-09-06
categories: misc
tags: tools shadowsocks vpn windows
---

# 安装 Shadowsocks

## 下载安装 Python

[下载](https://www.python.org/downloads/windows/) 安装最新版的 Win 安装包，对应 32 位下载 x86版本，64 位下载 x86-64 版本。本次测试时下载的是 32 位 2.7 版本。

## 下载安装 OpenSSL

[下载](https://slproweb.com/products/Win32OpenSSL.html) 安装 OpenSSL, 也需根据系统是 32 位或 64 位下载对应的版本，并且不要安装 Light 版本。本次测试时下载安装的是 32位 v1.0.2p 版本。

## 安装 Shadowsocks

在 cmd 中进入 Python 安装目录的 Scripts 目录下安装：

```basic
cd C:\Python27\Scripts
pip install shadowsocks
```

## 配置和运行 Shadowsocks

直接运行：

```basic
ssserver.exe -p 8136 -k password -m aes-256-cfb
```

也可以将配置内容放置在 `ssserver.exe` 的相同目录下，文件名为 `shadowsocks.json`, 内容为：

```json
{
    "server":"0.0.0.0",
    "server_port":8136,
    "local_address":"127.0.0.1",
    "local_port":1080,
    "password":"87238136",
    "timeout":300,
    "method":"aes-256-cfb",
    "fast_open":false
}
```

并使用以下命令运行：`ssserver.exe -c C:\Python27\Scripts\shadowsocks.json`

# 用 instsrv 和 srvany 将 ssserver 注册为 Windows 服务

[下载](http://dl.pconline.com.cn/download/558946-1.html) instsrv.exe 和 srvany.exe 文件。

将下载的文件放置在 `C:\Python27\Scripts\` 下。

## 注册服务

```basic
instsrv Shadowsocks C:\Python27\Scripts\srvany.exe
```

上面的 Shadowsocks 即为自定义的服务名称。

## 卸载服务

```basic
instsrv Shadowsocks remove
```

## 配置服务

注册后，需对 srvany.exe 进行配置，定位实际要运行的程序信息。

运行 `regedit` 打开注册表，定位到 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Shadowsocks`。

如果该服务名下没有 Parameters 项，则在服务名项右键菜单中选择`新建->项`，名称为 Parameters，然后定位到 Parameters 项，新建以下几个字符串值:
+ 名称 Application 值为要作为服务运行的程序路径，这里为 `C:\Python27\Scripts\ssserver.exe`
名称 AppDirectory 值为你要作为服务运行的程序所在目录路径，这里为 `C:\Python27\Scripts`
名称 AppParameters 值为你要作为服务运行的程序启动所需要的参数，这里为 ` -c C:\Python27\Scripts\shadowsocks.json`

reg操作文件：

```
//****************************************************

 Windows Registry Editor Version  5.00
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Shadowsocks\Parameters]
"Application"="C:\\Python27\\Scripts\\ssserver.exe"
"AppDirectory"="C:\\Python27\\Scripts\\"
"AppParameters"="-c C:\\Python27\\Scripts\\shadowsocks.json"
```

## 测试运行

运行 `services.msc`，打开服务列表，定位到 `Shadowsocks` 服务测试。


# 相关链接

+ [用instsrv将普通exe程序注册为服务](https://blog.csdn.net/zzzili/article/details/54693361)
