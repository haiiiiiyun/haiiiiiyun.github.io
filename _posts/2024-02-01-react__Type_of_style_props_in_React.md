---
title: Type of style props in React
date: 2024-02-01
tags: react types
categoris: Programming
---

When using inline styles in React, we can use `React.CSSProperties` to describe the object passed to the `style` prop. This style is a union of all the possible CSS properties, and is a good way to ensure we are passing valid CSS properties to the `style` prop.

```typescript
interface MyComponentProps {
  style: React.CSSProperties;
}
```

See https://react.dev/learn/typescript