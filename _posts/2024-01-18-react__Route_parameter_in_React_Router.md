---
title: Route parameter in React Router
date: 2024-01-18
tags: react router
categoris: Programming
---

A route parameter is a varying segment in a path defined using a colon followed by the parameter name, for example `{path: 'products/:id', element: <ProductPage />}`.

Route parameters can be accessed using React Router's `useParams` hook:

```typescript
import { useParams } from "react-router-dom";
import { products } from "../data/products";

type Params = {
    id: string;
};

export function ProductPage() {
    const { id } = useParams<Params>();
	// ...
}
```