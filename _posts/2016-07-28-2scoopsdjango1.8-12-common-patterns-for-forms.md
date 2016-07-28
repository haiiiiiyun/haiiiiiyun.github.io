---
title: Django 表单 Form 的常用模式
date: 2016-07-28
writing-time: 2016-07-28 11:17--14:19
categories: programming
tags: python Django programming Two&nbsp;Scoops&nbsp;of&nbsp;Django
---

结合表单、数据模型和视图，可以使我们以很少的代价完成大量工作。

Form 相关的 Django 包：

+ django-floppyforms: 能将 Django 输入框以 HTML5 呈现
+ django-crispy-forms: 呈现高级的表单布局组件。默认使用 Bootstrap 的表单元素和风格，可与 django-floppyforms 共用
+ django-forms-bootstrap: 一个使用 Bootstrap 风格呈现 Django 表单的简单工具。可与 django-floppyforms 共用，但和 django-crispy-forms 冲突。


# 模式1： 简单的 ModelForm 与默认验证器

采用一个简单的 ModelForm，并使用 Model 的默认验证器（不对项内容进行修改）。

例如：

```python
# flavors/views.py
from django.views.generic import CreateView, UpdateView

from braces.views import LoginRequiredMixin

from .models import Flavor

class FlavorCreateView(LoginRequiredMixin, CreateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

class FlavorUpdateView(LoginRequiredMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
```

上例中：

+ FlavorCreateView 和 FlavorUpdateView 指定 Flavor 为其数据模型
+ 这两个视图基于 Flavor 自动创建一个 ModelForm
+ 这些 ModelForm 依赖 Flavor 数据模型上定义的默认验证规则进行验证


## 模式2： 在 ModelForm 中使用自定义的表单项验证器

假设项目中要求所有的 *title* 项的值都以 *Tasty* 开头。

Django 的自定义验证器是就是一个函数。

在项目中创建一个 **validators.py** 模块，并定义验证器：

```python
# core/validators.py
from django.core.exceptions import ValidationError

def validate_tasty(value):
    """Raise a ValidationError if the value doesn't start with the
    word 'Tasty'.
    """

    if not value.startswith(u"Tasty"):
        msg = u"Must start with Tasty"
        raise ValidationError(msg)
```

由于验证器对于确保数据库不受破坏至关重要，因此要对其进行认真测试，包含对各种边缘条件的测试。

要使各相关数据模型都能用这个验证器，考虑创建一个抽象基类，并将该验证器添加到基类的项中，如下：

```python
# core/models.py
from django.db import models

from .validators import validate_tasty

class TastyTitleAbstractModel(models.Model):

    title = models.CharField(max_length=255, validators=[validate_tasty])

    class Meta:
        abstract = True
```

然后，基于 TastyTitleAbstractModel 创建具体的数据模型：

```python
# flavors/models.py
from django.core.urlresolvers import reverse
from django.db import models

from core.models import TastyTitleAbstractModel

class Flavor(TastyTitleAbstractModel):
    slug = models.SlugField()
    scoops_remaining = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("flavors:detail", kwargs={"slug": self.slug})
```

此后，一旦想保存 title 值不以 *Tasty* 开头的 Flavor 实例，都会抛出 ValidationError。

如果只想在 Form 中使用 validate_tasty，或者在数据模型的其它项中应用的话，应该：

```python
# flavors/forms.py
from django import forms

from core.validators import validate_tasty
from .models import Flavor

class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlavorForm, self).__init__(*args, **kwargs)
        self.fields["title"].validators.append(validate_tasty)
        self.fields["slug"].validators.append(validate_tasty)

    class Meta:
        model = Flavor
```

CBV 默认会基于数据模型自动生成 ModelForm，不过我们可以明确指定 ModelForm 类：

```python
# flavors/views.py

from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView

from braces.views import LoginRequiredMixin

from .models import Flavor
from .forms import FlavorForm

class FlavorActionMixin(object):

    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
                        CreateView):
    success_msg = "created"
    # Explicitly attach the FlavorForm class
    form_class = FlavorForm
    
class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin,
                        UpdateView):
    success_msg = "updated"
    # Explicitly attach the FlavorForm class
    form_class = FlavorForm

class FlavorDetailView(DetailView):
    model = Flavor
```

# 模式 3： 重载验证过程的 clean 阶段

适用于：

+ 多个数据项的组合验证
+ 验证涉及数据库中的已验证过的现有数据

这两种情况需要重载 **clean()** 和 **clean_&lt;field&gt;()** 函数。

下面的代码用 **clean_slug()** ，结合数据库中的现有数据，进行了组合验证：

```python
# flavors/forms.py
from django import forms
from flavors.models import Flavor

class IceCreamOrderForm(forms.Form):
    """Normally done with forms.ModelForm. But we use forms.Form here
    to demonstrate that these sorts of techniques work on every
    type of form.
    """

    slug = forms.ChoiceField("Flavor")
    toppings = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(IceCreamOrderForm, self).__init__(*args,
                                                **kwargs)
        # We dynamically set the choices here rather than
        # in the flavor field definition. Setting them in
        # the field definition means status updates won't
        # be reflected in the form without server restarts.
        self.fields["slug"].choices = [
            (x.slug, x.title) for x in Flavor.objects.all()
        ]
        # NOTE: We could filter by whether or not a flavor
        # has any scoops, but this is an example of
        # how to use clean_slug, not filter().

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg = u"Sorry, we are out of that flavor."
            raise forms.ValidationError(msg)
        return slug
```

