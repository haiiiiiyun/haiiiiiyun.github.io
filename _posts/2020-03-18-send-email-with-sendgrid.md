---
title: 用 SendGrid 发送免费电子邮件
date: 2020-03-18
writing-time: 2020-03-18
categories: email;python;django
tags: email;python;django
---

# 1. 概述

[SendGrid](https://sendgrid.com/pricing/) 免费账号可以限额发送 100/天封邮件，虽然比 Mailgun 的每月 10000 封的免费额度少，但胜成注册无需绑定信息卡。

集成 SendGrid 有 SMTP 和 API 两种方式。官方提供了 Python, Java, GO, Node.js, Ruby, PHP, C# 等语言的 API 库。

# 2. 注册

[注册页](https://signup.sendgrid.com/) 中会有显示 reCAPTCHA 验证，若无显示，需要科学上网。

# 3. 集成测试

本文示例使用 Python 3.8 发送邮件。

## 3.1. 通过 API 库集成

注册后在 [api keys](https://app.sendgrid.com/settings/api_keys） 设置页面创建应用和 API KEY。

官方的 python API 库是 [sendgrid-python](https://github.com/sendgrid/sendgrid-python)， 通过 pip 安装：

```bash
$ pip install sendgrid
```

测试如下：

```python
import sendgrid
import os
from sendgrid.helpers.mail import *

def send_via_api():
    SENDGRID_API_KEY = "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"
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = Email("test@example.com")
    to_email = To("jiang.haiyun@qq.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

send_via_api()
```

```
202
b''
Server: nginx
Date: Wed, 18 Mar 2020 04:46:11 GMT
Content-Length: 0
Connection: close
X-Message-Id: yrcMLevLRju8p9cEz4cUFg
Access-Control-Allow-Origin: https://sendgrid.api-docs.io
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Authorization, Content-Type, On-behalf-of, x-sg-elas-acl
Access-Control-Max-Age: 600
X-No-CORS-Reason: https://sendgrid.com/docs/Classroom/Basics/API/cors.html
```

获取到的状态码 `202` 表示服务器已接收发送邮件请求。


## 3.2. 通过 SMTP 集成

注册后在 [SMTP 配置页](https://app.sendgrid.com/guide/integrate/langs/smtp) 创建 API key，创建后会有 SMTP 相关的配置信息，如：

```conf
Server	smtp.sendgrid.net
Ports	25, 587	(for unencrypted/TLS connections) 465	(for SSL connections)
Username	apikey
Password	your_api_key_value
```

之后可以连接 SMTP 服务器 `smtp.sendgrid.net` 来发送邮件，其中用户名为 `apikey`, 密码为 `your_api_key_value`。

测试如下：

```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_via_smpt():
    from_addr = "test@example.com"
    to_addr = "test@example.com"
    password = SENDGRID_API_KEY ="YOUR_API_KEY_VALUE"
    smtp_server = "smtp.sendgrid.net"
    username = "apikey"
    subject = "Sending with SendGrid is Fun"

    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(1)
    server.login(username, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

send_via_smpt()
```

# 资源

+ [SendGrid](https://sendgrid.com)
+ [sendgrid-python](https://github.com/sendgrid/sendgrid-python)
