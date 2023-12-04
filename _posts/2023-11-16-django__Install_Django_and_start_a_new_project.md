---
title: Install Django and start a new project
date: 2023-11-16
tags: python django
categoris: Programming
---

## Install python and setup virtual environment

see [[Manage python versions and virtual environments with pyenv and pyenv-virtualenv]].

Note: we might have to use `python3`, `pip3`  instead of `python`, `pip` on Mac.

## install django using pip:

```bash
$ pip install Django

$ python -m django

Type 'python -m django help <subcommand>' for help on a specific subcommand.

Available subcommands:
...
```

## Start a new project

```bash
$ python -m django startproject moviereviews
```

A `moviereviews` folder will be created.  Its contents see: [[Django project structure and folder contents]]

## Start the local development server

```bash
$ cd moviereviews
$ python manage.py runserver
```

Now we can visit the link:  http://127.0.0.1:8000/