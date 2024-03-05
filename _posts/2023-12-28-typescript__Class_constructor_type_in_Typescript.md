---
title: Class constructor type in Typescript
date: 2023-12-28
tags: typescript types classes
categoris: Programming
---

Typescript is structurally typed, a `class` is anything that can be `new`ed, see [[Classes are structurally typed Typescript compares classes by their struct not by name]].

A constructor type of a class is something like: 

```typescript
type MyClassConstructor<R> = {
	new(...args: any[]) : R
}

// or shorthand version:
type MyClassConstructor<R> = new(...args: any[]) => R;
```

That `new()` bit is called a **constructor signature**.

Not only does a class declaration generates terms at the value and type levels, but it generates two at the type level: one representing an instance of the class; one representing the class constructor itself(reachable with the `typeof` type operator).