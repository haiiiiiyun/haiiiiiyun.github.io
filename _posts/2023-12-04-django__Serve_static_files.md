---
title: Serve static files
date: 2023-12-04
tags: python django statics
categoris: Programming
---

To server user uploaded files, see [[Sever media files uploaded by a user during development]].

1. In `settings.py` we already have a `STATIC_URL = 'static/'`
2. We create a folder `static/images/` under the project's folder such as `moviereviews`.
3. We store fixed images such as `logo.png` in this folder.
4. In template files such as the `moviereviews/templates/base.html`,  we first load the `static` function with <!--{% raw %}--> `{% load static %}`<!--{% endraw %} --> at the top of the template file and then reference the static file as<!--{% raw %}--> `{% static 'images/logo.png' %}`<!--{% endraw %}-->,  Django will iterates over apps to find the file that is stored in `static/images`.

<!--{% raw %}-->
```html
{% load static %}

<!DOCTYPE html>
<html>
  <head>
    <title>Movies App</title>
  </head>
  <body>
    <img src="{% static 'images/logo.svg' %}" />
  </body>
</html>
```
<!--{% endraw %} -->
5. Since the image is not attached to a specific app(it is attached to the project folder), we need to include the `moviereivews/static` folder in the settings.py:

```
STATICFILES_DIRS = [
    BASE_DIR / 'moviereviews/static/'
]
```

See: https://docs.djangoproject.com/en/4.2/howto/static-files/