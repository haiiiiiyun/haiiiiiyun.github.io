---
title: Use search parameters in React Router
date: 2024-01-24
tags: react router
categoris: Programming
---

**Search parameters** are part of a URL that comes after the `?` character and separated by the `&` character. Search parameters are sometimes referred to as **query parameters**. In the following URL, `type` and `when` are search parameters: https://somewhere.com/?type=sometype&when=recent.

React Router has a hook that returns functions for getting and setting search parameters called **useSearchParams**:

```typescript
const [searchParams, setSearchParams] = useSearchParams();
const type = searchParams.get('type');
setSearchParams({ type: 'sometype', when: 'recent' });
```

searchParams is a JS **URLSearchParams** object.

## Create a useQuery hook for getting query parameter

```typescript
import { useSearchParams } from "react-router-dom";

export function useQuery(param: string|undefined) {
    const [searchParams] = useSearchParams();
    return param ? searchParams.get(param) || '' : Object.fromEntries(searchParams);
}

const { type, when } = useQuery();
```