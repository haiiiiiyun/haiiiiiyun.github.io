---
title: Type cast or type assertion using as keyword in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

We use a type assertion `as` to tell TS that we know some variable is of some specific type:

```typescript
function formatString(input: string){}

function getUserInput(): string | number{ return 'test';}

let input = getUserInput(); // string | number

// formatString(input); // Argument of type 'string | number' is not assignable to parameter of type 'string'.
formatString(input as string);
```