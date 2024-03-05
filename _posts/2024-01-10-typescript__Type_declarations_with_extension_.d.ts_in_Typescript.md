---
title: Type declarations with extension .d.ts in Typescript
date: 2024-01-10
tags: typescript types
categoris: Programming
---

A type declaration is a file with the extension `.d.ts`. It's a way to attach TypeScript types to JavaScript code that would otherwise be untyped.

+ Type declarations can only define types, no values.
+ Type declarations can only declare that there exists a value defined somewhere in JS file using `declare` keyword

A type declaration has to live in a script-mode .ts or .d.ts file.

See [[DefinitelyTyped maintains module type declaration for open source projects]].