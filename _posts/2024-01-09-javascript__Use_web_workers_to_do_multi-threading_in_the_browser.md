---
title: Use web workers to do multi-threading in the browser
date: 2024-01-09
tags: javascript async typescript
categoris: Programming
---

To do multithreading in the browser, we spin up some workers--special restricted background threads--from the main JS thread, and use them to do things that would have otherwise blocked the main thread.

Web Workers are a way to run code in the browser in a truly parallel way; while asynchronous APIs like `Promise` and `setTimeout` run code concurrently.

In Typescript, we tell TSC that we're planning to run code in a browser by enabling the `dom` lib in `tsconfig.json`:

```json
{
	"compilerOptions": {
		"lib": ["dom", "es2015"]
	}
}
```


And for the code that we're running in a Web Worker，use the webworker lib:

```json
{
	"compilerOptions": {
		"lib": ["webworker", "es2015"]
	}
}
```

## communication with postMessage and onmessage

```typescript
// MainThread.ts
let worker = new Worker('WorkerScript.js');
worker.onmessage = e => {
	console.log(e.data);
}
worker.postMessage('some data');
```


```typescript
// WorkerScript.js
onmessage = e => {
	console.log(e.data);
	postMessage(`Ack: ${e.data}`);
}
```