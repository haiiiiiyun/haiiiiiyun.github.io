---
title: Show entire change history of a file
date: 2023-11-26
tags: git
categoris: Programming
---

```
git log --follow -p -- path-to-file
```

This will show the **entire** history of the file, including history beyond renames and with diffs for each change. In other words, if the file named `bar` was once named `foo`, then `git log -p bar` (without the `--follow` option) will only show the file's history up to the point where it was renamed.

Options: 
1.  `--follow` ensures that you see file renames
2. `-p` or `--patch` ensures that you see how the file gets changed
3. `--` option tells Git that it has reached the end of the options and that anything that follows `--` should be treated as an argument.

For a graphical view, use [`gitk`](https://git-scm.com/docs/gitk/):

```
gitk [filename]
```

To follow the file across file renames:

```
gitk --follow [filename]
```

See https://stackoverflow.com/questions/278192/view-the-change-history-of-a-file-using-git-versioning