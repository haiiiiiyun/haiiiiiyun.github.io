---
title: Generator functions in Typescript
date: 2023-12-21
tags: typescript functions generator
categoris: Programming
---

```typescript
function* createFibonacciGenerator(){
	let a = 0;
	let b = 1;
	while (true) {
		yield a;
		[a, b] = [b, a + b];
	}
}

let fibonacciGenerator = createFibonacciGenerator(); // IterableIterator<number>
fibonacciGenerator.next(); // {value: 0, done: false}
fibonacciGenerator.next(); // {value: 1, done: false}
```

1. The asterisk `*` before a function's name makes that function a generator. Calling a generator returns an iterable iterator.
2. Generators use `yield` keyword to yield values.
3. Typescript is able to infer the type of our iterator from the type of value we yielded.
4. Call `next()` on the iterator to get the next value.