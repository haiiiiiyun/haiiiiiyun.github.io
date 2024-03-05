---
title: Generic type aliases in Typescript
date: 2023-12-27
tags: typescript types
categoris: Programming
---

We can create a generic type alias similar to create a regular type alias:

```typescript
type MyEvent<T> = {
    target: T,
    type: string
};
```

When we use the generic type alias, we have to  explicitly bind its type parameters , TS won't infer them for us:

```typescript
type ButtonEvent = MyEvent<HTMLButtonElement>;

let myEvent: MyEvent<HTMLButtonElement | null> = {
    target: document.querySelector('#myButton'),
    type: 'click'
}
```


We can use the generic type alias to build another type:

```typescript
type TimedEvent<T> = {
    target: MyEvent<T>,
    from: Date,
    to: Date
}
```

We can use the generic type alias in a function's signature, when TS binds(infers) a type to T, it'll also bind it to the generic type:

```typescript
function triggerEvent<T>(event: MyEvent<T>): void {
    // ...
}

triggerEvent({
    target: document.querySelector('#myButton'),
    type: 'mouseover'
});
```