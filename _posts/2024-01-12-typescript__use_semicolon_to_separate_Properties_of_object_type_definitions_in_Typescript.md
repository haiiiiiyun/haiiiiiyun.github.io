---
title: use semicolon to separate Properties of object type definitions in Typescript
date: 2024-01-12
tags: typescript types
categoris: Programming
---

Properties in the object type definitions can be separated by `;` or `,`, but using a semicolon `;` is common practice. While we use commas `,` to separate the properties of value level object:

```typescript
type Product = { name: string; unitPrice: number; };

let myProduct: Product = {name: 'Car', unitPrice: 10 };
```