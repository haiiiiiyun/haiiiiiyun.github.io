---
title: Create CSS custom properties or CSS variables
date: 2023-11-14
tags: css variable
categoris: Programming
---

To create a custom property, or CSS variable, we prefix the variable name with two `--` immediately followed by the variable name:

```css
body {
	--primary: #de3c4b;
}
```

CSS vendor specific property has a prefix `-`, so it makes sense to have prefix of two `--` in CSS custom properties.

We reference the CSS variable with syntax `var(--variableName)`:

```css
body {
	color: var(--primary);
}
```