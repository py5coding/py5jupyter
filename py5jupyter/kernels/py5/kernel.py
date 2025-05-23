# *****************************************************************************
#
#   Part of the py5jupyter (& py5) library
#   Copyright (C) 2022-2025 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 2.1 of the License, or (at
#   your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
#   General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this library. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
import sys

from ipykernel.ipkernel import IPythonKernel
from ipykernel.kernelapp import IPKernelApp
from ipykernel.zmqshell import ZMQInteractiveShell
from IPython.core.interactiveshell import InteractiveShellABC
from py5_tools import __version__ as __py5_version__
from py5_tools.parsing import Py5CodeValidation, TransformDynamicVariablesToCalls
from traitlets import Instance, List, Type, Unicode

_PY5_HELP_LINKS = [
    {"text": "py5 Documentation", "url": "http://py5coding.org/"},
    {
        "text": "py5 Function Reference",
        "url": "http://py5coding.org/reference/sketch.html",
    },
]

_MACOSX_PRE_STARTUP = """
get_ipython().run_line_magic('gui', 'osx')
"""

_DEFAULT_STARTUP = """
import py5_tools
py5_tools.set_imported_mode(True)

try:
    import py5javafx
except ImportError:
    pass

from py5 import *
from py5_tools import sketch_portal
"""

_KERNEL_STARTUP = (
    _MACOSX_PRE_STARTUP if sys.platform == "darwin" else ""
) + _DEFAULT_STARTUP


class Py5Shell(ZMQInteractiveShell):

    ast_transformers = List(
        [TransformDynamicVariablesToCalls(), Py5CodeValidation()]
    ).tag(config=True)

    banner2 = Unicode(
        "py5 "
        + __py5_version__
        + " | py5 kernel 0.1.3a0 | A Python Jupyter kernel plus py5 in imported mode"
    ).tag(config=True)


InteractiveShellABC.register(Py5Shell)


class Py5Kernel(IPythonKernel):
    shell = Instance(
        "IPython.core.interactiveshell.InteractiveShellABC", allow_none=True
    )
    shell_class = Type(Py5Shell)

    help_links = List([*IPythonKernel.help_links.default(), *_PY5_HELP_LINKS]).tag(
        config=True
    )

    implementation = "py5"
    implementation_version = "0.1.3a0"


class Py5App(IPKernelApp):
    name = "py5-kernel"

    kernel_class = Type(
        "py5jupyter.kernels.py5.Py5Kernel", klass="ipykernel.kernelbase.Kernel"
    ).tag(config=True)

    exec_lines = List(Unicode(), [_KERNEL_STARTUP]).tag(config=True)

    extensions = List(Unicode(), ["py5_tools.magics", "py5_tools.magics.py5bot"]).tag(
        config=True
    )
