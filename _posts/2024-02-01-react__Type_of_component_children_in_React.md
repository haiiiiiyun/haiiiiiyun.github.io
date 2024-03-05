---
title: Type of component children in React
date: 2024-02-01
tags: react types
categoris: Programming
---

There are two common types to describe the children of a component.

1. `React.ReactNode`: it is a union of all the possible types that can be passed as children in JSX, it is a very broad definition of children:

```typescript
interface ModalRendererProps {
  title: string;
  children: React.ReactNode;
}
```

2. `React.ReactElement`, same as `React.JSX.Element`: it is only JSX elements and not Javascript primitives like strings or numbers:

```typescript
interface ModalRendererProps {
  title: string;
  children: React.ReactElement;
}
```

See https://react.dev/learn/typescript