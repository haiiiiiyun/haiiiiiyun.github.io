---
title: Handle errors with Option type in Typescript
date: 2024-01-08
tags: typescript types todo
categoris: Programming
---

Instead of returning null, throwing exceptions, returning exceptions for representing and handling errors, we can describe exceptions using special-purpose data types.

This data type gives us the ability to chain operations over possibly errored computations. Three of the most popular options are the `Option`, `Try` and `Either` types.

## Idea of Option type

The idea is that instead of returning a value, we return a `container` that may or may not have a value in it. The container has a few methods defined on it, which lets us chain operations even though there may not actually be a value inside.

```typescript
function ask() {
    let result = prompt('When is your birthday');
    if (result === null) return [];
    return [result];
}

function parse(birthday: string): Date[] {
    let date = new Date(birthday);
    if (!isValid(date)) {
        return [];
    }
    return [date];
}

// Flattens an array of arrays into an array
function flatten<T>(array: T[][]): T[] {
    return Array.prototype.concat.apply([], array);
}

flatten(
    ask()
    .map(parse))
    .map(date => date.toISOString())
    .forEach(date => console.info('Date is', date));
```

see [[Flatten an array of arrays into an array in Typescript]].

## Implement a Option type

We'll be able to use the data type like this:

```typescript
ask()
	.flatMap(parse)
	.flatMap(date => new Some(date.toISOString()))
	.flatMap(date => new Some('Date is ' + date))
	.getOrElse('Error parsing date for some reason')
```

### Option is an interface that's implemented by two classes

todo: 

```typescript

```