下面的代码，用 **clean()** 对两个数据项进行了组合验证：

```python
def clean(self):
    cleaned_data = super(IceCreamOrderForm, self).clean()
    slug = cleaned_data.get("slug", "")
    toppings = cleaned_data.get("toppings", "")

    # Silly "too much chocolate" validation example
    if u"chocolate" in slug.lower() and \
            u"chocolate" in toppings.lower():
        msg = u"Your order has too much chocolate."
        raise forms.ValidationError(msg)
    return cleaned_data
```

# 模式 4： Hacking Form Fields （2 CBVs， 2 Forms， 1 Model）

假设想设计一个 Store 数据模型，在数据初始输入时不要求输入 phone 和 description 项，而在编辑页面时才要求输入这两项，则数据模型定义如下：

```python
# stores/models.py

from django.core.urlresolvers import reverse
from django.db import models

class IceCreamStore(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"pk": self.pk})
```

上面的代码中，将 phone 和 description 两项设置为 blank=True，允许初始输入阶段不输入。

在过去，在实现编辑页面时，由于需要输入 phone 和 description 的内容，代码通常大量使用了 Ctrl-C Ctrl-V，将数据模型中的内容复制到表单中，如下：

```python
# stores/forms.py
from django import forms

from .models import IceCreamStore

class IceCreamStoreUpdateForm(forms.ModelForm):
    # Don't do this! Duplication of the model field!
    phone = forms.CharField(required=True)
    # Don't do this! Duplication of the model field!
    description = forms.TextField(required=True)

    class Meta:
        model = IceCreamStore
```

这种写法违反了 DRY。假如数据模型中的项添加了一个 *help_text*，则在表单中还需要进行再次添加。

由于已初始化了的 Django form 实例会将项定义保存在一个与字典类似的属性 *fields* 中，我们可以利用这个属性来改善代码：

```python
# stores/forms.py
# Call phone and description from the self.fields dict-like object
from django import forms

from .models import IceCreamStore

class IceCreamStoreUpdateForm(forms.ModelForm):

    class Meta:
        model = IceCreamStore

    def __init__(self, *args, **kwargs):
        # Call the original __init__ method before assigning
        # field overloads
        super(IceCreamStoreUpdateForm, self).__init__(*args,
                                                    **kwargs)
        self.fields["phone"].required = True
        self.fields["description"].required = True
```

上面代码中，使用 Form.fields 属性，从而避免了在 Model 和 Form 间的大量复制粘贴。


又因为 Django Form 本身是一个 Python 类，故还可以用继承来进一步改善代码：

```python
# stores/forms.py
from django import forms

from .models import IceCreamStore

class IceCreamStoreCreateForm(forms.ModelForm):

    class Meta:
        model = IceCreamStore
        fields = ("title", "block_address", )

class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):

    def __init__(self, *args, **kwargs):
        super(IceCreamStoreUpdateForm,
                self).__init__(*args, **kwargs)
        self.fields["phone"].required = True
        self.fields["description"].required = True

    class Meta(IceCreamStoreCreateForm.Meta):
        # show all the fields!
        fields = ("title", "block_address", "phone",
                "description", )
```

在 ModelForm 中指定项，要用 **Meta.fields**，避免使用 **Meta.exclude** 。


最后，定义两个视图：

```python
# stores/views
from django.views.generic import CreateView, UpdateView

from .forms import IceCreamStoreCreateForm
from .forms import IceCreamStoreUpdateForm
from .models import IceCreamStore

class IceCreamCreateView(CreateView):
    model = IceCreamStore
    form_class = IceCreamStoreCreateForm

class IceCreamUpdateView(UpdateView):
    model = IceCreamStore
    form_class = IceCreamStoreUpdateForm
```

这样，我们就有两个视图，两个表单，并对应一个数据模型了。


# 模式 5：可重用的查询 Mixin

假设多个数据模型都定义有 *title* 项，现在想实现一个可重用的 Mixin，可用于对多个数据模型进行查询。

一个简单的查询 Mixin：

```python
# core/views.py
class TitleSearchMixin(object):

    def get_queryset(self):
        # Fetch the queryset from the parent's get_queryset
        queryset = super(TitleSearchMixin, self).get_queryset()

        # Get the q GET parameter
        q = self.request.GET.get("q")
        if q:
            # return a filtered queryset
            return queryset.filter(title__icontains=q)
        # No q is specified so we return queryset
        return queryset
```

将该 Mixin 应用于 Flavor 视图：

```python
# add to flavors/views.py
from django.views.generic import ListView

from core.views import TitleSearchMixin
from .models import Flavor

class FlavorListView(TitleSearchMixin, ListView):
    model = Flavor
```

再应用于另一个数据模型的视图：

```python
# add to stores/views.py
from django.views.generic import ListView

from core.views import TitleSearchMixin
from .models import Store

class IceCreamStoreListView(TitleSearchMixin, ListView):
    model = Store
```

然后，在各视图模板代码中添加相应的表单代码：

```jinja2
{% raw %}
{# form to go into stores/store_list.html template #}
    <form action="" method="GET">
    <input type="text" name="q" />
    <button type="submit">search</button>
</form>
{% endraw %}
```

```jinja2
{% raw %}
{# form to go into flavors/flavor_list.html template #}
<form action="" method="GET">
    <input type="text" name="q" />
    <button type="submit">search</button>
</form>
{% endraw %}
```

> 参考文献： [Two Scoops of Django: Best Practices for Django 1.8](https://www.amazon.com/Two-Scoops-Django-Best-Practices/dp/0981467342/)
