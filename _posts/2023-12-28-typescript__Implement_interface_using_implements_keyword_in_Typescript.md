---
title: Implement interface using implements keyword in Typescript
date: 2023-12-28
tags: typescript types interfaces classes
categoris: Programming
---

Interfaces can declare instance properties, but they can't declare visibility modifiers (private, protected, public) and they can't use `static` keyword, we can also mark instance properties as `readonly`:

```typescript
interface IAnimal {
    readonly name: string,
    eat(food: string): void,
    sleep(hours: number): void
}

interface IFeline {
    meow(): void
}

class Cat implements IAnimal, IFeline {
    name = 'Tom'
    eat(food: string) {
        console.info('Ate some', food);
    }
    sleep(hours: number) {
        console.info('Slept for', hours, 'hours');
    }
    meow() {
        console.info('Meow');
    }
}
```