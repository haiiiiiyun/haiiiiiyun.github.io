---
title: Simulate final classes that are non-extensible in Typescript
date: 2023-12-29
tags: typescript classes
categoris: Programming
---

`final` is the keyword some languages use to mark a class as non-extensible, or a method as non-overridable.

To simulate `final` classes in TS, we can take advantage of private constructors, which prevents us from extending the class as well as from directly instantiating it.

We then need to add a `static` create method for creating new instances:

```typescript
class MessageQueue {
    private constructor(private messages: string[]){}
    static create(messages: string[]) {
        return new MessageQueue(messages);
    }
}

MessageQueue.create(['a', 'b']);

class BadQueue extends MessageQueue{} // Cannot extend a class 'MessageQueue'. Class constructor is marked as private.

new MessageQueue(['a', 'b']); // Constructor of class 'MessageQueue' is private and only accessible within the class declaration.
```