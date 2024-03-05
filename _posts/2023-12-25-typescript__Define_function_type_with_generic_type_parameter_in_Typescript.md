---
title: Define function type with generic type parameter in Typescript
date: 2023-12-25
tags: typescript functions types
categoris: Programming
---

**Generic type parameter** is a placeholder type used to enforce a type-level constraint in multiple places. Also known as **polymorphic type parameter**.

```typescript
type FilterFn<T> = (array: T[], f: (item: T) => boolean) => T[];

type FilterFn2 = {
    <T>(array: T[], f: (item: T) => boolean) : T[],
}

type MapFn<T, U> = (array: T[], f: (item: T) => U) => U[];
```

By convention, we use `T, U, V, W` and so on as generic type name.

The way to think about generics is as *constraints*. Just like annotating a function parameter as `n: number` constrains the value of the parameter n to the type `number`, so using a generic `T` constrains the `type` of whatever type you bind to `T` to be the same type everywhere that T shows up.