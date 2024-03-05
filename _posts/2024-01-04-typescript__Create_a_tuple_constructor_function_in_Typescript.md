---
title: Create a tuple constructor function in Typescript
date: 2024-01-04
tags: typescript types
categoris: Programming
---

When we declare a tuple in Typescript, it will widen it and infer it as a array:

```typescript
let a = [1, true]; // (number | boolean)[]
```

We can take advantage of the way Typescript infers a tuple type for rest parameters, and create a tuple constructor function.

```typescript
function tuple<T extends unknown[]>(...ts: T): T {
    return ts;
}
let b = tuple(1, true); // [number, boolean]
```