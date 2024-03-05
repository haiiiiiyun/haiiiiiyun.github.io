---
title: Collect HTML element all props with type ComponentPropsWithoutRef and use prop spreading in React
date: 2024-01-31
tags: react types
categoris: Programming
---

1. Use type `ComponentPropsWithoutRef` to reference the props of an HTML element such as `ul`. It is a generic type that takes the HTML element name as a generic parameter.
2. Add HTML element props to the component props type.
3. In component, add a *rest parameter* called `ulProps` to collect all the props from the HTML element into a single variable.

```typescript
import { ComponentPropsWithoutRef } from "react";
type Props<Data> = {
    data: Data[];
    id: keyof Data;
    primary: keyof Data;
    secondary: keyof Data;
} & ComponentPropsWithoutRef<'ul'>;

export function Checklist<Data>({
    data,
    id, 
    primary,
    secondary,
    ...ulProps
}: Props<Data>) {
    return (
        <ul className="bg-gray-300 rounded p-10" {...ulProps}>
            {data.map((item) => {
            })}
        </ul>
    );
}
```

The `id, primary, secondary` will be a union type of all the property names for each data item, we can pass in a field name of the data item when using the component:

<!-- {% raw %} -->
```typescript
function App() {
  return (
    <div className="p-10">
      <Checklist
        data={[
          {id: 1, name: 'Lucy', role: 'Manager'},
          {id: 2, name: 'Bob', role: 'Developer'},
        ]}
        id="id"
        primary="name"
        secondary="role"
        style={{
          width: '300px',
          maxHeight: '380px',
          overflowY: 'auto'
        }}
      />
    </div>
  );
}
```
<!-- {% endraw %} -->