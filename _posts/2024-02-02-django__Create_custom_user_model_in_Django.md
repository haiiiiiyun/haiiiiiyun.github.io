---
title: Create custom user model in Django
date: 2024-02-02
tags: python django auth
categoris: Programming
---

`User` is tightly interwoven with the Django internally, Django documentation highly recommends implementing a custom user model every time after created a new project.

One simple approach is to extend `AbstractUser` which keeps the default `User` fields and permissions. Another approach is to extend the `AbstractBaseUser` which requires more work.

4 steps for adding a custom user model:

1. Create a `CustomUser` model in a separated app `accounts`.
2. Update `settings.py`, add the app and specify `AUTH_USER_MODEL`
3. Customize `UserCreationForm` and `UserChangeForm`
4. Register custom user model to admin.py

1. Create a `CustomUser` model in a separated app `accounts`.

```bash
python manage.py startapp accounts
```

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
```

2. Update `settings.py`, add the app and specify `AUTH_USER_MODEL`

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig', # new
]

AUTH_USER_MODEL = 'accounts.CustomUser' # new
```

3. Customize `UserCreationForm` and `UserChangeForm`

```python
# accounts/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', )
```

5. Register custom user model to admin.py

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ['email', 'username', 'is_superuser', ]

admin.site.register(CustomUser, CustomUserAdmin)
```