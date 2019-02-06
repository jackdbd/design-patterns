# design-patterns

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/jackdbd/design-patterns.svg?branch=master)](https://travis-ci.org/jackdbd/design-patterns) [![Python 3](https://pyup.io/repos/github/jackdbd/design-patterns/python-3-shield.svg)](https://pyup.io/repos/github/jackdbd/design-patterns/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Some of the most common design patterns implemented in Python.

## Installation

This project uses [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://poetry.eustace.io/).

```shell
pyenv install 3.7.2
pyenv local 3.7.2
```

Install all the dependencies from the `poetry.lock` file.

```shell
poetry install
```


## Tests

If you want you can run all tests with:

```shell
pytest
```

You can also test the MVC pattern with:

```shell
cd mvc
poetry run python model_view_controller.py
```