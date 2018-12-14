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


# Certbot

$ sudo apt-get update
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot 

$sudo service nginx stop
sudo certbot certonly --standalone --email jiang.haiyun@gmail.com -d yun.xcitylab.com
hy@iZ23qrbzo5rZ:~/workspace/lets_encrypt/certbot$ sudo certbot certonly --standalone --email jiang.haiyun@gmail.com -d www.xcitylab.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator standalone, Installer None
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for www.xcitylab.com
http-01 challenge for api.xcitylab.com
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/api.xcitylab.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/api.xcitylab.com/privkey.pem
   Your cert will expire on 2019-01-06. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le

$sudo service nginx start

$ sudo certbot renew --dry-run


server {
    listen 443;
    server_name www.xcitylab.com, dev-api.xcitylab.com, api.xcitylab.com, dev-wx.xcitylab.com, wx.xcitylab.com, dev-yun.xcitylab.com, dev-rest.xcitylab.com, rest.xcitylab.com;

    ssl on;
    ssl_certificate /home/hy/workspace/lets_encrypt/signed.crt;
    ssl_certificate_key /home/hy/workspace/lets_encrypt/domain.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA;
    ssl_session_cache shared:SSL:50m;
    ssl_prefer_server_ciphers on;

    proxy_redirect http:// $scheme://;
    port_in_redirect on;

    location / {
        proxy_redirect off;
        proxy_set_header host $host:$server_port;
        proxy_set_header x-real-ip $remote_addr;
        proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
        proxy_set_header X-NginX-Proxy true;
        proxy_set_header X-Forwarded-Proto  $scheme;
        proxy_pass http://127.0.0.1:9999;
    }
    access_log /var/log/nginx/www.xcitylab.com_access.log;
}

https://letsencrypt.org/getting-started/
