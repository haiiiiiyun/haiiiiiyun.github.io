---
title: Use plain CSS to style React frontend apps
date: 2024-01-16
tags: react styles css
categoris: Programming
---

## Reference CSS

create-react-app has already enabled the use of plain CSS in the project.

```javascript
import './App.css';

function App() {
	return (
		<div className="App"></div>
	);
}
```

The `CSS import` statement is a webpack feature. As webpack processes all the files, it will include all the imported CSS in the bundle.

## CSS clashes

Plain CSS classes are scoped to the whole app and not just the file it is imported into. All the styles in an imported CSS file are applied to the app -- there is no scoping or removing redundant styles. 

This means that CSS classes can clash if they have the same name.

A solution to CSS clashes is to carefully name them using [[CSS architecture and BEM CSS Class naming]].