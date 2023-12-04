---
title: Create CSS list style  with counter style by @counter-style
date: 2023-11-14
tags: css list-style
categoris: Programming
---

## Create a custom list style with @counter-style

+ **symbols** defines the list counter symbols.
+ **system** specifies the algorithm for how to apply the list counter, such as `cyclic`
+ **suffix** defines the contents between the list counter symbol and the list item content.

Now apply the list style on a list container element with `list-style: styleName`.

```css
@counter-style emoji {
  symbols: "\2615";
  system: cyclic;
  suffix: " ";
}
article ul {
  list-stytle: emoji;
}
```


See the Pen [yLZoxOV](https://codepen.io/haiiiiiyun/pen/yLZoxOV).

```html
<html>

<head>
  <title>CSS Multi-column layout</title>
</head>

<body>
  <article>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
  </article>
</body>

</html>
```

```css
@counter-style emoji {
  symbols: "\2615";
  system: cyclic;
  suffix: " ";
}

article ul {
  list-style: emoji;
}
```