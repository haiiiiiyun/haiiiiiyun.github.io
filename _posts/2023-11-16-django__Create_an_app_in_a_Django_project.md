---
title: Create an app in a Django project
date: 2023-11-16
tags: python django
categoris: Programming
---

A single Django project can contain one or more **apps** that work together to power a web application. Django uses the concept of projects and apps to keep code clean and readable.

For example, on a movie review site such as Rotten Tomatoes, we can have an app for listing movies, an app for listing news, an app for payments, an app for user authentications, and so on.

Apps in Django are like pieces of a website. We can create an entire website with one single app, but it is useful to break it up into different apps, each representing a clear function.

To create an app movie, run:

```bash
$ cd projectfolder/
projectfoler/$ python manage.py startapp movie
```

A new folder `movie` will be added to the project folder.

Although the new app exists in the Django project, Django doesn't recognize it till we explicitly add it. To do so, we need to specify it in `settings.py`.

Go to `projectfoler/settings.py`, under `INSTALLED_APPS`, and you will see several
built-in apps already there, append the new app there:

```
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',

'movie',
]
```