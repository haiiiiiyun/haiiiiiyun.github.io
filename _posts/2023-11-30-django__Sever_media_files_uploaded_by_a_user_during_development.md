---
title: Sever media files uploaded by a user during development
date: 2023-11-30
tags: python django
categoris: Programming
---

During development, we can serve user uploaded media files from `MEDIA_ROOT` using the `django.views.static.server()` view.

**This is not suitable for production use.**

We have to configure where to store the uploaded files, in the `settings.py` file, add the following at the bottom of the file:

```python
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
```

Then add the url pattern to our `ROOT_URLCONF` file:

```python
from django.conf import settings
from django.conf.urls.static import static

# ...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```