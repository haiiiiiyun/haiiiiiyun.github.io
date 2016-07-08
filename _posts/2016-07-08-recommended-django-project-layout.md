---
title: 一种值得推荐的 Django 项目布局方法
date: 2016-07-08
writing-time: 2016-07-08 08:58--10:50
categories: programming
tags: Django python programming
---

# 一、这种布局的优点

1. 项目中的每个应用都相对独立，方便以后拿出来重用。

1. 这样的布局会促使你在开发过程中考虑每个应用的重用性。

1. 开发、测试、生产等不同的环境都有各自独立的配置文件，方便配置项的共享和定制。

1. 不同的环境都有各自独立的 pip requirements 文件。

1. 每个应用都有各自的 templates 和 static 目录，你可以通过项目级的 templates 和 static 目录中的文件对各应用中的相应内容进行覆盖。

1. 对 models、views、managers 等的测试都各自保存在独立的文件中，易于阅读和理解。

# 二、Django 默认产生的布局

假设项目名为 **foo**, 使用 `python django-admin.py startproject foo` 命令产生的默认布局会是：

```
foo/
    manage.py
    foo/
       __init__.py
       settings.py
       urls.py
       wsgi.py
```

# 三、推荐的项目布局

假设我们的项目名为 **myproject**, 其中有两个应用 **blog** 和 **users**，推荐的项目布局可以为：

```
myproject/
    manage.py
    myproject/
        __init__.py
        urls.py
        wsgi.py
        settings/
            __init__.py
            base.py
            dev.py
            prod.py
    blog/
        __init__.py
        models.py
        managers.py
        views.py
        urls.py
        templates/
            blog/
                base.html
                list.html
                detail.html
        static/
            css/
            js/
            …
        tests/
            __init__.py
            test_models.py
            test_managers.py
            test_views.py
    users/
        __init__.py
        models.py
        views.py
        urls.py
        templates/
            users/
                base.html
                list.html
                detail.html
        static/
            css/
            js/
            …
        tests/
            __init__.py
            test_models.py
            test_views.py
     static/
         css/
         js/
         …
     templates/
         base.html
         index.html
     requirements/
         base.txt
         dev.txt
         test.txt
         prod.txt
```

## 1. 每个应用的目录位置

