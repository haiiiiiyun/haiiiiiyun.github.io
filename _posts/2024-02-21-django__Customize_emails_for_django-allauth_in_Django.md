---
title: Customize emails for django-allauth in Django
date: 2024-02-21
tags: python django auth
categoris: Programming
---

See [[Create email login authentication with django-allauth in Django]].

## Custom confirmation emails

After signing up we receive an activation email with content `...You're receiving this e-mail because user...`.

To customize this email we first need to find the existing templates. Navigate over to the [djano-allauth source code on Github](https://github.com/pennersr/django-allauth) and perform a search with a portion of the generated text. This leads to template file `django-allauth/allauth/templates/account/email/email_confirmation_message.txt` and  `django-allauth/allauth/templates/account/email/email_confirmation_subject.txt` and 

To customize, create a directory `templates/account/email/`, and copy these two files to the directory and update them:

<!-- {% raw %} -->
email_confirmation_subject.txt:

```
{% load i18n %}
{% autoescape off %}
{% blocktrans %}Please Confirm Your E-mail Address{% endblocktrans %}
{% endautoescape %}
```

email_confirmation_message.txt:

```
{% extends "account/email/base_message.txt" %}
{% load account %}
{% load i18n %}
{% block content %}{% autoescape off %}{% user_display user as user_display %}\
{% blocktrans with site_name=current_site.name site_domain=current_site.domain %}\
You are receiving this e-mail because user {{ user_display }} has given your \
e-mail address to register an account on {{ site_domain }}.
To confirm this is correct, go to {{ activate_url }}\
{% endblocktrans %}{% endautoescape %}{% endblock %}
```
<!-- {% endraw %} -->

### site_name

We can update the `site_name` in Django admin page, in the Sites section.

### from email address

Default value is `webmaster@localhost`, update it in settings.py:

```python
DEFAULT_FROM_EMAIL = "admin@djangobookstore.com"
```

## Email confirmation page

Click on the unique URL link in the confirmation email which redirects to the email confirm page. It's template file is `account/email_confirm.html`, see https://github.com/pennersr/django-allauth/blob/main/allauth/templates/account/email_confirm.html


## Email services 

There are many transactional email providers available including SendGrid, MailGun, Amazon’s Simple Email Service. 

Django is agnostic about which provider is used.