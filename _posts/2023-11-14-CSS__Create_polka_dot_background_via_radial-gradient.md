---
title: Create polka dot background via radial-gradient
date: 2023-11-14
tags: css gradient
categoris: Programming
---

```css
body {
  background-color: var(--background);
  background-image: radial-gradient(var(--accent) .75px, transparent .75px);
  background-size: 15px 15px;
}
```

See Pen [KKJvraL](https://codepen.io/haiiiiiyun/pen/KKJvraL)

See [radial-gradient on MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/radial-gradient)

```html
<html>
<head>
  <title>CSS Grid layout</title>
</head>
<body>
  content
</body>
</html>
```

```css
body {
  --background: lightyellow;
  --accent: green;
}

body {
  background-color: var(--background);
  background-image: radial-gradient(var(--accent) .75px, transparent .75px);
  background-size: 15px 15px;
}
```