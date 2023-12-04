---
title: Why we have to place template files under a sub-folder that is named after app name
date: 2023-11-17
tags: python django templates
categoris: Programming
---

Each app should have its own templates folder, for example, in the `movie` app folder, create a folder called `templates/`, Django will look for template files iterating over every app's templates folder.

This is because we've set `'APP_DIRS': True` in `settings.py`, and Django will flatten all apps' templates folder, make it looks like a virtual templates folder that contains all files from apps' templates folder. If we have some template files with the same names, there will be a conflict, and Django will pick the first one it finds. To make sure Django will find the correct file, we might have to structure the template files under a sub-folder named after the app name. For example, in `movie` app, we can put template files under `movie/templates/movie/`.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

To connect view to template file, see [[Connect Django view to Django template]].