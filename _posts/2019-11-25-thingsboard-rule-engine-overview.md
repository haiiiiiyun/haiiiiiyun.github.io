---
title: thingsboard 规则引擎概述
date: 2019-11-25
writing-time: 2019-11-25
categories: java;thingsboard;iot
tags: java;thingsboard;iot
---

# 1. 概述

规则引擎 Rule Engine 高度可配置，用于事件处理，可对处种消息进行过滤、放大、变换、对接外部系统等处理。

# 2. 主要概念

# 2.1 Rule Engine Message

用于表示系统中的各种消息，序列化，不可修改，例如：

+ 来自设备的[数据上传](https://thingsboard.io/docs/user-guide/telemetry/)、[属性更新](https://thingsboard.io/docs/user-guide/attributes/) 和 [RPC 调用](https://thingsboard.io/docs/user-guide/rpc/) 等事件。
+ 实体的生命周期性事件: created, updated, deleted, assigned, unassigned, attributes updated.
+ 设备状态事件： connected, disconnected, active, inactive.
+ 其它系统事件。


消息中包含以下信息：

+ Message ID: 基于时间的唯一 ID
+ 消息来源者：设备、资产(Asset) 、其它实体的 ID
+ 消息类型： `Post telemetry`, `Inactivity Event` 等
+ 消息体 Payload: JSON body.
+ Metadata: KV 键值对，消息的额外数据。


# 2.2 邓定义消息类型

+ POST_ATTRIBUTES_REQUEST: Post attributes, 设备请求上传属性值，metadata 数据有： `deviceName`, `deviceType`, payload 例如 `{"currentState": "IDLE"}`。
+ POST_TELEMETRY_REQUEST: Post telemetry, 设备请求上传遥测数据，metadata 数据有： `deviceName`, `deviceType`, `ts`(timestamp, 毫秒)，payload 例如 `{"temperature": 22}`。
+ TO_SERVER_RPC_REQUEST: RPC Request from Device, 设备(客户端)请求 RPC 调用，metadata 数据有： `deviceName`, `deviceType`, `requestId`(由客户端提供的 RPC 请求 ID)，payload 例如 `{"method": "getTime", "params": {"param1":"val1"}}`。
+ RPC_CALL_FROM_SERVER_TO_DEVICE: RPC Request to Device, 服务端请求 RPC 调用，metadata 数据有：`requestUUID`(服务端提供，用于区别应答），`expirationTime`, `oneway`(true 时无需应答，false 时需应用)，payload 例如 `{"method": "getGpioStatus", "params": {"param1": "val1"}}`。
+ ACTIVITY_EVENT: Activity Event, 设备切换为活跃状态，metadata 数据有 `deviceName`, `deviceType`。
+ INACTIVITY_EVENT: Inactivity Event, 设备切换为非活跃状态。
+ CONNECT_EVENT: Connect Event, 设备已连接。
+ DISCONNECT_EVENT: Disconnect Event, 设备断开连接。
+ ENTITY_CREATED: Entity Created, 新实体已创建事件，metadata 数据有 `userName`(创建者名称), `userId`(创建者ID), payload 包含实体信息，如 `{"id":{"entityType": "DEVICE", "id": "uuid"}, "createdTime": timestamp, ..., "name": "my-device", "type": "temp-sensor"}`.
+ ENTITY_UPDATED.
+ ENTITY_DELETED.
+ ENTITY_ASSIGNED, Entity Assigned, 现有实体分配给客户事件，metadata 数据有 `userName`(操作者名称), `userId`, `assignedCustomerName`, `assignedCustomerId`.
+ ENTITY_UNASSIGNED.
+ ADDED_TO_ENTITY_GROUP.
+ REMOVED_FROM_ENTITY_GROUP.
+ ATTRIBUTES_UPDATED, Attributes Updated, 实体属性已更新事件，metadata 数据有 `userName`(操作者名称), `userId`, `scope`(SERVER_SCOPE 或 SHARED_SCOPE)，payload 为已更新的属性键值对，如 `{"softwareVersion": "1.2.3"}`.
+ ATTRIBUTES_DELETED.
+ ALARM: Alarm Event, 当报警生成、更新、删除时产生该事件。
+ REST_API_REQUEST: REST API Request to Rule Engine，当用户执行 REST API 调用时产生该事件。

# 2.3 规则结点 Rule Node

规则结点一次处理一个传入消息，并生成一个或多个输出消息。能过滤、放大、变换传入消息，执行动作或与外部系统交互。

# 2.4 规则结点关联 Rule Node Relation

规则结点可关联到其它规则结点。每种关联都有关联类似 (Relation Type), 即表示该关联的逻辑意思的名称。规则结点在生成输出消息时，通过指定关联类型将生成的消息路由到下一个结点。

规则结点关联类型（即名称）可为 `Success`, `Failure`, 也可为 `True`, `False`, `Post Telemetry`, `Attributes Updated`, `Entity Created` 等。

# 2.5 规则链

规则结点其及关联的逻辑组合。

租户管理员可定义一个根规则链(Root Rule Chain，默认规则链) 和多个其它规则链。


# 3 规则结点类型

+ 过滤结点 [Filter Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/filter-nodes/) 用于消息过滤和路由
+ 放大结点 [Enrichment Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/enrichment-nodes/) 用于更新消息的 metadata
+ 变换结点 [Transformation Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/transformation-nodes/) 用于变换消息中的信息项，如 Originator, Type, Payload, Metadata.
+ 动作结点 [Action Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/action-nodes/) 基于传入消息执行各种动作。
+ 外部结点 [External Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/external-nodes/) 用于和外部系统交互。


# 4 体系结构

based on actor model and message queue:

![规则引擎体系结构](https://thingsboard.io/images/user-guide/rule-engine-2-0/rule-engine-architecture.svg)

# Resources

+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/overview/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/architecture/
