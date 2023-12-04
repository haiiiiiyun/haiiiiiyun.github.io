---
title: Setup Mui on Codesandbox.io
date: 2023-11-30
tags: tools frontend react mui
categoris: Programming
---

If we see an error after added the Mui as dependency:

```
Could not find dependency: '@emotion/styled' relative to '/node_modules/@mui/styled-engine/index.js'
```

Then we also need to add `@emotion/styled` and `@emotion/react` to dependencies,  see https://stackoverflow.com/questions/69223243/material-ui-v5-not-working-styled-components-and-typescript
