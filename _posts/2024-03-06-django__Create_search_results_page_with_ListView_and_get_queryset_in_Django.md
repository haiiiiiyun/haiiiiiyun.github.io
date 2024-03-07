---
title: Create search results page with ListView and get_queryset in Django
date: 2024-03-06
tags: python django views class-based
categoris: Programming
---

```python
class SearchResultsListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'books/search_results.html'

	# queryset = Book.objects.all()
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
```

the `queryset` attribute on `ListView`  holds all results by default, we can override the default `queryset` by providing a `get_queryset()` method.