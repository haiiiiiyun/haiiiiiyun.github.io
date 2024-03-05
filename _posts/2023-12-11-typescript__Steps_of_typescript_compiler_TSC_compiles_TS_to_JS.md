---
title: Steps of typescript compiler TSC compiles TS to JS
date: 2023-12-11
tags: typescript
categoris: Programming
---

1. TypeScript source -> TypeScript AST
2. AST is checked by typechecker
3. TypeScript AST -> JavaScript source

when TSC compiles our code from TypeScript to JavaScript, it won't look at the types. The types are only used for typechecking, and won't affect our program's generated output.