---
title: Distributive conditional types in Typescript
date: 2024-01-05
tags: typescript types conditional
categoris: Programming
---

See [[Create conditional types in Typescript]].

Conditional types follow the **distributive law**, when we use a conditional type, TS will distribute union types over the conditional's branches. It's like taking the conditional type and mapping it over each element in union:

```typescript
type ToArray<T> = T extends unknown ? T[] : T[];
type A = ToArray<number>; // number[]
type B = ToArray<number | string>; // number[] | string[]
								   // NOT (number | string)[] !!!
```