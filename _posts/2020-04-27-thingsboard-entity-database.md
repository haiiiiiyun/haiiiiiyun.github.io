---
title: thingsboard 实体及数据存储研究
date: 2020-04-27
writing-time: 2020-04-27
categories: java thingsboard iot
tags: java thingsboard iot
---

## 1. 概述

本文主要研究 thingsboard 各种实体在关系型数据库 postgres 中的存储。

## 2. 安装与配置使用 Postgresql 数据库

从源码编译安装参考 : https://thingsboard.io/docs/user-guide/contribution/how-to-contribute/

编译运行后，需创建 thingsboard 数据库：

```bash
psql -U postgres -d postgres -h 127.0.0.1 -W
CREATE DATABASE thingsboard;
\q
```

Postgresql 的基本使用，见 http://www.atjiang.com/postgresql-beginner-11-tasks/

Thingsboard v2.4 中，默认使用的数据库用户名和密码都是 postgres, 见 `/application/src/main/resources/thingsboard.yml`:

```conf
datasource:
    driverClassName: "${SPRING_DRIVER_CLASS_NAME:org.postgresql.Driver}"
    url: "${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/thingsboard}"
    username: "${SPRING_DATASOURCE_USERNAME:postgres}"
    password: "${SPRING_DATASOURCE_PASSWORD:postgres}"
```

创建 schema 并导入测试数据：

```bash
cd ~/workspace/thingsboard/application/target/bin/install
chmod +x install_dev_db.sh
./install_dev_db.sh
```

### 登录测试

http://127.0.0.1:8080/

用户名 tenant@thingsboard.org
密码 tenant


# 实体

## Tenants 租户

是一个独立的商业实体：比如个人或组织，可以拥有若产生多个设备或资产。一个租户可有多个租户管理员用户及多个客户。

可将它理解为代理商，中间商，如中国移动是一个 tenant, 承包了某地区的所有项目，信息保存在 `tenant` 表中。

## Customers 客户

也是一个独立的商业实体：如何个人或组织，客户从租户那购买设备和资产。一个客户中可有多个用户。

可将它理解为甲方客户，如某单位或企业，从租户中国移动那购买服务。

信息保存在 `customer` 表中, 通过 `tenant_id` 关联相应的 tenant。

### Users 用户

用户登录系统，查看信息并管理实体的账号。系统中创建的用户，保存于 `tb_user` 中。

通过 `customer_id` 和 `tenant_id` 关联相应的租户和客户，用户权限由 `authority` 字段指定，值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/security/Authority.java

public enum Authority {
    
    SYS_ADMIN(0),
    TENANT_ADMIN(1),
    CUSTOMER_USER(2),
    REFRESH_TOKEN(10);
}
```

customer_id 和 tenant_id 有一个默认的值 1b21dd2138140008080808080808080，该值应该为系统中的一个默认 Tenant 和 Customer 值。 

例如系统管理员账户 "sysadmin@thingsboard.org" 对应的 customer_id 和 tenant_id 即为该值。

## Devices 设备

设备可上传遥测数据或执行 RPC 命令。

保存于 `device` 表中，通过 `customer_id` 和 `tenant_id` 关联相应的租户和客户。设备类型由 `type` 字符串字段指定，默认为 `default`, 可自由创建新值。

新建的设备，其默认 customer_id 为 1b21dd2138140008080808080808080，该值应该为系统中的一个默认 Customer 值。 

通过设备管理界面可以分配给指定客户。

设备的访问凭证信息保存在表 `device_credentials` 中，类型由 `credentials_type` 字段指定，类型值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/security/DeviceCredentialsType.java
public enum DeviceCredentialsType {
    ACCESS_TOKEN,
    X509_CERTIFICATE
}
```

## Assets  资产

一种用于关联其它设备和资产的抽象实体，如区域、建筑物、单位等，是一个容器概念。 保存于表 `asset` 中。

## Alarms 警报

与各种实体关联的警报事件。

