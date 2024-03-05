---
title: set the login redirect URL in Django
date: 2024-02-19
tags: python django auth
categoris: Programming
---

Set `LOGIN_REDIRECT_URL` in `settings.py`, default is `/accounts/profile`.

The value can be  he URL or named URL pattern where requests are redirected after login when the LoginView doesn’t get a next GET parameter.

Similar settings are:

+ LOGOUT_REDIRECT_URL
+ LOGIN_URL