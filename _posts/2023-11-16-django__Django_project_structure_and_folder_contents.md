---
title: Django project structure and folder contents
date: 2023-11-16
tags: python django
categoris: Programming
---

Django projects contain a predefined structure with some key files, and they are composed of one or more apps.

To create a Django project, see [[Install Django and start a new project]].

After created, we can see the project folder is `moviereviews`, look into the folder with `tree` command:

```bash
$ cd moviereviews
moviereviews/$ tree
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

## Rename the project folder name

As we can see, there is a folder with the same name as the project folder `moviereviews`. To avoid confusion and to distinguish between the two folders, we can keep the inner folder as it is and rename the outer folder with an suffix, like `moviereviewsproject`.

## Contents of Django project folder

The  `manage.py` file helps us to perform administrative operations. For example, we can start the local dev server with `python manage.py runserver` or create a new app with `python manage.py startapp`. We should not tinker with this file.

The `db.sqlite3` file contains our database.

### Contents of folder `moviereviewsproject/moviereviews`

+ `__pycache__`: This folder stores compiled bytecodes, can we ignore this folder.
+ `__init__.py`:  This file specifies what to run when Django launches for the first time.
+ `wsgi.py`: This file stands for the **Web Server Gateway Interface(WSGI)** and helps Django server our web pages.
+ `asgi.py`: This file allows an optional **Asynchronous Server Gateway Interface(ASGI)** to run.
+ `urls.py`: This file tells Django which pages to render in response to a browser or URL request.
+ `settings.py`: This file controls our project's settings. It contains several properties, see [[Basic settings of Django project]].

To create Django apps, see [[Create an app in a Django project]].