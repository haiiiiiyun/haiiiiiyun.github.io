---
title: Collect static files for production serving in Django
date: 2024-02-20
tags: python django statics
categoris: Programming
---

Run `python manage.py collectstatic` to combine all static files into one location and serve that in a professional HTTP server.

We need to configure some more settings in `settings.py` before `collectstatic` will work properly.

1. STATIC_ROOT: which sets the absolute location of these collected files. All collected files will be placed under this folder.
2. STATICFILES_DIRS: additional static files folders.
3. also see STATICFILES_STORAGE.


```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```