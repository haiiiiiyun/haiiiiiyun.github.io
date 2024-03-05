---
title: Type symbol in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---

##  Alternative to string keys

`symbol` does not come up often in practice, `symbol` values are used as an alternative to string keys in objects and maps, in places where we want to be extra sure that people are using the right well-known key and didn't accidentally set the key.

## each Symbol is unique

We call `Symbol(name)` to create a new `symbol` with the given name.
The way `Symbol(name)` works in Javascript is by creating a new `symbol` with the given name, that `symbol` is unique, and will not be equal(when compared with `==` or `===`) to any other `symbol`(even if create a second `symbol` with the same name).

Think of `Symbol(name)` always creates a Symbol and append it to a list, and returns back the index of the Symbol.

```typescript
let a1 = Symbol('a'); // symbol
let a2 = Symbol('a'); // symbol
console.log('a1 == a2', a1 == a2) // false
console.log('a1 === a2', a1 === a2) // false
```

## think of unique symbols like other literal types such as 1, true

```typescript
let a = Symbol('a'); // symbol
const b = Symbol('b'); // unique symbol
const c: unique symbol = Symbol('c'); // unique symbol
let d: unique symbol = Symbol('d');  // Error TS1332: A variable whose type is a `unique symbol` type must be 'const'.
```

1. When assignment a Symbol to a `let` or `var` variable, Typescript will infer its type as `symbol`, just like `number`(a)
2. When assignment a Symbol to a `const` variable, Typescript will infer its type as `unique symbol`(It will show up as `symbol`, not `unique symbol`), just like a number literal type `42`(b)
3.  We can explicitly annotate a `const` variable's type as `unique symbol`, but not a `let/var`(c, d)