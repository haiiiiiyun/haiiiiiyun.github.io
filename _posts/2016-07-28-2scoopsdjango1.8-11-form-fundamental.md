---
title: Django 表单 Form 基础
date: 2016-07-28
writing-time: 2016-07-28 08:52--11:12
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

> pydanny made-up statics:
> 100% Django 项目应该使用 Form。
> 95% Django 项目应该使用 ModelForm。
> 91% Django 项目使用了 ModelForm。
> 80% ModelForm 只需简单的逻辑
> 20% ModelForm 需要复杂逻辑

应该使用 Form 对所有进来的数据进行检验。

# 使用 Django Form 对所有进来的数据进行检验

Django Form 是一个意在检验 Python 字典数据的框架，但通常用来检验 HTTP 请求中的 POST 数据。

例如，一个 Django 应用想根据 CSV 文件来更新数据模型，一般会用下面的代码：

```
import csv
import StringIO

from .models import Purchase

def add_csv_purchases(rows):

    rows = StringIO.StringIO(rows)
    records_added = 0

    # Generate a dict per row, with the first CSV row being the keys
    for row in csv.DictReader(rows, delimiter=","):
        # DON'T DO THIS: Tossing unvalidated data into your model.
        Purchase.objects.create(**row)
        records_added += 1
    return records_added
```

该代码中没有对外部进入的 CSV 数据进行检验，甚至对 Seller 是否是有效的用户都没有检验。我们可以在 add_csv_purchases 函数中添加验证代码，但是为保持代码的维护性，最好使用 Django Form 进行验证：

```
import csv
import StringIO

from django import forms

from .models import Purchase, Seller

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase

    def clean_seller(self):
        seller = self.cleaned_data["seller"]
        try:
            Seller.objects.get(name=seller)
        except Seller.DoesNotExist:
            msg = "{0} does not exist in purchase #{1}.".format(
                seller,
                self.cleaned_data["purchase_number"]
            )
            raise forms.ValidationError(msg)
        return seller

    def add_csv_purchases(rows):

        rows = StringIO.StringIO(rows)

        records_added = 0
        errors = []

        # Generate a dict per row, with the first CSV row being the keys.
        for row in csv.DictReader(rows, delimiter=","):
            # Bind the row data to the PurchaseForm.
            form = PurchaseForm(row)
            # Check to see if the row data is valid.
            if form.is_valid():
                # Row data is valid so save the record.
                form.save()
                records_added += 1
            else:
                errors.append(form.errors)

        return records_added, errors
```

使用 Django Form 框架，避免自己创建一套验证系统，可以确保代码的健壮性。

Django 官方文档推荐将 **code** 参数传到 ValidationError 中，如：

```
ValidationError(_('Invalid value'), code='invalid')
```

这样可以对验证异常进行分类。

# 在 HTML 表单中使用 POST 方法

唯一的例外是查询表单，因它对应的操作只是查询，没有修改数据，因此应该用 GET 方法。


# 会对数据造成修改的 HTTP Form 必须要用 CSRF

关闭 CSRF 保护的唯一情况是当创建 API 时，如 django-tastypie 和 django-rest-framework 等 API 框架都是这么做的。因为 API 请求应该基于签名认证，而非基于 Cookies 认证。因此，关闭 CSRF 对这些框架基本不会有影响。

由于 HTML 查询表单使用的 GET 方法，因此不会触发 CSRF 保护机制。

应该使用 Django 的 **CsrfViewMiddleware** 对整个站点开启保护，而不是手动用 **csrf_protect** 装饰器对每个视图进行操作。

## 使用 X-CSRFToken 对 AJAX 提交的数据进行保护

不能关闭 CSRF 保护。当使用 AJAX 来 POST 数据时，因在 HTTP 请求中设置一个 **X-CSRFToken** 头。具体如何设置和验证可参考 [Django 官方文档](https://docs.djangoproject.com/en/1.8/ref/csrf/#ajax)


# 理解如何在 Django Form 实例中添加属性

有时需要为 Django Form 实例添加属性，如添加 **request.user**。需要重载其 **__init__** 定义：

```
from django import forms

from .models import Taster

class TasterForm(forms.ModelForm):

    class Meta:
        model = Taster

    def __init__(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super(TasterForm, self).__init__(*args, **kwargs)
```

上面代码中，使用 **kwargs.pop** 会使在多种继承时更加健壮。

而在 CBV 中，通过重载 **get_form_kwargs** 为 form 初始化提供额外的 kwargs 参数：

```
from django.views.generic import UpdateView

from braces.views import LoginRequiredMixin

from .forms import TasterForm
from .models import Taster

class TasterUpdateView(LoginRequiredMixin, UpdateView):
    model = Taster
    form_class = TasterForm
    success_url = "/someplace/"

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword arguments."""
        # grab the current set of form #kwargs
        kwargs = super(TasterUpdateView, self).get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs
```

将 **request.user** 对象加入 Form 非常普遍，因此 **django-braces** 已经提供了相关的 Mixin，
参考：  [django-braces UserFormKwargsMixin](http://django-braces.readthedocs.io/en/latest/form.html#userformkwargsmixin) 和 [django-braces UserKwargModelFormMixin](http://django-braces.readthedocs.io/en/latest/form.html#userkwargmodelformmixin)

# 理解 Form 验证的工作原理

理解 Form 验证的内部机理能显著提升我们的代码质量。

当调用 **form.is_valid()** 时，其工作流程如下：

1. 若该表单有数据绑定，则调用 **form.full_clean()**
1. **form.full_clean()** 会遍历每个表单项，对其一一进行验证
    1). 进入表单项的数据用 **to_python()** 方法将其转变成 Python 变量，无法转换的抛出 ValidationError
    2). 这些数据根据其表单项上指定的验证规则进行验证（包含自定义的验证器），验证失败的抛出 ValidationError
    3). 如果有定义 **clean_<field>()** 方法，现在进行调用
