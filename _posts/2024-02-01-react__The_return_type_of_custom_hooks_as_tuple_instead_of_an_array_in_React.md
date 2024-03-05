---
title: The return type of custom hooks as tuple instead of an array in React
date: 2024-02-01
tags: react types
categoris: Programming
---

If we are returning an array in Custom Hook, we'll want to avoid type inference as TS will infer a union type(when we actually want different types in each position of the array), use `const` assertions:

```typescript
import { useState } from "react";

export function useLoading() {
  const [isLoading, setState] = useState(false);
  const load = (aPromise: Promise<any>) => {
    setState(true);
    return aPromise.finally(() => setState(false));
  };
  return [isLoading, load] as const; // infers [boolean, typeof load] instead of (boolean | typeof load)[]
}
```