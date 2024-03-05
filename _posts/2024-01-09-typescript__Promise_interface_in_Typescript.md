---
title: Promise interface in Typescript
date: 2024-01-09
tags: typescript async
categoris: Programming
---

Promises are a way to abstract over asynchronous work so that we can compose it, sequence it, and so so.

## Promise executor arguments and resolve, reject

A **new Promise** takes a function we call an **executor**, which the Promise implementation will call with two arguments, a `resolve` function and a `reject` function. Promise calls back `resolve` on success, and calls back `reject` on failure.

```typescript
type Executor<R, E extends Error> = (
    resolve: (result: R) => void,
    reject: (error: E) => void
) => void;

class MyPromise<R, E extends Error> {
    constructor(f: Executor<R, E>){}
}
```

## Sequence Promise

`then` maps a successful result of a Promise to a new Promise, and `catch` recovers from a rejection by mapping an error to a new Promise.

```typescript
// ...
class MyPromise<R, E extends Error> {
    constructor(f: Executor<R, E>){}
    then<U, F extends Error>(g: (result: R) => MyPromise<U, F>): MyPromise<U, F>
    catch<U, F extends Error>(g: (error: E) => MyPromise<U, F>): MyPromise<U, F>
}
```

and using them look like this:

```typescript
let a: () => Promise<string, TypeError> = // ...
let b: (s: string) => Promise<number, never> = // ...
let c: () => Promise<boolean, RangeError> = // ...
a()
  .then(b)
  .catch(e => c()) // b won't error, so this is if a errors
  .then(result => console.info('Done', result))
  .catch(e => console.error('Error', e))
```

When we implement `then` and `catch`, we'll do this by wrapping code in `try/catch` and rejecting in the `catch` clause. But `Promise` won't always be rejected with an `Error`. Because TS as well as JS can `throw` anything--a string, a function, an array, a Promise, and not necessarily an Error. Taking that into account, let's loosen our Promise type a bit by not typing errors:

```typescript
type Executor<R> = (
    resolve: (result: R) => void,
    reject: (error: unknown) => void
) => void;

class MyPromise<R> {
    constructor(f: Executor<R>){}
    then<U>(g: (result: R) => MyPromise<U>): MyPromise<U>
    catch<U>(g: (error: E) => MyPromise<U>): MyPromise<U>
}
```