---
title: Use environs package in Django
date: 2024-02-21
tags: python django envs
categoris: Programming
---

[environs](https://pypi.org/project/environs/) package has a Django-specific option that installs a number of additional packages the help with configuration.

## Install environs

```bash
pip install environs
```

Or install with Django extension:

```bash
pip install environs[django]
```

## Usage

By default, `Env.read_env` will look for a `.env` file in current directory and (if no .env exists in the CWD) recursively upwards until a .env file is found.

environs supports many types, such as:

+ env.str (default)
+ env.bool
+ env.int
+ env.list
+ env.dict
+ env.json

With Django extension, it supports types such as:

+ env.dj_db_url
+ env.dj_cache_url
+ env.dj_email_url

## Example

```
# .env
SECRET_KEY = 'django-insecure-keyexample'
DEBUG = True
ALLOWED_HOSTS = 127.0.0.1,localhost
```

```python
# settings.py
from pathlib import Path
from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()  # read .env file, if it exists
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
```