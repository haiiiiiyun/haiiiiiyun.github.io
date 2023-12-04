---
title: How to download a file from URI using Javascript
date: 2023-11-30
tags: javascript
categoris: Programming
---

We create a temporary `<a href="uri" target="_blank" download="filename" />`  element using Javascript, append it to `document.body` and then trigger `elemnt.click()`.

```javascript
function downloadURI(uri, name) {
	const link = document.createElement("a");
	link.href = uri;
	link.download = name || uri.split('/').pop();
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
}
```

see https://stackoverflow.com/questions/3916191/download-data-url-file