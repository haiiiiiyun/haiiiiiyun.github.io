---
title: Flask Web App 大屏消息分发系统在树莓派 Raspberry Pi 上的部署
date: 2016-09-09
writing-time: 2016-09-08 12:47--2016-09-09 11:31
categories: programming
tags: Flask Python Raspberry&nbsp;Pi
---

# 一、 安装系统

## 1. 下载

到官方网站下载 [Raspbian 映像文件](https://www.raspberrypi.org/downloads/raspbian/)，当前版本是 RASPBIAN JESSIE， Version:May 2016, Release date:2016-05-27。下载下来的文件为 2016-05-27-raspbian-jessie.zip。

## 2. 将系统写入 SD 卡

树莓派 3 支持的是 microSD 卡，我用的是 SanDisk microSDXC I。

在 Ubuntu 系统上先查看当前的硬盘信息：

```bash
$ sudo fdisk -l

Device     Boot     Start       End   Sectors   Size Id Type
/dev/sda1            2048  20705279  20703232   9.9G 27 Hidden NTFS WinRE
/dev/sda2  *     20705280  20910079    204800   100M  7 HPFS/NTFS/exFAT
/dev/sda3        20910144 230661269 209751126   100G  7 HPFS/NTFS/exFAT
/dev/sda4       230661331 976771071 746109741 355.8G  5 Extended
/dev/sda5       230661333 440387796 209726464   100G  7 HPFS/NTFS/exFAT
/dev/sda6       440389908 650118419 209728512   100G  7 HPFS/NTFS/exFAT
/dev/sda7       650118483 771966016 121847534  58.1G  7 HPFS/NTFS/exFAT
/dev/sda8       872218624 973778943 101560320  48.4G 83 Linux
/dev/sda9       973780992 976771071   2990080   1.4G 82 Linux swap / Solaris
/dev/sda10      771966976 872216575 100249600  47.8G 83 Linux

Partition table entries are not in disk order.
```

由于我只有一个硬盘，该命令列出了我的 sda 硬盘的信息。

接着将 SD 卡插入系统，再次运行 fdisk 命令：

```bash
$ sudo fdisk -l

Device     Boot     Start       End   Sectors   Size Id Type
/dev/sda1            2048  20705279  20703232   9.9G 27 Hidden NTFS WinRE
/dev/sda2  *     20705280  20910079    204800   100M  7 HPFS/NTFS/exFAT
/dev/sda3        20910144 230661269 209751126   100G  7 HPFS/NTFS/exFAT
/dev/sda4       230661331 976771071 746109741 355.8G  5 Extended
/dev/sda5       230661333 440387796 209726464   100G  7 HPFS/NTFS/exFAT
/dev/sda6       440389908 650118419 209728512   100G  7 HPFS/NTFS/exFAT
/dev/sda7       650118483 771966016 121847534  58.1G  7 HPFS/NTFS/exFAT
/dev/sda8       872218624 973778943 101560320  48.4G 83 Linux
/dev/sda9       973780992 976771071   2990080   1.4G 82 Linux swap / Solaris
/dev/sda10      771966976 872216575 100249600  47.8G 83 Linux

Partition table entries are not in disk order.

Disk /dev/mmcblk0: 59.5 GiB, 63864569856 bytes, 124735488 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000


Device         Boot Start       End   Sectors  Size Id Type
/dev/mmcblk0p1      32768 124735487 124702720 59.5G  7 HPFS/NTFS/exFAT
```

可以看到多了一个设备 `/dev/mmcblk0` ，这个就是 SD 卡。

将下载下来的系统映射文件解压：

```bash
$ unzip ./2016-05-27-raspbian-jessie.zip
```

解压过程需要点时间，解压后得到 2016-05-27-raspbian-jessie.img。

如果 SD 卡显示挂载了， 先将 SD 卡卸载：

```bash
$ sudo umonut /dev/mmcblk0
```

使用 dd 命令将映像文件写入 SD 卡中：

```bash
$ sudo dd bs=1M if=2016-05-27-raspbian-jessie.img of=/dev/mmcblk0
```

执行这个命令可能需要好几分钟。

至此，系统已经写入 SD 卡中。

# 二、上电及初始化设置

按照提示一步步设置好后，更新系统里的软件：

```bash
# in root terminal
$ apt-get update
$ apt-get upgrade
```

# 三、网络设置

系统网络默认设置的是 DHCP，如果要设置成静态地址，需要修改 `/etc/network/interfaces` 文件：

在修改前最好先将原文件备份：

```bash
$ cp /etc/network/interfaces /etc/network/interfaces.bak
```

原始文件内容如下:

```conf
auto lo


iface lo inet loopback

iface eth0 inet dhcp


allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

如果用的是有线，可以将无线接口的内容全部删掉，再设置 IP 地址、网关和子网掩码：

```conf
auto lo

iface lo inet loopback

iface eth0 inet static

address 172.16.28.39
netmask 255.255.255.192
gateway 172.16.28.1
```

如果还需要修改 DNS，应修改 `/etc/resolv.conf` 文件，修改前最好也备份一下，内容如下：

```conf
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver 114.114.114.114
```

# 四、配置分辨率

本次连接的显示器是 SONY KDL-55HX750，分辨率为 1920X1080，即 1080p。

修改分辨率需要修改 `/boot/config.txt` 文件。

主要改两个参数，hdmi_group 和 hdmi_mode。

如果接的是电视机，则应设置为 `hdmi_group=1`。

CEA 规定的电视规格分辨率有：

```conf
hdmi_mode=1    VGA
hdmi_mode=2    480p  60Hz
hdmi_mode=3    480p  60Hz  H
hdmi_mode=4    720p  60Hz
hdmi_mode=5    1080i 60Hz
hdmi_mode=6    480i  60Hz
hdmi_mode=7    480i  60Hz  H
hdmi_mode=8    240p  60Hz
hdmi_mode=9    240p  60Hz  H
hdmi_mode=10   480i  60Hz  4x
hdmi_mode=11   480i  60Hz  4x H
hdmi_mode=12   240p  60Hz  4x
hdmi_mode=13   240p  60Hz  4x H
hdmi_mode=14   480p  60Hz  2x
hdmi_mode=15   480p  60Hz  2x H
hdmi_mode=16   1080p 60Hz
hdmi_mode=17   576p  50Hz
hdmi_mode=18   576p  50Hz  H
hdmi_mode=19   720p  50Hz
hdmi_mode=20   1080i 50Hz
hdmi_mode=21   576i  50Hz
hdmi_mode=22   576i  50Hz  H
hdmi_mode=23   288p  50Hz
hdmi_mode=24   288p  50Hz  H
hdmi_mode=25   576i  50Hz  4x
hdmi_mode=26   576i  50Hz  4x H
hdmi_mode=27   288p  50Hz  4x
hdmi_mode=28   288p  50Hz  4x H
hdmi_mode=29   576p  50Hz  2x
hdmi_mode=30   576p  50Hz  2x H
hdmi_mode=31   1080p 50Hz
hdmi_mode=32   1080p 24Hz
hdmi_mode=33   1080p 25Hz
hdmi_mode=34   1080p 30Hz
hdmi_mode=35   480p  60Hz  4x
hdmi_mode=36   480p  60Hz  4xH
hdmi_mode=37   576p  50Hz  4x
hdmi_mode=38   576p  50Hz  4x H
hdmi_mode=39   1080i 50Hz  reduced blanking
hdmi_mode=40   1080i 100Hz
hdmi_mode=41   720p  100Hz
hdmi_mode=42   576p  100Hz
hdmi_mode=43   576p  100Hz H
hdmi_mode=44   576i  100Hz
hdmi_mode=45   576i  100Hz H
hdmi_mode=46   1080i 120Hz
hdmi_mode=47   720p  120Hz
hdmi_mode=48   480p  120Hz
hdmi_mode=49   480p  120Hz H
hdmi_mode=50   480i  120Hz
hdmi_mode=51   480i  120Hz H
hdmi_mode=52   576p  200Hz
hdmi_mode=53   576p  200Hz H
hdmi_mode=54   576i  200Hz
hdmi_mode=55   576i  200Hz H
hdmi_mode=56   480p  240Hz
hdmi_mode=57   480p  240Hz H
hdmi_mode=58   480i  240Hz
hdmi_mode=59   480i  240Hz H
H means 16:9 variant (of a normally 4:3 mode).
2x means pixel doubled (i.e. higher clock rate, with each pixel repeated twice)
4x means pixel quadrupled (i.e. higher clock rate, with each pixel repeated four times)
```

由于我们的电视机是 1080p 的，因此设置 `hdmi_mode=16`。

如果接的是电脑显示器，则 `hdmi_group=2`， 同时 DMT 规定的分辨率如下：

```conf
hdmi_mode=1    640x350   85Hz
hdmi_mode=2    640x400   85Hz
hdmi_mode=3    720x400   85Hz
hdmi_mode=4    640x480   60Hz
hdmi_mode=5    640x480   72Hz
hdmi_mode=6    640x480   75Hz
hdmi_mode=7    640x480   85Hz
hdmi_mode=8    800x600   56Hz
hdmi_mode=9    800x600   60Hz
hdmi_mode=10   800x600   72Hz
hdmi_mode=11   800x600   75Hz
hdmi_mode=12   800x600   85Hz
hdmi_mode=13   800x600   120Hz
hdmi_mode=14   848x480   60Hz
hdmi_mode=15   1024x768  43Hz  DO NOT USE
hdmi_mode=16   1024x768  60Hz
hdmi_mode=17   1024x768  70Hz
hdmi_mode=18   1024x768  75Hz
hdmi_mode=19   1024x768  85Hz
hdmi_mode=20   1024x768  120Hz
hdmi_mode=21   1152x864  75Hz
hdmi_mode=22   1280x768        reduced blanking
hdmi_mode=23   1280x768  60Hz
hdmi_mode=24   1280x768  75Hz
hdmi_mode=25   1280x768  85Hz
hdmi_mode=26   1280x768  120Hz reduced blanking
hdmi_mode=27   1280x800        reduced blanking
hdmi_mode=28   1280x800  60Hz
hdmi_mode=29   1280x800  75Hz
hdmi_mode=30   1280x800  85Hz
hdmi_mode=31   1280x800  120Hz reduced blanking
hdmi_mode=32   1280x960  60Hz
hdmi_mode=33   1280x960  85Hz
hdmi_mode=34   1280x960  120Hz reduced blanking
hdmi_mode=35   1280x1024 60Hz
hdmi_mode=36   1280x1024 75Hz
hdmi_mode=37   1280x1024 85Hz
hdmi_mode=38   1280x1024 120Hz reduced blanking
hdmi_mode=39   1360x768  60Hz
hdmi_mode=40   1360x768  120Hz reduced blanking
hdmi_mode=41   1400x1050       reduced blanking
hdmi_mode=42   1400x1050 60Hz
hdmi_mode=43   1400x1050 75Hz
hdmi_mode=44   1400x1050 85Hz
hdmi_mode=45   1400x1050 120Hz reduced blanking
hdmi_mode=46   1440x900        reduced blanking
hdmi_mode=47   1440x900  60Hz
hdmi_mode=48   1440x900  75Hz
hdmi_mode=49   1440x900  85Hz
hdmi_mode=50   1440x900  120Hz reduced blanking
hdmi_mode=51   1600x1200 60Hz
hdmi_mode=52   1600x1200 65Hz
hdmi_mode=53   1600x1200 70Hz
hdmi_mode=54   1600x1200 75Hz
hdmi_mode=55   1600x1200 85Hz
hdmi_mode=56   1600x1200 120Hz reduced blanking
hdmi_mode=57   1680x1050       reduced blanking
hdmi_mode=58   1680x1050 60Hz
hdmi_mode=59   1680x1050 75Hz
hdmi_mode=60   1680x1050 85Hz
hdmi_mode=61   1680x1050 120Hz reduced blanking
hdmi_mode=62   1792x1344 60Hz
hdmi_mode=63   1792x1344 75Hz
hdmi_mode=64   1792x1344 120Hz reduced blanking
hdmi_mode=65   1856x1392 60Hz
hdmi_mode=66   1856x1392 75Hz
hdmi_mode=67   1856x1392 120Hz reduced blanking
hdmi_mode=68   1920x1200       reduced blanking
hdmi_mode=69   1920x1200 60Hz
hdmi_mode=70   1920x1200 75Hz
hdmi_mode=71   1920x1200 85Hz
hdmi_mode=72   1920x1200 120Hz reduced blanking
hdmi_mode=73   1920x1440 60Hz
hdmi_mode=74   1920x1440 75Hz
hdmi_mode=75   1920x1440 120Hz reduced blanking
hdmi_mode=76   2560x1600       reduced blanking
hdmi_mode=77   2560x1600 60Hz
hdmi_mode=78   2560x1600 75Hz
hdmi_mode=79   2560x1600 85Hz
hdmi_mode=80   2560x1600 120Hz reduced blanking
hdmi_mode=81   1366x768  60Hz
hdmi_mode=82   1080p     60Hz
hdmi_mode=83   1600x900        reduced blanking
hdmi_mode=84   2048x1152       reduced blanking
hdmi_mode=85   720p      60Hz
hdmi_mode=86   1366x768        reduced blanking
```

# 五、安装和配置 “大屏消息分发系统”

先建立一个工作目录：

```bash
$ mkdir workspace
```


下载项目源码，[这是 Github 仓库](https://github.com/haiiiiiyun/screen-message-delivery)：

```bash
$ git clone git@github.com:haiiiiiyun/screen-message-delivery.git
```

如果没有安装 pip (Python 2 >=2.7.9 及 Python 3 >=3.4 中都已经自带了) ，先安装：

```bash
# in root terminal
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
```

安装依赖包：

```bash
$ cd workspace
$ pip install -r requirements.py
```

安装 Chromium 软件



# 六、 设置自动启动

自动启动的功能：

+ 开机进行开启本系统的 Flask 后台服务
+ 自动打开 Chromium 并全屏显示
+ Chromium 显示本系统的展示页


完成以上功能只需将启动脚本添加到 `/etc/xdg/lxsession/LXDE-pi/autostart` 文件中：

```bash
# in root terminal
cd screen-message-delivery
cat "@bash /home/pi/workspace/screen-message-delivery/startup.sh" >> /etc/xdg/lxsession/LXDE-pi/autostart
```

# 七、运行图

## 树莓派
![树莓派](https://raw.githubusercontent.com/haiiiiiyun/screen-message-delivery/master/static/screenshots/raspberry.jpg)

### 首页

![首页](https://raw.githubusercontent.com/haiiiiiyun/screen-message-delivery/master/static/screenshots/homepage.jpg)

### 登录页

![登录页](https://raw.githubusercontent.com/haiiiiiyun/screen-message-delivery/master/static/screenshots/login.jpg)

### 消息类型设置页

![消息类型设置页](https://raw.githubusercontent.com/haiiiiiyun/screen-message-delivery/master/static/screenshots/settings.jpg)

### 屏幕显示页

![屏幕显示页](https://raw.githubusercontent.com/haiiiiiyun/screen-message-delivery/master/static/screenshots/screen.jpg)
