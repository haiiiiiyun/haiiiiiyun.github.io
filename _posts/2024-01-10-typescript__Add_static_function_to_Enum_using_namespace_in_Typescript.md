---
title: Add static function to Enum using namespace in Typescript
date: 2024-01-10
tags: typescript namespaces
categoris: Programming
---

We can use the declaration `enum + namespace` merging to add static methods to an enum:

```typescript
enum Weekday {
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday
};

namespace Weekday {
    export function isWeekend(day: Weekday): boolean {
        if (day === Weekday.Saturday || day === Weekday.Sunday) return true;
        return false;
    }
}

const mon = Weekday.Monday;
const sat = Weekday.Saturday;
console.log('Mon is weekend:', Weekday.isWeekend(mon)); // false
console.log('Sat is weekend:', Weekday.isWeekend(sat)); // true
```

See https://basarat.gitbook.io/typescript/type-system/enums#enum-with-static-functions