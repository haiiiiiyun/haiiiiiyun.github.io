---
title: Use Record type to create a map that enforces a specific set of keys in Typescript
date: 2024-01-03
tags: typescript types
categoris: Programming
---

With `Record` we can put some constraints on the keys and values, we get a helpful error message if some keys are missing in the properties:

```typescript
type Weekday = 'Mon' | 'Tue' | 'Wed' | 'Thu' | 'Fri';
type Day = Weekday | 'Sat' | 'Sun';

let nextDay: Record<Weekday, Day> = {
    Mon: 'Tue'
    // Type '{ Mon: "Tue"; }' is missing the following properties 
    // from type 'Record<Weekday, Day>': Tue, Wed, Thu, Fri
}
```

## Record vs regular object index signatures

With regular object index signatures, keys can only be `string | number | symbol`.

TS use mapped type to implement Record type, see [[Use Mapped types to create super index signatures in Typescript]].