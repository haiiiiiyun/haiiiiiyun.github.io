---
title: Navigate is similar to Link in React Router
date: 2024-01-25
tags: react router
categoris: Programming
---

Navigate component in React Router is similar to Link component, they both have `to` prop.  Navigate is used in the router declaration and is used to redirect to URL:

```typescript
import {createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { ContactPage, contactPageAction } from "./pages/ContactPage";

const router = createBrowserRouter([
  {path: '/', element: <Navigate to="contact" />},
  {path: '/contact', element: <ContactPage />, action: contactPageAction},
])
```