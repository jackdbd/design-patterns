# design-patterns

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Some of the most common design patterns implemented in Python.

> :warning: **READ THIS** :warning:
>
> *Design patterns are spoonfeed material for brainless programmers incapable of independent thought, who will be resolved to producing code as mediocre as the design patterns they use to create it*.
>
> — [Christer Ericson](https://realtimecollisiondetection.net/blog/?p=81), VP of Technology at Activision Central Tech.
>
> When I started programming, I thought that a serious programmer should have to know all major design patterns described in the book [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns), and religiously write code that would follow them.
>
> Over time, I realized that only a few of these patterns are actually good, most of them are bad, some others are completely unnecessary, especially in a dynamic language like Python. In fact, I don't recall having to use most of them, except for maybe Decorator, Observer and Strategy.
>
> Before reading the code in this repository, I suggest you have a look at these resources to understand whether a particular design pattern suits your use-case or not:
> - [Design Patterns and Anti-Patterns, Love and Hate](https://www.yegor256.com/2016/02/03/design-patterns-and-anti-patterns.html) — Yegor Bugayenko
> - [Design Patterns in Dynamic Languages](https://norvig.com/design-patterns/) — Peter Norvig

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

## Usage

Every python file contains an implementation of a design pattern and a simple example that can help you understand where the pattern might be useful.

For example

```shell
python observer.py
python strategy.py
# etc...
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
