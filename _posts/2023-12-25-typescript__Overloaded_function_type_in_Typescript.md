---
title: Overloaded function type in Typescript
date: 2023-12-25
tags: typescript functions types
categoris: Programming
---

`type Fn = (...) => ...` is a **shorthand call signature**, we can use the **full call signature**, for example:

```typescript
// shorthand call signature
type Log = (message: string, userId?: string) => void;

// full call signature
type Log = {
    (message: string, userId?: string): void
};
```

## declare overloaded signatures with full call signature

A overloaded function is a function that has multiple call signatures.

```typescript
type Reservation = number;

type Reserve = {
    (from: Date, to: Date, destination: string): Reservation,
    (from: Date, destination: string): Reservation, // one-way trip
}
```

From a caller's point of view, this function type is the union of those overloaded signatures. But from implementation's point of view, there needs to be a single, combined type that can actually be implemented. We need to **manually declare this combined call signature when implementing**:

```typescript
let reserve: Reserve = (from: Date, toOrDestination: Date | string, destination?: string) => {
    if (toOrDestination instanceof Date && destination != undefined){
        // Book a one-way trip
    } else if (typeof toOrDestination === 'string') {
        // Book a round trip
    }
    return 0;
}
```

Overloads come up naturally in browser DOM APIs, for example the `CreateElement` API:

```typescript
type CreateElement = {
  (tag: 'a'): HTMLAnchorElement,
  (tag: 'canvas'): HTMLCanvasElement,
  (tag: 'table'): HTMLTableElement,
  (tag: string): HTMLElement
};

let createElement: CreateElement = (tag: string): HTMLElement => {}
```

## declare function property with full call signature

Since function is just a callable object, we can assign properties to them to do things like:

```typescript
type WarnUser = {
    (warning: string): void,
    wasCalled: boolean
}

let warnUser: WarnUser = (warning: string) => {
    if (warnUser.wasCalled) return;
    warnUser.wasCalled = true;
    alert(warning);
};
warnUser.wasCalled = false;
```