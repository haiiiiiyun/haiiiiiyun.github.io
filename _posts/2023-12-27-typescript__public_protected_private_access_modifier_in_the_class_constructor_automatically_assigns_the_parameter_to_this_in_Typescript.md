---
title: public protected private access modifier in the class constructor automatically assigns the parameter to this in Typescript
date: 2023-12-27
tags: typescript classes
categoris: Programming
---



```typescript
class Piece {
    constructor(public color: string, rank: string){}
}

const p = new Piece('red', '1');
console.log(p.color); // red
console.log(p.rank); // Property 'rank' does not exist on type 'Piece'.
```