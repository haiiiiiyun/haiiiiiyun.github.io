---
title: Implement login required authentication for function views
date: 2023-12-11
tags: python django auth
categoris: Programming
---

1. We import and add the `@login_required` decoration to the views that we want to authorize

```python
# views.py
from django.contrib.auth.decorators import login_required
 
@login_requied
def delete_review(request, review_id):
  ＃...
```

2. We also have to add `LOGIN_URL` in `settings.py`.  This redirects a user who is not logged in to the login page when they attempt to access an authorized page.

```python
# settings.py
LOGIN_URL = 'login_account'
```