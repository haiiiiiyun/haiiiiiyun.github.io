---
title: Safely extend the prototype in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

In Javascript we can modify any built-in method(like `[].push`, `'abc'.toUpperCase`, `Object.assign`) at runtime. We can directly access prototypes for every built-in object -- `Array.prototype`, `Function.prototype`, `Object.prototype`, and so on.

In the example below we add `zip()` to `Array.prototype`.

## Interface

We take advantage of interface merging to augment the global `Array<T>` interface, adding our own `zip` method to the already globally defined interface:

```typescript
// in zip.ts file

// Tell TS about .zip
interface Array<T> {
    zip<U>(list: U[]): [T, U][];
}
```

Since our file doesn't have any explicit imports or exports---meaning it's in script mode, we were able to augment the global `Array` interface directly by declaring an interface with the exact same name. See [[Module mode vs script mode in Typescript]].

If our file were in module mode, we'd have to wrap our global extension in a `declare global` type declaration:

```typescript
// Tell TS about .zip
declare global {
    interface Array<T> {
        zip<U>(list: U[]): [T, U][];
    }
}
```

## Implementation

We use a `this` type so that TS correctly infers the T type of the array we're calling `.zip` on.

See [[Create a tuple constructor function in Typescript]],  we use our `tuple` utility to create a tuple type without resorting to a type assertion:

```typescript

// Implement .zip
Array.prototype.zip = function<T, U>(
    this: T[],
    list: U[]
) : [T, U][] {
    return this.map((item, idx) => tuple(item, list[idx]));
}
```

## load implementation before using

Update our `tsconfig.json` to explicitly exclude `zip.ts` from our project, so that consumers have to explicitly import it first:

```{
  exclude: ["./zip.ts"]
}
```


```typescript
import './zip';
[1, 2, 3]
	.map(n => n * 2)  // number[]
	.zip(['a', 'b', 'c']); // [number, string][]
```