最顶层的 **myproject** 目录包含有 **manage.py** 文件，因此是项目的根目录。 **myproject/myproject/** 是项目的内容目录，项目的根 URL 配置文件, WSGI 配置文件都存放在这里面。

**myproject/blog/** 和 **myproject/users/** 是项目的两个应用所在的目录，将 blog、 users 这两个应用的目录与 **myproject/myproject/** 平行放置，而不放置在 **myproject/myproject/** 目录内的好处是： 之后要 import 应用中的模块时，比如 import blog 应用中的 models 时，可以用 **import blog.models**，而不需要用 **import myproject.blog.models**，这样也方便之后能将应用独立出来重用。


## 2. 为每个环境设置各自的配置信息

针对项目的各个环境，如本地开发 dev、 内部测试 stage、 自动化流程环境 [jenkins](https://github.com/jenkinsci/jenkins) 及生产环境 prod，分别创建独立的配置文件。

1. 在 **myproject/myproject** 目录下新建一个 **settings** 目录并在里面创建一个空的 **__init__.py**。

2. 将 **myproject/myproject/settings.py** 文件搬到 **myproject/myproject/settings/** 目录下，并改名为 **base.py**，这个文件里面的配置信息被所有其它环境的配置文件所共享。

3. 在 **myproject/myproject/settings/** 目录下分别创建 **dev.py**、**stage.py**、**jenkins.py** 和 **prod.py** 4 个文件，每个文件中包含如下的一行代码：

```
from base import *
```

这样，这些环境配置文件就能读取默认的配置项了，之后就能在各自的配置文件中设置定制的配置值了。比如本地开发环境，可以在 **dev.py** 中添加 `DEBUG=True**， 而生产环境 **prod.py**，可以设置 `DEBUG=False`。

4. 指定使用哪个配置文件：

可以通过操作系统的环境变量指定，比如：

```
export DJANGO_SETTINGS_MODELS="myproject.settings.prod" 
```

也可以通过命令行参数指定， 比如：

```
./manage.py migrate --settings=myproject.settings.prod
```

或者

```
gunicorn -w 4 -b 127.0.0.1:8001 --settings=myproject.settings.prod
```

## 3. 修改 INSTALLED_APPS

默认的 INSTALLED_APPS 会是:

```
INSTALLED_APPS = (
    ...
)
```

可以将元组 **()** 改为列表 **[]**：

```
INSTALLED_APPS = [
    ...
]
```

进一步可以将 **INSTALLED_APPS** 中的第三方（内置）的应用与我们自己的应用分开，如： 

```
PREREQ_APPS = [
   ‘django.contrib.auth’,
   ‘django.contrib.contenttypes’,
   …
   ‘debug_toolbar’,
   ‘imagekit’,
   ‘haystack’,
]

PROJECT_APPS = [
   ‘homepage’,
   ‘users’,
   ‘blog’,
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS
```

这样分开后，我们就可以只针对我们自己的应用进行 test 和 code coverage。

以上针对 **INSTALLED_APPS** 的修改也可以针对 **TEMPLATE_DIRS** 和 **MIDDLEMARE_CLASSES** 进行。


## 4. 调整 pip requirements

项目一般都有一个 requirements.txt 文件，可以指定项目的依赖包，根据这个文件，可以用以下命令对依赖包进行自动安装：

```
pip install -r requirements.txt
```

在 requirements.txt 文件中可以用 `-r filename` 来包含进另一个文件的内容，这个功能和 C 语言中的 #include <filename.h> 类似。

因此，我们可以将通用的依赖信息保存在 **myproject/requirements/base.txt** 文件中，而针对不同的环境，比如测试环境，保存在另一个文件中，如 **myproject/requirements/test.txt**, 里面的内容可能会是：

```
-r base.txt
pytest==2.5.2
coverage==3.7.1
```

## 5. 分割测试文件

在每个应用中分别创建一个包含测试内容的目录 tests，将对应不同类别的测试分别保存在不同的文件中，如 **test_models.py**、 **test_views.py** 等。这样分配，比起将全部测试代码放在单个文件中的好处是：代码更易阅读，同时还能减少在编辑器中上下翻滚的时间。


## 6. URL 配置文件

先各个应用内的 **urls.py** 保存各自的 URL 配置，然后在项目的根 URL 配置文件中，通过 include 命令将子应用的 URL 配置信息包含进行：

```
urlpatterns = patterns(‘’,
    url(r’^$’, HomePageView.as_view(), name=‘home’),
    url(r’^blog/‘, include(‘blog.urls’)),
    url(r’^user/‘, include(‘users.urls’)),
)
```

## 7. 模板和静态文件

各个子应用都应该有各自的模板和静态文件目录，如 **blog** 的模板和静态文件目录位置应该为： **myproject/blog/templates/blog/** 和 **myproject/blog/static/blog/** 。如果想对子应用中的模板和静态文件进行覆盖，可以通过在项目根模板和根静态文件目录中创建相同名字的文件进行。比如要覆盖 **blog** 中的 **detail.html** 模板，可以通过创建 **myproject/templates/blog/detail.html** 文件来对默认的模板文件进行覆盖。

## 8. 重用子应用

如果想在另一个项目中重用 **blog** 应用，正确的方法是：

1. 将 **blog** 应用提取出来，创建一个独立的代码库
2. 在各个项目中，使用 pip install 的方式安装 **blog** 应用
3. 在各个项目中，使用 pip 对依赖的 **blog** 进行更新


> 参考文献： [http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/](http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/)
