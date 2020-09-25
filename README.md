# design-patterns

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/jackdbd/design-patterns.svg?branch=master)](https://travis-ci.org/jackdbd/design-patterns) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Some of the most common design patterns implemented in Python.

## Installation

This project uses [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage the Python virtual environment, and [poetry](https://poetry.eustace.io/) to manage the project dependencies.

If you don't have python `3.x.x`, you have to install it. For example, I'm using `3.7.9`.

```shell
pyenv install 3.7.9
```

Create a virtual environment and activate it.

```shell
pyenv virtualenv 3.7.9 design_patterns
pyenv activate design_patterns
```

Install all the dependencies from the `poetry.lock` file.

```shell
poetry install
```

## Tests

If you want you can run all tests with:

```shell
poetry run pytest --verbose
```

You can also test the MVC pattern with:

```shell
cd mvc
poetry run python model_view_controller.py

# or simply
python mvc/model_view_controller.py
```

## Troubleshooting

If you use pyenv and get the error `"No module named '_ctypes'"` on Ubuntu, you are probably missing the `libffi-dev` package. See [this answer](https://stackoverflow.com/a/60374453/3036129).

If you get `Error: pg_config executable not found.` on Ubuntu, install the `libpq-dev` package. See [here](https://stepupautomation.wordpress.com/2020/06/23/install-psycopg2-with-pg_config-error-in-ubuntu/).
