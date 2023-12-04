---
title: Create a Model in Django app and manage migrations
date: 2023-11-17
tags: python django models DB
categoris: Programming
---

Working with databases in Django involves working with models. A **model** contains the fields and behaviors of the data we want to store. 

Commonly, each **model** maps to a database **table**, and **field** in a model maps to table **column**.

Here are the Django model basics:

+ Each model is a class that extends `django.db.models.Model`
+ Each model property represents a database column.
+ Django provides us with a set of useful methods to **CRUD** model information from a database.

### Create model

Each app has the `models.py` file, we create model in this file, for example:

```python
from djang.db import models

class Movie(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	image = models.ImageField(upload_to='movie/images/')
	url = models.URLField(blank=True)
```

class `Movie` inherits from `Model` class, which allows us to interact with the database, create a table, and retrieve and make changes to data in the database.

Django provides many model fields to support common types such as CharField, ImageField, URLField.

### Manage migrations

**Migrations** allows us to generate a database schema based on model code. Once we make changes to our models(such as adding a field, renaming a field), new migrations should be created.

In the end, migrations allow us to have a trace of the evolution of our database schema(as a version control system).

After model changing,  run `makemigrations` command to generate the SQL commands for the defined models in all preinstalled apps in the `INSTALLED_APPS` setting. The SQL commands are not yet executed but are just a record of all changes to our models. The migrations are stored in an auto-generated folder `migrations/` under the app folder.

```bash
$ python manage.py makemigrations [appname]
```

To actually execute the SQL commands in the migrations file, run:

```bash
$ python manage.py migrate [appname]
```