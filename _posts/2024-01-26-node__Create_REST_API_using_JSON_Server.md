---
title: Create REST API using JSON Server
date: 2024-01-26
tags: rest
categoris: Programming
---

1. Install JSON Server:

```bash
npm i -D json-server
```

2. Define the data behind the API in a JSON file db.json:

```json
{
  "posts": [
	{
		"title": "Getting started with fetch",
		"description": "How to interact with backend APIs using fetch",
		"id": 1
	},
	{
		"title": "Getting started with useEffect",
		"description": "How to use React's useEffect hook for interacting with backend APIs",
		"id": 2
	}
  ]
}
```

3. Define npm script to start the JSON server.

Open **package.json** and add a script called **server**:

```json
{
  ...
  "scripts": {
	...
	"server": "json-server --watch db.json --port 3001"
  }
}
```

4. Run the script

```bash
npm run server
```

5. Check the api:  http://localhost:3001/posts

See https://github.com/typicode/json-server