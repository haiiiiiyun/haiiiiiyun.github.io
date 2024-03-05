---
title: Status of files in git
date: 2023-12-22
tags: git
categoris: Programming
---

1.  Untracked: any files  in the working directory(a checkout or a working copy) that are not in last snapshot and are not in the staging area.
2. Unmodified: files in the last snapshot
3. Modified: files in the working directory and modified
4. Staged(cached, indexed): files in the staging area

## State machine

- `untracked`   add the file--> `staged`
- `unmodified`  edit the file --> `modified`
- `unmodified` remove the file --> `untracked`
- `modified` stage the file --> `staged`
- `staged` commit the file --> `unmodified`