---
title: Connect Django view to Django template
date: 2023-11-16
tags: python django templates
categoris: Programming
---

Every web framework needs a way to generate full HTML pages. In Django we use `templates` to serve individual HTML files.

Each app should have its own templates folder, for example, in the `movie` app folder, create a folder called `templates/`, Django will look for template files iterating over every app's templates folder.

See [[Why we have to place template files under a sub-folder that is named after app name]]

In Django development, we will see pattern for each page: **templates**, **views** and **URLs**.

To create a function view and define an URL, see [[Define an URL and link it to a function view]].

## Template

Create a new template file `about.html` in `movie/templates`, fill it with the following:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Movies App</title>
  </head>
  <body>
    <h1>Welcome to About Page, {{ name }}</h1>
    <h2>This is the full about page</h2>
  </body>
</html>
```

## View

Back in `movie/views.py`, add a `about` view and connect it to the template `about.html`.

```python
from django.shortcuts import render

def about(request):
    return render(request, 'about.html', {'name': 'Jump Roper'})
```

The view contains the business logic or the **what**.

## Passing data into templates

When rendering views, we can pass in a dictionary with a key-value pair(here is `{'name': 'Jump Roper'}`) to the template `home.html`.

In the template, we retrieve the dictionary values with the `{{ key }}` notation, for example `{{ name }}`.

`{{ }}` is the variable syntax from Django Template Language(DTL).