-
--
title: MQTT 协议
date: 2017-10-09
writing-time: 2017-10-09
categories: programming
tags: MQTT IoT
---

# 概述

MQTT 是 MQ Telemetry Transport 的缩写，是一个 M2M(machine-to-machine)/IoT 通讯协议。它使用非常轻量级的 publish/subscribe 消息传输模式，设计用在受限设备、低带宽、高延时或不可靠的网络上。


# 数据表示

## bits

字节中的位用 bit0~bit7 标识，其中 bit7 是最高有效位，bit0 是最低有效位。

## 整数值

用 16 位的大端序表示，最高有效字节（MSB）在前，最低有效字节（LSB）在后。

## UTF-8 编码的字符串

字符串前有 2 字节的长度前缀，用来表示字符串的字节个数，因此字符串的长度最多为 $2^{16}-1=65535$ 个。

![字符串结构](/assets/images/mqtt/utf8-str-structure.png)


# MQTT 控制包格式

## 控制包的结构

一个 MQTT 控制包最多含有 3 个部分，且出现的顺序如下：

1. 固定头 Fixed header: 所有控制包中都必须包含
2. 可变头 Variable header: 某些包中存在
3. Payload: 某些包中存在


## 固定头

![固定头格式](/assets/images/mqtt/fixed-header-format.png)

即第 1 个字节中的 bit4-bit7 用来编码控制包类型（因此最多有 16 种包类型），而 bit0-bit3 用来设置某控制包的特定 flag。

控制包类型有：

名称      | 值 | 方向  | 描述
----------|
Reserved  | 0 | 禁止   | 预留
CONNECT   | 1 | C 到 S | 客户端请求连接到服务端
CONNACK   | 2 | S 到 C | 连接确认应答
PUBLISH   | 3 | 双向   | 发送方发布消息
PUBACK    | 4 | 双向   | 接收收确认应答
PUBREC    | 5 | 双向   | 接收方已接收到应答 publish received（保证交付中的第 1 部分）
PUBREL    | 6 | 双向   | 发送方发送 publish release （保证交付中的第 2 部分）
PUBCOMP   | 7 | 双向   | 接收收发送 publish complete (保证交付中的第 3 部分）
SUBSCRIBE | 8 | C 到 S | 客户端请求订阅
SUBACK    | 9 | S 到 C | 服务端确定应答
UNSUBSCRIBE | 10 | C 到 S | 客户端取消订阅
UNSUBACK    | 11 | S 到 C | 服务端确定应答
PINGREQ   | 12 | C 到 S | 客户端请求 PING
PINGRESP  | 13 | S 到 C | 服务端 PING 应答
DISCONNECT| 14 | C 到 S | 客户端断开连接
Reserved  | 15 | 禁止   | 预留


## 包的剩余长度

从第 2 个字节开始，接下来的最少 1 个，最多 4 个字节用来表示包的剩余字节长度：即包括可变头的字节数和包内容的字节数，但不包含表示剩余长度的字节数。

表示剩余长度的每个字节用低 7 位表示长度值，最高低为 1 时用来连接下一个字节，表示下一个字节也用来表示剩余长度。

因此用 1 个字节表示时，最大表示长度是 $2^7-1=127$，用 2 个字节时，最大表示长度是 $2^{14}-1$，3 个时，最大表示长度是 $2^{21}-1$, 4 个时最大表示长度是 $2^{28}-1$，即 256M。

例如，当剩余长度为 64 时，只用 1 个字节表示，且最高位为 0（0x40)。当剩余长度为 321 时 （$=65+2*128$），要用 2 个字节编码，第 1 字节的低 7 位编码为 65=0x41，且最高位为 1 ，即第 1 字节编码为 0x41+0x80=0xC1，第 2 个字节编码为 2。


## 可变头

可变头部分在固定头和包内容间。多个包类型的可变头中都含有包 ID (Packet Identifier)，例如 PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK.

包 ID 用 2 个字节表示，低字节是 MSB，高字节是 LSB:

![Packet Identifier](/assets/images/mqtt/packet-id.png)

客户端和服务端根据包 ID 来判断请求和确定包。

## Payload

有些控制包包含有包主体内容部分，例如 PUBLISH 包的主体内容是应用消息(Application Message)。


