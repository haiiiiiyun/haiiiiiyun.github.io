---
title: Use SVGs in react frontend apps
date: 2024-01-16
tags: react svgs
categoris: Programming
---

## Webpack needs to be configured to bundle SVG files and create-react-app does this configuration for us

## The default import for an SVG file is the path to the SVG, which can be used in an `img` element

```typescript
import logo from './logo.svg';

function App(){
	return <img src={logo} className="App-logo" alt="logo" />
}
```

## A named import called ReactComponent can be used to reference the SVG as a React component in JSX

```typescript
import { ReactComponent as InfoIcon } from './info.svg';

let icon = <InfoIcon className="fill-teal-900 w-5 h-5" />;
```