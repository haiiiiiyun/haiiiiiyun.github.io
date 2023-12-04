---
title: CSS SVG frame and viewBox size
date: 2023-11-14
tags: css svg
categoris: Programming
---

## SVG frame/viewport size

`width` and `height` properties define the frame/viewport size.

## content area size with viewBox

`viewBox` defines the area for image content.

viewBox is like the pan and zoom tools, we position the image in the frame/viewport with `minX, minY`,  the image is also scaled based on the frame's size.

```css
<svg viewBox="minX minY width height" width="100%" height="300px">
</svg>
```