---
title: Basic settings of Django project
date: 2023-11-16
tags: python django settings
categoris: Programming
---

`settings.py` file contains properties for project's settings.

Here are several basic properties:

+ `BASE_DIR`: Determines where on your machine the project is situated.
+ `SECRET_KEY`:  Used when we have data flowing in and out of our website. **DO NOT EVER** share this with others.
+ `DEBUG`: Our site can run in debug mode or not. In debug mode, we get detailed information on errors.
+ `INSTALLED_APPS`: Allows us to bring different pieces of code into our project.
+ `MIDDLEWARE`:  Refers to built-in Django functions to process application requests/responses, which include authentication, session and security.
+ `ROOT_URLCONF`: Specifies where our URLs are.
+ `TEMPLATES`: Defines the template engine class, the list of directories where the engine should look for template source files, and specific template settings.
 + `AUTH_PASSWORD_VALIDATORS`:  Allow us to specify the validations that we want on passwords - for example, a minimum length.