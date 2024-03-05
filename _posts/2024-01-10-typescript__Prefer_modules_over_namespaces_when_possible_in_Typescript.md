---
title: Prefer modules over namespaces when possible in Typescript
date: 2024-01-10
tags: typescript modules
categoris: Programming
---

## namespace

Use `namespace` keyword is another way to encapsulate code. Namespaces abstract away the nitty-gritty details of how files are laid out in the file system.

1. namespace can be augmented, support declaration merging, make it convenient to split them across files.
2. We can use aliases to shorted them for convenience using `import d = Network.DATA.d`.
3. 
```typescript
// HTTP.ts
namespace Network {
    export namespace HTTP {
        export function get<T>(url: string): Promise<T>{}
    }
}

// UDP.ts
namespace Network {
    export namespace UDP {
        export function send(url: string, packets: Buffer): Promise<void>{}
    }
    export namespace DATA {
        export let d = 3;
    }
}

Network.HTTP.get<Dog[]>('http://url.com/dogs');
Network.UDP.send('http://url.com/cats', new Buffer(123));

// MyApp.ts
import d = Network.DATA.d;
let e = d * 3;
```

### namespace compiled output

Unlike imports and exports, namespaces always compile to global variables.