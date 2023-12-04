---
title: thingsboard 规则引擎结点功能总结
date: 2020-04-30
writing-time: 2020-04-30
categories: java thingsboard iot
tags: java thingsboard iot
---

## 1. 概述

本文结合官方文档和v2.4.3版本源码总结了各规则引擎结点的功能。

官方文档的有些描述不太清楚，需要结合源码理清。


## 2. 核心概念

规则引擎是一个事件处理系统。

+ 能对由设备和资产上传的消息进行 filter, enrich, transform 处理
+ 并触发不同的动作，如 notification, 与外部系统交互等


### 2.1. Rule Engine Message 规则引擎消息

Rule Engine Message is a serializable, immutable data structure that represent various messages in the system. 例如：

+ 上传数据、属性更新、设备调用服务端 RPC
+ 实体生命周期事件： created, updated, deleted, assigned, unassigned, attributes updated;
+ 设备状态事件： connected, disconnected, active, inactive, etc;
+ 其它系统事件。


Rule Engine Message contains the following information:

+ Message ID: time based, universally unique identifier;
+ Originator of the message: Device, Asset or other Entity identifier;
+ Message Type: “Post telemetry” or “Inactivity Event”, etc;
+ Payload of the message: JSON body with actual message payload;
+ Metadata: List of key-value pairs with additional data about the message.

消息中包含以下信息：

+ Message ID: 基于时间的唯一 ID
+ 消息来源者：设备、资产(Asset) 、其它实体的 ID
+ 消息类型： `Post telemetry`, `Inactivity Event` 等
+ 消息体 Payload: JSON body.
+ Metadata: KV 键值对，消息的额外数据。


### 2.2. 预定义的消息类型

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

### 2.3. 规则结点 Rule Node

规则结点一次处理一个传入消息，并生成一个或多个输出消息。能过滤、增强、变换传入消息，执行动作或与外部系统交互。

### 2.4. 规则结点关联 Rule Node Relation

规则结点可关联到其它规则结点。每种关联都有关联类似 (Relation Type), 即表示该关联的逻辑意思的名称。规则结点在生成输出消息时，通过指定关联类型将生成的消息路由到下一个结点。

规则结点关联类型（即名称）可为 `Success`, `Failure`, 也可为 `True`, `False`, `Post Telemetry`, `Attributes Updated`, `Entity Created` 等。

### 2.5. 规则链

规则结点其及关联的逻辑组合。

租户管理员可定义一个根规则链(Root Rule Chain，默认规则链) 和多个其它规则链。

根规则链处理所有的输入消息，并可将消息转发到其它规则链。消息可在规则链间进行转发。


### 2.6. 规则结点类型

