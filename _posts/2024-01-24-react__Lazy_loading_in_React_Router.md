---
title: Lazy loading in React Router
date: 2024-01-24
tags: react router
categoris: Programming
---

By default all React components are bundled together and loaded when the app first loads.

Lazy loading React components aren't included in the initial bundles that is loaded; instead, their Javascript is fetched and loaded when rendered.

Two steps to lazy loading React componenets:

1. the component must be dynamically imported as follows, note the lazy page must be a default export -- lazy loading doesn't work with named exports:

```typescript
const LazyPage = lazy(() => import('./LazyPage'));
```

2.  Render the lazy component inside React's `Suspense` component:

```typescript
<Route
	path="lazy"
	element={
		<Suspense fallback={<div>Loading...</div>}>
			<LazyPage />
		</Suspense>
	}
/>
```