---
title: CSS gets element's attribute value via attr function, display HTML attributes via CSS using pseudo elements
date: 2023-11-14
tags: css function attr pseudo-element
categoris: Programming
---

In CSS, we can extract the attribute value of an element which is being applying the CSS rule via `attr(attrName)` function.

With this feature,  we can display HTML attributes via CSS using pseudo elements.

```css
td[data-name]::before {
	content: attr(data-name) ":";
	float: left;
}
```

```html
<tr>
	<td data-name="Price">$1.00</td>
<tr>
```

See the Pen [wvNqYpr](https://codepen.io/haiiiiiyun/pen/wvNqYpr).