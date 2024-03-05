---
title: Type literal in Typescript
date: 2023-12-13
tags: typescript types
categoris: Programming
---

Type literal is a type that represents a single value and nothing else. By using a value as a type, we essentially limit the possible values.

```typescript
let a = true; // boolean
var b = false; // boolean
const c = true; // true
let d: true = true; // true
let e: true = false; // Error TS2322: Type 'false' is not assignalbe to type 'true'
let f: 26.218 = 26.218; // 26.218
let g: 26.218 = 10; // Error TS2322: Type '10' is not assignalbe to type '26.218'
```

1. `a`, `b` is mutable and Typescript inferred a `boolean` type.
2. `c` is constant, Typescript inferred a type literal `true`.
3.  we annotate `d` , `e` , `f`, `g` as type literals, so that only specific value is assignable to it.