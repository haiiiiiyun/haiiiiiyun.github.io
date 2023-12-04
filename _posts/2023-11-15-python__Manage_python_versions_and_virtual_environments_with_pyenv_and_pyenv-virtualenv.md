---
title: Manage python versions and virtual environments with pyenv and pyenv-virtualenv
date: 2023-11-15
tags: python tools virtual-environment
categoris: Programming
---

## Tools and use case

+ Use [pyenv](https://github.com/pyenv/pyenv) to install multiple Python versions side by side, such as Python 3.8.2, Python 3.12.0, etc.
+ Use [virtualenv](https://github.com/pyenv/pyenv-virtualenv)  or [venv](https://docs.python.org/3/library/venv.html) to create isolated Python environments for Python libraries, so that each project can run with their own dependencies.

## Manage python versions with pyenv

### Install pyenv

```bash
$ curl https://pyenv.run | bash
```

It will clone pyenv repository from githhub.com to `~/.pyenv/`. 

After installing, add the following lines to `~/.bashrc` and restart bash:

```bash
### --start: pyenv & pyenv-virtualenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Load pyenv-virtualenv automatically by adding
# the following to ~/.bashrc:
eval "$(pyenv virtualenv-init -)"
alias workon='pyenv activate '
### --end: pyenv & pyenv-virtualenv
```

To update pyenv:

```bash
$ pyenv update
```

To remove pyenv:

```bash
$ rm -rf ~/.pyenv
```

and delete all config lines from ``~/.bashrc`.

### Manage multiple python versions

#### List all the installable python versions:

```bash
$ pyenv install --list
```

#### Install a version:

```bash
$ pyenv install 3.12.0
```

It will download the python source code file and compile it from source code.  Before building, we have to install all the required dev dependencies:

```bash
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev libssl-dev git libedit-dev libncurses5-dev
```

see [pyenv common build problems](https://github.com/pyenv/pyenv/wiki/Common-build-problems)

All python versions that are installed by pyenv all stored under `~/.pyenv/versions/`

#### show all installed versions and the current default version

```bash
$ pyenv versions

* system (set by /home/hy/.pyenv/version)
  3.12.0
```

### Switch between versions

Set the default python version globally:

```bash
$ pyenv global 3.12.0
```

Set the default python version locally under the current directory:

```bash
$ pyenv local 3.12.0

$ cat .python-version
3.12.0
```
It will create file `.python-version` with content `3.12.0` under the current directory.

## Manage virtual environments with pyenv-virtualenv

Install pyenv installs pyenv-virtualenv by default.

### Create an isolated virtual environment

Similar to the `cp src dst` command: 

```bash
$ pyenv virtualenv 3.12.0 py3.12

$ pyenv versions
* system (set by /home/hy/.pyenv/version)
  3.12.0
  3.12.0/envs/py3.12
  py3.12 --> /home/hy/.pyenv/versions/3.12.0/envs/py3.12
```

### Activate and use a virtual environment

```bash
$ pyenv activate py3.12

$ pip install XXX

$ pyenv deactivate
```

It's convenient to create an alias for switching between virtual environments:

```bash
$ echo 'workon="pyenv activate "' >> ~/.bashrc
$ ~/.bashrc 
$ workon py3.12
```

### Remove virtual environment

```bash
$ pyenv uninstall py3.12 # or
# $ rm -rf ~/.pyenv/versions/py3.12/
```

## Settings on Mac

Save the settings in `~/.bash_profile`  instead of in `~/.bashrc`

## Links

See [what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe](https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe)
