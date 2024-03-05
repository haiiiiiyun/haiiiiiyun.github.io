---
title: Type operators for Object types in Typescript
date: 2023-01-03
tags: typescript types
categoris: Programming
---

1. We can key  in to any shape(object, array) to get a new type.
Note that we have to use `[]` notation, not the `.` notation to look up property types.  To key in an array type, use `[number]`, and use `[0]` or another number literal type for tuples:

```typescript
type APIResponse = {
    user: {
        userId: string,
        friendList: {
            count: number,
            friends: {
                firstName: string,
                lastName: string
            }[]
        }
    }
};

type FriendList = APIResponse["user"]["friendList"]; // key in to shape
type Friend = FriendList["friends"][number]; // key in to an array
```

2. Use `keyof typeName` to get all of an object's keys as a union of string literal types:

```typescript
type ResponseKeys = keyof APIResponse; // 'user'
type UserKeys = keyof APIResponse["user"]; // "userId" | "friendList"
type FriendListKeys = keyof APIResponse["user"]["friendList"]; // "count" | "friends"
```

3. Combining the keying-in and keyof operators, we can implement a typesafe getter function that looks up the value at the given key in a object:

```typescript
function get<Obj extends object, K extends keyof Obj>(
    obj: Obj, key: K
): Obj[K]{
    return obj[key];
}
```

We could extend this in order to key in an object more deeply and accept up to three keys:

```typescript
type Get = {
    <Obj extends object, K1 extends keyof Obj>(
        obj: Obj, key1: K1
    ): Obj[K1],
    <Obj extends object, K1 extends keyof Obj, K2 extends keyof Obj[K1]>(
        obj: Obj, key1: K1, key2: K2
    ): Obj[K1][K2],
    <Obj extends object, K1 extends keyof Obj, K2 extends keyof Obj[K1], K3 extends keyof Obj[K1][K2]>(
        obj: Obj, key1: K1, key2: K2, key3: K3
    ): Obj[K1][K2][K3]
}
```