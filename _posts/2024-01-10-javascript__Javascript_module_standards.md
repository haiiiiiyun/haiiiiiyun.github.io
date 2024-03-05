---
title: Javascript module standards
date: 2024-01-10
tags: javascript
categoris: Programming
---

1. around 2009: CommonJS module standard pushed by NodeJS

```javascript
var emailList = required('emailListModule');
var emailComposer = required('emailComposerModule');

module.exports.renderBase = function(){}
```

2. around 2009: on the web the AMD module standard pushed by Dojo and RequireJS

```javascript
define('emailBaseModule',
	  ['require', 'exports', 'emailListModule', 'emailComposerModule'],
	  function(require, exports, emailListModule, emailComposerModule){
		  exports.rnderBase = function(){}
	  }
)
```

3. in 2011, Browserify makes CommonJS available on the frontend. CommonJS became the de facto standard for module bundling and import/export syntax
4. ES2015 introduced a new standard for imports and exports that had a clean syntax and was statically analyzable:

```javascript
import emailList from 'emailListModule'
import emailComposer from 'emailComposerModule'
export function renderBase() {}
```

This is the standard we use today.