---
title: Differences between type aliases and interfaces in Typescript
date: 2023-12-28
tags: typescript types interfaces
categoris: Programming
---

1. Extend type alias using `&` operator, extend interface with `extends` keyword:

```typescript
type Food = {
    calories: number,
    tasty: boolean
};
type Sushi = Food & {
    salty: boolean
};
type Cake = Food & {
    sweet: boolean
}

interface IFood {
    calories: number,
    salty: boolean
}
interface iSushi extends IFood {
    salty: boolean
}
interface ICake extends IFood {
    sweet: boolean
}
```

2. Type aliases are more general, their right-hand side can be any type, including a type expression; while the right-hand of interface must be a shape:

```typescript
type A = number;
type B = A | string;
```

3. When extend an interface, TS will make sure that the interface we're extending is assignable to the extension:

```typescript
interface A {
    good(x: number): string,
    bad(x: number): string
}

interface B extends A {
    bad(x: string): string // Types of property 'bad' are incompatible.
}
```

4. Multiple interfaces with the same name in the same scope are automatically merged; while we can't redefine a type alias:

```typescript
interface IUser {
    name: string
}

interface IUser {
    age: number
}

let a: IUser = {
    name: 'Ashley',
    age: 30
}
```

If the interface declares generics, those generics have to be declared the exact same way for two interfaces to be mergeable-down to the generic's name.

5. Prefer interface while creating public package, so that consumers can extend the interface themselves.