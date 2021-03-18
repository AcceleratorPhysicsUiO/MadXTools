# Mad-X Tools

A simple package for reading MadX `.tfs` files in Python 3.

Written by: V. Berglyd Olsen and K.N. Sjobak

## Usage

Simple usage:

```python
from madxtools import TableFS

tfsObj = TableFS("/path/to/file")
tfsObj.convertToNumpy()

# ... your code
```

You can also re-use the object multiple times with:

```python
from madxtools import TableFS

tfsObj = TableFS()

tfsObj.readFile("/path/to/first/file")
tfsObj.convertToNumpy()

# ... your code

tfsObj.readFile("/path/to/second/file")
tfsObj.convertToNumpy()

# ... your code
```

## Installation

MadXTools can be installed automatically using `pip`.

If you are using Anaconda Python or similar, it can be installed using the command:

```pip3 install git+https://github.com/AcceleratorPhysicsUiO/MadXTools```

For “system” python, for example if you are running the standard Python that comes with
a Linux machine, it can be installed into your user home directory using the command:

```pip3 install --user git+https://github.com/AcceleratorPhysicsUiO/MadXTools```

## Test Suite

Requires python package `pytest`, and optionally, `pytest-cov`.

You can test the package with:

```bash
pytest-3 -v
```

For a coverage report, use one of the following:
```bash
pytest-3 -v --cov=madxtools
pytest-3 -v --cov=madxtools --cov-report=html
```

The latter creates a full report in a folder named `htmlcov`.
Open the `index.html` file in your browser.
