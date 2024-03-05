---
title: Type aliases in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---

## Declare a type alias just like declare a variable

Just like we can use variable declarations(let, var, const) to declare a variable that aliases to a value, we can declare a type alias that points to a type.

```typescript
type Age = number;
type Person = {
    name: string,
    age: Age
}

let age:Age = 5;
let driver: Person = { name: 'Jump Roper', age: age };

type Color = 'red'; // a type aliases to a type literal
let color:Color = 'red';
```

Whenever we see a type alias used, we can substitute in the type it aliases without changing the meaning of the program.

## Like variable declaration, we can't declare a type twice

## Like let and const, type aliases are block-scoped
