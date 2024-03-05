---
title: Nested routes and Outlet in React Router
date: 2024-01-18
tags: react router
categoris: Programming
---

When a page is composed of  segments, we can use nested routes. Parent component can render template contents, such as navbar, footer, and specify a place called `<Outlet />` to render nested/child component.

```typescript
// Routes.ts
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ProductsPage } from "./pages/ProductsPage";
import App from "./App";

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        children: [
            {path: 'products', element: <ProductsPage />}
        ]
    },
]);

export function Routes() {
    return <RouterProvider router={router} />;
}
```

```typescript
// Parent component App.tsx
import { Outlet } from "react-router-dom";
import { Header } from "./Header";

function App() {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}

export default App;
```