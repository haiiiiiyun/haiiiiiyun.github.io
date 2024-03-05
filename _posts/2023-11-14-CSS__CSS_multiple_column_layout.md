---
title: CSS multiple column layout
date: 2023-11-14
tags: css layout column
categoris: Programming
---

Dictate the column width or column counter with `column-count` to apply a multi-column layout on a container element.

```css
articl {
  column-count: 3;
  column-rule: 2px solid #333333;
}
```

`column-rule` is just like `border`, it defines the borders between columns.

See the Pen [rNPzvwY](https://codepen.io/haiiiiiyun/pen/rNPzvwY).

```html
<html>

<head>
  <title>CSS Multi-column layout</title>
</head>

<body>
  <article>
    <div class="article1">Article1</div>
    <div class="article2">Article2</div>
    <div class="article3">Article3</div>
    <div class="article4">Article4</div>
    <div class="article5">Article5</div>
  </article>
</body>

</html>
```

```css
article {
  column-count: 3;
  column-rule: 2px solid #333;
}

article div {
  border: 1px solid;
}
```