---
title: Types of DOM events in React
date: 2024-02-01
tags: react types
categoris: Programming
---

When we want to extract a function to be passed to an event handler, we will need to explicitly set the type of event, such as `React.MouseEvent`, `React.ChangeEvent`, `React.FormEvent`, .etc. The generic event is `React.SyntheticEvent`.

```typescript
import { useState } from 'react';

export default function Form() {
  const [value, setValue] = useState("Change me");

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setValue(event.currentTarget.value);
  }

  return (
    <>
      <input value={value} onChange={handleChange} />
      <p>Value: {value}</p>
    </>
  );
}
```

The full list can be found on [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/b580df54c0819ec9df62b0835a315dd48b8594a9/types/react/index.d.ts#L1247C1-L1373) which is based on the [most popular events from the DOM](https://developer.mozilla.org/en-US/docs/Web/Events)

See https://react.dev/learn/typescript