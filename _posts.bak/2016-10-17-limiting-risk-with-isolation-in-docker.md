---
title: Docker 中通过隔离来限制风险
date: 2016-10-17
writing-time: 2016-10-17 09:59--2016-10-18 10:20
categories: programming
tags: Docker Programming Utility 《Docker&nbsp;in&nbsp;Action》
---

# 资源限制

Docker 使用了 cgroups 技术，因而可以控制容器的内存使用， CPU 权重、设备访问等。

## 内存限制

它限制容器中的进程可以使用的内存量。通过在 `docker run` 或 `docker create` 中加 `-m` 或 `--memory` 选项来实现限制，选项接受的值格式如下：

`<number><可选的一个单位> 其中单位=b(指byte), k(指kb), m(指mb) 或 g(指gb)`

开启一个最多能使用 256m 内存的数据库容器：

```bash
$ docker run -d --name ch6_mariadb \
    --memory 256m \
    --cup-shares 1024 \
    --user nobody \
    --cap-drop all \
    dockerfile/mariadb
```

这里只是限制为最多能使用 256m，并不是表示为该容器保留 256m 内存。在一个有 swap 的系统上，容器限制的内存甚至可以超过主机的物理内存。


## CPU 限制

有两种方法，一种是在 `docker run` 或 `docker create` 中的 `--cpu-shares` 选项中，为容器提供一个相对的权重，如：

```bash
$ docker run -d -P --name ch6_wordpress
    --memory 512m \
    --cpu-shared 512 \
    --user nobody \
    --cap-drp net_raw \
    --link ch6_raw \
    wordpress:4.1
```

上面开启的 MariaDB 容器，其相对 CPU 权重是 1024，而 WordPress 的为 512，应该 MariaDB 容器获取的 CPU 周期数为 WordPress 的两倍。如果再开一个权重为 2048 的容器，那么总权重份数为 1024+512+2048，而第三个容器获取的 CPU 周期数约占 2048/(1024+512+2048)=0.57。

![相对权重与 CPU 共享数](/assets/images/dockerinaction/docker-relative-weight-and-cpu-shares.png)

另一种方法是在 `docker run` 或 `docker create` 中使用 `--cpuset-cpus` 选项，将容器限制在某些核上运行。

在多核机器上，防止多个容器在相同核上运行，能最大化多核的使用。

```bash
# 将容器限制在编号为 0 的核上运行
$ docker run -d \
    --cpuset-cpus 0 \
    --name ch6_stresser dockerinaction/ch6_stresser

# 开启另一个容器来显示机器上 CPU 的负荷
$ docker run -it --rm dockerinaction/ch6_htop
```

`--cpuset-cpus` 的值可以为：

+ 单个 CPU 编号， 如 `0`
+ 以 `,` 分隔的多个 CPU 编号列表，如 `0,1,2`
+ 以 `-` 连接的 CPU 编号区间，如 `0-2`


## 限制对设备的访问

通过 `--device` 将主机上的设备挂载到容器中，如将主机上的摄像头设备挂载到容器中的相同位置：

```bash
$ docker -it --rm \
    --device /dev/video0:/dev/video0 \  # mount video0
    ubuntu:latest ls -al /dev
```

该选项可以使用多次，将多个设备挂载到容器中，格式为 `--device dev_path_on_host:dev_path_on_container`。


# 内存共享

这种类型的 IPC 性能好于基于网络或管道的 IPC。

## 在容器间共享 IPC 原语

dockerinaction/ch6_ipc 映像内包含有一个 producer 和 consumer，它们通过共享内存通信。producer 创建一个消息队列，并把消息广播到队列中，而 consumer 会从队列中提取消息并写入日志。开启两个容器并查看日志：

```bash
$ docker run -d -u nobody --name ch6_ipc_producer \
    dockerinaction/ch6_ipc -producer

$ docker run -d -u nobody --name ch6_ipc_consumer \
    dockerinaction/ch6_ipc -consumer

$ docker logs ch6_ipc_producer
$ docker logs ch6_ipc_consumer
```

