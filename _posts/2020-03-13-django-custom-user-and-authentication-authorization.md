---
title: Django 中自定义用户模型及集成认证授权功能总结
date: 2020-03-13
writing-time: 2020-03-13
categories: python;django
tags: python;django
---

# 1. 概述

Django 中的 `django.contrib.auth` 应用提供了完整的用户及认证授权功能。

Django 官方推荐基于内置 User 数据模型创建新的自定义用户模型，方便添加 `birthday` 等新的用户字段和功能。

本文包含的内容有：

+ 介绍在 Django 中如何自定义用户模型，并集成到系统。
+ 定制 `django.contrib.auth` 应用使用的模板文件。
+ 在系统中集成认证与授权功能。

以下所有示例在 Python 3.8.2 + Django 2.1 中实现。

# 2. 自定义用户模型

## 2.1. 创建认证与授权相关的单独应用 accounts

```bash
$ python manage.py startapp accounts
```

将应用添加到项目中：

```python
# project_dir/settings.py
INSTALLED_APPS = [
    # Local
    'accounts.apps.AccountsConfig',
    #...
]
```

## 2.2. 创建自定义用户模型 CustomUser

Django 官方文档中推荐基于 AbstractBaseUser 创建自定义用户模型，但是一般基于 AbstractUser 创建再方便。

本命中的自定义 CustomUser 中新增了字段 birthday。

```python
# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    birthday = models.DateField(null=True, blank=True)
```

## 2.3. 集成自定义用户模型

通过 `AUTH_USER_MODEL` 告诉系统新的用户模型:


```python
# project_dir/settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

之后可通过 `get_user_model()` 获取该自定义用户模型：

```python
# in view or model files
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
```

`django.contrib.auth` 应用已实现了完整的 login, logout 功能，并已在 `django.contrib.auth.urls` 中定义了 login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete 等 URL。

将 `django.contrib.auth.urls` 集成到项目中：

```python
# project_dir/urls.py
from django.urls import path, include
urlpatterns = [
   path('accounts/',  include('django.contrib.auth.urls'),
   #...
]
```

集成后，即可访问 `/accounts/login/`, `/accounts/logout/`, `/accounts/password_change/` 等功能，同时时视图和模板中也可访问这个 URL 定义：

```html
<!-- in template files -->
{% raw %}
<a href="{% url 'login' %}">Login URL</a>
{% endraw %}
```

```python
# in view files
from django.urls import reverse, reverse_lazy

login_url = reverse('login')

#in Class Based View:
login_url = reverse_lazy('login')
```

## 2.4. 集成自定义用户模型到后台管理界面

后台管理界面中，添加新用户时呈现的表单由 `django.contrib.auth.forms.UserCreationForm` 提供，而更新用户时呈现的表单由 `django.contrib.auth.forms.UserChangeForm` 提供。

为自定义用户模型定制这两个表单：

```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):

        model = CustomUser
        fields = ('username', 'email', 'birthday', )


class CustomUserChangeForm(UserChangeForm):


    class Meta(UserChangeForm.Meta):

        model = CustomUser
        fields = UserChangeForm.Meta.fields + ( 'birthday', )
```

注册到 admin 中：

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):

    model = CustomUser

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ['email', 'username', 'birthday', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
```


# 3. 定制 `django.contrib.auth` 应用使用的模板文件

## 3.1. 定义模板文件

`django.contrib.auth` 中 login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete 等视图，访问的相应模板需保存在`registration/` 目录下，模板文件有: login.html, password_change_done.html, password_change_form.html, password_reset_complete.html, password_reset_confirm.html, password_reset_done.html, password_reset_form.html 等。

默认配置下，模板文件需保存在 `<app-name>/templates/<app-name>/registration/` 目录下，如 `accounts/templates/accounts/registration/login.html`。

对于小项目，可以将模板目录设置为扁平化:

```python
# project_dir/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # new
        #...
    }
]
```

从而模板可以保存在 `templates/` 目录中，如 `templates/registration/login.html`。


模板中可使用 `form` 变量，例如：

```html
<!-- templates/registration/login.html -->
{% raw %}
{% extends 'base.html' %}

{% block title %}Login{% endblock title %}

{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button class="btn btn-success ml-2" type="submit">Login</button>
</form>
{% endblock content %}
{% endraw %}
```

## 3.2. 创建注册功能

`django.contrib.auth` 没有实现 sign up 功能。

基于 CreateView 创建 SignUpView 视图:

```python
# accounts/views.py
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import CustomUserCreationForm

class SignupView(CreateView):
    #model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'signup.html'

    success_url = reverse_lazy('login')
```

添加模板文件:

```html
<!-- templates/signup.html -->
{% raw %}
{% extends 'base.html' %}

{% load crispy_forms_tags %}
{% block title %}Signup{% endblock title %}

{% block content %}
<h2>Signup</h2>
<form method="post">
  {% csrf_token %}
  {{ form|crispy }}
  <button class="btn btn-success" type="submit">Signup</button>
</form>
{% endblock content %}
{% endraw %}
```

添加应用级别的 URL 配置:

```python
# accounts/urls.py
from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
```

集成到项目级别的 URL 配置中：

```python
# project_dir/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #...
]
```

# 4. 在系统中集成认证与授权功能

## 4.1. 认证：要求登录后才能访问

视图应继承加入 `LoginRequiredMixin`，属性值 `login_url` 设置当没有登录时，将转向的登录页面地址或 URL name：

```python
# in view files

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Article

class ArticleDeleteView(LoginRequiredMixin, DeleteView):

    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'
```

## 4.2. 授权：只有特定的用户或权限才能访问

CBV 中，代码调用入口是 `dispatch()` 方法，可以在该方法中实现权限验证，当权限不够时抛出异常:

```python
# in view files

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Article

class ArticleDeleteView(LoginRequiredMixin, DeleteView):

    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)
```

# 资源

+ [Django for beginners](https://book.douban.com/subject/30389913/)
