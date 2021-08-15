# launchii, a fast, cross-platform, Python-based app launcher, similar to Alfred or Wox

launchii is (will be) versatile, include a simple & clean UI with theming support (coming soon), plugin support (coming soon), cross platform support w/ selfhosted cloud config syncing, and fast indexing.

![](https://github.com/SmatMan/launchii/blob/main/imgs/main.png)

## Goals of this project
- Create an easy to use launcher that works on *every* popular desktop platform (MacOS, Windows, Linux). Currently, the only popular options are **platform-specific**, which makes it hard to sync workflows.
- Add an easy plugin API to allow developers to create plugins for launchii
- Efficient indexing, but easily modifiable by the user
- Completely open source

## Using launchii

Right now launchii is early in development and needs to be launched by checking out the project.

```console
$ git clone https://github.com/SmatMan/launchii
$ cd launchii
$ python -m venv venv
$ # activate your environment, different per platform
$ pip install poetry
$ poetry install
$ launchii --cli # for cli
$ launchii --gui # for gui
```

To run unit tests
```console
$ poetry run pytest
```

## Contributions?
Yes please! Contributions/PRs are highly appreciated!
