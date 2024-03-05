---
title: Get code coverage for React Testing Library tests
date: 2024-01-31
tags: react tests react-testing-library
categoris: Programming
---

Run:

```
npm t -- --coverage --watchAll=false
```

A code coverage report is output in the terminal with the test results, an HTML report is also created in `coverage/lcov-report/` folder.

## Ignoring files in the coverage report

We can will files such as index.ts, types.ts from the coverage report because they don't contain any logic and create unnecessary noise.

We can configure Jest in the `package.json` file in a `jest` field, there is a `converagePathIgnorePatterns` configuration option for removing files from the coverage report:

```json
{
 ...
 "jest": {
   "coveragePathIgnorePatterns": [
     "types.ts",
     "index.ts"
   ]
 }
}
```