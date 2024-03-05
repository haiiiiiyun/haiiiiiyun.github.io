---
title: Use CSS-in-JS to style React frontend apps
date: 2024-01-16
tags: react styles css-in-js
categoris: Programming
---

CSS-in-JS isn't a browser feature, it is a type of library, popular examples of CSS-in-JS libraries are `styled-components` and `Emotion`, they are both popular and have similar APIs.

## Use Emotion

Emotion generates styles that are scoped, similar to CSS modules. However we write the CSS in JS rather than in a CSS file, hence the name CSS-in-JS.

### Install emotion

create-react-app doesn't install and set up Emotions, so we first need to install:

```bash
npm i @emotion/react
```

### use Emotion's jsx function to transpile JSX elements

```typescript
/** @jsxImportSource @emotion/react */
import { css } from '@emotion/react';
import { useState } from 'react';
```

Add an import for the `css` prop from Emotion with a special comment at the top of the file. This special comment changes JSX elements to be transpiled using Emotion's `jsx` function instead of React's `createElement` function.  Emotion's `jsx` function adds styles to elements containing Emotion's `css` prop:

```typescript
<div
  css={css`
    display: inline-flex;
    flex-direction: column;
    text-align: left;
    padding: 10px 15px;
    border-radius: 4px;
    border: 1px solid transparent;
    color: ${type === "warning" ? "#e7650f" : "#118da0"};
    background-color: ${type === "warning"
      ? "#f3e8da"
      : "#dcf1f3"};
  `}
>
  ...
</div>
```

### Use css attribute to apply in-JS CSS

The `css` attribute isn't usually valid on JSX elements. The special comment at the top of the file allows this:  `/** @jsxImportSource @emotion/react */`.

The `css` attribute is set to a **tagged template literal**. This is a special string that gets processed by the function specified before it, which is `css` here.

The tagged template literal converts to scoped CSS class name **at runtime**. Emotion generates the styles at runtime via JS rather than at build time. There is no bundled CSS in `build` folder.