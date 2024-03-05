---
title: Create a superuser account for a Django project
date: 2023-11-17
tags: python django auth
categoris: Programming
---

We need username and password to log in to Django Admin page.

To first create a superuser, run:

```bash
$ python manage.py createsuperuser
```

Note:  user information are stored in databases. When we first start up a new project, there is no user related database table existing. We have to run `python manage.py migrate` and apply all models migrations for the built-in apps, including the `django.contrib.auth` app.

To manage model migrations, see [[Create a Model in Django app and manage migrations]].

To change user password:

```bash
$ python manage.py changepassword <username>
```