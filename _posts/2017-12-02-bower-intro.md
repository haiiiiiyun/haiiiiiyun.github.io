---
title: Bower 入门
date: 2017-12-02
writing-time: 2017-12-02
categories: programming
tags: bower npm node nodejs webpack yarn
---

# 简介
Bower 是一个前端项目的包管理器，用来管理项目的依赖包，类似 [Yarn](https://yarnpkg.com/en/)。同时它也能管理 HTML, CSS, JS, fonts，图片文件，类似 [Webpack](https://webpack.js.org/)。


# 安装

```bash
$ npm install -g bower
```

# 包管理

## 依赖包管理文件

所有的依赖包都记录在 `bower.json` 文件中，类似 npm 的 `package.json` 文件。该文件可以通过运行 `bower init` 创建。

## 安装依赖包

使用 `bower install` 来安装依赖包，依赖包安装在 `bower_components/` 下。

可以通过已注册的包名、URL 等来安装：

```bash
# installs the project dependencies listed in bower.json
$ bower install
# registered package
$ bower install jquery
# GitHub shorthand
$ bower install desandro/masonry
# Git endpoint
$ bower install git://github.com/user/package.git
# URL
$ bower install http://example.com/script.js
```

通过 `bower install PACKAGE --save` 将安装的依赖包同时登记到 `bower.json` 文件中。

## 使用包

可以直接使用安装了的包：

```html
<script src="bower_components/jquery/dist/jquery.min.js"></script>
```

也可以结合其它工具，如 Grunt, RequireJS, Yeoman 等使用。

## 包查找

可以在 https://bower.io/search/ 中查找需要的包。也可以用 `bower search <name>` 命令查找。


# 配置文件

Bower 的配置文件是一个名为 `.bowerrc` 的 JSON 文件。内容如：

```json
{
  "directory": "app/components/",
  "timeout": 120000,
  "registry": {
    "search": [
      "http://localhost:8000",
      "https://registry.bower.io"
    ]
  }
}
```

## 配置项的来源及优先次序

优先级从高到低依次如下：


+ 通过命令行的 `--config` 参数配置的配置项，例如 `--config.endpoint-parser=<parser>` 传入了 `endpoint-parser` 配置项。
+ 环境变量，例如 `bower_endpoint_parser` 环境变量将解析成 `endpoint-parser` 配置项。数组值的环境变量定义为： `export bower_registry__search='[http://localhost:8080, http://registry.bower.io]'; bower install`。
+ 当前工作目录下的 `.bowerrc` 文件中的配置项。
+ 目录树上所有 `.bowerrc` 文件中的配置项。
+ HOME 目录下的 `.bowerrc` 文件中的配置项。
+ `/` 下的 `.bowerrc` 文件中的配置项。

`.bowerrc` 文件中可配置项有：

```json
{
  "cwd": "~/.my-project",
  "directory": "bower_components",
  "registry": "https://registry.bower.io",
  "shorthand-resolver": "git://github.com//.git",
  "proxy": "http://proxy.local",
  "https-proxy": "http://proxy.local",
  "ca": "/var/certificate.pem",
  "color": true,
  "timeout": 60000,
  "save": true,
  "save-exact": true,
  "strict-ssl": true,
  "storage": {
    "packages" : "~/.bower/packages",
    "registry" : "~/.bower/registry",
    "links" : "~/.bower/links"
  },
  "interactive": true,
  "resolvers": [
    "mercurial-bower-resolver"
  ],
  "shallowCloneHosts": [
    "myGitHost.example.com"
  ],
  "scripts": {
    "preinstall": "",
    "postinstall": "",
    "preuninstall": ""
  },
  "ignoredDependencies": [
    "jquery"
  ]
}
```

配置项的详细描述见 [bower/spec](https://github.com/bower/spec/blob/master/config.md)。

`.bowerrc` 文件中配置项内容可以引用环境变量，形如 `${ENV_VAR}`：

```json
"storage" : {
  "packages": "/path/to/${USER}/packages"
}
```

## Hooks

Bower 支持 3 个 hook，当 Bower 安装或删除包后，可用来触发其它工具将相关的安装包关联到项目中。

```json
{
  "scripts": {
    "preinstall": "<your command here>",
    "postinstall": "<your command here>",
    "preuninstall": "<your command here>"
  }
}
```

配置的命令中可以包含 `%`，脚本调用时，安装/删除的所有包名，以空格为分隔符，组合一个字符串用来替代 `%`。

脚本中还可以访问 `BOWER_PID` 环境变量，用来判断触发该脚本的 Bower PID。



## 参考

+ https://bower.io/
