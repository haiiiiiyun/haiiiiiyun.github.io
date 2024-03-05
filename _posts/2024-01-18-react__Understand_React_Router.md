---
title: Understand React Router
date: 2024-01-18
tags: react router
categoris: Programming
---

A router in [React Router](https://reactrouter.com/en/main/routers/create-browser-router) is a component that tracks the browser's URL and performs navigation.

Routes are defined using `createBrowserRouter`, each route has a path and a component to render:

The router returned from `createBrowserRouter` is passed into a `RouterProvider` component, which should be placed high up in the component tree:

```typescript
// src/Routes.ts
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ProductsPage } from "./pages/ProductsPage";

const router = createBrowserRouter([
    {path: 'products', element: <ProductsPage />}
])

export function Routes() {
    return <RouterProvider router={router} />;
}
```

```typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Routes } from './Routes';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Routes />
  </React.StrictMode>
);

reportWebVitals();
```