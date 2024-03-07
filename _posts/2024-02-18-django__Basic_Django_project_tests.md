---
title: Basic Django project tests
date: 2024-02-18
tags: python django tests
categoris: Programming
---

Django's automated testing framework extends Python's unit testing framework [unittest](https://docs.python.org/3/library/unittest.html) with multiple additions into a web context.

## Test file location

We write unit tests in `tests.py` file under Django app.

## Unit tests

We create unit tests by extending `django.tests.TestCase`.

Each method must be prefaced with `test` in order to be run by the Django test suite.

```python
from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):
    def test_create_user(self):
		pass
```

## Authentication

Use TestCase's `client` to login and logout:

```python
self.client.login(username="name", password="pass")
self.client.logout()
```

## Test web pages that do not have a model included

`django.tests.SimpleTestCase` is a special subset of `TestCase` that is designed for web pages that does not involve any database queries.

We can use TestCase's `client` to visit URL: `self.client.get(url)`.

```python
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```

## Test templates

Use `assertTemplateUsed(response, template_name)`:

```python
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
```

## Test HTML content

Use `assertContains(response, text)` and `assertNotContains(response, text):

```python
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_homepage_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, 'home page')

    def test_homepage_not_contains_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Hi there! I should not be on the page.')
```

## Test context

We can get context variable from `response.context`:

```python
class SignUpPageTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
```

## DRY with setUp()

`setUp()` is called before running each unit test.

We can extract the same steps from test methods into `setUp()`.

```python
from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)
```

## Set up init data with setUpTestData() at class level

```python
from django.test import TestCase
from django.urls import reverse
from .models import Book

class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title = "Harry Potter",
            author="JK Powling",
            price="25.00",
        )
```

Using `setUpTestData` often dramatically increases the speed of tests because the initial data is created once rather than each time for each unit test.

## resolve test

`resolve(path)` function can be used for resolving URL paths to the corresponding view functions, while `reverse(url_name)` function can be used for getting the URL path from URL name.

```python
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView

class HomepageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
```


## Some assertion method

+ assertEqual
+ assertTrue
+ assertFalse
+ assertTemplateUsed
+ assertContains
+ assertNotContains
+ self.assertIsInstance
+ self.assertRedirects

```python
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView

class HomepageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'home page')

    def test_homepage_not_contains_incorrect_html(self):
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
```

## Necessary tests for a html page

1.  test_page_status_code()
2. test_page_template()
3. test_page_contains_correct_html()
4. test_page_not_contains_incorrect_html()
5. test_page_url_resolves_to_correct_view()

## Necessary tests for model based page

1. set up init data with setupTestData(cls)
2. test_object_listing():  test string representations of model field and model instance itself.
3. test_object_list_view()
4. test_object_detail_view()