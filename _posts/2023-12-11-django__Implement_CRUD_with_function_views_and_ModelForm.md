---
title: Implement CRUD with function views and ModelForm
date: 2023-12-11
tags: python django views models forms
categoris: Programming
---

To create a model form, see [[Create django form from model]].

1. Create view: 

We create a form instance with the POST data, and then create a new model instance with `form.save(commit=False)`:

```python
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        return render(request, 'create_review.html', {'form': ReviewForm(), 'movie': Movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'create_review.html', {'form': ReviewForm(), 'movie': Movie, 'error': 'bad data passed in.'})
```

2. Update  view:

We retrieve the model instance with its id, and also supply the logged-in user to ensure that other users can't access the instance - for example, if they manually enter the URL path in the browser, only the user who created this can update/delete it.

When create form instance, we pass in the model object so that the form's fields will be populated with the object's values, ready for the user to edit:

```python
def update_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'update_review.html', {'form': form, 'review': review})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'update_review.html', {'form': form, 'review': review, 'error': 'Bad data in form.'})
```

3. Delete view:

```python
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)
```