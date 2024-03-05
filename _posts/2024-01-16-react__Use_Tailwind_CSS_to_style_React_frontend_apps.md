---
title: Use Tailwind CSS to style React frontend apps
date: 2024-01-16
tags: react styles css tailwind
categoris: Programming
---

## Tailwind is a set of prebuilt CSS classes that can be used to style an app

It is referred to as a **utility first CSS framework** because the prebuilt classes can be thought of as flexible utilities.

```typescript
<button className="border-none rounded-md bg-emerald-700 text-white cursor-pointer hover:bg-emerald-800"></button>
```

Tailwind can specify that a class should be applied when the elements is in a hover state by prefixing it with `hover:`.

A key point of [tailwind](https://tailwindcss.com/) is that we don't write new CSS classes for each element we wan to style, instead, we use a large range of well-thought-through existing classes.

## Install and configure Tailwind CSS

1. install Tailwind library:

```bash
npm i -D tailwindcss
```

2. Tailwind integrates into create-react-app using a library PostCSS.

PostCSS is a tool that transforms CSS using JS, and Tailwind runs as a plugin in it:

```bash
npm i -D postcss
```

3. Tailwind also recommends another PostCSS called **Autoprefixer**, which adds vendor prefixes to CSS:

```bash
npm i -D autoprefixer
```

4. generate configuration files for Tailwind and PostCSS:

```bash
npx tailwindcss init -p
```

It generates configuration files `tailwind.config.js` and `postcss.config.js`.

5. Open tailwind.config.js and specify the path to the React components as follows:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

6. Install form plugin, which provides nice styles for field elements out of the box:

```bash
npm i -D @tailwindcss/forms
```

Then open tailwind.config.js and add the plugin config:

```javascript
plugins: [require('@tailwindcss/forms')],
```

8. open `src/index.css` and add the following 3 lines at the top of the file:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

These are called **directives** and will generate the CSS required by Tailwind during the build process.

Tailwind is now installed and ready to use.

## Using Tailwind CSS

Now we can set tailwind CSS classes in component's `className` attribute:

```typescript
<div className={`inline-flex flex-col text-left px-4 py-3 rounded-md border-1 border-transparent`}
>
</div>
```

`px-4` adds 4 spacing units of left and right padding, spacing units are defined in Tailwind and are a proportional scale. One spacing unit is equal to 0.25rem, which translates roughly to 4px.

## Performance

Tailwind does not incur a runtime performance penalty like Emotion, see [[Use CSS-in-JS to style React frontend apps]]. Only classes used on React elements are included in the CSS build bundle.