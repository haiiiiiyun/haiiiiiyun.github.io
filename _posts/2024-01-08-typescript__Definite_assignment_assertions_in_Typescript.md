---
title: Definite assignment assertions in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

A definite assignment check is TS's way of making sure that by the time we use a variable, that variable has been assigned a value:

```typescript
let userId: string;
userId.toUpperCase(); // Variable 'userId' is used before being assigned.
```

We can use definite assignment assertion to tell TS that the variable will definitely be assigned by the time we read it:

```typescript
let userId!: string; // notice the ! after variable name
fetchUser();

userId.toUpperCase();

function fetchUser(){
    userId = 'testId';
}
```