# Python analogue of MATLAB publish
# Copyright 2023 Lawrence Mitchell <wence@gmx.li>, 2023 Patrick Farrell <patrick.farrell@maths.ox.ac.uk>
# Released under BSD 3-clause license
# 2023-09-18

import inspect
import jupytext
import subprocess
import sys
import pathlib


def publish():
    """
    Analogue of MATLAB's publish function.

    This works by getting the path to the script being executed,
    interpreting it as a Jupyter notebook in the py:light format
    with jupytext, and then calling Jupyter's nbviewer to execute
    the notebook and render the output to HTML.
    """
    script = pathlib.Path(inspect.stack()[1].filename)
    nbconvert(script)


def nbconvert(script):
    with open(script, "r") as f:
        original_lines = f.readlines()
        lines = [l for l in original_lines if not l.startswith("publish()")]

    if len(lines) != len(original_lines) - 1:
        raise RuntimeError("Only one publish() call allowed")
    script_data = jupytext.reads("".join(lines), fmt="py:light")

    nb = script.with_suffix(".ipynb")
    jupytext.write(script_data, nb, fmt="ipynb")
    subprocess.check_call([sys.executable, "-m", "nbconvert", "--execute", "--no-prompt", "--to", "html", str(nb)])


def render(obj, name=None):
    """
    Render a sympy object in the published document.

    This works by getting sympy to give a latex representation,
    and then using IPython's display features to make a math cell
    for it.
    """

    from IPython.display import display, Math
    import sympy as sp

    if name:
        prestring = name + " = "
    else:
        prestring = ""

    display(Math("$$" + prestring + sp.latex(obj) + "$$"))


if __name__ == "__main__":
    import sys
    script = pathlib.Path(sys.argv[1])
    nbconvert(script)
