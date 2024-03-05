---
title: Create React Router error page
date: 2024-01-23
tags: react router
categoris: Programming
---

An `element` prop can be used on a route to define a regular page, while the `errorElement` prop can be used to override the standard error page:

```typescript
const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {path: 'products', element: <ProductsPage />},
            {path: 'products/:id', element: <ProductPage />}
        ]
    },
]);
```

## Access error info in error page

Similar to `useParams()` hook,  React Router providers us with `useRouteError` hook, which can be used to get error info:

The hook returns a value of type `unknown`, we can extract the `statusText` prop from it:

```typescript
import { useRouteError } from "react-router-dom";
import { Header } from "../Header";

function isError(error: any): error is { statusText: string } {
    return 'statusText' in error;
}

export function ErrorPage() {
    const error = useRouteError();
    console.log('error=', error);
    return (
        <>
            <Header />
            <div className="text-center p-5 text-xl">
                <h1 className="text-xl text-slate-900">
                    Sorry, an error has occurred
                </h1>
                {isError(error) && (
                    <p className="text-base text-slate-700">
                        {error.statusText}
                    </p>
                )}
            </div>
        </>
    );
}
```