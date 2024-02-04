"""For testing functions that print to stdout/stderr.

Use it like this:

with captured_output() as (out, err):
    foo()

# This can go inside or outside the `with` block
output = out.getvalue().strip()
self.assertEqual(output, 'hello world!')
"""

import sys
from contextlib import contextmanager
from StringIO import StringIO


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
