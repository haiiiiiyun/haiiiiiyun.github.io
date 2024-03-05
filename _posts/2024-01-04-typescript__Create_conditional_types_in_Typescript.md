---
title: Create conditional types in Typescript
date: 2024-01-04
tags: typescript types conditional
categoris: Programming
---

The syntax looks just like the regular value-level ternary expression, but at the type level:

```typescript
type IsString<T> = T extends string ? true : false;
type A = IsString<string>; // true
type B = IsString<number>; // false
```