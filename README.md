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
