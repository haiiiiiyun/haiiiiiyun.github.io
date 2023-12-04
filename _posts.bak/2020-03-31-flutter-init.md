---
title: Ubuntu 上开发 Flutter 设置
date: 2020-03-31
writing-time: 2020-03-31
categories: flutter dart android ubuntu
tags: flutter dart android ubuntu
---

# 1. 安装 flutter SDK

可以直接 git clone flutter 的 github 库，或从官网下载压缩包，但都比较慢，最好从 [中文镜像](https://flutter.cn/docs/get-started/install) 下载压缩包。

解压到 `$HOME/opt/flutter/`，并更新路径: `export PATH="$PATH:$HOME/opt/flutter/bin"`

国内下载安装 flutter 相关包会比较慢，最好设置从国内镜像下载，在 ~/.bashrc 中设置：


```bash
# flutter
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
export PATH="$PATH:$HOME/opt/flutter/bin"
```

下载解压后，运行 `flutter doctor` 检测 flutter 安装情况。

doctor 命令会列出相关的问题列表，如未安装 Android Studio, Android Studio 中未安装相关的 SDK 或工具等，逐个修复。

# 2. 安装 Android Studio

下载安装 [Android Studio](https://developer.android.google.cn/studio)，`File > Settings > Plugins` 安装 Flutter 和 Dart 插件。

如果在插件搜索页中无法搜索插件，则需要 FanQiang。

# 创建虚拟设备

`Tools > Avd manager` 中创建 Pixel 2 API 28 设备。

# 3. 创建项目

`File > New > New Flutter Project...` 创建测试项目。


# 资源

+ [flutter 官网](https://flutter.dev/)
+ [flutter 社区中文资源](https://flutter.cn/)
