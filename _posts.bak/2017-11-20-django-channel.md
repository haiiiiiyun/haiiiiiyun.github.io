---
title: Django Channel
date: 2017-11-20
writing-time: 2017-11-20
categories: programming
tags: Django Python Channel websocket
---

# Channel 的基本概述

##什么是 Channel

类似一个消息队列，有序，先入先出。

channel 用一个字符串命名，位于不同主机或进程中的生产都可连接同名的 channel 后端，向 channel 发送消息，消费者(listener) 可稍后连接来获取消息，但是 Django channel 使用最多分发一次策略，即每个消息最多发送给一个消费者。

## 如何使用

传统的 Django 应用是请求-应用模式，安装 Channel 后，会将 Django 修改成在 `worker` 模式下运行，即 Django 分成 3 个独立层运行：

+ 接口服务(Interface servers，例如 WSGI adapter, WebSocket server): 将外部连接（HTTP, WebSocket 等）转换成 channel 上的消息。通过编写 `worker` 来处理消息。
+ channel backend, 及 Redis 等，用来传输消息
+ workers，侦听相关的 channel，有消息来时运行消息者代码。


先在一个 `url.py` 的 channel routing 文件中登记消费者与 channel 的关联：

```python
channel_routing = {
    "some-channel": "myapp.consumers.my_consumer",
}
```

定义一个消息者：

```python
# myapp/consumers.py
def my_consumer(message):
    pass
```

在这种模式下，传统的页面请求处理如下：

+ 系统内已创建有一个请求 channel 叫 `http.request`。
+ 每个请求客户应答都自动会创建一个独立 channel，例如 `http.response.o4F2h2Fd`（可以从请求 channel 消息中的 `reply_channel` 获取）。
+ 关联 `http.request` channel 的消息者代码向应答 channel 发送消息，实现应答，如下：


```python
# Listens on http.request
def my_consumer(message):
    # Decode the request from message format to a Request object
    django_request = AsgiRequest(message)
    # Run view
    django_response = view(django_request)
    # Encode the response into message format
    for chunk in AsgiHandler.encode_response(django_response):
        message.reply_channel.send(chunk)
```

## Channel 类型

一种是普通 channel，例如 `http.request`，用于将任务分发到消费者。所有消费者都能处理消息，因此可用负载均衡器随机将普通 channel 在多个 `channel servers` 和 `workers` 集群内均衡。

另一种是应答 channel，另每一个请求客户端都会创建一个应答 channel，该 channel 只由对应的 `interface server` 侦听。这种 channel 无法在集群内负载均衡。一般在 channel 名中包含 `!` 来表示不能均衡，例如 `http.response!f5G3fE21f`。


## 组

channel 中的一个消息只能分发给一个侦听者，可用组来组织多个客户端，实现多播。

一个  liveblog 中，文章保存后，手工实现多播如下：

```python
redis_conn = redis.Redis("localhost", 6379)

@receiver(post_save, sender=BlogUpdate)
def send_update(sender, instance, **kwargs):
    # Loop through all reply channels and send the update
    for reply_channel in redis_conn.smembers("readers"):
        Channel(reply_channel).send({
            "text": json.dumps({
                "id": instance.id,
                "content": instance.content
            })
        })

# Connected to websocket.connect
def ws_connect(message):
    # Add to reader set
    redis_conn.sadd("readers", message.reply_channel.name)
```

Channels 中实现了 Group，Group 中还包含了成员过期的管理：

```python
@receiver(post_save, sender=BlogUpdate)
def send_update(sender, instance, **kwargs):
    Group("liveblog").send({
        "text": json.dumps({
            "id": instance.id,
            "content": instance.content
        })
    })

# Connected to websocket.connect
def ws_connect(message):
    # Add to reader group
    Group("liveblog").add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({"accept": True})

# Connected to websocket.disconnect
def ws_disconnect(message):
    # Remove from reader group on clean disconnect
    Group("liveblog").discard(message.reply_channel)
```



## 参考

+ http://channels.readthedocs.io/en/latest/concepts.html
