---
title: Use react-error-boundary package with TS support built-in for function components in React
date: 2024-02-02
tags: react errors
categoris: Programming
---

[React-error-boundary](https://github.com/bvaughn/react-error-boundary)- is a lightweight package ready to use with TS support built-in. This approach also lets you avoid class components that are not that popular anymore.

```typescript
import { ErrorBoundary } from "react-error-boundary";

<ErrorBoundary fallback={<div>Something went wrong</div>}>
  <ExampleApplication />
</ErrorBoundary>
```