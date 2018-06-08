---
title: 申请和配置免费 HTTPS 证书 Let's Encrypt
date: 2018-04-27
writing-time: 2018-04-27
categories: programming
tags: Programming miniprogram https ssl
---

openssl genrsa 4096 > account.key

openssl genrsa 4096 > domain.key




# For multiple domains (use this one if you want both www.yoursite.com and yoursite.com)
openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:www.xcitylab.com,DNS:dev-api.xcitylab.com,DNS:api.xcitylab.com,DNS:dev-wx.xcitylab.com,DNS:wx.xcitylab.com,DNS:dev-yun.xcitylab.com,DNS:yun.xcitylab.com,DNS:dev-rest.xcitylab.com,DNS:rest.xcitylab.com")) > domain.csr

openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:www.xcitylab.com,DNS:yun.xcitylab.com")) > domain.csr


mkdir -p /home/hy/workspace/lets_encrypt/acme-challenges


```nginx
server {
    listen 80;
    server_name www.xcitylab.com dev-api.xcitylab.com api.xcitylab.com dev-wx.xcitylab.com wx.xcitylab.com dev-yun.xcitylab.com yun.xcitylab.com dev-rest.xcitylab.com rest.xcitylab.com;
    location ^~ /.well-known/acme-challenge/ {
        alias /home/hy/workspace/lets_encrypt/acme-challenges/;
        try_files $uri =404;
    }
}
```

wget https://raw.githubusercontent.com/diafygi/acme-tiny/master/acme_tiny.py


python acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir /home/hy/workspace/lets_encrypt/acme-challenges/ > ./signed.crt


wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > intermediate.pem
cat signed.crt intermediate.pem > chained.pem

```bash
# 下载脚本
wget -O - "https://gist.githubusercontent.com/JonLundy/f25c99ee0770e19dc595/raw/6035c1c8938fae85810de6aad1ecf6e2db663e26/conv.py" > conv.py

# 把private key 拷贝到你的工作目录
cp /etc/letsencrypt/accounts/acme-v01.api.letsencrypt.org/directory/<id>/private_key.json private_key.json

# 创建一个DER编码的private key
openssl asn1parse -noout -out private_key.der -genconf <(python conv.py private_key.json)

# 转换成PEM格式
openssl rsa -in private_key.der -inform der > account.key


```

openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:atjiang.com,DNS:www.atjiang.com,DNS:weapp.atjiang.com")) > domain.csr

# 参考

+[免费HTTPS证书Let's Encrypt安装教程](http://foofish.net/https-free-for-lets-encrypt.html)

https://letsencrypt.org
