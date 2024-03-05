---
title: Create a typescript project with create-react-app
date: 2024-01-15
tags: typescript react
categoris: Programming
---

## Create a project

```bash
npx create-react-app myapp --template typescript
```

## Add linting to VS Code

1.  install `ESlint` extension by Microsoft
2. Make sure the ESLint is configured to check React and Typescript. Open **Preferences->Settings**, in the `Workspace` tab, query `eslint:probe`,  make sure that `typescript` and `typescriptreact` are on the list.

## Add code formatting

1. Install Prettier: `npm i -D prettier`
2. Prettier has overlapping style rules with ESLint, so install the following two libraries to allow Prettier to take responsibility for the styling rules from ESLint:

```bash
npm i -D eslint-config-prettier eslint-plugin-prettier`
```

3. The ESLint config needs to be updated to allow Prettier to manage the styling rules. Add the Prettier rules to the `eslintConfig` section in `package.json` as follows:

```json
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest",
      "plugin:prettier/recommended"
    ]
  }
```

4. Prettier can be configured in a file called `.prettierrc.json`. Create this file with the following content in the root folder:

```json
{
    "printWidth": 100,
    "singleQuote": true,
    "semi": true,
    "tabWidth": 2,
    "trailingComma": "all",
    "endOfLine": "auto"
}
```

## VS Code integrates with Prettier to automatically format code when source files are saved

1. install extension `Prettier - Code formatter`
2. Open **Preferences->Settings**, in the `Workspace` tab, query `format on save`,  make sure that `Editor: Format On Save` option is ticked.
3. One more settings. Tell VS Code the default formatter to use to format code. In the `Workspace` tab, query `default formatter`, make sure `Editor: Default Formatter` is set to `Prettier - Code formatter`.

 Or replace the step 2 and step 3 with a VS Code settings file `.vscode/settings.json`:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

## Start the app in development mode

```bash
npm start
```

## Produce a production build

```bash
npm run build
```