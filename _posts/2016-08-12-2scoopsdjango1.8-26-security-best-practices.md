---
title: Django 安全最佳实践
date: 2016-08-12
writing-time: 2016-08-12 11:42
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

# 加固服务器

包括修改 SSH 商品，关闭/删除不必要的服务等。

# 理解 Django 的安全特性

包括：

+ 跨站脚本保护 XSS
+ 跨丫请求伪造保护 CSRF
+ SQL 注入保护
+ 劫持保护
+ 支持 TLS/HTTPS/HSTS，包括安全 cookie
+ 安全的密码存储，默认使用 PBKDF2 算法和 SHA256 哈希算法
+ 自动 HTML 转义
+ 一个能对付 XML Bomb 攻击的 expat 解析器
+ 加固了的 JSON、YAML 和 XML 序列化/反序列化工具

更多知识，见[官方文档相应页面](https://docs.djangoproject.com/en/1.8/topics/security/)

# 在生产环境下关闭 DEBUG 模式

关闭后，同时也要设置  **ALLOWED_HOSTS**，否则抛出的 *SuspiciousOperation** 错误而导致的 500 页会很难调试。

# 妥善保管  SECRET_KEY 等信息

# 全部采用 HTTPS

包括图片等静态文件也使用 HTTPS，不然出现的 "insecure resources" 警告信息会使用户离开我们的网站。

T

添加 django.middleware.security.SecurityMiddleware 的方式：

1.  添加 django.middleware.security.SecurityMiddleware 到 settings.MIDDLEWARE_CLASSES
1. 设置  settings.SECURE_SSL = True

需要注意的是， django.middleware.security.SecurityMiddleware 不会对 JS、CSS 和图片进行 HTTPS 重定向，需要在 Web 服务器进行配置。

关于 SSL 证书，应该从一个可信源购买一个，不要使用自签名的证书。比较方便快捷的应该是通过 namecheap.com 购买 Comodo Positive SSL 和 RapidSSL，两者都是 $10 左右一年，一般在 10 来分钟之内就能完成。

## 使用安全 cookie

应该告诉浏览器不要在非 HTTPS 下传输 cookies，设置如下：

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 使用 HTTP 严格传输安全协议（HSTS）

HSTS 可以在 Web 服务器级上设置，也可以在 Django 中设置（通过 settings.SECURE_HSTS_SECONDS)。

值得注意的是，HSTS是一个单向开头，一旦设置成了 N 秒，无法通知浏览器进行重置。因此不要将 HSTS 的 max-age 值设置超出你的可维护范围。

Wikipedia 上有关于 [HSTS 配置的示例段](https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security)，可以拿来使用。

当开启 HSTS 后，你的网页会包含一个 HTTP 头也指示那些支持 HSTS 的浏览器只能通过安全连接进行访问：

+ 浏览器会将 HTTP 连接重定向到 HTTPS
+ 如果无法进行安全连接（比如证书是自签名的或已过期），会抛出错误消息并禁止继续访问

一个 HSTS 应答头可能如下：

```conf
-Strict-Transport-Security: max-age=31536000; includeSubDomains
```

HSTS 配置的一些建议：

+ 尽可能使用 HSTS 的 **includeSubDomains**，它能防止通过非安全子域名向你域名写 cookie 的相关攻击
+ 初次部署时将 **max-age** 值设小一些，如 3600 (1 小时)。因此一旦设置后就无法重置。
+ 一旦确信网站已经没有问题了，再将 **max-age** 值设置成大一点，如 31536000 (12 个月) 或 63072000 (24 个人)。 

要注意的是，一旦 HSTS 使用了 **includeSubDomains**，所有的子域名都要使用 HTTPS，而且无法修改回使用 HTTP。

## HTTPS 配置工具

