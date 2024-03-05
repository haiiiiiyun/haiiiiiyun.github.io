---
title: Type tuple in Typescript
date: 2023-12-20
tags: typescript types
categoris: Programming
---

##  tuple is sub-type of  array

`tuple` is sub-type of array, see [[Type array in Typescript]]. They're a special way to type arrays that have **fixed** lengths, where the values at each index have specific, known types.

## we should explicitly declare tuple type

Unlike most other types, tuples have to be explicitly typed when we declare them. That's because the Javascript syntax is the same for tuples and arrays(both `[]`).

```typescript
let a: [number] = 1;
let b: [string, string, number] = ['malcolm', 'gladwell', 1963];
b = ['queen', 'elizabeth', 'ii', 1926]; // Type 'string' is not assignable to type 'number'.
```

see [[Create a tuple constructor function in Typescript]].

## tuple supports optional elements

```typescript
// An array of train fares, which sometimes vary depending on direction
let trainFares: [number, number?][] = [
	[3.75], [8.25, 7.70], [10.50]
];
```

## tuple supports rest elements, which we can use to type tuples with minimum lengths.

```typescript
// A list of strings with at least 1 element
let friends: [string, ...string[]] = ['Sara', 'Tali', 'Chloe', 'Claire'];

// A heterogenous list
let list: [number, boolean, ...string[]] = [1, false, 'a', 'b'];
```
