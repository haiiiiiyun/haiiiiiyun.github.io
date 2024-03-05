---
title: Index route in React Router
date: 2024-01-23
tags: react router
categoris: Programming
---

An **index route** can be thought of as a default child route. In React Router, if no children match a parent route, it will display an index route if one is defined. An index route has no path and instead has a `index` boolean property:

```typescript
const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {index: true, element: <HomePage />},
            {path: 'products', element: <ProductsPage />},
            {path: 'products/:id', element: <ProductPage />}
        ]
    },
]);
```