---
title: Excess property checking for fresh object literal type when assign to another type
date: 2024-01-03
tags: typescript types
categoris: Programming
---

A fresh object literal type is the type TS infers from an object literal. If that object literal either uses a type assertion or is assigned to a variable, then the fresh object literal type is **widened** to a regular object type, and its freshness disappears.

When we try to assign a fresh object literal type T to another type U, and T has properties that aren't present in U, TS reports an error.

This feature is helpful. In the following example, TS helps us catch the misspell option bug, which is a common bug when working with Javascript:

```typescript
type Options = {
    baseURL: string,
    cacheSize?: number,
    tier?: 'prod' | 'dev'
};

class API {
    constructor(private options: Options){}
}

new API({
    baseURL: 'https://api.site.com',
    tierr: 'prod' // Object literal may only specify known properties, 
                  // but 'tierr' does not exist in type 'Options'. 
                  //Did you mean to write 'tier'?
})
```