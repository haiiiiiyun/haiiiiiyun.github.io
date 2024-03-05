---
title: Use this as a  return type in Typescript
date: 2023-12-27
tags: typescript classes types
categoris: Programming
---

Just like we can use `this` as a value, we can also use it as a `type`. `this` type can be useful for annotating methods' return types in classes:

```typescript
class MySet {
    constructor(public array: number[]){}
    add(n: number): this {
        this.array.push(n);
        return this;
    }
}

let s = new MySet([1, 2]);
s.add(3);
console.log(s.array); // [1, 2, 3]
```