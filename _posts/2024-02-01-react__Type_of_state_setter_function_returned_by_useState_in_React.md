---
title: Type of state setter function returned by useState in React
date: 2024-02-01
tags: react types
categoris: Programming
---

When passing down the state setter function to a child component, we should set the type of function as:

```typescript
type Props = {
    setState: React.Dispatch<React.SetStateAction<number>>;
}
```

Here `number` is an example type of the state.