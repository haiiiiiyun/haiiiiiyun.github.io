---
title: Show wether a user is logged in
date: 2023-12-05
tags: python django auth
categoris: Programming
---

In template file, we have a `user`, which is provided by Django via `auth` app:

<!-- {% raw %} -->
```html
{% if user.is_authenticated %}
	<a class="nav-link" href="#">Logout ({{ user.username }})</a>
{% else %}
	<a class="nav-link" href="#">Login</a>
	<a class="nav-link" href="#">Sign Up</a>
{% endif %}
```
<!-- {% endraw %} -->