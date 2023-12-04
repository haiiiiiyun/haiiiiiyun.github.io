---
title: Define app URLs under their own path
date: 2023-12-01
tags: python django url
categoris: Programming
---

To better segregate the paths into their own apps, each app can have its own `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
	path('', views.news, name='news')
]
```

In the project's `URL_CONF` file:  include the app's URLs:

```python
from django.contrib import admin
from djang.urls import path, include

#...
urlpattern = [
	path('admin/', admin.site.urls),
	path('news/', include('news.urls')),
]
```

Request `localhost:8000/news` forwards to view `news`.