上面的例子中，会出现 ch6_ipc_consumer 中没有任何日志，这是因为虽然这两个容器中的进程都引用了相同的共享内存资源，但是由于每个容器都有各自独立的共享内存命名空间，因此引用的是完全不同的内存。

如果想基于共享内存通信，通信的容器必须通过 `--ipc` 选项将 IPC 命名空间组合起来，这和 `--net` 选项是类似的：

```bash
$ docker rm -v ch6_ipc_consumer # remove original consumer
$ docker run -d --name ch6_ipc_consumer \
    --ipc container:ch6_ipc_producer \ # join IPC namespace
    dockerinaction/ch6_ipc -consumer 

$ docker logs ch6_ipc_producer
$ docker logs ch6_ipc_consumer
```

## 使用开放内存容器 (open memory container)

开放内存容器相互之间，以及与主机之间都能进行内存共享。它通过 `--ipc host` 实现：

```bash
$ docker run -d -u nobody --name ch6_ipc_producer \
    --ipc host \
    dockerinaction/ch6_ipc -producer

$ docker run -d -u nobody --name ch6_ipc_consumer \
    --ipc host \
    dockerinaction/ch6_ipc -consumer

$ docker rm -vf ch6_ipc_producer ch6_ipc_consumer
```

为减少冲突，应尽量少用这种类型的容器。


# 理解系统用户

在容器中 Docker 默认使用的是 root 用户。

## Linux USR 命名空间简介

Linux 最新的 user(USR) 命名空间允许将一个空间中的用户映射到另一个空间中，它和 PID 命名空间类似。

但是 Docker 还没有整合 USR 命名空间。因此容器中用户（组）和主机上的用户（组），只要 ID 相同，那么在容器和主机上都具有相同的权限。故容器中的高权限用户通过 Volume 可操作主机上的文件系统。

## 使用 run-as 用户

获取容器/映像中 run-as 用户的 3 种方法：

### 使用 `docker inspect` 获取

```bash
$ docker create --name bob busybox:latest ping localhost

$ docker inspect bob  # display all of bob's metadata

$ docker inspect --format "{{.Config.User}}" bob  # show only run-as user defined by bob's image
```

`--format` 选项能接受任何有效的 Go 语言模板。

这种方式有 2 个问题：

1. run-as 用户可能会被容器的启动脚本修改，因此，本方法获取的只是映像文件中配置的用户
2. 必须先从映像文件创建出一个容器后，方能获取，创建容器有一定的风险


就以上的问题，只能通过手动解压映像文件，查看它的 metadata 和启动脚本来解决，但这种方法又很费时。因此，最好通过运行一些简单的实验命令来检测默认用户。

以下能解决第 1 个问题：

```bash
$ docker run --rm --entrypoint "" busybox:latest whoami  # output: root

$ docker run --rm --entrypoint "" busybox:latest id # output: uid=0(root) gid=0(root) groups=IO(wheel)
```

以上的命令都先将容器的 entrypoint 清空，以确保容器只运行本命令中指定的程序，不执行默认的启动脚本。

创建容器时，可以通过 `--user` 或 `-u` 来修改容器中的默认 run-as 用户，但是指定的用户名必须要在映像中已经存在。

列出映像中的所有用户名：

```bash
$ docker run --rm busybox:latest awk -F: '$0=$1' /etc/passwd

root
daemon
bin
sys
sync
mail
www-data
operator
nobody
```

设定默认用户的例子：

```bash
$ docker run --rm \ 
    --user nobody \ # set run-as user to nobody
    busybox:latest id # output: uid=99(nobody) gid=99(nobody)

uid=99(nobody) gid=99(nobody)

# 也可以用 username:group 对
$ docker run --rm \
    -u nobody:www-data \ # set run-as user to nobody and group to www.data
    busybox:latest id

uid=99(nobody) gid=33(www-data)

# 也可以用 ID 值
$ docker run --rm \
    -u 99:33 \ # set UID and GID
    busybox:latest id

uid=99(nobody) gid=33(www-data)
```

通过容器，恶意软件可以很容易将用户改成 root，再通过 Volume 危害主机：

