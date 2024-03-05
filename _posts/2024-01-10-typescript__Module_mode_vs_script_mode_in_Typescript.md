---
title: Module mode vs script mode in Typescript
date: 2024-01-10
tags: typescript modules
categoris: Programming
---

Typescript parses each of our Typescript files into one of two modes:

+ module mode: the file has any imports or exports
+ script mode: the file does not use any imports or exports

We'll almost always want to stick to Module mode.

## Script mode

In script mode, any top-level variables we declare will be available to other files in the project without an explicit import, and we can safely consume global exports from third-party UMD modules without explicitly importing them first.

Use cases of script mode:

1. To quickly prototype browser code that you plan to compile to no module system at all (`{"module": "none"}`) in `tsconfig.json` and include as raw `<script />` tags in HTML file.
2. to create type declarations
