---
title: Contextual typing in Typescript
date: 2023-12-21
tags: typescript types functions
categoris: Programming
---

See the example in [[Function type or function call signature in Typescript]], where we didn't have to explicitly annotate our function parameter types, Typescript is able to infer from context. This is a powerful feature of Typescript's type inference called **contextual typing**.

Here we declare a function `times` that calls its callback `f`, when we call `times`, we don't have to explicitly annotate the function we pass to `times` if we declare that function inline:

```typescript
function times(
	f: (index: number) => void,
	n: number
) {
	for (let i = 0; i < n; i++){
		f(i);
	}
}

// here we're declaring f as an inline function, we don't need to annotate `n`, TS can infer from context that n is a number.
times(n => console.log(n), 4)

// if we don't declare f inline:
function f(n){...}
times(f, 4) // Error: Parameter 'n' implicitly has an 'any' type.
```