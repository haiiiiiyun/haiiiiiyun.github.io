---
title: Simulate nominal types in Typescript
date: 2024-01-08
tags: typescript types
categoris: Programming
---

Typescript's type system is structural, not nominal. In the example below, we can pass in any string value to the function. Since UserID is just an alias for string, this approach does little to prevent bugs. An engineer might accidentally pass in the wrong type of ID:

```typescript
type CompanyID = string;
type UserID = string;
type ID = CompanyID | UserID;

function queryForUser(id: UserID){};

let id: CompanyID = 'bbaa';
queryForUser(id); // OK !!!
```

This is where nominal types come in handy. 

## We can simulate them with a technique called **type branding**

Branded types can make our program significantly safer. Start by creating a synthetic *type brand* for each of our nominal types. An intersection of `string` and `{readonly brand: unique symbol}` is impossible to naturally construct , only way to create a value of that type is with an assertion.  We used `unique symbol` as the `brand` because it's one of two truly nominal kinds of types in TS(the other is enum).


```typescript
type CompanyID = string & { readonly brand: unique symbol};
type OrderID = string & { readonly brand: unique symbol};
type UserID = string & { readonly brand: unique symbol};
type ID = CompanyID | OrderID | UserID;

function CompanyID(id: string){
    return id as CompanyID;
}

function OrderID(id: string){
    return id as OrderID;
}

function UserID(id: string){
    return id as UserID;
}

function queryForUser(id: UserID){}

let companyId = CompanyID('cid');
let userId = UserID('uid');
queryForUser(userId); // ok
queryForUser(companyId); // Argument of type 'CompanyID' is not assignable to parameter of type 'UserID'.
```