```bash
$ docker run -it --name escalation -u nobody \
    busybox:latest id \
    /bin/sh -c "whoami; su -c whoami" # output: "nobody" and then "root"
```

## 用户和 Volume

容器上的用户命名空间和主机上的用户命名空间是共享的。因此，容器中 root 用户，对于 Volume 中的文件系统，也有 root 权限，从而会对主机上的对应文件系统造成权限影响。下面是一个简单例子：

```bash
$ echo "e=mc^2" > garbage  # create a file on host
$ chmod 600 garbage # make file readable only by its owner
$ sudo chown root:root garbage # make file owned by root

$ docker run --rm -v "$(pwd)"/garbage:/test/garbage \
    -u nobody \
    ubuntu:latest cat /test/garbage # nobody can't read file

cat: /test/garbage: Permission denied

$ docker run --rm -v "$(pwd)"/garbage:/test/garbage \
    -u root \
    ubuntu:latest cat /test/garbage # root can read file

e=mc^2

$ sudo rm -f garbage # cleanup that garbage
```

克服这个难题的方法是事先计划好目标目录的用户和组：

```bash
$ mkdir logFiles
$ sudo chown 2000:2000 logFiles # set ownership of directory to desired user and group

# write important log file
$ docker run --rm -v "$(pwd)"/logFiles:/logFiles \
    -u 2000:2000 ubuntu:latest \
    /bin/bash -c "echo This is important info > /logFiles/important.log"

# append to log from another container
$ docker run --rm -v "$(pwd)"/logFiles:/logFiles \
    -u 2000:2000 ubuntu:latest \
    /bin/bash -c "echo More info >> /logFiles/important.log"


$ sudo rm -r logFiles
```

# 使用 capability 来调整对 OS 的功能访问

Docker 能调整容器中的进程针对主机上的 OS 功能的访问授权，这些功能访问授权称为 capability。 Docker 在创建容器时，会默认去除一组 capability，包括：

+ SETPCAP: 修改进程的 capability
+ SYS_MODULE: 插入/删除内核模块
+ SYS_RAWIO: 修改内核内存
+ SYS_PACCT: 配置进程的记账
+ SYS_NICE: 修改进程的优先级
+ SYS_RESOURCE: 覆盖资源的限制
+ SYS_TIME: 修改系统时钟
+ SYS_TTY_CONFIG: 配置 TTY 设备
+ AUDIT_WRITE: 写审计日志
+ AUDIT_CONTROL: 配置审计子系统
+ MAC_OVERRIDE: 忽略内核 MAC 策略
+ MAC_ADMIN: 配置 MAC 设置信息
+ SYSLOG: 修改内核的 print 行为
+ NET_ADMIN: 配置网络
+ SYS_ADMIN: 表示系统管理的全部功能


添加容器的 capability 用 `--cap-add`，去除容器的 capability 用 `--cap-drop`。 Linux 文档中的所有 capability 名都是以 `CAP_` 开头的全部大写字母，但是这里用其不带前缀的小字版本。例子：

```bash
$ docker run --rm -u nobody \
    ubuntu:latest \
    /bin/bash -c "capsh --print | grep net_raw"

Current: = cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap+i
    Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap

$ docker run --rm -u nobody \
    --cap-drop net_raw \ # drop NET_RAW capability
    ubuntu:latest \
    /bin/bash -c "capsh --print | grep net_raw" # no output

$ docker run --rm -u nobody \
    ubuntu:latest \
    /bin/bash -c "capsh --print | grep sys_admin" # no output

$ docker run --rm -u nobody \
    --cap-add sys_admin \
    ubuntu:latest \
    /bin/bash -c "capsh --print | grep sys_admin"

urrent: = cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_sys_admin,cap_mknod,cap_audit_write,cap_setfcap+i
Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_chroot,cap_sys_admin,cap_mknod,cap_audit_write,cap_setfcap
hp
```

# 运行一个全权限的容器

这种容器适于运行系统管理类的任务，它除了维护自己的文件系统和网络的隔离性外，能全权访问主机的共享内存、设备、所有的 capability 等。

