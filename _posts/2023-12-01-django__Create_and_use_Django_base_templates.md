---
title: Create and use Django base templates
date: 2023-12-01
tags: python django templates
categoris: Programming
---

Multiple pages share same code block, such as `<nav>` and `<footer>`,  if we copy the exact same code into multiple pages, it would duplicate a lot of the same code. Worse, it will be hard to maintain the code .

To fix this, we use base templates, this allow us to make changes in a single place, and it will apply to every page.

Since this will be a "global" template (which will be used across all pages and apps), we will add it to the main folder(the one that has `settings.py` and `wsgi.py`). 

1. Under this folder, create a folder `templates`, and create a file `base.html` under this folder:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Movies App</title>
  </head>
  <body>
    <nav>
      <a class="nav-link" href="#">News</a>
      <a class="nav-link" href="#">Login</a>
      <a class="nav-link" href="#">Sign Up</a>
    </nav>
    <div class="container">
      {% block content %}
      {% endblock content %}
    </div>
    <div class="footer">footer: copywrite</div>
  </body>
</html>
```

In the base template, we allocate a block with name `content`, where content can be slotted in from other child pages:

```html
{% block content %}
{% endblock content %}
```

2. Register the template folder in our project `settings.py`:

```python
TEMPLATES = [
    {
        # ...
        'DIRS': [os.path.join(BASE_DIR, 'moviereviews/templates')],
        # ...
        },
    },
]
```

3. Use the base template in child page:

```html
{% extends 'base.html' %}

{% block content %}
My content
{% endblock content %}
```