---
title: 使用 thingsboard 示例应用
date: 2019-11-22
writing-time: 2019-11-22
categories: java;thingsboard;iot
tags: java;thingsboard;iot
---

# 1. 访问

地址: 127.0.0.1:8080

测试用户: tenant@thingsboard.org
密码: tenant

其它的测试账号、测试设备 Tokens 见 [Demo Account](https://thingsboard.io/docs/samples/demo-account/)。

# 2. 数据上传

Dashboard 中的 `Temperature & Humidity Demo` 对应设备 DHT11 Demo，Token 为 DHT11_DEMO_TOKEN。

## 2.1 通过 cURL 上传数据

```bash
sudo apt-get install curl

curl -v -X POST -d "{\"temperature\": 30, \"humidity\": 80}" http://localhost:8080/api/v1/DHT11_DEMO_TOKEN/telemetry --header "Content-Type:application/json"   # Dashboards 上的数据有时候不能同步刷新?
```

## 2.2 通过 MQTT.js 上传数据

```bash
mkdir tmp #创建临时目录用于保存测试数据
cd tmp
npm install mqtt  # 安装 mqtt
```

创建数据文件 `attributes-data.json`, 其包含设备属性值 `firmware_version` 和 `serial_number`:

```json
{"firmware_version":"1.0.1", "serial_number":"SN-001"}
```

创建数据文件 `telemetry-data.json`, 其包含设备温湿度值:

```json
{"temperature":21, "humidity":55.0, "active": false}
```

创建 `publish.js`:

```javascript
var mqtt = require('mqtt');

console.log('Connecting to: %s using access token: %s', process.env.THINGSBOARD_HOST, process.env.ACCESS_TOKEN);

var client  = mqtt.connect('mqtt://'+ process.env.THINGSBOARD_HOST,{
    username: process.env.ACCESS_TOKEN
});

client.on('connect', function () {
    console.log('Client connected!');
    client.publish('v1/devices/me/attributes', process.env.ATTRIBUTES);
    console.log('Attributes published!');
    client.publish('v1/devices/me/telemetry', process.env.TELEMETRY);
    console.log('Telemetry published!');
    client.end();
});
```

创建 `mqtt-js.sh`:

```bash
#!/bin/sh

# Set ThingsBoard host to "demo.thingsboard.io" or "localhost"
export THINGSBOARD_HOST=localhost

# Replace YOUR_ACCESS_TOKEN with one from Device details panel.
export ACCESS_TOKEN=DHT11_DEMO_TOKEN

# Read serial number and firmware version attributes
ATTRIBUTES=$( cat attributes-data.json )
export ATTRIBUTES

# Read timeseries data as an object without timestamp (server-side timestamp will be used)
TELEMETRY=$( cat telemetry-data.json )
export TELEMETRY

# publish attributes and telemetry data via mqtt client
node publish.js
```

```bash
chmod +x mqtt-js.sh
./mqtt-js.sh
Connecting to: localhost using access token: DHT11_DEMO_TOKEN
Client connected!
Attributes published!
Telemetry published!
```


## 2.3 通过 MQTT Mosquitto 客户端上传数据

```bash
sudo apt-get install mosquitto-clients
```

创建 `mosquitto.sh`:

```bash
#!/bin/sh

# Set ThingsBoard host to "demo.thingsboard.io" or "localhost"
THINGSBOARD_HOST="localhost"
# Replace YOUR_ACCESS_TOKEN with one from Device details panel.
ACCESS_TOKEN="DHT11_DEMO_TOKEN"

# Publish serial number and firmware version attributes
mosquitto_pub -d -h "$THINGSBOARD_HOST" -t "v1/devices/me/attributes" -u "$ACCESS_TOKEN" -f "attributes-data.json"
# Publish timeseries data as an object without timestamp (server-side timestamp will be used)
mosquitto_pub -d -h "$THINGSBOARD_HOST" -t "v1/devices/me/telemetry" -u "$ACCESS_TOKEN" -f "telemetry-data.json"
```

上传:

```bash
chmod +x mosquitto.sh
./mosquitto.sh

Client mosqpub/23608-hy-OptiPl sending CONNECT
Client mosqpub/23608-hy-OptiPl received CONNACK
Client mosqpub/23608-hy-OptiPl sending PUBLISH (d0, q0, r0, m1, 'v1/devices/me/attributes', ... (55 bytes))
Client mosqpub/23608-hy-OptiPl sending DISCONNECT
Client mosqpub/23614-hy-OptiPl sending CONNECT
Client mosqpub/23614-hy-OptiPl received CONNACK
Client mosqpub/23614-hy-OptiPl sending PUBLISH (d0, q0, r0, m1, 'v1/devices/me/telemetry', ... (53 bytes))
Client mosqpub/23614-hy-OptiPl sending DISCONNECT
```

## 2.4 通过 CoAP 客户端上传数据

```bash
sudo npm install coap-cli -g
```

创建 `coap-js.sh`:

```bash
#!/bin/sh

# Set ThingsBoard host to "demo.thingsboard.io" or "localhost"
THINGSBOARD_HOST="localhost"
# Replace YOUR_ACCESS_TOKEN with one from Device details panel.
ACCESS_TOKEN="DHT11_DEMO_TOKEN"

# Publish serial number and firmware version attributes
cat attributes-data.json | coap post coap://$THINGSBOARD_HOST/api/v1/$ACCESS_TOKEN/attributes
# Publish timeseries data as an object without timestamp (server-side timestamp will be used)
cat telemetry-data.json | coap post coap://$THINGSBOARD_HOST/api/v1/$ACCESS_TOKEN/telemetry
```

上传:

```bash
chmod +x coap-js.sh
./coap-js.sh
```

# Resources
https://thingsboard.io/docs/samples/demo-account/
https://thingsboard.io/docs/getting-started-guides/helloworld/
