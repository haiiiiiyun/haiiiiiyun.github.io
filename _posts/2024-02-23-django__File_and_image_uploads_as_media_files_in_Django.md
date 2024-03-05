---
title: File and image uploads as media files in Django
date: 2024-02-23
tags: python django medias
categoris: Programming
---

Django refers to static assets as `static` whereas anything uploaded by a user, whether it is a file or an image, is referred to as `media`.

The process for adding files or images is similar, but for images the `Pillow` library must b installed which includes additional features such as basic validation.

## Settings

Fundamentally the difference between static and media files is that we can trust the former, but we definitely can't trust the latter by default. Notably, it's important to **validate all uploaded files** to ensure they are what they say they are.

Add `MEDIA_URL` and `MEDIA_ROOT` in settings:

+ MEDIA_ROOT: is the absolute file system path to the directory for user-uploaded files
+ MEDIA_URL: is the URL we can use in our templates for the files

```python
MEDIA_URL = '/media/' # Don't forget to include the trailing slash /
MEDIA_ROOT = BASE_DIR / 'media'
```

## urls

Serve media files via `static` function:

```python
# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('books/', include('books.urls')),
    path('', include('pages.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
```

## Model field

To store image, we use `ImageField` which comes with some basic image processing validation logic. To store file, we use `FileField`.

We specify the upload location via `upload_to` attribute:

```python
class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover = models.ImageField(upload_to='cover/', blank=True)

    def __str__(self):
        return self.title

    # canonical URL for the model
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.pk)])
```

Here, cover images will be  stored in `MEDIA_ROOT / cover`.

## Template

We reference the image url in template:

<!-- {% raw %} -->
```html
<img src="{{ book.cover.url }}" class="bookcover" alt="{{ book.title }}" />
```
<!-- {% endraw %} -->

## Third-pard

+ [django-storages](https://github.com/jschneier/django-storages): allows for storing Django media files on service like Amazon's S3.
+ [django-cleanup](https://github.com/un1t/django-cleanup): automatically deletes old files.