---
title: Classes declare both values and types in Typescript
date: 2023-12-28
tags: typescript classes
categoris: Programming
---

Types and values are namespaced separately in TS.

Classes and enums generate both a type in the type namespace and a value in the value namespace.

```typescript
class C {}
let c: C  // C refers to the instance type of C class
  = new C // C refers to C the value
enum E {F, G}
let e: E  // E refers to the type of E enum
  = E.F   // E refers to E the value
```


See [[Typescript has separate namespaces for values and for types and the companion object pattern]].