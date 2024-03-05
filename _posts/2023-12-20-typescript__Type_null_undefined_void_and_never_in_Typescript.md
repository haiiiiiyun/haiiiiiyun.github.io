---
title: Type null undefined void and never in Typescript
date: 2023-12-20
tags: typescript types
categoris: Programming
---

These types are used to represent an absence of something.

1.  `null` type has only one value `null`, it means an absence of a value, like if we tried to compute a value, but ran into an error along the way.
2.  `undefined` type has only one value `undefined`, it means that something has not been defined yet.
3. `void` is the return type of a function that doesn't explicitly return anything, for example, `console.log`
4. `never` is the type of a function that never returns at all, like a function that throws an exception, or one that runs forever.

| type      | description                                                                                          |
| --------- | ---------------------------------------------------------------------------------------------------- |
| undefined | sth hasn't been defined yet                                                                          |
| null      | an absence of a value                                                                                |
| void      | the return type of a function that doesn't explicitly return anything                                 |
| never     | type of a function that never return at all(like a fun that throws an exc, or one that runs 

```typescript
// 1. A function that returns a number or null
function a(x: number) {
    if (x < 0) return x;
    return null;
}

// 2. A function that returns undefined
function b() {
    return undefined;
}

// 3. A function that return void, no explicit return at all
function c() {
    let a = 2 + 2;
    let b = a * a;
}

// 4. A function that returns never
function d(){
    throw TypeError('I always error');
}

// 5. Another function that returns never
function e(){
    while (true) {
        // doSomething();
    }
}
```