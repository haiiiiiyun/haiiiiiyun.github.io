---
title: Some built-in conditional types in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

## Exclude<T, U>

Computes those types in T that are not in U:

```typescript
type A = number | string;
type B = string;

type C = Exclude<A, B>; // number
```


## Extract<T, U>

Computes those types in T that we can assign to U:

```typescript
type D = Extract<A, B>; // string
```

##  NonNullable

Computes a version of T that excludes null and undefined:

```typescript
type E = {a?: number | null};
type F = NonNullable<E['a']>; // number
```

## ReturnType

Passing a function type, and computes the function's return type:

```typescript
type Fun = (a:number) => string;
type R = ReturnType<Fun>; // string
```

## InstanceType

Computes the instance type of a class constructor:

```typescript
type ConstructorType = {new(): I};
type I = {b: number};
type IT = InstanceType<ConstructorType>; // {b: number}
```