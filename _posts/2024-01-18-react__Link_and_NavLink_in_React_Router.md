---
title: Link and NavLink in React Router
date: 2024-01-18
tags: react router
categoris: Programming
---

React Router comes with components `Link` and `NavLink`, they both are rendered as HTML anchor element.

`NavLink` is like `Link` but allows it to be styled differently when active, the `className` on `NavLink` can be a function with parameters `{ isActive }`:

```typescript
import { Link, NavLink } from "react-router-dom";

export function Header() {
    return (
      <nav>
        <Link to="products" className="text-white no-underline p-1">Products</Link>
         <NavLink to="/" className={({ isActive }) => `text-white no-underline p-1 pb-0.5 border-solid border-b-2 ${isActive ? "border-white" : "border-transparent"}`}>home</NavLink>
      </nav>
    );
}
```