---
title: Typescript uses infer keyword to declare generic types inline for conditional types
date: 2024-01-05
tags: typescript types conditional
categoris: Programming
---

Use `infer` keyword, we can declare generic types inline:

```typescript
type ElementType<T> = T extends (infer U)[] ? U : T;
type A = ElementType<number[]>; // number
```

`infer` clause declares a new variable U -- TS will infer the type of U from context.

In the following example, we declare a conditional type for second argument of a function:

```typescript
type SecondArgType<F> = F extends (a:any, b: infer B) => any ? B : never;

// Get the type of Array.slice
type F = typeof Array["prototype"]["slice"];
type A = SecondArgType<F>; // number | undefined
```