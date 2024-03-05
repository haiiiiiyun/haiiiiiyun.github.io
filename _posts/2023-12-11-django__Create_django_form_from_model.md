---
title: Create django form from model
date: 2023-12-11
tags: python django forms
categoris: Programming
---

Create a form based on a model using `ModelForm`, and specify the `model`, `fields`, `labes`, `widgets` in a inner `Meta class`:

```python
# in forms.py
from django.forms import ModelForm, Textarea
from .models import Review

class ReviewForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['watch_again'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Review
        fields = ['text', 'watch_again']
        labels = {
            'watch_again': ('Watch Again')
        }
        widgets = {
            'text': Textarea(attrs={'rows': 4})
        }
```

```python
# in models.py
from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):

    text = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_again = models.BooleanField()

    def __str__(self):
        return self.text
```