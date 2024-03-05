---
title: Type number and bigint in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---

1. `number` is the set of all numbers: integers, floats, positives, negatives, Infinity, NaN and so on.

2. numeric separators: We can use numeric separators to make numbers easier to read when working with long numbers: 

```typescript
let oneMillion = 1_000_000; // Equivalent to 1000000
let twoMillion: 2_000_000 = 2_000_000;
```

3. bigint 

It let us work with large integers without running into rounding errors. `bigint` is not yet natively supported by every JS engine.

To represent a bigint, we add a suffix `n` to an integer:

```typescript
let a = 1234n; // bigint
const b = 567n; // 567n
var c = a + b; // bigint
let d = 88.5n; // Error TS1353: A bigint literal must be an integer
let e: bigint = 100; // Error TS2322: Type '100' is not assignable to type `bigint`.
```

