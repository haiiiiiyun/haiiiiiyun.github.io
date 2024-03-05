---
title: Type unknown in Typescript
date: 2023-12-13
tags: typescript types
categoris: Programming
---

Like `any`, `unknown` represents any value, but we can't operate on `unknown` type until we refine it by checking what it is with `typeof` or `instanceof`.

Like `boolean`, `unknown` only supports comparison operations(`==, ===, ||, &&, ?`) and negation operation(`!`).

```typescript
let a: unknown = 10;  //unknown
let b = a === 123;  // boolean
let c = a + 10; // Error TS2571: Object is of type 'unknown'
if (typeof a === 'number') {
	let d = a + 10;  // number
}
```

1. Typescript will never infer something as `unknown`, we have to explicitly annotate it (a).
2.  `unknown` supports comparison operations and negation operation, same as  `boolean` does(b).
3.  we can't do things that assume an `unknown` value is of a specific type(c).
4.  We can operate on `unknown` type after checking it with `typeof` or `instanceof`.