---
title: Use Mapped types to create super index signatures in Typescript
date: 2024-01-03
tags: typescript types
categoris: Programming
---

Mapped types are a language feature unique to TS, mapped types have their own special syntax, and like index signatures, we can have at most one mapped type per object.

```typescript
type MyMappedType = {
	[Key in UnionType]: ValueType
}
```

Mapped type is a way to map over an object's key and value types. TS uses mapped types to implement its built-in `Record` type, also see [[Use Record type to create a map that enforces a specific set of keys in Typescript]]:

```typescript
type Record<K extends any, T> = {
	[P in K]: T
}
```

## Utilities of Mapped types and the built-in mapped types

```typescript
type Account = {
    id: number,
    isEmployee: boolean,
    notes: string[]
};

// Make all fields optional
type OptionalAccount = {
    [Key in keyof Account]?: Account[Key]
}
//// Same as the built-in Partial<ObjectType> type
type OptionalAccount2 = Partial<Account>;

// Make all fields nullable
type NullableAccont = {
    [Key in keyof Account]: Account[Key] | null
}

// Make all fields read-only
type ReadonlyAccount = {
    readonly [Key in keyof Account]: Account[Key]
}
//// Same as the built-in Readonly<ObjectType> type
type ReadonlyAccount2 = Readonly<Account>;

// Make all fields writable again(equivalent to Account)
type Account2 = {
    -readonly [Key in keyof ReadonlyAccount]: ReadonlyAccount[Key]
}

// Make all fields required again(equivalent to Account)
type Account3 = {
    [Key in keyof OptionalAccount]-?: OptionalAccount[Key]
}
//// Make as the built-in Requied<ObjectType> type
type RequiedAccount = Required<Account>;
```