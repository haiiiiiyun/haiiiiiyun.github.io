---
title: Use EventHander functions from React types to provide type for event handler as defining useCallback
date: 2024-02-01
tags: react types
categoris: Programming
---

When working in Typescript strict mode `useCallback` requires adding types for the parameters in the callback.

We can use `*EventHandler` functions from the React types to provide the type for the event handler at the same time as defining the callback:

```typescript
import { useState, useCallback } from 'react';

export default function Form() {
  const [value, setValue] = useState("change me");

  const handleChange = useCallback<React.ChangeEventHandler<HTMLInputElement>>((event)=>{
    setValue(event.currentTarget.value);
  }, [setValue]);

  return ...
}
```

See https://react.dev/learn/typescript