---
title: Manage node versions with nvm
date: 2023-11-17
tags: node tools
categoris: Programming
---


The [Node Version Manager(NVM)](https://github.com/nvm-sh/nvm) is an open source version manager for [Node.js(Node)](https://nodejs.org/en/).

`nvm` allows you to easily install and mange different versions of Node and switch between them on a per-shell basis.

## Install nvm

```bash
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
```

It will clone the nvm repository to `~/.nvm` and attempts to add the source lines from the snippet below to the correct profile file(`~/.bashrc`, `~/.bash_profile`, .etc)

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

For troubleshooting and updates, see https://github.com/nvm-sh/nvm#installing-and-updating

To confirm the version of nvm that is running:

```bash
$ nvm -v
```

## Usage

### List all installable node versions

```bash
$ nvm ls-remote
```

### Install a specific version of node

```bash
$ nvm install v20.9.0
```

Or install the latest LTS version:

```bash
$ nvm install --lts
```

### Switch between node versions

#### Switch version locally

In any new shell just use the node:

```bash
$ nvm use v20.9.0
```

Or just run it:

```bash
$ nvm run v20.9.0
```

#### Switch version globally

Use the `alias` command to  link the alias `default` to the specify version:

```bash
$ nvm alias default v20.9.0
```


To review all installed versions of node and the default(global) node version with the `ls` command:

```bash
$ nvm ls
       v16.20.0
->     v18.16.0
         system
default -> v18.16.0
```

NVM returns a list of all Node versions and aliases, along with an arrow indicating the current version.

### Uninstall

Use nvm to unstall node:

```bash
$ nvm uninstall v16.20.0
```


#### Uninstall nvm

Clear any path variables:

```bash
$ nvm deactivate
```

Uninstall nvm:

```bash
$ nvm unload
```

Clean up `.bashrc` file by removing the following lines:

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm
```

## Links

+ https://github.com/nvm-sh/nvm#installing-and-updating
+ https://www.linode.com/docs/guides/how-to-install-use-node-version-manager-nvm/