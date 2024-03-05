---
title: Flatten an array of arrays into an array in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

```typescript
function flatten<T>(array: T[][]): T[] {
    return Array.prototype.concat.apply([], array);
}
```