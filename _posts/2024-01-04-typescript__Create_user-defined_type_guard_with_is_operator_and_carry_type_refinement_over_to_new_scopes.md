---
title: Create user-defined type guard with is operator and carry type refinement over to new scopes
date: 2024-01-04
tags: typescript types
categoris: Programming
---

Type refinement is only powerful enough to refine the type of a variable in the scope we're in. As soon as we leave the scope, the refinement doesn't carry over to new scope:

```typescript
function isString(a: unknown): boolean {
    return typeof a === 'string';
}

function parseInput(input: string | number){
    if (isString(input)){ // input type is not refined
        let formattedInput = input.toUpperCase(); // Property 'toUpperCase' does not exist on type 'string | number'.
    }
}
```

We can tell the typechecker that not only does `isString` return a boolean, but whenever that boolean is true, the argument we passed to is a string. To do that, we use something called a `user-defined type guard`:

```typescript
function isString(a: unknown): a is string {
    return typeof a === 'string';
}
```

When we have a function that refines its parameters' type and returns a boolean, we can use user-defined type guard to make sure that refinement is flowed whenever we use that function.
User-defined type guards are limited to a single parameter, but they aren't limited to a simple type.