---
title: Generic type defaults in Typescript
date: 2023-12-27
tags: typescript types
categoris: Programming
---

Just like we can give function parameters default value, we can give generic type parameters default types:

```typescript
type MyEvent<T = HTMLElement> = {
    target: T,
    name: string
};
```

see [[Add bound to generic type using extends in Typescript]], we can add bound to generic type at the same time:

```typescript
type MyEvent<T extends HTMLElement = HTMLElement> = {
    target: T,
    name: string
};
```

Like optional parameters in functions, generic types with defaults have to appear after generic types without defaults:

```typescript
type MyEvent<
    Type extends string,
    Target extends HTMLElement = HTMLElement
> = {
    target: Target,
    type: Type
}
```