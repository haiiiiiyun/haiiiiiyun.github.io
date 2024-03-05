---
title: Ignore files that have already been committed to a Git repository
date: 2023-11-26
tags: git
categoris: Programming
---

To untrack a *single* file that has already been added/initialized to your repository, *i.e.*, stop tracking the file but not delete it from your system use:

```
git rm --cached filename
```

Use `--cached` option to unstage and remove paths only from the index. Working tree files, whether modified or not, will be left alone.

To untrack *every* file that is now in your `.gitignore`:

**First commit any outstanding code changes**, and then, run this command:

```
git rm -r --cached .
```

This removes any changed files from the *index*(staging area), then just run:

```
git add .
```

Commit it:

```
git commit -m ".gitignore is now working"
```

To undo `git rm --cached filename`, use `git add filename`.

see https://stackoverflow.com/questions/1139762/ignore-files-that-have-already-been-committed-to-a-git-repository