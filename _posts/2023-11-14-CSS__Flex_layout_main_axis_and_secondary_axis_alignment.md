---
title: Flex layout main axis and secondary axis alignment
date: 2023-11-14
tags: css layout flex
categoris: Programming
---

In flex layout, the default  flex-direction is `row`,  which means the row(horizontal) axis  is the main axis and the column(vertical) axis is the secondary axis.

`justify-content` defines how elements are distributed across the main axis.  

`align-items` defines how elements are positioned relative to one another and to the container across the secondary axis.

```css
body {
	display: flex;
	justify-content: center;
	align-items: center;
}
```