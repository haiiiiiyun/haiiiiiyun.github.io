---
title: Types for forwardRef in React
date: 2024-02-02
tags: react types
categoris: Programming
---

`forwardRef` is a generic function with generic types `Ref` and `Props`,  the `Ref` type should be a HTMLElement, and the `Props` type is for the component:

```typescript
import { forwardRef, ReactNode } from "react";

interface Props {
  children?: ReactNode;
  type: "submit" | "button";
}
export type Ref = HTMLButtonElement;

export const FancyButton = forwardRef<Ref, Props>((props, ref) => (
  <button ref={ref} className="MyClassName" type={props.type}>
    {props.children}
  </button>
));
```

Also see [[type for useRef Hook in React]] and [[Use useImperativeHandle Hook to expose custom ref handle in React]].