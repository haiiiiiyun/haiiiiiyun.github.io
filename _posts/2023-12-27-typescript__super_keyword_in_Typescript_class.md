---
title: super keyword in Typescript class
date: 2023-12-27
tags: typescript classes
categoris: Programming
---

`super` keyword is used to call methods or access properties of a parent class.

1. The `super(...args)` expression is valid only in class constructors.
2. The `super.prop` and `super[expr]` expressions are valid in any method definition in both classes and object literals.

```typescript
class Foo {
    constructor(public name: string){}

    getNameSeperator() {
        return '-';
    }
}

class FooBar extends Foo {
    constructor(public name: string, public index: number){
        super(name);
    }

    getFullName(){
        return this.name + super.getNameSeperator() + this.index;
    }
}

let fb = new FooBar('foo', 1);
console.log(fb.name); // foo
console.log(fb.getFullName()); // foo-1
```