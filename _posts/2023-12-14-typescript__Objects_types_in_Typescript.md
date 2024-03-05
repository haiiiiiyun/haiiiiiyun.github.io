---
title: Objects types in Typescript
date: 2023-12-14
tags: typescript types
categoris: Programming
---


## let Typescript infer the object's shape for us with a object literal syntax

```typescript
let a = { b: 'x' };
a.b; // 'x'

let b = {
	c: {
		d: 'f'
	}
};
b.c.d; // 'f'
```

## explicitly describe the shape in a curly braces `{}`

```typescript
let a: {b: number} = { b: 12 };
a.b; // 12
```

## duck typing in Javascript

Javascript is generally structurally typed. When a value satisfies a shape, no matter it's a object literal or a class instance, it works.

```typescript
let c: {
    firstName: string,
    lastName: string
} = {
    firstName: 'jump',
    lastName: 'roper'
};

class Person {
    constructor(
        public firstName: string,
        public lastName: string
    ){}
}

c = new Person('matt', 'smith');
```

## add optional properties with modifier `?`

A value should match the shape exactly, missing a property or adding extra properties fails the assignment:

```typescript
let a: {b: number};
a = {}; // Property 'b' is missing in type '{}' but required in type '{ b: number; }'.
a = {b: 1, c: 2}; // Object literal may only specify known properties, and 'c' does not exist in type '{ b: number; }'.
```

We can tell Typescript that some properties are optional with `?`:

```typescript
let a: {
    b: number,
    c?: string
};

a = {b:1}; // a has a property b, but property c is optional here
a = {b:1, c: undefined}; // the optioanl property c can be set as undefined
a = {b:1, c: 'd'}; // if not undefined, the optioanl property c should be a string
```

1. a has a property b that’s a number.
2. a might have a property c that’s a string. And if c is set, it might be undefined.

Optional (?) isn’t the only modiﬁer we can use when declaring object types. We can also mark ﬁelds as read-only:

```typescript
let user: { readonly firstName: string } = { firstName: 'abby' };
```

## add more properties with index signatures

```typescript
let a: {
    b: number,
    [key: number]: boolean
};

a = {b:1, 10: true };
a = {b:1, 10: true, 20: false };
a = {b:1, 33: 'red'}; // Type 'string' is not assignable to type 'boolean'.
```

`[key: T]: U` syntax is called an index signature, and this is the way we tell Typescript that the given object might contain more keys.

The way to read it is: For this object, all keys of type T must have values of type U.

1. The index signature key's type(T) must be assignable to either `number` or `string`.
2. We can use any word for the index signature key's name--it doesn't have to be `key`

## avoid using object type

`object` is a little narrower than `any`, it only tells a value is a Javascript object and it's not a `null` or `undefined`, we can't do much with it:

```typescript
let a: object = { b: 'x' };
a.b;  // Error TS2339: Property 'b' does not exist on type 'object'.
```

## avoid using empty object type `{}`

For every type except `null` and `undefined` is assignable to an {} type, which can make it tricky to use:

```typescript
let danger: {}
danger = {}
danger = {x: 1}
danger = []
danger = 2
```