---
title: Type widening in Typescript
date: 2024-01-02
tags: typescript types
categoris: Programming
---

1. Declare a variable in a way that allows it to be mutated later(e.g., with `let`, `var`), its type is widened from its literal value to the base type that literal belongs to:

```typescript
let a = 'x'; // string
a = 'y';
let b = 3; // number
b = 4;
var c = true; // boolean
c = false;
const d = { x: 3}; // { x: number }
d.x = 4;

enum E{X, Y, Z};
let e = E.Y; // E
e = E.Z;
```

2. Variables initialized to `null` or `undefined` are widened to `any`:

```typescript
let a = null;
a = 3;
a = 'b';
```

But if this variable leaves out of the scope(e.g., return from a function) it was declared in, Typescript assigns it a definite type.