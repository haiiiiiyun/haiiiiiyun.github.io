---
title: Annotate the type for function this parameter in Typescript
date: 2023-12-21
tags: typescript functions
categoris: Programming
---

In Javascript `this` variable is defined for every function, not just for those functions that live as methods on classes.

`this` has a different value depending on how you called the function.

If our function uses `this`, be sure to declare the expected `this` type as the function's first parameter, `this` isn't treated like other parameters, it's a reserved word when used as part of a function signature:

```typescript
function fancyDate(this: Date){
	return ${this.getDate()}/${this.getMonth()}/${this.getFullYear()}
}

fancyDate.call(new Date()) // evaluates to a string date
fancyDate(); //error: The 'this' context of type 'void' is not assignable to method's 'this' of type 'Date'
```