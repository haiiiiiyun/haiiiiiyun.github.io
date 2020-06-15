Django 国际化

在 Django 2.2 版本中，支持中文的翻译：

1. 在 settings.py 中：

```python
LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)
```

这是使用 `zh-hans`，不是下划线。

2. 生成翻译文件：

用 `python manage.py makemessages -l zh_Hans` 和 
用 `python manage.py compilemessages -l zh_Hans` 

这里使用的是下划线，并且 `H` 大写。


参考： https://code.ziqiangxuetang.com/django/django-internationalization.html
