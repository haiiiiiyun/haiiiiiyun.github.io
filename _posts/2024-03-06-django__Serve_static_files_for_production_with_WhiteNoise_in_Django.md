---
title: Serve static files for production with WhiteNoise in Django
date: 2024-03-06
tags: python django statics
categoris: Programming
---

Django relies on the `staticfiles` app to serve static files for local development.

For production, we run `collectstatic` command to compile all static files into a single directory specified by `STATIC_ROOT`, see [[Collect static files for production serving in Django]]. The files can then be served by the same django server with the aid of [Whitenoise](https://whitenoise.readthedocs.io/en/stable/index.html) .

## Install WhiteNoise

```python
pip install whitenoise
```

## Make sure staticfiles is configured correctly

see [[Collect static files for production serving in Django]]

## Enable WhiteNoise

Add the WhiteNoise middleware after `SecurityMiddleware` and before all other middlewares:

```python
MIDDLEWARE = [
    # ...
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...
]
```

## Add compression and caching support

WhiteNoise comes with a storage backend which compresses your files and hashes them to unique names, so they can safely be cached forever. To use it, set it as your staticfiles storage backend in your settings file.

On Django 4.2+:

```python
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

On older Django versions:

```python
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

## Using WhiteNoise in development

In development Django's `runserver` automatically takes over static file handling.

We can disable Django's static file handling and allow WhiteNoise to take over simply by passing the `--nostatic`  option to the `runserver` command. Another way is to edit `settings.py` file and add `whitenoise.runserver_nostatic` to the top of `django.contrib.staticfiles`:

```python
INSTALLED_APPS = [
    # ...
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # ...
]
```