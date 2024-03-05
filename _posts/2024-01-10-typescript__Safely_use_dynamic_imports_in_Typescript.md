---
title: Safely use dynamic imports in Typescript
date: 2024-01-10
tags: typescript modules
categoris: Programming
---

We can use `import` either as a statement to statically pull in code, or as a function that returns a `Promise` for our module:

`let locale = await import('locale_us-en')`

While we can pass an arbitrary expression that evaluates to a string to `import`, we lose type safety when we do. To safely use dynamic imports, be sure to either:

1. Pass a string literal directly to `import`, without assigning the string to a variable first.
2. Pass an expression to `import` and manually annotate the module's signature:

```typescript
import {locale} from './locales/locale-us';

async function main() {
	let userLocale = await getUserLocale();
	let path = `./locales/locale-${userLocale}`;
	let localeUS: typeof locale = await import(path);
}
```