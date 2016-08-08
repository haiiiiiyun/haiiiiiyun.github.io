---
title: Django 使用 REST API
date: 2016-08-08
writing-time: 2016-08-08 12:43--16:53
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

以下的前端 JavaScript 框架使得使用 REST API 更加容易：

+ [React.js](https://facebook.github.io/react/): Facebook 发布，可用于构建 HTML、iOS 和 Android 应用。
+ [Angular.js](http://angularjs.org)：Google 发布，可用于创建单页应用， Django 社区用地较多。
+ [Backbone.js](http://backbonejs.org)：基于 underscope.js 库。
+ [jQuery](http://jquery.com)。

# 学习如何调试客户端

客户端调试不只是写 **console.log()** 和 **console.dir()**。但是大多数的测试工具都是针对框架的，一旦选择了工具，值得我们花时间深入学习如何写测试。

# 考虑使用 JavaScript 版本的静态内容预处理器

之前一直使用 Python 来完成 JavaScript 和 CSS 的压缩等工作，但是现在 JavaScript 社区中的相关工具更加专业，效果更好。该领域中最常用的工具是 [Gulp](http://gulpjs.com)，它类似 Python 中的 Fabric、Invoke 等自动化工具。

# 使内容能被搜索引擎索引

## 参考搜索引擎文档

+ [google ajax crawling](https://developers.google.com/webmasters/ajax-crawling/)
+ [Search Engine Optimization Best Practices for AJAX URLs](http://blogs.bing.com/webmaster/2013/03/21/search-engine-optimization-best-practices-for-ajax-urls/)

## 创建 sitemap.xml

百度等没有索引指导文档，为这些引擎创建相应的 *sitemap.xml*，由于 AJAX 视图不是具体的 HTML，需要创建一个定制的视图：

```python
from __future__ import absolute_import

from django.views.generic import TemplateView

from .flavors.models import Flavor

class SiteMapView(TemplateView):
    template_name = "sitemap.xml"

    def flavors(self):
        return Flavor.objects.all()
```

以下是一个简单的 *sitempa.xml*:

```jinja
{% raw %}
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {# Snip the home page, contact, etc #}
    {% for flavor in view.flavors %}
        <url>
            <loc>{{ site.domain }}/app/#{{ flavor.slug }}</loc>
            <lastmod>{{ flavor.modified }}</lastmod>
            <changefreq>monthly</changefreq>
            <priority>0.8</priority>
        </url>
    {% endfor %}
</urlset>
{% endraw %}
```

## 通过服务来使你的网站能被索引

除了自创 *sitempa.xml*，还可以通过 brombone.com 等服务来处理你的 Angular.js 、Backbone.js 等网站，从而生成一个 Google 预览的 HTML 版页面。

# 实时与延时

优化最好的网站，往返半个地球产生的时延还是可察觉的，这是物理规律。因此，需要处理延时的问题。

## 方法一：使用动画来覆盖延时操作，以便分散用户注意力
## 方法二：在客户端假装交互成功，然后再在后端处理
## 方法三：根据用户地理位置部署多个服务器
## 方法四：限制用户的使用地理位置

# 避免使用反模式的方法

## 能采用多页型应用时不采用单页型应用

多页型应用更容易创建。

## 一定要写测试

## 了解各 JavaScript 框架的内存管理，避免内存泄漏

## 使用 jQuery 时将数据保存在 DOM, 使用其它框架时参考其数据管理方式

# AJAX 和 CSRF 

## jQuery 和 CSRF

使用 jQuery 时，可以创建一个 *csrf.js* 文件，然后在所有使用 AJAX 更新数据的页面上包含该文件。

```javascript
// Place at /static/js/csrf.js
// CSRF helper functions taken directly from Django docs
function getCookie(name) {
var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/ˆ(GET|HEAD|OPTIONS|TRACE)$/.test(method));
} 

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
```

之后，将这些代码包含到页面中：

```jinja
{% raw %}
{% extends "base.html" %}
{% load static %}

{% block title %}Ice Cream Shopping Cart{% endblock %}

{% block content %}
    <h1>Ice Cream Shopping Cart</h1>
    <div class="shopping-cart"></div>
{% endblock %}

{% block javascript %}
    {{ block.super }}
    <script type="text/javascript"
        src="{% static "js/csrf.js" %}"></script>
    <script type="text/javascript"
        src="{% static "js/shopping_cart.js" %}"></script>
{% endblock %}
{% endraw %}
```

## Backbone.js 和 CSRF

```javascript

// Place at /static/models.js
var newSync = Backbone.sync;
Backbone.sync = function(method, model, options){
    options.beforeSend = function(xhr){
        xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
    };
    return newSync(method, model, options);
};
```

## AngularJS 和 CSRF

通常将 CSRF 标识放在 HTTP 头中：

```javascript
var app = angular.module('icecreamlandia.app');
app.config(['$httpProvider', function($httpProvider) {
    // The next two lines should just be one, but we had to break it
    // up in order to preserve book formatting.
    var common = $httpProvider.defaults.headers.common;
    common['X-CSRFToken'] = '{{ csrf_token|escapejs }}';
}]);
```

# 提高 JavaScript 技能

+ 评估技能水平： [js-assessment](https://github.com/rmurphey/js-assessment)
+ [Lightweight Django](https://www.amazon.com/Lightweight-Django-Julia-Elman/dp/149194594X?tag=mlinar-20)
+ [Using Django Tastypie And Backbone.js To Create RESTful APIs](http://blog.mathandpencil.com/using-django-tastypie-to-create-RESTful-APIs/)
+ [Getting Started with Django Rest Framework and AngularJS](http://blog.kevinastone.com/getting-started-with-django-rest-framework-and-angularjs.html)

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
