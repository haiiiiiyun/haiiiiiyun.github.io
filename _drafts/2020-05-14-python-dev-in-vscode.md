---
title: 在 VSCode 中开发 Python 程序
date: 2020-05-14
writing-time: 2020-05-14
categories: python ubuntu vscode django
tags: python ubuntu vscode django
---

插件： [Python By Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

用 pyenv 安装多个 python 版本。

打开项目

```bash
mkdir hello
cd hello
code .
```

这样，VS Code 的相关配置会保存在当前目录的 `.vscode/settings.json` 中。


# 选择 Python 解释器

用 `Ctrl+Shift+P` 打开 `Command Palette` 界面，输入 `Python:Select Interpreter` 命令进行选择。也可以点击 VS Code 左下边状态栏上的 `Select Python Environment` 进行选择。

一般是选择由 pyenv virtualenv 创建的虚拟环境中的 python 程序，例如 `/home/hy/.pyenv/versions/py38django22/bin/python3`。

配置后，会在左下边状态栏上显示当前的 python 版本及环境，如 `Python 3.8.2 64-bit('py38django22':venv)`，表示当前的 Python 来自 venv 创建的虚拟环境 py38django22 中。

同时，会在配置文件 `.vscode/settings.json` 中进行记录，如 `"python.pythonPath": "/home/hy/.pyenv/versions/py38django22/bin/python3"`。


# 运行

+ 点击当前 python 文件编辑器工具栏右上角的 `Run Python File in Terminal` 按钮。
+ 当前文件中右键-> `Run Python File in Terminal`。
+ 选中多行，右键-> `Run Selection/Line in Python Terminal` 或 `Shift+Enter`。


# 调试

创建断点： `F9`，开始/继续执行 `F5`，首次调试执行时会打开 `Command Palette` 对 `debug configuration` 进行配置，选择 `Python File` 或 `Django` 等，这些调试配置信息保存 在 `launch.json` 中。


# 编辑功能

+ 跳转到定义处： `F12` 
+ 在当前位置直接显示定义信息： `Ctrl+Shift+F10`


## 配置自动补全功能

将不用通过 pip 安装的第三方包路径添加到 `settings.json` 中，为这些包实现自动补全，如：

```json
"python.autoComplete.extraPaths": [
    "~/.local/lib/Google/google_appengine",
    "~/.local/lib/Google/google_appengine/lib/flask-0.12" ]
```

配置自动添加对应的括号符（默认 false)：

```json
"python.autoComplete.addBrackets": true,
```

## 重构代码

重构 import 语句： 右键 `Sort Imports`

# 使用 PEP8 和 lint 

在 settings.json 中添加：

```json
{
  "python.linting.pep8Enabled": true,
  "python.linting.pylintPath": "/path/to/virtualenv/bin/pylint",
  "python.linting.pylintArgs": ["--load-plugins", "pylint_django"],
  "python.linting.pylintEnabled": true
}
```

VS Code 会提示安装 pylint 和 autopep8，也可以先直接安装：

```bash
pip install autopep8
pip install pylint
```


# Django debugging

In launch.json:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "stopOnEntry": true,
      "pythonPath": "${config:python.pythonPath}",
      "program": "${workspaceRoot}/manage.py",
      "cwd": "${workspaceRoot}",
      "args": ["runserver", "--noreload", "--nothreading"],
      "env": {},
      "envFile": "${workspaceRoot}/path/to/virtualenv",
      "debugOptions": [
        "WaitOnAbnormalExit",
        "WaitOnNormalExit",
        "RedirectOutput",
        "DjangoDebugging"
      ]
    }
  ]
}

```

Djaneiro this extension provides a collection of snippets for Django templates,

使用 Material Icon Theme:  File-> Preferences -> File Icon Theme


其它设置：

settings.json

```json
"editor.formatOnSave": true,
    "editor.rulers": [
        80,
        120
    ],
    "files.exclude": {
        "**/.git": true,
        "**/.svn": true,
        "**/.hg": true,
        "**/CVS": true,
        "**/.DS_Store": true,
        ".vscode": true,
        "**/*.pyc": true
    },
    "workbench.editor.enablePreview": false,
    "editor.minimap.enabled": false,
```



# 资源

+ [vscode python tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
+ [vscode python editing code](https://code.visualstudio.com/docs/python/editing)
+ https://ruddra.com/posts/vs-code-for-python-development/
+ https://djangocentral.com/visual-studio-code-setup-for-django-developers/
