---
title: Prevent type widening in Typescript
date: 2024-01-02
tags: typescript types
categoris: Programming
---

Also see [[Type widening in Typescript]].

1. Use literal type for preventing type widening:

```typescript
let a: 'x' = 'x';
let b: 3 = 3
var c: true = true
const d: {x: 3} = {x: 3}
```

2. When reassign a non-widened type using `let` or `var`, TS widens it, to keep it narrow, add an explicit type annotation to the original declaration:

```typescript
const a = 'x'; // 'x'
let b = a; // string
b = 'y';

const c: 'x' = 'x'; // 'x'
let d = c; // 'x'
d = 'y'; // Type '"y"' is not assignable to type '"x"'.
```

3. const type opts the type out of widening and recursively marks its members as readonly, even for deeply nested data structures:

```typescript
let a = {x: 3} as const; // { readonly x: 3 }
a.x = 4; // Cannot assign to 'x' because it is a read-only property.

let b = [1, {x: 3}] as const; // readonly [1, { readonly x: 3}]
b[1].x = 4; // Cannot assign to 'x' because it is a read-only property.
```