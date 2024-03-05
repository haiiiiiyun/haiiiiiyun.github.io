---
title: Type any in Typescript
date: 2023-12-13
tags: typescript types
categoris: Programming
---

In Typescript everything needs to have a type at compile time, and `any` is the default type when you(programmer) and Typescript(typechecker) can't figure out what type something is.

`let c = a + b;` line would throw a compile-time exception,  but here by explicitly annotating a and b with the `any` type, we avoid the exception.
```typescript
let a: any = 666;
let b: any = ['danger'];
let c = a + b;
console.log('c=', c);
```

`any` makes our value behave like it would in regular Javascript, and totally prevents the typechecker from working its magic.

**It's the last resort type, we should avoid it when possible.**
