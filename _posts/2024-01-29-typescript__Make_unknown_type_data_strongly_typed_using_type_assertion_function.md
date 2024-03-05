---
title: Make unknown type data strongly typed using type assertion function
date: 2024-01-29
tags: typescript types functions
categoris: Programming
---

The type assertion function is like this:

```typescript
function assertIsSomeType(data: unknown): asserts data is SomeType {
  //...
}
```

1. Notice the return type annotation `asserts data is SomeType`, this is called an **assertion signature** and specifies that the **unknown type data** parameter is of type **SomeType** if no error occurs in the function execution.
2. The input parameter is of type **unknown**.

See an example:

```typescript
import { PostData } from "./types";

export async function getPosts() {
    const response = await fetch(
        process.env.REACT_APP_API_URL!
    );
    const body = (await response.json()) as unknown;
    assertIsPosts(body);
    return body;
}

export function assertIsPosts(postsData: unknown): asserts postsData is PostData[] {
    if(!Array.isArray(postsData)){
        throw new Error("posts isn't an array");
    }
    if (postsData.length === 0){
        return;
    }
    postsData.forEach((post) => {
        if (!('id' in post)){
            throw new Error("post doesn't contain id");
        }
        if (typeof post.id !== "number"){
            throw new Error("id is not a number");
        }
    })
}
```

Also see [[Create user-defined type guard with is operator and carry type refinement over to new scopes]].