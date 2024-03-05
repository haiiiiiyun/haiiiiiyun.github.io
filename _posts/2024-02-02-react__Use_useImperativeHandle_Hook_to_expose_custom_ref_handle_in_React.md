---
title: Use useImperativeHandle Hook to expose custom ref handle in React
date: 2024-02-02
tags: react hooks
categoris: Programming
---

## forwardRef exposes DOM nodes to parent component

By default, components don't expose their DOM nodes to parent components. We have to opt in with `forwardRef` to expose, see [[Types for forwardRef in React]].

## forwardRef exposes an object instead of DOM node to parent  component

Use `forwardRef` together with `useImperativeHandle` hook, we can expose custom ref handle. In the following example, the `Ref` type is an object type instead of a HTMLElement type:

```typescript
// Countdown.tsx

// Define the handle types which will be passed to the forwardRef
export type CountdownHandle = {
  start: () => void;
};

type CountdownProps = {};

const Countdown = forwardRef<CountdownHandle, CountdownProps>((props, ref) => {
  useImperativeHandle(ref, () => ({
    // start() has type inference here
    start() {
      alert("Start");
    },
  }));

  return <div>Countdown</div>;
});
```

By binding `ref` prop to the component, the `ref.current` is assigned to the object created by the `useImperativeHandle` hook:

```typescript
// The component uses the Countdown component

import Countdown, { CountdownHandle } from "./Countdown.tsx";

function App() {
  const countdownEl = useRef<CountdownHandle>(null);

  useEffect(() => {
    if (countdownEl.current) {
      // start() has type inference here as well
      countdownEl.current.start();
    }
  }, []);

  return <Countdown ref={countdownEl} />;
}
```