保存于表 `alarm`，由 `originator_id` 和 `originator_type` 关联实体，状态由 `status` 字段指定，值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/alarm/AlarmSearchStatus.java
public enum AlarmSearchStatus {
    ANY, ACTIVE, CLEARED, ACK, UNACK
}
```

## Dashboards

可视化面板，可可视化数据，并操控设备。

保存于表 `dashboard` 中，Dashboard 由 tenant 所有，通过 `tenant_id` 字段关联。并可以分配给多人 customer, 分配信息保存在 `assigned_customers` 字段中，如:

```json
[
    {
        "customerId":{
            "entityType":"CUSTOMER",
            "id":"5c3c4ff0-8763-11ea-b734-6151c7bf4d3f"
        },
        "title":"Customer B",
        "public":false
    },
    {
        "customerId":{
            "entityType":"CUSTOMER",
            "id":"5c360e60-8763-11ea-b734-6151c7bf4d3f"
        },
        "title":"Customer A",
        "public":false
    }
]
```

## Rule Node 规则结点

处理结点，对上报的信息及实体事件进行处理。

保存在表 `rule_node` 中，通过 `rule_chain_id` 关联到某个规则链。

系统已创建了多种结点类型，当前结点类型在 `type` 字段中指定，值例如（有很多)：

+ "org.thingsboard.rule.engine.telemetry.TbMsgTimeseriesNode"
+ "org.thingsboard.rule.engine.telemetry.TbMsgAttributesNode"
+ "org.thingsboard.rule.engine.filter.TbMsgTypeSwitchNode"
+ "org.thingsboard.rule.engine.action.TbLogNode"
+ "org.thingsboard.rule.engine.rpc.TbSendRPCRequestNode"

见 thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/telemetry/TbMsgTimeseriesNode.java, thingsboard/rule-engine/rule-engine-components/src/main/java/org/thingsboard/rule/engine/action/TbLogNode.java 等文件中的定义。

配置信息保存在字段 `configuration` 中，是 JSON 字串，如 `{"timeoutInSeconds":60}`。

`additional_info` 字段中保存当前结点在规则链配置界面中的坐标，是 JSON 字串，如 `{"layoutX":824,"layoutY":138}`。


## Rule Chain 规则链

关联的多个规则结点的一个逻辑单元。

保存于表 `rule_chain` 中，首个结点通过 `first_rule_node_id` 指定，通过 `root boolean` 指定是否为根链，通过 `tenant_id` 关联 Tenant。描述信息等以 JSON 字串形式保存在 `additional_info` 字段中。


# 所有实体支持属性、遥测数据和关联： Attributes, Telemetry date, Relations.

## Attributes 属性

属性值是键值对， 保存于表 `attribute_kv` 中。实体由 `entity_type` 和 `entity_id` 字段关联，属性类型由 `attribute_type` 指定，值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/DataConstants.java
public class DataConstants {
    public static final String CLIENT_SCOPE = "CLIENT_SCOPE";
    public static final String SERVER_SCOPE = "SERVER_SCOPE";
    public static final String SHARED_SCOPE = "SHARED_SCOPE";

    public static final String[] allScopes() {
        return new String[]{CLIENT_SCOPE, SHARED_SCOPE, SERVER_SCOPE};
    }
```

kv 值中的 key 在 `attribute_key` 中保存，value 在 `bool_v`, `str_v`, `long_v`, `dbl_v` 字段其中一个中保存，分别表示为 bool, string, long, double 值。

## Telemetry data 遥测数据

时序数据。

历史值在 `ts_kv` 表中保存， 最新数据在 `ts_kv_latest` 表中保存。

实体由 `entity_type` 和 `entity_id` 字段关联，key 在 `key` 字段，时间在 `ts` 字段，值在 `bool_v`, `str_v`, `long_v`, `dbl_v`。

## Relations 关联

实体间的有向连接关系信息。

保存于表 `relation` 中，关联是两个实体间的一种关系，由 `from_id`, `from_type` 字段指定 from 端的实体，实体类型值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/EntityType.java
public enum EntityType {
    TENANT, CUSTOMER, USER, DASHBOARD, ASSET, DEVICE, ALARM, RULE_CHAIN, RULE_NODE, ENTITY_VIEW, WIDGETS_BUNDLE, WIDGET_TYPE
}
```

由 `to_id`, `to_type` 字段指定 to 端的实体。

关联关系由 `relation_type_group` 和 `relation_type` 字段指定。


### Audit Logs 审计日志

审计/操作记录信息保存在表 `audit_log` 中，操作者通过 `tenant_id`, `customer_id`, `user_id`, `user_name` 字段指定，操作对象通过 `entity_id`, `entity_type`, `entity_name` 字段指定， 操作类型由 `action_type` 字段指定，值见：

```java
// thingsboard/common/data/src/main/java/org/thingsboard/server/common/data/audit/ActionType.java
public enum ActionType {
    ADDED(false), // log entity
    DELETED(false), // log string id
    UPDATED(false), // log entity
    ATTRIBUTES_UPDATED(false), // log attributes/values
    ATTRIBUTES_DELETED(false), // log attributes
    TIMESERIES_DELETED(false), // log timeseries
    RPC_CALL(false), // log method and params
    CREDENTIALS_UPDATED(false), // log new credentials
    ASSIGNED_TO_CUSTOMER(false), // log customer name
    UNASSIGNED_FROM_CUSTOMER(false), // log customer name
    ACTIVATED(false), // log string id
    SUSPENDED(false), // log string id
    CREDENTIALS_READ(true), // log device id
    ATTRIBUTES_READ(true), // log attributes
    RELATION_ADD_OR_UPDATE(false),
    RELATION_DELETED(false),
    RELATIONS_DELETED(false),
    ALARM_ACK(false),
    ALARM_CLEAR(false),
    LOGIN(false),
    LOGOUT(false),
    LOCKOUT(false);

    private final boolean isRead;

    ActionType(boolean isRead) {
        this.isRead = isRead;
    }
}
```

操作数据以 JSON 字串形式保存在 `action_data` 中。

操作状态在 `action_status` 字段指定，值有 `SUCCESS` 和 `FAILURE`，如果失败，则失败信息在 `action_failure_details` 字段中保存，如 `PRC Error: Timeout`。


# 资源

+ [Install from source](https://thingsboard.io/docs/user-guide/contribution/how-to-contribute/)
+ [Entities and relations](https://thingsboard.io/docs/user-guide/entities-and-relations/)