1. **form.full_clean()** 调用 **form.clean()**
1. 如果是一个 ModelForm 实例，**form._post_clean()** 做如下工作：
    1). 不管 form.is_valid() 结果是 True 还是 False，都将 ModelForm 的数据设置到 Model 实例上
    2). 调用 Model 的 **clean()** 方法。需要注意的是，如果通过 ORM 来保存一个 Model 实例，是不会调用 Model 的 **clean()** 方法的


## ModelForm 的数据先保存到 Form 实例上，然后再保存到 Model 实例

由于 ModelForm 的数据只有当调用 **form.save()** 时才会将数据保存到 Model 实例中，我们可以利用这个特性。

例如，当用户提交失败时，可以将用户的提交数据和期望对 Model 实例的修改数据进行捕获和记录，先定义 Model：

```
# core/models.py
from django.db import models

class ModelFormFailureHistory(models.Model):
    form_data = models.TextField()
    model_data = models.TextField()
```

然后添加一个 Mixin:

```
# flavors/views.py
import json

from django.contrib import messages
from django.core import serializers

from core.models import ModelFormFailureHistory

class FlavorActionMixin(object):

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """Save invalid form and model data for later reference."""
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize("json",
                                          [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(
            form_data=form_data,
            model_data=model_data
        )
        return super(FlavorActionMixin,
                    self).form_invalid(form)
```

**form_invalid()** 是在验证失败时才调用的。

而定义 **success_msg** 属性，是为了当子类没有定义相应的属性时，会抛出一个 NotImplemented 异常。


# 通过 Form.add_error() 将错误添加到 Form 中

一般在 **Form.clean()** 中使用 **Form.add_error()**，如：

```
from django import forms

class IceCreamReviewForm(forms.Form):
    # Rest of tester form goes here
    ...

    def clean(self):
        cleaned_data = super(TasterForm, self).clean()
        flavor = cleaned_data.get("flavor")
        age = cleaned_data.get("age")

        if flavor == 'coffee' and age < 3:
            # Record errors that will be displayed later.
            msg = u"Coffee Ice Cream is not for Babies."
            self.add_error('flavor', msg)
            self.add_error('age', msg)

        # Always return the full collection of cleaned data.
        return cleaned_data
```

## 其它一些很有用的 Form 方法：

## Form.errors.as_data()

返回一个以项名为关键字，ValidationError 实例数组为值的 Dict，如：

```
>>> f.errors.as_data()
{'sender': [ValidationError(['Enter a valid email address.'])],
'subject': [ValidationError(['This field is required.'])]}
```

当想通过 **code** 来识别错误时，可以用这个方法。

## Form.errors.as_json(escape_html=False)

如：

```
>>> f.errors.as_json()
{"sender": [{"message": "Enter a valid email address.", "code": "invalid"}],
"subject": [{"message": "This field is required.", "code": "required"}]}
```

escape_html=True 时，其内容适合直接插入 HTML 页面中，而当escape_html=False 时，要插入 HTML 页面，不能直接用 jQuery 的 .html()，而应该用 $(el).text(errorText)

## Form.has_error(field, code=None)

根据检测是否有特定 code 的错误，如果要检测非数据项的错误， field 参数用值 NON_FIELD_ERRORS。

## Form.non_field_errors()

返回没有与特定项关联的错误，包括在 Form.clean() 中抛出的 ValidationError 和  Form.add_error(None, "...") 添加的错误。

# 其它有用的资源

+ [Daniel Roy Greenfeld 的 Form系列文章](http://www.pydanny.com/tag/forms.html)
+ [Brad Montgomery 的文章：如何为 Postgresql 的 ArrayField 创建一个 Widget](https://bradmontgomery.net/blog/2015/04/25/nice-arrayfield-widgets-choices-and-chosenjs/)
+ [Miguel Araujo 的如何创建自定义的表单项和组件的教程](http://tothinkornottothink.com/post/10815277049/django-forms-i-custom-fields-and-widgets-in]


> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
