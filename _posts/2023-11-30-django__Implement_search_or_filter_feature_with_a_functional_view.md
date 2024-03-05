---
title: Implement search or filter feature with a functional view
date: 2023-11-30
tags: python django views functional templates
categoris: Programming
---

In views.py,  use `request.GET.get(param_name)` to get  the search term, and grab the filtered objects using `Model.objects.filter()`:

```python
def home(request):
    searchTerm = request.GET.get('searchTerm')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})
```

How to list objects, see [[Implement object listing feature with a functional view]].