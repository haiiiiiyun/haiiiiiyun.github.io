---
title: Raspberry 上安装 OSMC 实现大屏消息分发系统
date: 2017-08-21
writing-time: 2017-08-18--2017-08-21
categories: misc
tags: Raspberry&nbsp;Pi osmc xbmc kodi
---

# 安装系统

## 下载


到官方网站下载 [OSMC 映像文件](https://osmc.tv/download/)，当前版本是 OSMC_TGT_rbp2_20170803.img。

## 将系统写入 SD 卡

树莓派 3 支持的是 microSD 卡，我用的是 SanDisk microSDXC I。

在 Ubuntu 系统上先查看当前的硬盘信息：

```bash
$ sudo fdisk -l

Device     Boot     Start        End    Sectors   Size Id Type
/dev/sda1  *         2048  107319295  107317248  51.2G  7 HPFS/NTFS/exFAT
/dev/sda2       107319296  209717247  102397952  48.8G  7 HPFS/NTFS/exFAT
/dev/sda3       209719294  817717247  607997954 289.9G  5 Extended
/dev/sda4       817717248 1953519615 1135802368 541.6G  7 HPFS/NTFS/exFAT
/dev/sda5       209719296  809717759  599998464 286.1G 83 Linux
/dev/sda6       809719808  817717247    7997440   3.8G 82 Linux swap / Solaris

Partition 3 does not start on physical sector boundary.
Partition table entries are not in disk order.
```

由于我只有一个硬盘，该命令列出了我的 sda 硬盘的信息。

接着将 SD 卡插入系统，再次运行 fdisk 命令：

```bash
$ sudo fdisk -l

Device     Boot     Start        End    Sectors   Size Id Type
/dev/sda1  *         2048  107319295  107317248  51.2G  7 HPFS/NTFS/exFAT
/dev/sda2       107319296  209717247  102397952  48.8G  7 HPFS/NTFS/exFAT
/dev/sda3       209719294  817717247  607997954 289.9G  5 Extended
/dev/sda4       817717248 1953519615 1135802368 541.6G  7 HPFS/NTFS/exFAT
/dev/sda5       209719296  809717759  599998464 286.1G 83 Linux
/dev/sda6       809719808  817717247    7997440   3.8G 82 Linux swap / Solaris

Partition 3 does not start on physical sector boundary.
Partition table entries are not in disk order.



Disk /dev/mmcblk0: 14.9 GiB, 15931539456 bytes, 31116288 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000

Device         Boot Start      End  Sectors  Size Id Type
/dev/mmcblk0p1       8192 31116287 31108096 14.9G  c W95 FAT32 (LBA)
```

可以看到多了一个设备 `/dev/mmcblk0` ，这个就是 SD 卡。

将下载下来的系统映射文件解压， 解压过程需要点时间，解压后得到 OSMC_TGT_rbp2_20170803.img。

如果 SD 卡显示挂载了， 先将 SD 卡卸载。

使用 dd 命令将映像文件写入 SD 卡中：

```bash
$ sudo dd bs=8M if=OSMC_TGT_rbp2_20170803.img  of=/dev/mmcblk0
```

执行这个命令可能需要好几分钟。

至此，系统已经写入 SD 卡中。

# 上电及初始化设置

按照提示一步步设置 OSMC 的时区、语言、网络等，并开启 SSH服务。

假设设置的无线网卡（v3 内置有无线网卡和蓝牙）的地址是 192.168.31.199。

ssh 登录后进一步进行设置（默认的用户名和密码都是 osmc）：

```bash
$ ssh osmc@192.168.31.199
```

登录后，更新系统里的软件：

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

设置系统的键盘为 USA-English。

# 设置每天自动关机

在 /root/.bashrc 中添加 `export EDITOR=vi`，设置默认编辑器。


```bash
$ sudo apt-get install cron
$ sudo crontab -e
```

在文件的最后一行添加下列内容：

```
25 16 * * * /sbin/shutdown -h now
```

表示在每天的 16:25 执行关机命令 `shutdown -h now`。


# 添加插件源

File manager -> Add source: superrepo，添加的源地址为 http://srp.nu


# 实现启动后自动开启幻灯片播放功能

## 安装 Picture Slidershow Screensave 插件

Settings -> Add-on browser -> Install from repository -> Look and feel -> Screensaver -> Picture Slideshow Screensaver -> Install

## 设置 Picture Slideshow Screensaver 插件

Settings -> Add-on browser -> My add-ons -> Look and feel ->  Screensaver -> Picture Slideshow Screensaver -> Configure:

Basic:

Source of slideshow images: Image Folder

Home folder -> Pictures

Amount of seconds to display each image: 30s

Effect: Crossfade

Dim: 100%

Additional: Display background picture: 不选中

Auto-update: 不选中

Settings -> Interface -> Screensaver -> Wait time: 1m


参考： http://kodi.wiki/view/Add-on:Multi_Slideshow_Screensaver 和 https://discourse.osmc.tv/t/auto-start-slideshow-on-boot/1476


# 安装 Chorus2 进行 Web 管理

管理界面项目地址为 https://github.com/xbmc/chorus2

在 Settings -> Services -> Control 中进行设置。


# FTP 服务

## 安装 FTP 服务端

My Program -> App Store -> Ftp Server: Install


## 客户端

使用 [Filezilla ftp client](https://filezilla-project.org/download.php?type=client)


# VNC 服务

## 安装 VNC 服务端

第一步：安装编译所需的依赖包。

```bash
$ sudo apt-get install build-essential rbp-userland-dev-osmc libvncserver-dev libconfig++-dev unzip
$ cd /home/osmc
$ sudo wget https://github.com/patrikolausson/dispmanx_vnc/archive/master.zip
$ unzip master.zip -d  /home/osmc/
$ rm master.zip
$ cd dispmanx_vnc-master
$ make
```

第二步：将 vnc server 添加成为服务。

```bash
$ sudo cp dispmanx_vncserver /usr/bin
$ sudo chmod +x /usr/bin/dispmanx_vncserver
$ sudo cp dispmanx_vncserver.conf.sample /etc/dispmanx_vncserver.conf
$ sudo vi /etc/dispmanx_vncserver.conf
```

配置文件修改成为：

```conf
relative = false;
port = 0;
screen = 0;
unsafe = false;
fullscreen = false;
multi-threaded = false;
password = "mypassword";
frame-rate = 23;
downscale = false;
localhost = false;
vnc-params = "";
```

第三步：创建 service 文件，实现随系统自动启动。

```bash
$ sudo vi /etc/systemd/system/dispmanx_vncserver.service
```

内容修改为：

```conf
[Unit]
Description=VNC Server
After=network-online.target mediacenter.service
Requires=mediacenter.service

[Service]
Restart=on-failure
RestartSec=30
Nice=15
User=root
Group=root
Type=simple
ExecStartPre=/sbin/modprobe evdev
ExecStart=/usr/bin/dispmanx_vncserver
KillMode=process

[Install]
WantedBy=multi-user.target
```

最后，重启系统或者用以下命令开启 svn 服务：

```bash
$ sudo systemctl start dispmanx_vncserver.service
$ sudo systemctl enable dispmanx_vncserver.service
$ sudo systemctl daemon-reload
```

参考 [Install a vnc server on the Raspberry pi](https://discourse.osmc.tv/t/howto-install-a-vnc-server-on-the-raspberry-pi/1517)。


# 备份 SD 卡

```bash
cd workspace/
$ sudo dd bs=8M if=/dev/mmcblk0 of=OSMC_screen_delivery20170820.img
```
