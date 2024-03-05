---
title: Rest parameters of functions in Typescript
date: 2023-12-21
tags: typescript functions
categoris: Programming
---

A function can have at most one rest parameter, and that parameter has to be the last one in the function's parameter list.

```typescript
function log(message: string, ...optionalParams: any[]){}
```