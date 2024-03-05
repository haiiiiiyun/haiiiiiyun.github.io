---
title: How to view directory tree structure in Linux
date: 2023-11-16
tags: linux shell
categoris: Programming
---

We can use `tree` command to display the contents of a directory in a tree-like format in Linux and Unix-like OS. `tree` command is a recursive directory listing program that produces a depth indented listing of files.

Install tree on Ubuntu:

```bash
$ sudo apt-get install tree
```

If we run the `tree` without any arguments, it will display all contents of the current working directory in a tree-like format:

```bash
$ moviereviews/$ tree
.
├── db.sqlite3
├── manage.py
└── moviereviews
    ├── asgi.py
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-312.pyc
    │   ├── settings.cpython-312.pyc
    │   ├── urls.cpython-312.pyc
    │   └── wsgi.cpython-312.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

2 directories, 11 files
```

Some parameters:

+ only list the directories with `-d`:  `$ tree -d /etc/`
+ list hidden files as well with `-a`:  `$ tree -a /etc/`

See https://ostechnix.com/view-directory-tree-structure-linux/