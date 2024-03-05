---
title: Annotated types and inferred types in Typescript
date: 2023-12-12
tags: typescript types
categoris: Programming
---

1. We can explicitly annotate types, annotations take the form `value:type`, for example:

```typescript
let a: number = 1; // a is a number
let b: string = 'hello'; // b is a string
let c: boolean[] = [true, false]; // c is an array of booleans
```

2. We can let Typescript infer most of them for us, just leave them off and let Typescript get to work:

```typescript
let a = 1; // a is a number
let b = 'hello'; // b is a string
let c = [true, false]; // c is an array of booleans
```

We use annotations only when necessary, keeping explicitly typed code to a minimum, and let Typescript work its inference magic for us whenever possible.