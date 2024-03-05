---
title: Implement mixin in Typescript
date: 2023-12-28
tags: typescript classes interfaces
categoris: Programming
---

Typescript and Javascript don't have `trait` or `mixin` keywords, but it's straightforward to implement them.

Mixins are a pattern that allows us to mix behaviors and properties into a class. By convention, mixins:

+ Can have state(i.e., instance properties)
+ Can only provide concrete methods
+ Can have constructors, which are called in the same order as their classes mixed in.

## A mixin is just a function that takes a class constructor and returns a class constructor

In the following example, we implement a mixin with a `debug` method.  Since this mixin requires the passing class having a `getDebugValue()` method, we constrains it with a generic type:

```typescript
type ClassConstructor<T> = new(...args: any[]) => T;

function withDebugMixin<C extends 
    ClassConstructor<{
        getDebugValue(): object
    }>
>(Klass: C) {
    return class extends Klass {
        constructor(...args: any[]) {
            super(...args);
        }
        debug() {
            let name = Klass.constructor.name;
            let value = this.getDebugValue();
            console.log(name + '(' + JSON.stringify(value) + ')');
        }
    }
}

class HardToDebugUser {
    constructor(
        private id: number,
        private firstName: string,
        private lastName: string
    ){}
    getDebugValue(){
        return {
            id: this.id,
            name: this.firstName + ' ' + this.lastName
        }
    }
}

let User = withDebugMixin(HardToDebugUser);
let user = new User(3, 'Emma', 'Gluzman');
user.debug(); // "Function({"id":3,"name":"Emma Gluzman"})" 
```

We can apply as many mixins to a class as we want to yield a class with richer and richer behavior. Mixins help encapsulate behavior and are an expressive way to specify reusable behaviors.