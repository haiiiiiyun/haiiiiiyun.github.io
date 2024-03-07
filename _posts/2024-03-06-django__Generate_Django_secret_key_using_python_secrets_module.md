---
title: Generate Django secret key using python secrets module
date: 2024-03-06
tags: python django
categoris: Programming
---

In production mode, Django `SECRET_KEY` needs to have at least 50 characters, and not be prefixed with "django-insecure-".

We can use Python's built-in `secrets` module. The parameter `token_urlsafe` returns the number of bytes in a URL-safe text string. With Base64 encoding on average each byte has 1.3 character. So using 38 results in 51 characters:

```python
>>> import secrets
>>> secrets.token_urlsafe(38)
'XhJ_bfyvg5vwnyxmrijBIYbpLouqu0OOXczj7guoChYWZ7E7f-o'
```