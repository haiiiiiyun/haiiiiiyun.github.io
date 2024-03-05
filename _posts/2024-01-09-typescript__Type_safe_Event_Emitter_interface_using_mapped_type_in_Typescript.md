---
title: Type safe Event Emitter interface using mapped type in Typescript
date: 2024-01-09
tags: typescript async
categoris: Programming
---

## unsafe emitter interface

Event emitters offer APIs that support emitting events on a channel and listening for events on that channel:

```typescript
interface Emitter {
    emit(channel: string, value: unknown): void,
    on(channel: string, f: (value: unknown) => void): void
}
```

This version of emitter is unsafe, that's because the type of value depends on the specific channel.

## Emitter example in the wild: NodeRedis client

```typescript
import Redis from 'redis';

let client = redis.createClient()

// Listen for a few events emitted by the client
client.on('ready', () => console.info('Client is ready'))
client.on('error', e => console.error('An error occurred!', e))
client.on('reconnecting', params => console.info('Reconnecting...',
params))
```

## Define a type safe emitter using mapped types

```typescript
type MyEvent = {
    ready: void,
    error: Error,
    reconnecting: {attemp: number, delay: number}
}

type RedisClient = {
    on<E extends keyof MyEvent>(event: E, f: (arg: MyEvent[E]) => void): void,
    emit<E extends keyof MyEvent>(event: E, arg: MyEvent[E]): void
}
```

This pattern of pulling out event names and arguments into a shape and mapping over that shape to generate listeners and emitters is common in real-world TS code.