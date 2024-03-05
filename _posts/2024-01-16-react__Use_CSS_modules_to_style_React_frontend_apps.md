---
title: Use CSS modules to style React frontend apps
date: 2024-01-16
tags: react styles css-modules
categoris: Programming
---

1. CSS modules allow CSS class names to be automatically scoped to a React component. This prevent styles from different React components from clashing.
2. CSS modules isn't a standard browser feature, [CSS modules](https://github.com/css-modules/css-modules) is an open source library available on GitHub, which can be added to the webpack process to facilitate the automatic scoping of CSS class names.
3. CSS modules are pre-installed and pre-configured in projects created with create-react-app.
4. Similar to plain CSS, redundant CSS classes are not pruned from the production CSS bundle.

## CSS module is a CSS file with extension .module.css

This special extension allows webpack to differentiate a CSS module from a plain CSS file so that it can be processed differently.

## usage of CSS module

```javascript
import styles from './styles.module.css';

let span = <span className={styles.headerText}>text</span>;
```

The CSS class name information is imported into a variable, this variable is an object containing property names corresponding to the CSS class names. Each class name property contains a value of a scoped class name to be used on a React component. Here is an example of the mapping object that has been imported into a component called MyComponent:

```json
{
  container: "MyComponent_container__M7tzC",
  error: "MyComponent_error__vj8Oj"
}
```

The scope CSS class name is:  component filename + original CSS class name + random string.

### Camel case CSS class names

Change the CSS class names to camel case rather than kebab case. This will allow use to reference the scoped CSS class names more easily, for example `styles.headerText` rather than `styles["header-text"]`.
```