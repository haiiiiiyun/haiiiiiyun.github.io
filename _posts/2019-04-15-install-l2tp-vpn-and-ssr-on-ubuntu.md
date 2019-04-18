---
title: Run IPsec/L2TP VPN server and SSR server via Docker on Ubuntu 16.04
date: 2019-04-15
writing-time: 2019-04-15
categories: vpn;ssr;l2tp
tags: vpn;ssr;l2tp
---

# 1 Environment setup

# 1.1. Add User

```bash
#1. Use the adduser command to add a new user to your system.
ubuntu@server$ sudo adduser dev

#2. Use the usermod command to add the user to the sudo group
ubuntu@server$ sudo usermod -aG sudo dev

#3. Test sudo access on new user account
ubuntu@server$ su - dev
```

# 1.2. Install Docker

```bash
# install docker
# see: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-14-04
# The quickest way to install Docker is to download and install their installation script (you'll be prompted for a sudo password).
ubuntu@server$ sudo wget -qO- https://get.docker.com/ | sh
# The above command downloads and executes a small installation script written by the Docker team.

#Working with Docker is a pain if your user is not configured correctly, so add your user to the docker group with the following command.
ubuntu@server$ sudo usermod -aG docker dev  # add dev user to docker group

# install Docker-compose
# see: https://docs.docker.com/compose/install/#install-compose
#1. Run this command to download the latest version of Docker Compose:
#ubuntu@server$ sudo curl -L "https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#2. Apply executable permissions to the binary:
#ubuntu@server$ sudo chmod +x /usr/local/bin/docker-compose

# we should re-login to activate the `docker` daemon
```

# 2. Run IPsec/L2TP VPN server

# 2.1 Create a file `vpn/vpn.env` for holding credentials

```conf
# Define your own values for these variables
# - DO NOT put "" or '' around values, or add space around =
# - DO NOT use these special characters within values: \ " '
VPN_IPSEC_PSK=your_ipsec_pre_shared_key
VPN_USER=your_vpn_username
VPN_PASSWORD=your_vpn_password

# (Optional) Define additional VPN users
# - Uncomment and replace with your own values
# - Usernames and passwords must be separated by spaces
# VPN_ADDL_USERS=additional_username_1 additional_username_2
# VPN_ADDL_PASSWORDS=additional_password_1 additional_password_2

# (Optional) Use alternative DNS servers
# - By default, clients are set to use Google Public DNS
# - Example below shows using Cloudflare's DNS service
# VPN_DNS_SRV1=1.1.1.1
# VPN_DNS_SRV2=1.0.0.1
```

## 2.2 Start VPN Server

```bash
dev@server$ mkdir vpn
dev@server$ cd vpn

dev@server$ docker run \
    --name ipsec-vpn-server \
    --env-file ./vpn.env \
    --restart=always \
    -p 500:500/udp \
    -p 4500:4500/udp \
    -v /lib/modules:/lib/modules:ro \
    -d --privileged \
    hwdsl2/ipsec-vpn-server
```

That's it.

# 3. Run SSR server

```bash
$ mkdir shadowsocksr
$ cd shadowsocksr/
$ wget https://github.com/cndaqiang/shadowsocksr/archive/manyuser.zip
$ sudo apt-get install unzip
$ unzip manyuser.zip 
$ cd shadowsocksr-manyuser/
```

Customize config file `shadowsocksr-manyuser/config.json`.

```bash
sudo  python ./shadowsocks/server.py -c config.json -d start
sudo  python ./shadowsocks/server.py -c config.json -d stop
```

# 4. Enable BBR

```bash
$ sudo -i

# enable bbr
$ echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
$ echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf

# save
$ sysctl -p

# verify if enabled
$ sysctl net.ipv4.tcp_available_congestion_control
$ sysctl net.ipv4.tcp_congestion_control
```

# Resources
+ https://github.com/hwdsl2/docker-ipsec-vpn-server
+ https://hub.docker.com/r/hwdsl2/ipsec-vpn-server/
+ https://blog.csdn.net/DumpDoctorWang/article/details/81088880
+ https://github.com/shadowsocksr-backup/shadowsocksr
+ https://medium.com/@waylybaye/%E5%A6%82%E4%BD%95%E5%85%8D%E8%B4%B9%E6%89%93%E9%80%A0%E4%B8%80%E4%B8%AA%E5%AE%89%E5%85%A8%E7%A8%B3%E5%AE%9A%E8%B6%85%E9%AB%98%E9%80%9F%E7%9A%84%E7%A7%91%E5%AD%A6%E4%B8%8A%E7%BD%91%E7%8E%AF%E5%A2%83-fee52b7ad2f4
