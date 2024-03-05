---
title: Create a Typescript project from scratch
date: 2023-12-12
tags: typescript node npm
categoris: Programming
---


Install nvm and node, see [[Manage node versions with nvm]].

Set npm source, see [[Config mirrors for yarn and npm]].

## Create and init a project

```bash
$ mkdir typescript-playground
$ cd typescript-playground

# Initialize a new NPM project
$ npm init

# Install TSC, TSLint and type declarations for NodeJS
npm install --save-dev typescript tslint @types/node
```

## tsconfig.json file

Every Typescript project should include a file called `tsconfig.json` in its root directory. This file is where Typescript projects define things like which files should be compiled, which directory to compile them to, and which version of Javascript to emit.

Create file `tsconfig.json` with the following contents:

```json
{
    "compilerOptions": {
        "lib": ["es2015"],
        "module": "commonjs",
        "outDir": "dist",
        "sourceMap": true,
        "strict": true,
        "target": "es2015"
    },
    "include": [
        "src"
    ]
}
```

We should add `"dom"` to `lib` when writing Typescript for the browser.

## tslint.json

Our project should also have a `tslint.json` file containing TSLint configuration, codifying whatever stylistic conventions you want for your code(tabs versus spaces, etc.).

Generate `tslint.json` with  a default TSLint configuration:

```bash
$ ./node_modules/.bin/tslint --init
```

```json
{
    "defaultSeverity": "error",
    "extends": [
        "tslint:recommended"
    ],
    "jsRules": {},
    "rules": {},
    "rulesDirectory": []
}
```

We can then add overrides to this to conform with our own coding style.  See [full list of tslint rules](https://palantir.github.io/tslint/rules/).

## src/index.ts

Place our Typescript files under `src`, for example:

```typescript
console.log("Hello Typescript")
```

## Project folder structure

```bash
$ tree -L 1
.
├── node_modules/
├── package.json
├── package-lock.json
├── src/
├── tsconfig.json
└── tslint.json

2 directories, 4 files
```

## Compile and run

```bash
# compile Typescript with TSC
$ ./node_modules/.bin/tsc

# Run code with node
$ node ./dist/index.js
```