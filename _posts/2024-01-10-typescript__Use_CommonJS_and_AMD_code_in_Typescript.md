---
title: Use CommonJS and AMD code in Typescript
date: 2024-01-10
tags: typescript modules
categoris: Programming
---

When consuming a JS module that used the CommonJS or AMD standard, we can simply import names from it, just like for ES2015 modules:

```typescript
import {something} from './a/legacy/commonjs/module';
```

## use default export

By default, CommonJS default exports don't interoperate with ES2015 default imports; to use a default export, we have to use a wild import:

```typescript
import * as fs from 'fs';
fs.readFile('some/file.txt');
```

To interoperate more smoothly, set `{"esModuleInterop": true}` in `tsconfig.json`'s `compilerOptions`. Now we can leave out the wildcard:

```typescript
import fs from 'fs';
fs.readFile('some/file.txt');
```