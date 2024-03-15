---
title: Event.target vs Event.currentTarget in Javascript
date: 2024-03-13
tags: javascript events
categoris: Programming
---

+ target: refers to the element that triggered the event
+ currentTarget: refers to the element that the event handler/listener is attached to.

## Example one, target and currentTarget are not the same

```html
<div id="target">
    <span>click me</span>
</div>
```

```js
const elem = document.getElementById('target'); // div

elem.addEventListener('click', function (event) {
    console.log(event.target); // span
    console.log(event.currentTarget); // div
});
```

## Example two, target and currentTarget are the same

```html
<div>
    <span id="target">click me</span>
</div>
```

```js
const elem = document.getElementById('target'); // span

elem.addEventListener('click', function (event) {
    console.log(event.target); // span
    console.log(event.currentTarget); // span
});
```