# MQTT 控制包

## CONNECT: 客户端向服务端请求连接

当客户端到服务端的网络连接建立后，客户端向服务端发送的首个包必须是 CONNECT，且只能发送一次。

包 payload 部分包含 1 到多个编码项。它们指定了唯一的 Client ID, Will topic, Will Message, User Name 和 Password。Client iD 项是必须的，其它都可选，基于可变头中的 flag 确定有无。

### 可变头部分

按顺序包含4 个部分： Protocol Name, Protocol Level, Coonnect Flags, Keep Alive。

Protocol Name 部分的值是按 UTF-8 编码的字符串 "MQTT"，且有 2 个字节的长度前缀，这是一个常量。

Protocol Level 部分用一个字节表示协议的版本号，v3.1.1 的协议版本号是 0x04。

Connect Flags 字节中的各位用来表示包内容中是否有相关项。

![Packet Identifier](/assets/images/mqtt/connect-flag-bits.png)


#### Clear Session

若 Clear Session 位为 0, 则连接后客户端和服务端都要保存当前会话状态，当连接断开重连后重用之前的会话。断开后，服务端必须存储后来接收的 QoS 为 1 和 2 的消息，当客户端重连上发送。

若 Clear Session 位为 1, 则每次断开后删除会话状态信息。

#### Will Flag

为 1 时表示：若连接请求被接受，则服务端必须保存一个 Will Message, 并与该网络连接关联。该 Will Message 除非当服务端在接收到 DISCONNECT 包时删除了，否则在之后在当前网络连接被关闭时必须发送。发送 Will Message 的情况有：

+ 当服务端检测到 IO 或网络出错时。
+ 当客户端无法在 Keep Alive 时间内完成通讯时。
+ 当客户端未首先发送 DISCONNECT 包时即关闭网络连接。
+ 服务端因协议错误而关闭网络连接时。


当 Will Flag 为 1 时，服务端将解读 Connect Flags 中的 Will QoS 和 Will Retain，而 Will Topic 和 Will Message 项必须要在 payload 中。

Will Message 当服务端在发送一次后，或服务端接收到 DISCONNECT 包后必须删除。

当 Will Flag 为 0 时，Connect Falgs 中的 Will QoS 和 Will Ratain 位必须为 0,且 payload 中不能有 Will Topic 和 Will Message。

#### Will Retain

如果 Will Flag 和 Will Retain 都为 1, 则服务端必须将 Will Message 作为一个 retained message 发布。

#### Keep Alive

用 2 个字节来表示 Keep Alive 的时间间隔，单位是秒。客户端必须要在该时间内至少有一次通讯，如果没有可通过发送 PINGREQ 和 PINGRESP 保持心跳。

该值为 0 时表示关闭时间间隔机制。

![Keep Alive](/assets/images/mqtt/keep-alive.png)

### Payload

里面包含哪些项由可变头中的 flags 确定，有包含的有： Client ID, Will Topic, Will Message, User Name, Password。

### Client ID

唯一值，用来标识连接会话，是一个 UTF-8 编码的字符串。


## CONNACT：连接请求应答

服务端发送给客户端的首个包必须是 CONNACK。

### 可变头

可变头的第 1 个字节为 Connect Acknowledge Flags，其中 bit1-7 预留，必须为 0, bit0 用来表示 SP(Session Present Flag)。如果服务端接受 CONNECT 请求中的 ClearSession 为 1 的值，则 CONNACK 包中的 SP Flag 必须为 0。如果 CONNECT 请求中的 ClearSession 为 0, 而服务端接受后，CONNACK 包中的 SP Flag 必须为 1。

即通过 CONNECT 中的 ClearSession 和 CONNACK 中的 SP 值，双方达成是否对会话状态进行保存。

可变头的第 2 个字节表示返回代码。0x0 表示连接成功，0x01-0x05 表示失败， 0x06-0xff 预留。

### payload 都内容

## PUBLISH： 用来传输应用消息

![PUBLISH 包固定头结构](/assets/images/mqtt/publish-packet-fixed-header.png)


bit2 的 DUP(duplication) 标识为 1 时，表示该包为重发包。

bit1-2 为 QoS 标识，表示分发的确保值，如下：

