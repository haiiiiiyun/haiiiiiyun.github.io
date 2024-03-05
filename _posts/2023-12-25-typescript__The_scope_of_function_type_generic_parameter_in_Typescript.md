---
title: The scope of function type generic parameter in Typescript
date: 2023-12-25
tags: typescript functions types
categoris: Programming
---

See [[Define function type with generic type parameter in Typescript]].

1. If generic type is scoped to an individual signature, TS will bind the type to a concrete type when we call a function of the type, Each call will get its own binding.

```typescript
type FilterFn = <T>(array: T[], f: (item: T) => boolean) => T[];

type FilterFn2 = {
    <T>(array: T[], f: (item: T) => boolean) : T[],
}

let filter: FilterFn = (array, f) => [];
let filter2: FilterFn2 = (array, f) => [];

filter<number>([1, 2, 11], item => item < 10);
filter2<number>([1, 2, 11], item => item < 10);
```

2. if generic type is scoped to the type declaration(to all of the signatures),  TS will bind the generic type when we declare a function of this type.

```typescript
type FilterFn<T> = (array: T[], f: (item: T) => boolean) => T[];

type FilterFn2<T> = {
    (array: T[], f: (item: T) => boolean) : T[],
}

let filter: FilterFn<number> = (array, f) => [];
let filter2: FilterFn2<number> = (array, f) => [];

filter([1, 2, 11], item => item < 10);
filter2([1, 2, 11], item => item < 10);
```