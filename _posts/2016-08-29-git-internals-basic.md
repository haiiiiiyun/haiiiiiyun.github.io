---
title: Git 内部机制与存储对象的图形化简介
date: 2016-08-29
writing-time: 2016-08-29 15:15--17:26
categories: programming
tags: Git Utility
---

# 抽象

Git 内部基本上是一个 [有向无环图 Directed Acyclic Graph(DAG)](http://en.wikipedia.org/wiki/Directed_acyclic_graph)。

# 存储

Git 中存储的只是大量不同类型的 DAG 对象。这些对象被压缩存储，并且以一个 SHA-1 哈希值来唯一标识（不是对象内容对应计算出的 SHA-1，只是做标识用）。

## blob

blob 是最简单的对象，只是一段字节。它通常表示一个文件等的内容。而 blob 的语义则由指向它的对象所决定。

<img src="/assets/images/git-storage.1.dot.svg">

## tree

目录由 tree 对象表示。tree 内容包括：指向表示文件内容的 blob、表示子目录的其它 tree，以及文件名、访问模式信息等。

当 DAG 的一个节点指向另一个节点后，这两个节点就形成相互依赖，无法单独存在。而没有被其它节点所指向的节点可以在运行 `git gc` 时被垃圾回收，也可以使用 `git fsck --lost-found` 时进行修复。


<img src="/assets/images/git-storage.2.dot.svg">

## commit

一个 commit 指向一个表示提交时文件状态的一颗 tree。它也指向 0..n 个其它 commit， 作为父 commit。

如果有多个父 commit，则表示这个 commit 是由合并而来的。没有父 commit 则表示 是初始 commit。有趣的是，可以有多个初始 commit，这表示该项目是由两个项目合并而来的。

commit 对象中包含的内容是提交消息。

<img src="/assets/images/git-storage.3.dot.svg">

## refs

指参考、头或分支，它们就像贴在 DAG 节点上的便签纸。因为 DAG 中的新节点只能关联到现有的节点，因此 DAG 不可能突变，从而使得这些 “便签纸” 可以自由移动。

它们不保存到历史记录中，也不会在仓库间直接传送。它们也类似于书签：“我当前在这里”。

`git commit` 在 DAG 中增加一个新节点，并将当前分支上的 “便签纸” 移到这个新节点。

`HEAD` ref 比较特殊，它实际上指向另外一个 ref。它是指向当前活跃分支的指针。普通 refs 的命名空间为 `heads/xxx`，但通常可以省略 `heads/` 部分。

<img src="/assets/images/git-storage.4.dot.svg">

## remote refs

远程 refs 和普通 refs 的区别在于命名空间，而这些远程 refs 本质上是由远程服务器控制的。可以通过 `git fetch` 进行更新。

<img src="/assets/images/git-storage.5.dot.svg">


## tag

tag 即是 DAG 中的一个节点，也是一个 “便签纸”。它指向一个 commit，并可包含一条信息及一个 GPG 标识。

而这个 “便签纸” 提供了快速访问 tag 方法。

一旦丢失，可以通过 `git fsck --lost-fount` 命令来修复。

DAG 中的节点可以在仓库间移动，可以以更高效的方式（压缩）存储，而未使用的节点可以被垃圾回收。但最终，一个 git 仓库总是一个 DAG + “便签纸”。

<img src="/assets/images/git-storage.6.dot.svg">


# 可视化修改历史

1. 最简单的仓库，克隆至一个只有一个 commit 的远程仓库

<img src="/assets/images/git-history.1.dot.svg">

2. 通过 `git fetch` 从远程获取一个新 commit，但还没有合并

<img src="/assets/images/git-history.2.dot.svg">

3. 进行 `git merge remotes/MYSERVER/master` 后的情况。由于在本地分支上没有新的 commit，本次合并是快进 `fast forward` 操作，只是将 “便签纸” 进行了移动，并修改了当前工作目录下的相关文件。

<img src="/assets/images/git-history.3.dot.svg">

4. 在本地进行 `git commit` 和 `git fetch` 后，现在已有一个新的本地 commit 和新的远程 commit，显然，需要进行合并操作。

<img src="/assets/images/git-history.4.dot.svg">

5. 进行 `git merge remotes/MYSERVER/master` 之后的结果。由于这次不是 fast forward，因此会在 DAG 中创建一个新节点，该节点有两个父 commit 节点。

<img src="/assets/images/git-history.5.dot.svg">

6. 当进行多次 commit 和 merge 操作后可能的样子。可以看到出现了 “缝线” 模式。git 的 DAG 准确地记录了操作的历史。


<img src="/assets/images/git-history.6.dot.svg">

7. 当还没有对你的分支进行发布时，可以对你的分支进行 `git rebase` 操作，即你的 commit 被另一个具有不同父 commit 的 commit 替换。你的旧 commit 会一直保留在 DAG 中直到被垃圾回收。

<img src="/assets/images/git-history.7.dot.svg">

8. 使用 `git gc` 进行垃圾回收，然后创建一个新的 commit 后：

<img src="/assets/images/git-history.8.dot.svg">

9. `rebase` 也可以对多个 commit 进行 rebase 操作：

<img src="/assets/images/git-history.9.dot.svg">


> 参考文献： [Git for Computer Scientists](http://eagain.net/articles/git-for-computer-scientists/)
