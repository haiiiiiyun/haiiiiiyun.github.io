---
title: Avoid using enum in Typescript
date: 2023-12-21
tags: typescript types
categoris: Programming
---

## enums are special maps

Enums are unordered data structures that map keys to values:
	1. map from strings to strings
	2. map from strings to numbers

```
enum Lang {
	English, // same as English = 0,
	Chinese, // same as Chinese = 1,
	Spanish = 500
}

let myFirstLang = Lang.English; //dot notation
let mySecondLang = Lang['Chinese']; // bracket notation
```

By convention, enum names are uppercase and singular. Their keys are also uppercase.

## values of enum member

Typescript will automatically infer a number as the value for each member of enum(starting at 0), but we can also set values explicitly, even mix with string and number values:

```typescript
enum Language {
    English = 1,
    Spanish = 20,
    Russian // Typescript infers 21
};

console.log('English value=', Language.English); // English value=1
console.log('Russian value=', Language.Russian); // Russian value=21
```

## enums are special maps, with both key -> value lookup and reverse value -> key lookup

```typescript
enum Language {
	English,
	Spanish,
	Russian
}
```

will be compiled to 

```javascript
"use strict";
var Language;
(function (Language) {
  Language[Language["English"] = 0] = "English";
  Language[Language["Spanish"] = 1] = "Spanish";
  Language[Language["Russian"] = 2] = "Russian";
 })(Language || (Language = {}));
```

and will create a dict:

```javascript
var Language = {
    "0": "English",
    "1": "Spanish",
    "2": "Russian",
    "English": 0,
    "Spanish": 1,
    "Russian": 2
}
```

**Typescript allows us to access not-existing element by index, this is unsafe**

```typescript
let c = Language[6]; // undefined
```

## const enum member can only be accessed using key.

```typescript
const enum Language {
    English,
    Spanish,
    Russian
};

let a = Language.English;
let b = Language[0]; // A const enum member can only be accessed using a string literal.
```

A `const enum` behaves a lot like a regular JS object. It also doesn't generate any Javascript code by default, and instead inlines the enum member's value wherever it's used.