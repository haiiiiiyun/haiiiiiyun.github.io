---
title: Non-null assertion in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

If a type that's `T | null` or `T | null | undefined`, we use non-null assertion operator `!` to tell TS that we're sure it's not `null | undefined`:

```typescript
function removeFromDOM(element: Element){
    // element.parentNode.removeChild(element); // 'element.parentNode' is possibly 'null'.
    element.parentNode!.removeChild(element);
}

let id = 'testId';
// removeFromDOM(document.getElementById(id)); // Argument of type 'HTMLElement | null' is not assignable to parameter of type 'Element'.
removeFromDOM(document.getElementById(id)!);
```