---
title: HTTP Basic, Session, Token 三种认证方法简介
date: 2020-03-13
writing-time: 2020-03-13
categories: http web authentication authorization
tags: http web authentication authorization
---

# 1. 概述

本文简介 HTTP Basic，Session，Token 三种认证方法。

+ Basic 认证：户籍部门已给你签发了一张身份证。你每次去办事，都要带上身份证证，后台要拿你的身份证去系统上查一下。
+ Session 认证：户籍部门已给你签发了一张身份证，但只告诉你身份证号码。你每次去办事，只要报出你的身份证号码，后台要查一个即否有效。
+ Token 认证：户籍部门已给你签发了一张有防伪功能的身份证。你每次去办事，只要出示这张卡片，它就知道你一定是自己人。 


# 2. HTTP Basic 认证

这是一种最基本的认证方法。

在这种认证方法下，用户每次发送请求时，请求头中都必须携带能通过认证的身份信息。

其交互过程如下：

1. 开始时，客户端发送未携带身份信息的请求。
2. 服务端返回 401 Unauthorized 状态，并在返回头中说明要用 `Basic` 方法进行认证： `WWW-Authenticate: Basic`。
3. 客户端重新发送请求，并将身份信息包含在请求头中: `Authorization: Basic aHk6bXlwYXNzd29yZA==`。
4. 服务端验证请求头中的身份信息，并相应返回  200 OK 或 403 Forbidden 状态。
5. 之后，客户端每次发送请求都在请求头中携带该身份信息。


```
客户端                                                          服务端
------                                                          ------

1----------------------------------------->
GET / HTTP/1.1

                                           <-------------------------2
                                            HTTP/1.1 401 Unauthorized
                                            WWW-Authenticate: Basic

3----------------------------------------->
GET / HTTP/1.1
Authorization: Basic aHk6bXlwYXNzd29yZA==

                                            <------------------------4
                                                       HTTP/1.1 200 OK

5----------------------------------------->
GET /another-path/ HTTP/1.1
Authorization: Basic aHk6bXlwYXNzd29yZA==
```

其中传送的身份信息是 `<username>:<password>` 经 base64 编码后的字串。如本例中的 `aHk6bXlwYXNzd29yZA==`， 经 base64 解码后为 `hy:mypassword`。

这种认证方法的优点是简单，容易理解。

缺点有：

+ 不安全：认证身份信息用明文传送，因此需结合 https 使用。
+ 效率低：服务端处理请求时，每次都需要验证身份信息，如用户名和密码。


# 3. Session 认证

这种认证方法结合了 Session 和 Cookie。服务端将本次会话信息以 Session 对象的形式保存在服务端的内存、数据库或文件系统中，并将对应的 Session 对象 ID 值 SessionID 以 Cookie 形式返回给客户端，SessionID 保存在客户端的 Cookie 中。

这是一种有状态的认证方法：服务端保存 Session 对象，客户端以 Cookie 形式保存 SessionID。

其交互过程如下：

1. 客户端在登录页面输入身份信息，如用户名/密码。
2. 服务端验证身份信息，通过后生成一个 Session 对象，保存到服务端，并将 SessionID 值以 Cookie 形式返回给客户端。
3. 客户端将接收到的 SessionID 保存到 Cookie 中，并且之后每次请求都在请求头中携带 SessionID Cookie。
4. 服务端从请求的 Cookie 中获取 SessionID，并查询其对应的 Session 对象，从而获得身份信息。
5. 客户端退出本次会话后，客户端删除 SessionID 的 Cookie，服务端删除 Session 对象。
6. 如果客户端之后要重新登录，需重新生成 Session 对象和 SessionID。

优点：

+ 较安全：客户端每次请求时无需发送身份信息，只需发送 SessionID。
+ 较高效：服务端无需每次处理请求时都要验证身份信息，只需通过 SessionID 查询 Session 对象。


缺点：

+ 扩展性差，Session 对象保存在服务端，如果是保存在多个服务器上，有一致性问题，如果保存在单个服务器上，无法适应用户增长。
+ 基于 Cookie 的 SessionID 不能跨域共享，同一用户的多个客户端（如浏览器客户端和 APP）不能共享 SessionId。
+ 基于 Cookie 的 SessionID 易被截获生成 CSRF 攻击。

## 4. Token 认证

这是一种 SPA 应用和 APP 经常使用的认证方法。它是一种无状态的认证方法。

客户端首先将用户信息发送给服务端，服务端根据用户信息+私钥生成一个唯一的 Token 并返回给客户端。Token 只保存在客户端，之后客户端的每个请求头中都携带 Token，而服务端只通过运算（无需查询）来验证用户。


```
客户端                                                          服务端
------                                                          ------

1----------------------------------------->
GET / HTTP/1.1

                                           <-------------------------2
                                            HTTP/1.1 401 Unauthorized
                                            WWW-Authenticate: Token

3----------------------------------------->
GET / HTTP/1.1
Authorization: Token f613d789819ff93537ee6a

                                            <------------------------4
                                                       HTTP/1.1 200 OK

5----------------------------------------->
GET /another-path/ HTTP/1.1
Authorization: Token f613d789819ff93537ee6a
```

优点：

+ Token 只保存在客户端，因此不影响服务端扩展性。
+ 为用户生成的 Token 可以在多个客户端共用。


缺点：

+ Token 包含了用户的全部信息，不只是如 SessionID 类似的一个 ID 值，因此会增加每次请求包的大小。


目前使用较多的是基于JWT(JSON Web Tokens) 的 Token 认证法。


# 资源

+ [Django for beginners](https://book.douban.com/subject/30389913/)
+ [Session、Token身份验证方法](https://blog.csdn.net/pan_tian/article/details/84841154)
