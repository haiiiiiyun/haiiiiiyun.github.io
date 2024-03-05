---
title: Customize fields of UserCreationForm
date: 2023-12-05
tags: python django auth signup
categoris: Programming
---

First [[Implement a basic sign up feature]], we can customize fields of UserCreationForm by creating a new class that extends `UserCreationForm`.

create a new file `forms.py` and fill it with the following:

```python
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ('username', 'password1', 'password2'):
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )
```

We replace all `UserCreationForm` with this new `UserCreateForm` in views.py.