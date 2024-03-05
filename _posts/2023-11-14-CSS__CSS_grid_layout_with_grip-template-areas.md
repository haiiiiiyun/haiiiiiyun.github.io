---
title: CSS grid layout with grip-template-areas
date: 2023-11-14
tags: css layout grid
categoris: Programming
---

1. apply `display:grid` on the container element.
2. `grid-template-columns` and `grid-template-rows` for defining column width and row height;
3. `grid-template-areas` for defining grid cell names
4. `gap` for defining grid gutter: row-gap column-gap.
5. apply the grid cell name on the element with `grid-area: cellName`

For example:

```css
main {
	display: grid;
	 /* grid-template-columns and grid-template-rows for defining column width and row width */
	grid-template-columns: repeat(3, minmax(auto, 1fr));
	 /* grid-template-areas for defining grid cell names */
    grid-template-areas:
	  "header  header   header"
      "content content  aside"
	  "footer  footer   footer";
   gap: 20px 10px; /* grid gutter: row-gap column-gap */
}

/* assign tag to a grid cell */
header { grid-area: header }
```

See the Pen [LYqjdvQ](https://codepen.io/haiiiiiyun/pen/LYqjdvQ).

```html
<html>

<head>
  <title>CSS Grid layout</title>
</head>

<body>
  <main>
    <div class="header">Header</div>
    <div class="content">Content</div>
    <div class="aside">Aside</div>
    <div class="footer">Footer</div>
  </main>
</body>

</html>
```

```css
main {
  display: grid;
  grid-template-columns: repeat(3, minmax(auto, 1fr));
  gap: 20px 10px;
  grid-template-areas:
    "header  header header"
    "content content aside"
    "footer  footer footer";
}

div.header {grid-area: header; }
div.content {grid-area: content; }
div.aside {grid-area: aside; }
div.footer {grid-area: footer; }

main div {
  border: 1px solid;
}
```