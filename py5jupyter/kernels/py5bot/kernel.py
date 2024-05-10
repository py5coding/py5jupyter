# *****************************************************************************
#
#   Part of the py5jupyter (& py5) library
#   Copyright (C) 2022-2024 Jim Schmitz
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
from ipykernel.zmqshell import ZMQInteractiveShell
from IPython.core.interactiveshell import InteractiveShellABC
from ipykernel.kernelapp import IPKernelApp

from traitlets import Type, Instance, Unicode, List

from py5_tools import split_setup
from py5_tools.parsing import (
    TransformDynamicVariablesToCalls,
    Py5CodeValidation,
    check_for_problems,
)
from py5_tools import __version__ as __py5_version__

from . import py5bot


_PY5_HELP_LINKS = [
    {"text": "py5 Documentation", "url": "http://py5coding.org/"},
    {
        "text": "py5 Function Reference",
        "url": "http://py5coding.org/reference/sketch.html",
    },
]


class Py5BotShell(ZMQInteractiveShell):

    # needed to make sure code using the %%python bypass gets transformed
    ast_transformers = List(
        [TransformDynamicVariablesToCalls(), Py5CodeValidation()]
    ).tag(config=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._py5bot_mgr = py5bot.Py5BotManager()

    banner2 = Unicode(
        "py5 "
        + __py5_version__
        + " | py5bot kernel 0.1.3a0 | A static drawing environment for py5"
    ).tag(config=True)

    def run_cell(self, raw_cell, *args, **kwargs):
        # check for special code that should bypass py5bot processing
        if raw_cell.strip().startswith("%%python\n"):
            return super(Py5BotShell, self).run_cell(
                raw_cell.replace("%%python\n", ""), *args, **kwargs
            )

        success, result = check_for_problems(raw_cell, "<py5bot>", tool="py5bot")
        if success:
            py5bot_globals, py5bot_settings, py5bot_setup = result
            if split_setup.count_noncomment_lines(py5bot_settings) == 0:
                py5bot_settings = "size(100, 100, HIDDEN)"
            self._py5bot_mgr.write_code(py5bot_globals, py5bot_settings, py5bot_setup)

            return super(Py5BotShell, self).run_cell(
                self._py5bot_mgr.run_code, *args, **kwargs
            )
        else:
            print(result, file=sys.stderr)

            return super(Py5BotShell, self).run_cell("None", *args, **kwargs)


InteractiveShellABC.register(Py5BotShell)


class Py5BotKernel(IPythonKernel):
    shell = Instance(
        "IPython.core.interactiveshell.InteractiveShellABC", allow_none=True
    )
    shell_class = Type(Py5BotShell)

    help_links = List([*IPythonKernel.help_links.default(), *_PY5_HELP_LINKS]).tag(
        config=True
    )

    implementation = "py5bot"
    implementation_version = "0.1.3a0"


class Py5BotApp(IPKernelApp):
    name = "py5bot-kernel"

    kernel_class = Type(
        "py5jupyter.kernels.py5bot.Py5BotKernel", klass="ipykernel.kernelbase.Kernel"
    ).tag(config=True)

    exec_lines = List(Unicode(), ["%%python\n" + py5bot.PY5BOT_CODE_STARTUP]).tag(
        config=True
    )
