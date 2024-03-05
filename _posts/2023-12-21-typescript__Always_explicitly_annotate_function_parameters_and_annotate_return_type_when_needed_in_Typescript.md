---
title: Always explicitly annotate function parameters and annotate return type when needed in Typescript
date: 2023-12-21
tags: typescript functions
categoris: Programming
---

Typescript won't infer types for parameters in most cases, so we will usually explicitly annotate function parameters.

Typescript will always infer types throughout the body of the function, and the return type can be inferred.  It's not necessary to annotate return type, but explicitly annotate return types helps the code reader.

```typescript
function add(a: number, b: number) {
  return a + b;
}
```