---
title: Create email login authentication with django-allauth in Django
date: 2024-02-20
tags: python django auth
categoris: Programming
---

[Django-allauth](https://docs.allauth.org/en/latest/) integrate set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.

## Create custom user model

see [[Create custom user model in Django]].

## Install django-allauth

```python
pip install django-allauth
```

### add to INSTALLED_APPS and MIDDLEWARE

Add `allauth` and `allauth.account` feature to settings.py, `allauth` depends on Django site framework, so we need to add it as well:

```python
INSTALLED_APPS = [
	# ...
    'django.contrib.sites',

    # third-party
    'allauth',
    'allauth.account',
]

MIDDLEWARE = [
	# ...
    'allauth.account.middleware.AccountMiddleware',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
# django-allauth config
SITE_ID = 1
```

### authentication backends

Django sets  `AUTHENTICATION_BACKENDS108` setting to `'django.contrib.auth.backends.ModelBackend'` implictly, which is used when Django attempts to authenticate a user.

Add the `django-allauth` specific authentication option, which will allow us to switch over to using login via email.

```python
# django-allauth config
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
```

### Email backend

Django sets `EMAIL_BACKEND` implicitly, by default Django will look for a configured SMTP server to send emails.

`django-allauth` will send such an email upon a successful user registration. For test purpose, we can have Django output any emails to the command line console by updating the `EMAIL_BACKEND` setting:

```python
# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new
```

Or we can disable email verification by set `ACCOUNT_EMAIL_VERIFICATION = "none"`

## account logout redirect

The default setting for `ACCOUNT_LOGOUT_REDIRECT` is `/`.

django-allauth's `ACCOUNT_LOGOUT_REDIRECT` actually overrides the built-in `LOGOUT_REDIRECT_URL`. We can move the two redirect lines under django-allauth config section:

```python
# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## run migrate to update DB

```python
python manage.py migrate
```

## URLs

Include `allauth.urls` in project's urls.py file, under path `accounts/`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
```

We'll have URLs such as `/accounts/login/`, `/accounts/signup/`,.etc.

## Templates

Django's `auth` app looks for templates within a `registration` directory, but `allauth` prefers they be located within a `account` directory(not **accounts**). We'll need to provide template files such as `account/login.html`, `account/signup.html`, `account/logout.html`.

The URL names from `allauth` are different with the ones from `auth`, all of the URL name from `allauth` have a `account_` prefix, so Djanog's `logout` will now be `account_logout`, ...

<!-- {% raw %} -->
```html
<ul class="navbar-nav me-auto mb-2 mb-md-0">
	<li class="nav-item"><a class="nav-link" href="{% url 'about' %}">About</a></li>
	{% if user.is_authenticated %}
		<li class="nav-item"><a class="nav-link" href="{% url 'account_logout' %}">Log Out</a></li>
	{% else %}
		<li class="nav-item"><a class="nav-link" href="{% url 'account_login' %}">Log In</a></li>
		<li class="nav-item"><a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a></li>
	{% endif %}
</ul>
```
<!-- {% endraw %} -->

## Log in page

The template file is `account/login.html`.

Now the login page has a `Remember Me` box option by default, we can remove it by setting `ACCOUNT_SESSION_REMEMBER = True`:

```python
# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_SESSION_REMEMBER = True # new
```

## Log out page

Click logout will display a log out confirmation page, the template of which is `account/logout.html`:

<!-- {% raw %} -->
```html
{% extends "_base.html" %}
{% load crispy_forms_tags %}

{% block title %}Log In{% endblock title %}

{% block content %}
    <h2>Log Out</h2>
    <p>Are you sure you want to log out?</p>
    <form method="post" action="{% url 'account_logout' %}">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-danger" type="submit">Log Out</button>
    </form>
{% endblock content %}
```
<!-- {% endraw %} -->

## Sign up page

The template is `account/signup.html`.

An optional customization we can make via django-allauth is to only ask for a password once:

```python
# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False # new
```

## Email only login

This requires a few changes. First we'll make `username` not required, but set `email` instead to be required. Then we'll require `email` to be unique and the authentication method of choice:

```python
# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False # new
ACCOUNT_EMAIL_REQUIRED = True # new
ACCOUNT_UNIQUE_EMAIL = True # new
ACCOUNT_AUTHENTICATION_METHOD = 'email' # new
```