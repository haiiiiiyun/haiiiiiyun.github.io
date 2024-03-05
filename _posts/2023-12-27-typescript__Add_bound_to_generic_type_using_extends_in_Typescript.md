---
title: Add bound to generic type using extends in Typescript
date: 2023-12-27
tags: typescript types
categoris: Programming
---

We can put a constraint/put an upper bound on the generic type. In the following example, the generic type `Shape` have to extend `HasSides` and `SidesHaveLength`:

```typescript
type HasSides = { numberOfSides: number };
type SidesHaveLenth = { sideLength: number };

function logPrimeter<Shape extends HasSides & SidesHaveLenth>(s: Shape): Shape {
    console.log(s.numberOfSides * s.sideLength);
    return s;
}
```

We can use it to model variadic functions such as `call`:

```typescript
function call<T extends unknown[], R>(
    f: (...args: T) => R,
    ...args: T
): R {
    return f(...args);
}
```

1. `call` has two type parameters: T and R. T is a subtype of `unknown[]`.
2. call's first parameter is a function `f`, `f` is also a variadic and its arguments share a type with `args`.
3. call has a variable number of additional parameters `...args`, which is a rest parameter, and with a type `T`.