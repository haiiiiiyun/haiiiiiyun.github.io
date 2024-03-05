---
title: Implement a factory pattern in Typescript
date: 2023-12-29
tags: typescript classes
categoris: Programming
---

The `factory pattern` is a way to create objects of some type, leaving the decision of which concrete object to create to the specific factory that creates that object:

See [[Typescript has separate namespaces for values and for types and the companion object pattern]], we declare a type `Shoe` and a value `Shoe` with the same name:

```typescript
type Shoe = {
    purpose: string
}

class BalletFlat implements Shoe {
    purpose = 'dancing'
}

class Boot implements Shoe {
    purpose = 'woodcutting'
}

class Sneaker implements Shoe {
    purpose = 'walking'
}

let Shoe = {
    create(type: 'balletFlat' | 'boot' | 'sneaker'): Shoe {
        switch(type) {
            case 'balletFlat': return new BalletFlat;
            case 'boot': return new Boot;
            case 'sneaker': return new Sneaker;
        }
    }
}

Shoe.create('boot'); 
```