---
title: Define an abstract class in Typescript
date: 2023-12-27
tags: typescript classes
categoris: Programming
---

```typescript
abstract class Piece {
    constructor(public color: string, rank: string){}

    abstract canMoveTo(position: number): boolean
}

class KingPiece extends Piece {
    canMoveTo(position: number) {
        return true;
    }
}

const p = new Piece('red', '1'); // Cannot create an instance of an abstract class.
```

We can't instantiate an abstract class directly, we can only `extends` an abstract class.