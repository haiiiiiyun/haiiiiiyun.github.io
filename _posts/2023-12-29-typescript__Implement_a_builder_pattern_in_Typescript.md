---
title: Implement a builder pattern in Typescript
date: 2023-12-29
tags: typescript classes
categoris: Programming
---

The `builder pattern` is a way to separate the construction of an object from the way that object is actually implemented.

Here's what is looks like:

```typescript
class RequestBuilder {
    private url: string | null = null;
    private method: 'get' | 'post' | null = null;
    private data: object | null = null;

    setURL(url: string): this {
        this.url = url;
        return this;
    }

    setMethod(method: 'get' | 'post'): this {
        this.method = method;
        return this;
    }
    
    setData(data: object): this {
        this.data = data;
        return this;
    }

    send() {}
}

new RequestBuilder()
    .setURL('/users')
    .setMethod('get')
    .setData({firstName: 'Roper'})
    .send()
```