在 `docker create` 和 `docker run` 中添加 `--privileged` 选项实现全权限容器，如：

```bash
$ docker run --rm \
    --privileged 
    ubuntu:latest id

uid=0(root) gid=0(root) groups=0(root)

$ docker run --rm \
   --privileged \
   ubuntu:latest capsh --print

Current: = cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,37+eip
Bounding set =cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,37
Securebits: 00/0x0/1'b0
secure-noroot: no (unlocked)
secure-no-suid-fixup: no (unlocked)
secure-keep-caps: no (unlocked)
uid=0(root)
gid=0(root)
groups=

$ docker run --rm \
    --privileged \
    ubuntu:latest ls /dev  # check out list of mounted devices

$ docker run --rm \
    --privileged \
    ubuntu:latest ifconfig  # examine network configuration
```

全权限容器的网络命名空间还是起作用的，要想和主机共用网络，用 `--net host` 选项。

# 利用增强工具使容器更健壮

## 指定额外的安全选项

Docker 通过 `--security-opt` 可以为 Linux 安全模块 (Linux Security Modules, LSM) 指定选项。LSM 是 Linux 上的操作系统与安全提供者的接口层。

AppArmor 和 SELinux 都是 LSM 提供者，它们都提供强制性的安全控制（mandatory access control, MAC，指由系统定义访问规则），并替换标准 Linux 上的默认访问控制（指由文件所有者定义访问规则）。

在 `docker run` 和 `docker create` 中，可多次使用 `--security-opt` 来传递多个值，传递的值有 6 种格式：

+ 设置一个 SELinux user label，用 `label:user:<USERNAME>`，其中 <USERNAME> 是你想用于该 label 的用户名
+ 设置一个 SELinux role label，用 `label:role:<ROLE>`, 其中 <ROLE> 是你想应用于容器中的进程上的角色名
+ 设置一个 SELinux type label，用 `label:type:<TYPE>`，其中 <TYPE> 是容器中进程的类型名
+ 设置一个 SELinux level label，用 `label:level:<LEVEL>`，其中 <LEVEL> 是容器中的进程要运行的 level 值
+ 在容器上关闭 SELinux 的 label 限制，用 `label:disable`
+ 将一个 APPArmor profile 应用到容器，使用 `label:apparmor:<PROFILE>`，其中 <PROFILE> 是 AppArmor 的 profile 名


SELinux 是一个标签系统。一组标签，称一个上下文 *context*，它被应用于每个文件和系统对象。类似的一组标签会应用于每个用户和进程上。进程若想与一个文件或系统资源交互，多组标签会自行计算，以决定是否允许或阻止该项行为。

人们通常用 AppArmor 来代替 SELinux 使用，因为它使用文件路径，不使用标签，同时还有一个训练模块，可以基于观察到的应用行为来被动地创建 profiles。

## 对 LXC 进行调优

Docker 原来是基于 Linux Container(LXC) 开发的，但是后期考虑可移植性，用一个新的容器运行时 libcontainer 来替换掉了 LXC。

但是 LXC 比 libcontainer 更成熟，有更多功能，因此如果不考虑移植性，在开启 Docker daemon 时可通过 `--exec-driver=lxc` 来切换回使用 LXC。使用 LXC 时，在 `docker run` 或 `docker create` 中可使用 `--lxc-conf` 选项向 LXC 传递配置选项：

```bash
$ docker run -d \
    --lxc-conf="lxc.cgroup.cupset.cpus=0,1" \ # limited to two CPU cores by LXC
    --name ch6_stresser dockerinaction/ch6_stresser

$ docker run -it --rm dockerinaction/ch6_htop

$ docker rm -vf ch6_stresser
```

由于这些配置是专门针对 LXC 的，并不通用，由此容器并不会理解这些配置项。


# 按需创建容器

根据实际情况，为容器开启最少权限，最多隔离性。



参考文献： 

+ [《Docker in Action》by Jeff Nickoloff: Limiting risk with isolation](https://www.amazon.com/Docker-Action-Jeff-Nickoloff/dp/1633430235/)
