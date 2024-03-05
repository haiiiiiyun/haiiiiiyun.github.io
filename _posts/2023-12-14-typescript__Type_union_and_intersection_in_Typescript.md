---
title: Type union and intersection in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---

Types are a lot like sets, we can use special type operations to describe unions and intersections of types:

+ `|` for union
+ `&` for intersection

## Union

A value(or partial of a value) with a union type `|` satisfy at least one of a type, it can satisfy all of the types at once:

```typescript
type Cat = { name: string, purrs: true};
type Dog = { name: string, barks: true, wags: true};
type CatOrDogOrBoth = Cat | Dog;

let cat: CatOrDogOrBoth = { name: 'Bonkers', purrs: true }; // satisfy Cat
let dog: CatOrDogOrBoth = { name: 'Domino', barks: true, wags: true }; // satisfy Dog
let both: CatOrDogOrBoth = { name: 'Donkers', barks: true, wags: true, purrs: true}; // satisfy both: Dog and Cat
let cat2: CatOrDogOrBoth = { name: 'Donkers', barks: true, purrs: true}; // partial of it satisfy Cat
let both3: CatOrDogOrBoth = { name: 'Donkers', barks: true}; // Type '{ name: string; barks: true; }' is not assignable to type 'CatOrDogOrBoth'.
  Property 'wags' is missing in type '{ name: string; barks: true; }' but required in type 'Dog'
```

Another example, if a function returns `type Results = string | null`, then it might return a `string`, or it might return a `null`.

## Intersection

A value with a intersection type `&` must satisfy all of the types at once.

```typescript
type CatAndDog = Cat & Dog;
let both: CatAndDog = { name: 'Donkers', barks: true, wags: true, purrs: true};
```