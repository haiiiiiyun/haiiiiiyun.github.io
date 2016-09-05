---
title: Git 基础知识
date: 2016-09-05
writing-time: 2016-09-05 08:52--16:17
categories: programming
tags: Git Utility LearnXinYminutes
---

Git 是一个分布式的版本控制和源码管理系统。

它通过一系列的项目快照来实现，并利用这些快照向你提供版本控制和管理源码的功能。

## 版本控制概念

### 什么是版本控制？

版本控制就是一个依据时间顺序记录对文件的修改情况的系统。

### 集中式版本控制 VS 分布式版本控制

* 集中式版本控制注重同步，跟踪和备份文件。
* 分布式版本控制注重共享更改。每一次更改都有一个唯一的标识号。
* 分布式系统没有预定结构。通过 git ，你也可以很容易实现一个 SVN 类型的集中式系统。

[更多信息](http://git-scm.com/book/en/Getting-Started-About-Version-Control)

### 为什么要用 Git?

* 可以离线使用。
* 与他人协作很容易！
* 分支操作很容易！
* 分支操作很快速!
* 合并操作很容易！
* Git 运行很快。
* Git 很灵活。

## Git 体系结构

### 仓库 (Repository)

就是一组文件、目录、历史记录、提交和头。可以将它想象成源代码的一种数据结构，通过每个源代码 “元素” 上的属性，你能访问其版本历史等内容。

一个 git 仓库由 .git 目录 & 工作树组成。

### .git 目录 (仓库的组成部分)

.git 目录包含所有的配置、日志、分支、HEAD 等信息。
[详细列表。](http://gitready.com/advanced/2009/03/23/whats-inside-your-git-directory.html)

### 工作树 Working Tree (仓库的组成部分)

它基本上就是你的仓库中的目录和文件。它通常被称为你的工作目录。

### 索引 Index (.git 目录的组成部分)

索引是 git 的 staging 区。它基本上是将你的工作树与 Git 仓库进行隔离的层。它能使开发人员能更加灵活地控制将向 Git 仓库发送什么内容。

### 提交 Commit

一个 git 提交就是关于你的工作树的一系列更改的一个快照。
例如，如果你新增了 5 个文件，删除了 2 个文件，这些更改将会包含在
一个提交（或快照）中。这个提交之后可以推送到其它的仓库中，也可以不推送。

### 分支 Branch

一个分支本质上是指向你的上次提交的一个指针。
随着你不断地进行提交，这个指针将自动更新指向到最近的提交上。

### 标签 Tag

一个标签就是在修改历史的某个特定点上做的标记。人们通常利用该功能来标记发布点 (如 v1.0 等)。

### HEAD 和头 (.git 目录的组成部分)

HEAD 是指向当前分支的一个指针。一个仓库只能有 1 个 *活跃* HEAD。
而头是指向任意一个提交的一个指针。一个仓库可以有无限多个头。

### Git 的 Stages
* Modified - 对文件已做了修改但是还没有提交到 Git 数据库
* Staged - 已将更改标记为将进入下一个提交快照
* Committed - 文件已经提交到 Git 数据库中

### 有关概念的相关资源

* [Git For Computer Scientists](http://eagain.net/articles/git-for-computer-scientists/)
* [Git For Designers](http://hoth.entp.com/output/git_for_designers.html)

## 命令

### init

创建一个空 Git 仓库。Git 仓库的设置、存储信息等都将保存在一个叫 ".git" 的目录中。

```bash
$ git init
```

### config

可用于设置仓库、系统本身
或者全局配置 ( 全局配置文件是 `~/.gitconfig` )。

```bash
# 打印 & 设置一些基本配置变量（全局）
$ git config --global user.email "MyEmail@Zoho.com"
$ git config --global user.name "My Name"
```

[学习关于 git config 的更多知识。](http://git-scm.com/docs/git-config)

### help

使你能快速访问关于每个命令的非常详细的教程。
或者能给出关于一些语义的快速提醒。

```bash
# 快速检查可用命令
$ git help

# 检查所有可用命令
$ git help -a

# 特定命令的帮助 - 用户手册
# git help <command_here>
$ git help add
$ git help commit
$ git help init
# 或者 git <command_here> --help
$ git add --help
$ git commit --help
$ git init --help
```

### 忽略的文件 .gitignore

特意不想在 git 中记录某些文件 & 目录。通常指那些不能在仓库中共享的私有 & 临时文件。

```bash
$ echo "temp/" >> .gitignore
$ echo "private_key" >> .gitignore
```

### status

显示索引文件（基本上是你的工作树/仓库) 与当前 HEAD 提交之间的差异。

```bash
# 将显示分支、未追踪的文件、修改及其它差异
$ git status

# 学习关于 git status 的其它知识
$ git help status
```

### add

将文件添加到 staging 区/索引。如果你没有将新文件 `git add` 到
staging 区/索引中，它们将不会被包含到提交中！

```bash
# 将一个文件新增到你的当前工作目录中
$ git add HelloWorld.java

# 新增一个在嵌套目录中的文件
$ git add /path/to/file/HelloWorld.c

# 正则表达式支持！
$ git add ./*.java
```

这只是将文件添加到 staging 区/索引中，并没有提交到
工作目录/仓库。

### branch

管理你的分支。你使用该命令来查看、编辑、创建和删除分支。

```bash
# 列出现存的分支
$ git branch -a

# 新建一个分支
$ git branch myNewBranch

# 删除一个分支
$ git branch -d myBranch

# 重命名一个分支
# git branch -m <oldname> <newname>
$ git branch -m myBranchName myNewBranchName

# 编辑一个分支的描述信息
$ git branch myBranchName --edit-description
```

### tag

管理你的标签

```bash
# 列出标签
$ git tag

# 创建一个有注解的标签
# -m 指定标记消息，它会与标签一起保存。
# 如果你没有指定标记消息，
# Git 会开启一个编辑器让你输入。
$ git tag -a v2.0 -m 'my version 2.0'

# 显示关于标签的信息
# 这将显示该标签的作者，标记的日期，
# 以及在显示提交信息前显示注解消息。
$ git show v2.0

# 推送一个标签到远端
$ git push origin v2.0

# 推送多个标签到远端
$ git push origin --tags
```

### checkout

更新工作树中的所有文件以便能匹配索引，或者特定树中的版本。

```bash
# 检出一个仓库 - 默认到 master 分支
$ git checkout

# 检出一个特定分支
$ git checkout branchName

# 创建一个新分支 & 切换到该分支
# 等同于 "git branch <name>; git checkout <name>"

$ git checkout -b newBranch
```

### clone

克隆，或者复制一个现有创建到一个新目录。它还为
被克隆仓库中的每个仓库创建远程追踪分支， 以使你能推送到远程分支。

```bash
# 克隆 learnxinyminutes-docs
$ git clone https://github.com/adambard/learnxinyminutes-docs.git

# 影子克隆 - 只拉取最近快照的更快地克隆法
$ git clone --depth 1 https://github.com/adambard/learnxinyminutes-docs.git

# 只克隆一个特定分支
$ git clone -b master-cn https://github.com/adambard/learnxinyminutes-docs.git --single-branch
```

### commit

将索引中的当前内容保存到一个新 “提交” 中。
这次提交包含所做的更改以及由用户创建的一条消息。

```bash
# 连同一条消息进行提交
$ git commit -m "Added multiplyNumbers() function to HelloWorld.c"

# 自动将修改了的或删除了的文件转到 stage 区（不包括新建文件），然后提交
$ git commit -a -m "Modified foo.php and removed bar.php"

# 修改上次的提交（这将删除之前的提交并生成一个新提交）
$ git commit --amend -m "Correct message"
```

### diff

显示文件在工作目录、索引和提交间的差异

```bash
# 显示你的工作目录和索引间的差异
$ git diff

# 显示索引与最近提交间的差异
$ git diff --cached

# 显示你的工作目录与最近提交间的差异
$ git diff HEAD
```

### grep

允许快速搜索一个仓库。

可选配置：

```bash
# 多谢 Travis Jeffery 指点
# 设置在 grep 搜索结果中显示行号
$ git config --global grep.lineNumber true

# 使搜索结果更易读，并包含分组
$ git config --global alias.g "grep --break --heading --line-number"
```

```bash
# 在所有的 java 文件中搜索 "variableName"
$ git grep 'variableName' -- '*.java'

# 搜索包含 "arrayListName" 及, "add" 或者 "remove" 的行
$ git grep -e 'arrayListName' --and \( -e add -e remove \)
```

更多例子： [Git Grep Ninja](http://travisjeffery.com/b/2012/02/search-a-git-repo-like-a-ninja)

### log

显示仓库中的提交信息

```bash
# 显示所有提交信息
$ git log

# 只显示提交的消息 & ref
$ git log --oneline

# 只显示合并提交
$ git log --merges

# 通过一个 ASCII 图显示所有提交
$ git log --graph
```

### merge

将外部提交中的更新 “合并” 到当前分支中。

```bash
# 将特定分支合并到当前分支
$ git merge branchName

# 合并时总是创建一个合并提交记录
$ git merge --no-ff branchName
```

### mv

重命名或移动一个文件

```bash
# 重命名文件
$ git mv HelloWorld.c HelloNewWorld.c

# 移动文件
$ git mv HelloWorld.c ./new/path/HelloWorld.c

# 强制重命名或移动
# "existingFile" 如果已存在于目录中，将会被覆盖
$ git mv -f myFile existingFile
```

### pull

从仓库中拉取并与另一个分支合并

```bash
# 通过合并名为 "origin" 的远程 "master" 分支
# 中的更改来更新你的本地仓库。
# git pull <remote> <branch>
$ git pull origin master

# 默认地，git 通过合并它的远程追踪分支
# 中的更改来更新你的当前分支。
$ git pull

# 合并远程分支中的更新，
# 并将分支提交记录 rebase 到你的本地仓库，
# 像： "git fetch <remote> <branch> && git rebase <remote>/<branch>"
$ git pull origin master --rebase
```

### push

推送并将分支中的更改合并到一个远程分支中。

```bash
# 推送并将本地仓库中的更改合并到
# 名为 "origin" 的远程 "master" 分支
# git push <remote> <branch>
$ git push origin master

# 默认地，git push 会将当前分支的更改合并到其远程追踪分支上。
$ git push

# 要将当前本地分支与远程分支关联，使用 -u 选项：
# -u 指 --set-upstream
$ git push -u origin master
# 之后，如果你想推送相同的本地分支，使用快捷方式：
$ git push
```

### stash

Stash 将你当前工作目录中的未提交修改保存到一个未完成更新堆栈中，
以便你能在任意时间重新取回。

假设你已在 git 仓库中做了一些修改，但你想从远程拉取。
因你对一些文件的修改还没有提交，因此无法运行 `git pull`。
此时你可运行 `git stash` 将你的修改保存到堆栈中！

```bash
$ git stash
Saved working directory and index state \
  "WIP on master: 049d078 added the index file"
  HEAD is now at 049d078 added the index file
  (To restore them type "git stash apply")
```

现在你可以拉取了！

```bash
git pull
```
`...changes apply...`

现在可以检查下一切是否正常

```bash
$ git status
# On branch master
nothing to commit, working directory clean
```

你可以使用 `git stash list` 来查看已保存的 stash 记录。
因这些记录是以 后进先出 方式保存在堆栈中的，
我们的最近修改将会在最上面。

```bash
$ git stash list
stash@{0}: WIP on master: 049d078 added the index file
stash@{1}: WIP on master: c264051 Revert "added file_size"
stash@{2}: WIP on master: 21d80a5 added number to log
```

现在通过从堆栈中弹出，来取回我们的未完成修改信息。

```bash
$ git stash pop
# On branch master
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#
#      modified:   index.html
#      modified:   lib/simplegit.rb
#
```

`git stash apply` 具有相同的功能。

现在你可以继续之前的工作了！

[更多资源](http://git-scm.com/book/en/v1/Git-Tools-Stashing)

### rebase (小心)

将某个分支上提交的所有更新，在另一个分支上重做一遍。
*如果已经推送到了一个公共仓库，不要 rebase*。

```bash
# 将 experimentBranch rebase 到 master 上
# git rebase <basebranch> <topicbranch>
$ git rebase master experimentBranch
```

[更多资源](http://git-scm.com/book/en/Git-Branching-Rebasing)

### reset (小心)

将当前 HEAD 重置到一个特定状态。它能使你撤销合并、
拉取、提交、新增等操作。这是个很赞的命令，但如果你
不知道在做什么的话也会很危险。

```bash
# 重置 stage 区，以便匹配最后的提交记录（不改动当前工作目录内容）
$ git reset

# 重置 stage 区，以便匹配最后的提交记录，并覆盖工作目录内容
$ git reset --hard

# 将当前分支指向特定提交记录（不改动当前工作目录内容）
# 目录下的所有修改仍旧存在。
$ git reset 31f2bb1

# 将当前分支指向特定提交记录，
# 并匹配工作目录（未提交的修改及该提交记录后的所有提交
# 都将删除）
$ git reset --hard 31f2bb1
```

### reflog (小心)

Reflog 将列出给定时间段内你所完成的大部分 git 命令，默认为 90 天。

它将给你一个反转任意 git 命令的机会，例如一次 rebase 破坏了你的应用。

你可以这样做：

1. `git reflog` 列出该次 rebase 的所有 git 命令
```
38b323f HEAD@{0}: rebase -i (finish): returning to refs/heads/feature/add_git_reflog
38b323f HEAD@{1}: rebase -i (pick): Clarify inc/dec operators
4fff859 HEAD@{2}: rebase -i (pick): Update java.html.markdown
34ed963 HEAD@{3}: rebase -i (pick): [yaml/en] Add more resources (#1666)
ed8ddf2 HEAD@{4}: rebase -i (pick): pythonstatcomp spanish translation (#1748)
2e6c386 HEAD@{5}: rebase -i (start): checkout 02fb96d
```
2. 选择重置到何处，在我们的例子中是 `2e6c386`, 或者 `HEAD@{5}`
3. `git reset --hard HEAD@{5}` 会将你的仓库重置到那个头
4. 你可以重新进行 rebase

[更多资源](https://git-scm.com/docs/git-reflog)

### revert

Revert 可以用来撤销一个提交。不要和 reset 搞混淆。
Reset 是将项目的状态还原到之前的某个点。
Revert 会新增一个提交，这个提交与那个特定提交正好相反，
从而实现撤销。

```bash
# 撤销一个特定提交
$ git revert <commit>
```

### rm

是 git add 的相反操作，git rm 将文件从当前工作树中删除。

```bash
# 删除 HelloWorld.c
$ git rm HelloWorld.c

# 从一个嵌套目录中删除文件
$ git rm /pather/to/the/file/HelloWorld.c
```

## 更多信息是

* [tryGit - A fun interactive way to learn Git.](http://try.github.io/levels/1/challenges/1)

* [Udemy Git Tutorial: A Comprehensive Guide](https://blog.udemy.com/git-tutorial-a-comprehensive-guide/)

* [Git Immersion - A Guided tour that walks through the fundamentals of git](http://gitimmersion.com/)

* [git-scm - Video Tutorials](http://git-scm.com/videos)

* [git-scm - Documentation](http://git-scm.com/docs)

* [Atlassian Git - Tutorials & Workflows](https://www.atlassian.com/git/)

* [SalesForce Cheat Sheet](http://res.cloudinary.com/hy4kyit2a/image/upload/SF_git_cheatsheet.pdf)

* [GitGuys](http://www.gitguys.com/)

* [Git - the simple guide](http://rogerdudler.github.io/git-guide/index.html)

* [Pro Git](http://www.git-scm.com/book/en/v2)

* [An introduction to Git and GitHub for Beginners (Tutorial)](http://product.hubspot.com/blog/git-and-github-tutorial-for-beginners)

> 参考文献： [Learn Git in Y minutes](https://learnxinyminutes.com/docs/git/)
