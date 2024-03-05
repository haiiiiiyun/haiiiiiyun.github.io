---
title: Javascript Event Loop
date: 2024-01-09
tags: javascript async
categoris: Programming
---

Javascript VM simulates concurrency like this:

1. The main JS thread calls into native asynchronous API like `XMLHTTPRequest`, `setTime`, `readFile`, and so on. These APIs are provided by the JS platform.
2. Once we call into a native asynchronous API, JS platform sets up a new thread for the asynchronous operation, control returns to the main thread and execution continues as if the API was never called.
3. Once the asynchronous operation is done, the JS platform puts a task in main thread's **event queue**. Each thread has its own queue, used for relaying the results of asynchronous operations back to the main thread.
4. Whenever the main thread's call stack is emptied, the JS platfrom will check its event queue for pending tasks. If there is a task waiting, the platform runs it.
5. Run task triggers a function call, and control returns to the main thread function. When the call stack resulting from the task call is once again empty, JS platform again  checks the event queue for tasks that are ready to go.

## Example

```javascript
setTimeout(() => console.log('A'), 1);
setTimeout(() => console.log('B'), 2);
console.log('C');
let i = 0;
while(i<1000){
    console.log('D');
    i += 1;
}
```

The output is:
```
C
D
D
...
A
B
```

`A` is not printed exactly after 1 millisecond because JS platform checks the task from event queue only when the main thread's call stack is emptied.