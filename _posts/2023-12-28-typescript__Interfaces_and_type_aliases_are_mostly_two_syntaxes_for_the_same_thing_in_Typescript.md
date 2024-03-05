---
title: Interfaces and type aliases are mostly two syntaxes for the same thing in Typescript
date: 2023-12-28
tags: typescript types interfaces
categoris: Programming
---

The type alias syntax is like the syntax for defining variables. The interface syntax is like the syntax for defining classes.

```typescript
type Sushi = {
    calories: number,
    salty: boolean,
    tasty: boolean
};

interface ISushi {
    calories: number,
    salty: boolean,
    tasty: boolean
}
```

Everywhere we used `Sushi` type alias, we can also use the `ISushi` interface. Both declarations define shapes, and those shapes are assignable to one another(in fact, they're identical).