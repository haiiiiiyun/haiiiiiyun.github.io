---
title: Typescript has separate namespaces for values and for types and the companion object pattern
date: 2024-01-03
tags: typescript types
categoris: Programming
---

We can create a type and a value with the same name:

```typescript
type Shoe = {
    purpose: string
};

let Shoe = {
    create(): Shoe { return new Shoe}
}
```

Also see an example in [[Implement a factory pattern in Typescript]].

## Companion object pattern

The companion object pattern is a way to pair together objects and classes that share the same name. 

This pattern has a few nice properties. It let us group type and value information that's semantically part of a single name together:

```typescript
type Currency = {
    unit: 'EUR' | 'GBP' | 'JPY' | 'USD',
    value: number
};

let Currency = {
    DEFAULT: 'USD',
    from(value: number, unit = Currency.DEFAULT): Currency {
        return {unit, value};
    }
}
```

It also lets import both at once:

```typescript
import {Currency} from './Currency';

let amountDue: Currency = {
    unit: 'JPY',
    value: 83733.10
};

let otherAmountDue = Currency.from(330, 'EUR');
```