+ 过滤结点 [Filter Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/filter-nodes/) 用于消息过滤和路由
+ 增强结点 [Enrichment Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/enrichment-nodes/) 用于更新消息的 metadata
+ 变换结点 [Transformation Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/transformation-nodes/) 用于变换消息中的信息项，如 Originator, Type, Payload, Metadata.
+ 动作结点 [Action Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/action-nodes/) 基于传入消息执行各种动作。
+ 外部结点 [External Nodes](https://thingsboard.io/docs/user-guide/rule-engine-2-0/external-nodes/) 用于和外部系统交互。


## 3. 体系结构

based on actor model and message queue:

![规则引擎体系结构](https://thingsboard.io/images/user-guide/rule-engine-2-0/rule-engine-architecture.svg)


# 4. 结点类型

## 4.1 Filter Node 过滤型结点

### 4.1.1. Check Relation Filter Node

消息发起者与当前结点中指定的实体关联性对比，比如结点中指定 Direction: From, Type: Asset, Asset: Field C, Relation type: Contains, 
则当消息发起者是包含在 Field C 内的实体时，消息从 `True` 路流出，否则从 `False` 路流出。


### 4.1.2. Check Existence Fields Node

检测消息中的 data 和 metadata 中是否有相关字段。


### 4.1.3. Message Type Filter Node

检测消息类型。

### 4.1.4. Message Type Switch Node

根据消息类型路由到指定路径，未指定类型路径的消息路由到 Other 路径。

### 4.1.5. Originator Type Filter Node

检测输入消息中消息发起者的实体类型值，如果类型在结点中指定的类型中，则消息从 `True` 路流出，否则从 `False` 路流出。

### 4.1.6. Originator Type Switch Node

根据消息发起者的实体类型路由到指定路径。


### 4.1.7. Script Filter Node

结点中定义一个 bool 值 javascript 函数来过滤输入消息，函数有三个参数：

+ msg
+ metaData
+ msgType

例如：

```javascript
function Filter(msg, metadata, msgType) {
    if(msgType === 'POST_TELEMETRY_REQUEST') {
        if(metadata.deviceType === 'vehicle') {
            return msg.humidity > 50;
        } else if(metadata.deviceType === 'controller') {
            return msg.temperature > 20 && msg.humidity > 60;
        }
    }

    return false;
}
```

### 4.1.8. Switch Node

结点中可定义一个返回字符串数组的 javascript 函数，同 Filter Node 也有三个参数，如：

```javascript
if (msgType === 'POST_TELEMETRY_REQUEST') {
    if (msg.temperature < 18) {
        return ['Low Temperature Telemetry'];
    } else {
        return ['Normal Temperature Telemetry'];
    }
} else if (msgType === 'POST_ATTRIBUTES_REQUEST') {
    if (msg.currentState === 'IDLE') {
        return ['Idle State', 'Update State Attribute'];
    } else if (msg.currentState === 'RUNNING') {
        return ['Running State', 'Update State Attribute'];
    } else {
        return ['Unknown State'];
    }
}
return [];
```

返回值是关联路径名，基于路径名可关联到下一个 **规则链**。


### 4.1.9. GPS Geofencing Filter Node

可定义2种地理围栏:

+ 多边形： 如果是定义在消息的 metadata 中，则定义为 `{perimeter: [[lat1,lon1],[lat2,lon2], ... ,[latN,lonN]],}`。如果是定义在结点中，则 `Perimeter type` 选 `Polygon`，定义体为 `[[lat1,lon1],[lat2,lon2], ... ,[latN,lonN]]`
+ 圆形：如果是定义在消息的 metadata 中，则需要定义这 4 个参数， centerLatitude, centerLongitude, range, rangeUnit，数值参数都是 double 浮点数，rangeUnit 表示单位，值为 METER, KILOMETER, FOOT, MILE, NAUTICAL_MILE。如果是定义在结点中，则 `Perimeter type` 选 `Circle`，并定义相关参数。

参见源文件 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/geo/AbstractGeofencingNode.java` 中的 `protected List<Perimeter> getPerimeters(TbMsg msg, JsonObject msgDataObj) throws TbNodeException`。


可以在结点中指定经纬度参数的 key 名，这些参数将在消息体 msg 或 metadata 中获取。


## 4.2. Enrichment Nodes 增强型结点

用于更新输入消息中的 metada。

### 4.2.1. Customer attributes 客户实体属性增强

找到输入消息发起者实体所属的客户实体，将该客户实体的属性值增加到消息的 metadata 中。

可配置源属性名和目标属性名。

如果选中 `Latest Telemetry`，则将客户实体中最新遥测数据中的值添加到消息的 metadata 中，否则添加客户的服务端属性(server scope)。

消息发起者实体类型必须为 Customer, User, Asset, Device，因为只有它们都有所属客户实体，如果不是，则路由到 `Failure` 路径。


### 4.2.2. Device attributes 设备实体属性增强

找到与输入消息发起者实体相关的设备实体，将该设备实体的所有属性值和最新遥测数据增加到消息的 metadata 中。

增加到 metadata 中的属性名前缀:

+ 设备的共享属性-> shared_
+ 设备的客户端属性 -> cs_
+ 设备的服务端属性 -> ss_
+ 设备的遥测数据 -> 无前缀

通过结点中的 `Device relations query` 配置进行相关设备实体查询。

Direction 值：

+ From: 表示该设备实体必须在关联关系的 From 端，而消息发起者在 To 端。
+ To: 与 From 相反。

Relation type: 指定关联类型。

Device types: 指定匹配设备的类型。

如果找个多处设备，则只用第一个找到的设备。没有找到时路由到 `Failure` 路径。

### 4.2.3. Originator attributes 消息发起者实体属性增强

类似 Device attributes。

### 4.2.4. Originator fields 消息发起者字段增强

将消息发起者实体的字段值添加到 metadata，结点中可以配置字段名映射信息。

消息发起者实体类型必须为 Tenant, Customer, User, Asset, Device, Alarm, Rule Chain，否则会路由到 `Failure` 路径。

### 4.2.5. Related attributes 关联实体属性增强

是 Device attributes 结点的通用版本，通过 `Relations query` 定义关联实体查询方式。

### 4.2.6. Tenant attributes 租房实体属性增强

类似 Customer attributes 结点，将消息发起者所属租房的属性或最新遥测数据到 metadata。

### 4.2.7. Originator telemetry 消息发起者遥测数据增强

将消息发起者特定时间段内的遥测数据添加到 metadaba。

`Latest timeseries` 指定数据指定遥测数据键名，用 `,` 分隔多个键名。

Fetch mode:

+ FIRST: 从数据库中提取指定时间段最接近开始时间的数据。
+ LAST: 从数据库中提取指定时间段最接近结束时间的数据。
+ ALL: 提取时间段内的所有数据，以数组形式返回，可指定返回数据个数（最多1000）及排序。

时间段是根据当前系统时间点计算出来的（精确到毫秒），如当前系统时间是 ts, 结点中指定 `Start Interval` 为 2 Minutes, 指定 `End Interval` 为 1 Minutes，则时间段为 [ts-2*60*1000, ts-1*60-1000]。

如果配置为 `Use metadata interval patterns`，则 `Start Interval` 和 `End Interal` 值可从消息的 metadata 中提取，从而只需在结点中定义要从 metadata 中提取的变量名模式，如 `{metaKeyName}`。

详细见源码 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/metadata/TbGetTelemetryNode.java` 中的 `private Interval getInterval(TbMsg msg)` 函数。

### 4.2.8. Tenant details 租户实体数据库字段增强

将消息发起者所属租户的某些数据库字段增加到 metadata, 名称前加 `tenant_` 前缀。

### 4.2.9. Customer details 客户实体数据库字段增强

类似 Tenant details

## 4.2.10. Transformation Nodes 变换结点

用于修改输入消息中的消息字段。

### 4.2.11. Change originator 变换消息发起者字段

输入消息中有一个 `originator` 字段用来表示消息的发起者实体。该结点能将 `originator` 值修改为消息发起者实体所属的客户或租户实体，或其关联的其它实体。查询关联实体要配置 `Relation Query`，具体和 `related attributes` 增强结点中的配置类似。

使用情景：若设备上传遥测数据，此时消息的发起者为该设备实体，通过修改为设备实体的租户实体，则之后该遥测数据则被归结到该租户。


### 4.2.12. Script Transformation Node 通过 javascript 脚本变换

结点中配置 `function Transform(msg, metadata, msgType){}` 函数，函数有三个参数，并返回变换后的消息，返回结构为：

```javascript
{   
    msg: new payload,
    metadata: new metadata,
    msgType: new msgType 
}
```

### 4.2.13. To Email Node 变换为 Email 结点

将消息变换为 Email Message，Email 消息所需字段值可直接在结点中配置，若配置对应的变量模板，并从 metadata 中提取。转换后的消息可路由给 *Send Email Node* 结点。

## 4.3. Action Nodes 动作结点

基于输入消息执行各种动作。

### 4.3.1. 实体警报

警报信息保存在表 `alarm` 中，每个警报都有生命周期过程：创建/更新，清除，确认。

警报的发起者实体用字段 `originator_id` 和 `originator_type` 表示。

一个实体的警报默认会传递到该实体关联的所有父实体上。

警报由发起者 originator, 警报类型 type, 和开始时间 start_ts 唯一标识，因此同一个实体，在同一时间，不能触发同类型的警报，只能对现有警报进行更新。

警报级别保存在字段 `severity` 中，值有: CRITICAL, MAJOR, MINOR, WARNING, INDETERMINATE.

警报的清除时间、确认时间和最近修改时间分别保存在字段 `clear_ts`, `ack_ts`, `end_ts` 中。

### 4.3.2. Create Alarm Node 创建/更新警报结点

结点会基于设备的 Alarm Type 和消息发起者实体，从数据库导入警报记录，若找到一个未清除的警报，则该结点会对该警报进行更新，否则在数据库中创建新警报。

`Alarm Detial Builder` 定义的javascript函数返回一个 Alarm Details JsonNode 对象，用于保存警报的一些额外信息，例如：

```javascript
function Details(msg, metadata, msgType) {
    var details = {temperature: msg.temperature, count: 1};

    if (metadata.prevAlarmDetails) {
        var prevDetails = JSON.parse(metadata.prevAlarmDetails); // 注意 prevAlarmDetails 是 JSON 字串
        if(prevDetails.count) {
            details.count = prevDetails.count + 1;
        }
    }

    return details;
}
```

当前消息中的警报额外信息可从 metadata.prevAlarmDetails 中获取。

如果勾选了 `Use message alarm data`，则从消息的 payload 中导入警报配置信息，见源码 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/action/TbCreateAlarmNode.java` 中的 `processAlarm` 方法。

配置信息也可以配置为从消息的 metadata 中提取，如将 Alarm type 配置为 `{metaKeyName}`。

如果勾选 `Propagate`，则还要配置警报要传递到父实体的关联类型，如 `Contains`, `Managers`, 用回车来添加。

创建/更新后的 Alarm 对象有如下属性：

+ Alarm details - object returned from Alarm Details Builder script, Details 函数返回的对象
+ Alarm status - 新创建的警报状态值为 ACTIVE_UNACK. 若是更新时，则状态值不变。
+ Severity - value from Node Configuration，警报等级
+ Propagation - value from Node Configuration，是否要上传给关联父实体
+ Alarm type - value from Node Configuration，警报类型
+ Alarm start time - 新创建时，开始时间是当前系统时间，若是更新时，则开始时间不变。
+ Alarm end time - current system time，表示最近修改时间，为当前系统时间。


结点处理后产生的消息结构为：

+ Message Type - ALARM
+ Originator - the same originator from inbound Message，同传入消息的
+ Payload - JSON representation of new Alarm that was created/updated，上节描述的 Alarm 对象数据
+ Metadata - all fields from original Message Metadata，来自原传入消息的 metadata。

若是新创建，则 metadata 会有 `isNewAlarm: true`，并且消息将路由到 `Created` 路径。
若是更新，则 metadata 会有 `isExistingAlarm: true`，并且消息将路由到 `Updated` 路径。

消息体 Payload 例如如下：

```javascript
{
  "tenantId": {
    "entityType": "TENANT",
    "id": "22cd8888-5dac-11e8-bbab-ad47060c9bbb"
  },
  "type": "High Temperature Alarm",
  "originator": {
    "entityType": "DEVICE",
    "id": "11cd8777-5dac-11e8-bbab-ad55560c9ccc"
  },
  "severity": "CRITICAL",
  "status": "ACTIVE_UNACK",
  "startTs": 1526985698000,
  "endTs": 1526985698000,
  "ackTs": 0,
  "clearTs": 0,
  "details": {
    "temperature": 70,
    "ts": 1526985696000
  },
  "propagate": true,
  "id": "33cd8999-5dac-11e8-bbab-ad47060c9431",
  "createdTime": 1526985698000,
  "name": "High Temperature Alarm"
}
```

### 4.3.3. Clear Alarm Node 清除警报结点

基于结点中的 `Alarm type` 和输入消息的发起者实体，从数据库中加载相关警报并进行清除操作。

结点中定义的 `Alarm Details Builder` javascript 函数用来更新 Alarm Details 对象数据。

结点对警报进行如下更新：

+ 若警报当前状态为 ACK，则更新为 CLEARED_ACK, 当前为 UNACK, 则更新为 CLEARED_UNACK。
+ 设置 `clear_ts` 为当前系统时间。
+ 用 `Alarm Details Builder` 返回值更新 Details 数据。


如果相关警报未找到，或已清除，路由到 `False` 路径。否则路由到 `Cleared` 路径。

该结点更新后的消息中 metadata 中会添加 `isClearedAlarm:true`。


### 4.3.4. Delay Node 延时结点

将消息延时一段时间后再转出。结点中可配置延时多长时间，及最大待转队列长度。队列满后，传入的消息会路由到 `Failure` 路径。


### 4.3.5. Generator Node 消息生成器结点

结点中可配置生成消息的个数，时间间隔，消息发起者，并定义一个返回消息体的 javascript 函数，例如：

```javascript
function Generate(prevMsg, prevMetadata, prevMsgType) {
    return {   
        msg: new payload,
        metadata: new metadata,
        msgType: new msgType 
    }
}
```

### 4.3.6. Log Node 日志结点

定义一个 javascript 函数，例如： 

```javascript
function ToString(msg, metadata, msgType) {
    return 'Incoming message:\n' + JSON.stringify(msg) + '\nIncoming metadata:\n' + JSON.stringify(metadata);
}
```

将消息转换成一个字串，并写入日志。写入的 LOG Level 是 `INFO`。


### 4.3.7. RPC 功能

Thingsboard 中可以在服务端应用中调用设备实体应用中的 RPC，也可以从设备实体应用中调用服务端应用中的 RPC。

服务端发起的 RPC 调用为服务端 RPC，分 2 种：

+ One-way RPC request: 单向 RPC 请求无需设备进行收到确认或应答。
+ Two-way RPC request: 双向的则需要设备在指定时间内有应答。

服务端通过 **System RPC Service** 提供的功能向设备发送 RPC 调用，即向 `http(s)://host:port/api/plugins/rpc/{callType}/{deviceId}` POST RPC 请求，其中：

+ callType: 值为 oneway 或 twoway
+ deviceId：设备 ID


请求体是包含 `method` 和 `params` 字段的 JSON 对象，如：

```javascript
{
  "method": "setGpio",
  "params": {
    "pin": "23",
    "value": 1
  }
}
```

设备端可以使用 [MQTT RPC API](https://thingsboard.io/docs/reference/mqtt-api/#rpc-api), [CoAP RPC API](https://thingsboard.io/docs/reference/coap-api/#rpc-api), [HTTP](https://thingsboard.io/docs/reference/http-api/#rpc-api) 进行 RPC 调用。

### 4.3.8. RPC Call Reply Node，RPC 调用应答结点

该结点向 RPC 调用者，即消息发起者 `originator` 发送 RPC 应答。由于 RPC 调用者必须是设备实体，因此消息发起者也必须是设备实体。

设备端发起的 RPC 请求会作为消息流转过各规则链进行处理，消息 metadata 中都有 `request ID` 相关的字段，用来匹配请求和应答消息。

结点中可配置 metadata 中 `request ID` 字段映射名，默认为 `requestId`。

结点基于 requestId, originator, 输入消息中的数据，创建应答包向设备发送应答。

有以下情况，结点处理后的消息会路由到 `Failure` 路径：

+ 输入消息的发起者不是设备实体
+ 消息 metadata 中没有 request ID 数据
+ 消息数据为空


### 4.3.9. RPC Call Request Node，向设备发送 RPC 请求结点

向设备（即该消息的发起者）发送 RPC 请求，等待应答，并将应答作为输出消息，路由到下一个结点。

结点中可配置等待超时时间 timeout。

消息数据中必须要有 `method` 和 `params` 字段，如：

```javascript
{
  "method": "setGpio",
  "params": {
    "pin": "23",
    "value": 1
  }
}
```

如果消息数据中没有 `requestId` 字段，系统会自动创建一个随机数填入。

生成的消息内容为：

+ 发起者 originator: 同传入消息
+ metadata: 同传入消息
+ 消息数据：设备的 RPC 应答内容会添加到消息数据中。

有以下情况，输出的消息会路由到 `Failure` 路径：

+ 输入消息的发起者不是设备实体
+ 输入消息数据中没有 `method` 和 `params` 字段
+ 结点获取 RPC 应答超时


### 4.3.10. Save Attributes Node 存储实体属性结点

将输入消息数据中的各值作为消息发起者实体的属性值存入数据库。结点中可配置对应存入的属性域，如客户端属性、共享属性、服务端属性。

输入消息类型必须为 `POST_ATTRIBUTES_REQUEST`，否则输出消息会路由到 `Failure` 路径。消息体例如： 

```javascript
{
  "firmware_version": "1.0.1",
  "serial_number": "SN-001"
}
```

其它消息类型可前置一个 `Script Transform Node` 来进行消息类型转换。

### 4.3.11. Save Timeseries Node 存储实体的时序数据结点

将输入消息数据中的时序遥测数据作为消息发起者实体的时序数据存入数据库。结点中可设置默认的 TTL 数值为时序数据过期秒数，TTL 只当使用 Cassandra 存储时有用。

输入消息类型必须为 `POST_TELEMETRY_REQUESTS`，否则输出消息会路由到 `Failure` 路径。消息体例如： 

```javascript
{  
  "values": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

其它消息类型可前置一个 `Script Transform Node` 来进行消息类型转换。

消息的 metadata 中必须有 `ts` 字段用来指定上传的遥测数据的时间，如果 metadata 有 `TTL` 字段，则结点优先使用该值。

### 4.3.12. Save to Custom Table 将消息内容存储到 Cassandra 自定义表的结点

**只适用于 Cassandra 数据库**。

将消息数据中的各字段存储到 Cassandra 某些的对应列中，结点中需配置表名，及字段名和列名的对应关系。

### 4.3.13. Assign To Customer Node 将消息发起者分配给某客户实体的结点

输入消息的发起者实体类型必须为：Asset, Device, Entity View, Dashboard。

结点中配置目标客户的名称，该值也可设置为名称变量模式如 `{metaKeyName}` 从而从消息的 metadata 中提取。

该值与数据库表 `customer` 中字段 `title` 进行匹配从而提取出相应客户实体，若结点中勾选 `Create new customer if not exists`，则在未找到时新建一个。

见源码 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/action/TbAbstractCustomerActionNode.java` 中的 `protected ListenableFuture<CustomerId> getCustomer(TbContext ctx, TbMsg msg)` 方法。


### 4.3.14. Unassign From Customer Node 将消息发起者从目标客户实体处取消分配的结点

与 `Assign To Customer Node` 功能相反。


### 4.3.15. Create Relation Node 创建关联关系的结点

为所选的目标实体与消息发起者实体创建关联关系。消息发起者必须为如下实体： Asset, Device, Entity View, Customer, Tenant, Dashboard.

结点中要配置目标实体的查询方法，如：

+ 实体类型 Type
+ 实体名 Name pattern 可设置为静态时，也可设备为变量模式如 `{metaKeyName}` 从而从消息的 metadata 中提取。
+ 类别名 Type pattern 可设置为静态时，也可设备为变量模式如 `{metaKeyName}` 从而从消息的 metadata 中提取。

见源码 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/action/TbAbstractRelationActionNode.java` 中的 `private EntityContainer loadEntity(EntityKey entitykey)` 方法，查询是 Name pattern 的值一般是匹配数据库实体记录中的 `name` 或 `title` 字段。

勾选 `Create new entity if not exists` 则在找不到实体时会创建新实体。

需创建的关联关系还要配置：

+ Direction: From, To。例如当值为 From 时，则表示目标实体应当在关联关系的 `From` 端，而消息发起者在 `To` 端。见源码 `thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/action/TbAbstractRelationActionNode.java` 中的 `protected SearchDirectionIds processSingleSearchDirection(TbMsg msg, EntityContainer entityContainer)` 方法。
+ Relation Type：如 Contains, Managers


勾选 `Remove current relations` 会删除旧有的相同关联。
勾选 `Change originator to related entity` 会将输出消息中的发起者更改为找到的目标实体。

### 4.3.16. Delete Relation Node 删除关联关系的结点

类似 Create Relation Node

### 4.3.17. GPS Geofencing Events Node 

从输入消息中提出坐标，与地理围栏对比，生成相应的事件：

+ Entered: 进入围栏
+ Left： 离开围栏
+ Inside: 当前状态在围栏内
+ Outside: 当前状态在围栏外

`Minimal inside duration` 和 `Minimal outside duration` 表示消息发起者实体处于相关状态的持续时间。

结点参数配置类似 `GPS Geofencing Filter Node`。


## 4.4. 外部结点

实现与外部系统交互。

结点的输出消息的 metadata 中会包含外部系统应答消息中的一个关键字段，原输入消息的数据原样复制到输出消息中。

### 4.4.1. AWS SNS Node

发布消息到 Amazon Simple Notification Service。


### 4.4.2.  AWS SQS Node

发布消息到 Amazon Simple Queue Service。

### 4.4.3. Kafka Node

发送消息到 Kafka 代理。

### 4.4.4. MQTT Node

将输入消息的数据发布到相应的 MQTT 主题上。

主题可基于 metadata 中的字段创建。结点中需配置 MQTT 代理的连接参数。

### 4.4.5. RabbitMQ Node

将输入消息的数据发布到 RabbitMQ.

### 4.4.6. REST API Call Node

调用外部系统的 REST API。

+ Endpoint URL 和 URL 头信息可基于 metadata 中的字段创建。
+ 消息数据作为 REST 的请求体发送。


输出消息的 metadata 中会包含 REST 应答中的 status, statusCode, statusReason, headers。输出消息体 message payload 与 REST 应答体相同。消息类型和发起者不变。


### 4.4.7. Send Email Node

发送邮件结点，其前置结点必须是 `To Email` 结点。

结点中需配置邮件服务器连接方式。

### 4.4.8 Twilio SMS Node

通过 Twilio 发送短信。


# Resources

+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/overview/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/architecture/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/filter-nodes/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/enrichment-nodes/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/transformation-nodes/
+ https://thingsboard.io/docs/user-guide/alarms/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/action-nodes/
+ https://thingsboard.io/docs/user-guide/rule-engine-2-0/external-nodes/
