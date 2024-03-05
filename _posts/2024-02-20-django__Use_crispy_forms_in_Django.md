---
title: Use crispy forms in Django
date: 2024-02-20
tags: python django forms django-crispy-forms
categoris: Programming
---

[Django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) provides a tag and filter that lets us quickly render forms in a div format while providing an enormous amount of capability to configure and control the rendered HTML.

Django-crispy-forms supports CSS frameworks such as Bootstrap, tailwind, Bulma and Foundation. 

## Install packages

```python
pip install django-crispy-forms crispy-bootstrap5
```

install crispy-bootstrap5 if we want to work with bootstrap5.

## Settings

In `settings.py`, add crispy_forms to `INSTALLED_APPS`:

```python
# django_project/settings.py
INSTALLED_APPS = [
	#...
	# Third-party
	"crispy_forms",
	"crispy_bootstrap5",
]
```

Also append the following to settings:

```python
# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

Now django_crispy_forms will provide pre-styled forms for us.

## Use it in template file

<!-- {% raw %} -->
To use Cripsy Forms we load `crispy_forms_tags` at the top of a template and add `{{ form|crispy }}` to replace `{{ form.as_p }}` for displaying form fields.

```html
<!-- templates/registration/login.html -->
{% extends "_base.html" %}
{% load crispy_forms_tags %}

{% block title %}Log In{% endblock title %}

{% block content %}
    <h2>Log In</h2>
    <form method="post">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success" type="submit">Log In</button>
    </form>
{% endblock content %}
```
<!-- {% endraw %} -->