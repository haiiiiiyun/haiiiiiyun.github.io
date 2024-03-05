---
title: Type array in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---

Typescript infers the types of the array's elements on initialization:

```typescript
let a = [1, 2, 3]; // number[]
let b = [1, 'a']; // (number | string)[]
const c = [2, 'b']; // (number | string)[]
let d: string[] = ['a']; // string[]

let f = ['red']; // string[]
f.push('blue');
f.push(true); // Argument of type 'true' is not assignable to parameter of type 'string'.
```

When we initialize an empty array, Typescript doesn't know what type the array's elements should be, so it makes them `any`. As we manipulate the array and add elements to it, Typescript starts to piece together array's type.

```typescript
function buildArray() {
    let g = []; // any[], so we can push elements of any type
    g.push(1); // number[]
    g.push('red'); // (number | string) []
    return g;
}
```

Once our array leaves the scope it was defined in(for example, if we declared it in a function, then returned it),  Typescript will assign it a final type that can't be expanded anymore.

```typescript
let myArray = buildArray();
myArray.push(true); // Argument of type 'boolean' is not assignable to parameter of type 'string | number'.
```

We can explicitly annotate an array as read-only. We can't update read-only arrays in place, to update, we use non-mutating methods like `.concat`, `.slice` instead of mutating ones like `.push` and `.splice`.

```typescript
let as: readonly number[] = [1, 2, 3]; // readonly number[]
let bs: readonly number[] = as.concat(4);
let three = bs[2];
as[1] = 0; // Error: Index signature in type 'readonly number[]' only permits reading.
as.push(6); // Error: Property 'push' does not exist on type 'readonly number[]'.
```