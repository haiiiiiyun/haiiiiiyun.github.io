---
title: Add environment variables to create-react-app React APP
date: 2024-01-29
tags: react
categoris: Programming
---

1. Environment variables in Create-react-app projects must be prefixed with `REACT_APP_`, for example: `REACT_APP_API_URL = http://localhost:3001/posts/`
2. Another special environment variable is `NODE_ENV`,  we can read it from `process.env.NODE_ENV`, the value will be `development`, `test`, or `production`.
3. Environment variable is injected into code at **build time**.
4. Access it using `process.env.REACT_APP_VAR_NAME` in JS code.
5. Access it in the HTML using `%REACT_APP_VAR_NAME%`.

## Add environment variables in .env file

Create `.env` file under the project's root folder.

## Add temporary environment variables in Shell

for example:  `REACT_APP_NOT_SECRET_CODE=abcdef npm start`.

Also see https://create-react-app.dev/docs/adding-custom-environment-variables/