Mozilla 提供了一个 [SSL 配置生产工具](https://mozilla.github.io/server-side-tls/ssl-config-generatori/)。虽然不是很完美，但是如安全专家所说：“一般来说，HTTPS 总是 HTTP 好。”

设置好后，可能使用 [Qualys SSL Labs 的测试工具](https://www.ssllabs.com/ssltest/) 进行测试，看看我们配置的有多好，最好拿到 A+ 分 :)

# 使用 ALLOWED_HOSTS 验证

生产环境中一定要设置 ALLOWED_HOSTS，从而避免抛出 SuspiciousOperation 异常。

# 修改数据的表单一定要开启 CSRF 保护

# 避免跨站脚本攻击 XSS

## 优先使用 Django 模板系统，而不是 make_safe

即使是很少的 HTML 字符串，也尽量通用模板系统处理。

## 不要让用户有在 HTML Tag 上设置属性的功能

## 返回给 JavaScript 使用的数据先进行 JSON 编码

# 防御对 Python 代码注入攻击

## Python 内置可以执行代码的函数

小心使用 eval(), exec() 和 execfile()。如果你在项目中允许将任意字符串或文件转入到这些函数，就会有安全漏洞。更多 [Eval Really Is Dangerous by Ned Batchelder](http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html)。

## Python 标准库中可以执行代码的模块

> “Never unpickle data received from an untrusted or unauthenticated source.”

不可以使用 **pickle** 模块对用户发送来的数据进行反序列化。关于 pickle 的更多安全资料：

+ https://lincolnloop.com/blog/playing-pickle-security/
+ https://blog.nelhage.com/2011/03/exploiting-pickle/

## 能执行代码的第三方库

当使用 PyYAML 时，只使用 yaml.safe_load()。

## 避免使用基于 cookie 的会话

这种会话有几下问题：

+ 用户有可能看到会话的内容
+ 如果攻击者获知了项目的 SECRET_KEY，并且你的会话数据是基于 JSON 的，就可能被破解来伪造登录
+ 如果攻击者获知了项目的 SECRET_KEY，并且你的会话数据是基于 pickle 的，破解后不仅能伪造登录，而且可以上传任意可执行代码
+ 这种会话不能确保使其失效。攻击者可以一直使用旧会话数据。

# 所有进入 Django 表单的数据都要验证

# 禁止到有关支付表单项上的自动填充功能

包括信息卡、CVV、PIN 等。因此用户可能会在公共电脑上输入。

实现代码如下：

```python
from django import forms

class SpecialForm(forms.Form):
    my_secret = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off'}))
```

对于会在公共场合要填入的，考虑将输入项修改成 PasswordInput:

```python
from django import forms

class SecretInPublicForm(forms.Form):
    my_secret = forms.CharField(widget=forms.PasswordInput())
```

# 小心处理用户上传的文件

要完全安全地处理只能通过一个完全独立的域名进行处理。或者将上传的文件保存到 CDN 中。

服务器头要设置  **Content-Disposition: attachment** 来避免浏览器会自动显示这些内容。

## 当无法用 CDN 时

确保上传的文件保存到一个无法被执行的目录中。并且要将上传文件的后缀限制到一份白名单中。

## Django 与用户上传的文件

Django 有两个项能允许用户上传文件： FileField 和 ImageField。

如果只接受特定格式的文件类型，尽可能确保上传的就是这些类型：

+ 使用 [python-magic](https://github.com/ahupp/python-magic) 库检查上传的文件头
+ 使用专门针对该类型文件的 Python 库进行验证。例如 Django 的 ImageField 源码中就是用 PIL 库来验证的
+ 使用 defusedxml 而不是 Python 的内置 XML 库或 lxml

自定义的验证器这里不管用，因此它们是在项内容通过  to_python() 方法转化成 Python 对象后再进行验证的。

# 不要使用 ModelForms.Meta.exclude

使用 ModelForms 时，应该使用 Meta.fields。

# 不要使用 ModelForms.Meta.fields = "__all__"

# 小心 SQL 注入攻击

确保在原始 SQL 进行正确转义处理：

+ ORM 的 .raw()
+ ORM 的 .extra()
+ 直接访问数据库的指针

# 不要保存信用卡数据

推荐使用第三方服务如 Stripe、Braintree、Adyen、PayPal 等，然后将它们整合到项目中。

如果评估一个开源的电子商务解决方式，先了解下它是否将支付相关信息存放在了数据库中，如果是，那就换用其它的吧。

# 加固 Django Admin

## 修改默认的 Admin URL

默认的是 *yoursite.com/admin/*，将它修改成一个又长又难猜的。

## 使用 django-admin-honeypot

通过一个虚假的 admin/ 登录页将记录企图登录的用户信息。

## 只允许通过 HTTPS 访问 Admin

## 限制访问的 IP

限制 IP 可以在 Web 服务器级设置，如 [Django admin logins on Nginx](http://tech.marksblogg.com/django-admin-logins.html)。也可以通过在 django 的 middleware 中实现。


## 小心使用 allow_tags

通过 allow_tags 和 django.utils.html.format_html，HTML 标签就可以在 admin 中显示了。

推荐的原则是：只允许将 allow_tags 使用在系统生成的数据上，如主键、日期、计算结果等。而字符串和用户输入的数据上绝不能用。

## Admin Docs 与 Admin 采取一样的安全措施

因此 Admin Docs 中可以看到项目的体系结构，故可加以保护。


# 监测你的网站

定期检查网站的访问和错误日志。安装监测工具进行定义检查。

# 保持依赖包更新

推荐使用 [requires.io](https://requires.io/)，它能自动将 requirements 文件与 PyPI 上的版本进行核对。

# 防止点击劫持

见： https://docs.djangoproject.com/en/1.8/ref/clickjacking/

# 使用 defusedxml 来避免 XML Bomb 攻击









> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