QoS 值 | bit2 | bit1 | 描述
-------|
0      | 0    | 0    | 最多发送 1 次，即发送后不管有没有收到，都不重发
1      | 0    | 1    | 最少发送 1 次，即未接收接收应答的话会重发
2      | 1    | 0    | 有且仅发 1 次，即 PUBLISH, PUBREC, PUBREL, PUBCOMP 过程
3      | 1    | 1    | 预留

bit0 为 RETAIN 标识，当值为 1 时，服务端会将该包保存起来，发送给以后订阅该主题的客户端。

### 可变头

按序含有下面的项： Topic Name, Packet ID。

Topic Name 相当于频道名，是一个 UTF-8 编码的字符串。

当 QoS 值为 1 或 2 时（即有重发时），才会有 Packet ID 项。

### Payload

内容是特定到各应用的。

### 应答

当 QoS 为 0 时，无需应答，当 QoS 为 1 时，应答是 PUBACK，当 QoS 为 2 时，应答是 PUBREC。

### 操作

客户端使用 PUBLISH 包向服务端发送应用消息，从而实现客户端间的相关匹配订阅的发布。

服务端使用 PUBLISH 包向匹配订阅的各客户端发送应用消息。

## PUBACK：用来应答 QoS 为 1 的 PUBLISH

可变头包含 2 字节的 Packet ID，无 payload。


## PUBREC, PUBREL, PUBCOMP

当 QoS 为 2 时，使用多步走实现仅发 1 次的要求。

```
END1                        END2
PUBLISH --------------------PUBREC(publish received)
PUBREL(publish released) -- PUBCOMP(publish completed)
```


## SUBSCRIBE: 订阅主题

客户端使用 SUBSCRIBE 订阅，一次可完成多个订阅。

### 可变头中的 2 个字节表示 Packet ID

### Payload

包含一组 Topic Filters，每个 Topic Filter 都是一个 UTF-8 字符串+QoS，w全组连续存放。

![SUBSCRIBE payload format](/assets/images/mqtt/subscribe-payload-format.png)

### 应答

服务端必须用 SUBACK 应答，应答包中的 Packet ID 必须匹配，应答包中必须为每对 TopicFilter/QoS 返回应答码。


## SUBACK

可变头中的 2 个字节为 Packet ID。

### Payload

包含一组返回码，对应 SUBSCRIBE 包中 TopicFilter/QoS 对。一个返回码用一个字节表示，编码为：

![SUBSCRIBE payload format](/assets/images/mqtt/suback-return-code.png)

返回值如下：

+ 0x00 - Success - Maximum QoS 0
+ 0x01 - Success - Maximum QoS 1
+ 0x02 - Success - Maximum QoS 2
+ 0x80 - Failure


## UNSUBSCRIBE

可变头中的 2 字节编码 Packet ID，Payload 中包含要取消的一组 TopicFilter。

## UNSUBACK

对 UNSUBSCRIBE 的应答。可变头中的 2 字节编码 Packet ID，无 Payload。

## PINGREQ: Ping 请求

无可变头无 Payload。

## PINGRESP: Ping 应答

无可变头无 Payload。


## DISCONNECT

客户端向服务端发送的最后一个包。无可变头无 Payload。


# 网络连接

MQTT 协议需要运行在一个有序可靠的字符流传输层上。可采用的传输层有：

+ TCP
+ TLS
+ WebSocket


# Topic Names 和 Topic Filters

+ 可用 `/` 进行分级，如 `sport/tennis/p1`
+ `#` 是多级匹配符，能匹配多级，如 `sport/#` 能匹配 `sport/tennis/p1`
+ `+` 是单级匹配符，如 `sport/tennis/#` 能匹配 `sport/tennis/p1`
+ `$` 开头的 Topic 不能使用 `#` 和 `+` 默认匹配到，一般作为系统 Topic 使用，如 `$SYS/etc` 等
+ 只用 `+` 能匹配除以 `$` 开头的所有主题，要匹配 `$` 开头的主题，要明确写出，如 `$SYS/#`
+ 名字中是大小写敏感的
+ 名字中能使用空格

# 参考

+ [MQTT 主页](http://mqtt.org/)
+ [MQTT v3.1.1 is an OASIS Standard](http://mqtt.org/documentation)
