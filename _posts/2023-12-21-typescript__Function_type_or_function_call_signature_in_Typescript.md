---
title: Function type or function call signature in Typescript
date: 2023-12-21
tags: typescript functions types
categoris: Programming
---

We declare a function call signature using a syntax that is remarkably similar to an arrow function:

```typescript
type Log = (message: string, userId?: string) => void;

let log:Log = (message, userId='Not signed in') => {
    let time = new Date().toISOString();
    console.log(time, message, userId);
}
```

When implementing, we don't need to annotate our parameter twice. Since parameters are already annotated in the definition of the function type.

see [[Contextual typing in Typescript]].