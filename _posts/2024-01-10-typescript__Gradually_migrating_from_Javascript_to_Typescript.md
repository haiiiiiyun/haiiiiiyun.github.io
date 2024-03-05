---
title: Gradually migrating from Javascript to Typescript
date: 2024-01-10
tags: typescript javascript
categoris: Programming
---

## 1. Add TSC

In `tsconfig.json`:

```json
{
	"compilerOptions": {
		"allowJs": true
	}
}
```

Now we can use TSC to compile JavaScript. TypeScript won't typecheck the existing JavaScript code, but it will transpile it.

## 2a. Enable typechecking for JavaScript(optional)

Enable this in `tsconfig.json`:

```json
{
	"compilerOptions": {
		"allowJs": true,
		"checkJS": true
	}
}
```

Now whenever TS compiles a JS file it'll do its best to infer types and typecheck as it goes.

enable `checkJS` may report too many type errors at once, we can:

1. turn `checkJS` off, and instead enable checking for an individual Javascript file at a time by add the `// @ts-check` directive (a regular comment at the top of the file).
2. keep `checkJS` on, add the `// @ts-nocheck` directive to those files that we don't want to fix now.

## 2b. Add JSDoc Annotations (optional)

JSDoc are funny looking comments above some Javascript and Typescript code with `@-annotations` like `@param`, `@returns`, and so do.  TS understands JSDoc and uses it as input to its typechecker the same way that it uses explicit type annotations in TS code:

```javascript
/**
 * @param word {string} An input string to convert
 * @returns {string} The string in PAscalCase
 */
export function toPascalCase(word){
  return ...;
}
```

## 3. Rename files to .ts

## 4. Make it strict

Fix all type-related errors and disable TSC's JS interoperability flags:

```json
{
	"compilerOptions": {
		"allowJs": false,
		"checkJS": false
	}
}
```