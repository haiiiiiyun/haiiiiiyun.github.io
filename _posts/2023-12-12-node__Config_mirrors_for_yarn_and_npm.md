---
title: Config mirrors for yarn and npm
date: 2023-12-12
tags: node yarn npm
categoris: Programming
---

## Yarn

```bash
yarn config get registry
yarn config set registry https://registry.npmmirror.com
yarn config delete registry
```

## NPM

```bash
npm config get registry
npm config set registry https://registry.npmmirror.com
npm config delete registry
```

See https://www.cnblogs.com/develon/p/13814675.html