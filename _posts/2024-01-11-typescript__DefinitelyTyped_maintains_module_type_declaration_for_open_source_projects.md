---
title: DefinitelyTyped maintains module type declaration for open source projects
date: 2024-01-11
tags: typescript types javascript
categoris: Programming
---

[DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) is a community-maintained, centralized repository for ambient module declarations for open source projects.

To check if the package you installed has type declarations available on DefinitelyTypes, either search on [TypeSearch](https://microsoft.github.io/TypeSearch/) or just try installing the declarations. All DefinitelyTyped type declarations are published to NPM under the `@types` scope:

```bash
$ npm install lodash --save
$ npm install @types/lodash --save-dev
```