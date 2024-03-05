---
title: Optional and default parameters in Typescript
date: 2023-12-21
tags: typescript functions
categoris: Programming
---

## optional parameter

Annotate optional parameter with `?`,  optional parameters have to be at the end of the list of parameters:

```typescript
function log(message: string, userId?: string){}
```

## default parameter

Default parameters don't have to be at the end of the list of parameters. Typescript can infer the parameter type from its default value, it's not necessary to add explicit type annotations to the default parameters:

```typescript
function log(message: string, userId="Not signed in"){}
```