---
title: Install wechat min program development environment on Ubuntu
date: 2024-03-11
tags: wechat
categoris: Programming
---

# Build with docker

## Install wine and wine-binfmt
```bash
sudo apt-get update
sudo apt-get install wine wine-binfmt
```

## Install docker and docker-compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

See https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04

## Clone 

```bash
$ git clone --recurse-submodules https://github.com/msojocs/wechat-web-devtools-linux.git
```

## Build with docker-compse

```bash
sudo docker-compose up
```

## Install icon

```bash
./tools/install-desktop-icon-node
```

# Usage

Start with command `bin/wechat-devtools`. Or just click the icon

See https://github.com/msojocs/wechat-web-devtools-linux