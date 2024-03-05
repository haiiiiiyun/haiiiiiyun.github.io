---
title: Types for class components in React
date: 2024-02-01
tags: react types
categoris: Programming
---

`React.Component` is a generic type(aka `React.Component<PropType, StateType>`), so we want to provide it with (optional) prop and state type parameters:

```typescript
type MyProps = {
  // using `interface` is also ok
  message: string;
};
type MyState = {
  count: number; // like this
};
class App extends React.Component<MyProps, MyState> {
  state: MyState = {
    // optional second annotation for better type inference
    count: 0,
  };
  render() {
    return (
      <div>
        {this.props.message} {this.state.count}
      </div>
    );
  }
}
```