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
from pathlib import Path
import tempfile


PY5BOT_CODE_STARTUP = """
import functools
import ast as _PY5BOT_ast

from IPython.display import SVG as _PY5BOT_SVG

import py5_tools
py5_tools.set_imported_mode(True)
from py5 import *
from py5 import _prepare_dynamic_variables as _PY5BOT_PREPARE_DYNAMIC_VARIABLES
import py5_tools.parsing as _PY5BOT_parsing


@functools.wraps(size)
def _PY5BOT_altered_size(*args):
    import sys
    if len(args) == 2:
        args = *args, HIDDEN
    elif len(args) >= 3 and isinstance(renderer := args[2], str):
        renderer_name = {SVG: 'SVG', PDF: 'PDF', DXF: 'DXF', P2D: 'P2D', P3D: 'P3D', HIDDEN: 'HIDDEN', JAVA2D: 'JAVA2D'}.get(renderer, renderer)
        if renderer in [SVG, PDF]:
            if not (len(args) >= 4 and isinstance(args[3], str)):
                print(f'If you want to use the {renderer_name} renderer, the 4th parameter to size() must be a filename to save the {renderer_name} to.')
                args = *args[:2], HIDDEN, *args[3:]
        else:
            renderers = [HIDDEN, JAVA2D] if sys.platform == 'darwin' else [HIDDEN, JAVA2D, P2D, P3D]
            if renderer not in renderers:
                print(f'Sorry, py5bot does not support the {renderer_name} renderer' + (' on OSX.' if sys.platform == 'darwin' else '.'), file=sys.stderr)
                args = *args[:2], HIDDEN, *args[3:]
            if renderer == JAVA2D:
                args = *args[:2], HIDDEN, *args[3:]
    size(*args)


del functools
"""


PY5BOT_CODE = """
_PY5BOT_OUTPUT_ = None
reset_py5()
_PY5_NS_ = locals().copy()
_PY5_NS_['size'] = _PY5BOT_altered_size
_PY5BOT_PREPARE_DYNAMIC_VARIABLES(_PY5_NS_, _PY5_NS_)


def _py5bot_settings():
    with open('{0}', 'r') as f:
        exec(
            compile(
                _PY5BOT_parsing.transform_py5_code(
                    _PY5BOT_ast.parse(f.read(), filename='{0}', mode='exec'),
                ),
                filename='{0}',
                mode='exec'
            ),
            _PY5_NS_
        )


def _py5bot_setup():
    global _PY5BOT_OUTPUT_

    with open('{1}', 'r') as f:
        exec(
            compile(
                _PY5BOT_parsing.transform_py5_code(
                    _PY5BOT_ast.parse(f.read(), filename='{1}', mode='exec'),
                ),
                filename='{1}',
                mode='exec'
            ),
            _PY5_NS_
        )

    sketch_renderer = get_current_sketch()._instance.sketchRenderer()
    if sketch_renderer == SVG:
        _PY5BOT_OUTPUT_ = _PY5BOT_SVG()
    elif sketch_renderer != PDF:
        from PIL import Image
        load_np_pixels()
        _PY5BOT_OUTPUT_ = Image.fromarray(np_pixels()[:, :, 1:])

    exit_sketch()


run_sketch(sketch_functions=dict(settings=_py5bot_settings, setup=_py5bot_setup), block=True, _osx_alt_run_method=False)
if is_dead_from_error:
    exit_sketch()

if isinstance(_PY5BOT_OUTPUT_, _PY5BOT_SVG):
    try:
        with open(str(get_current_sketch()._instance.sketchOutputPath()), 'r') as f:
            _PY5BOT_OUTPUT_.data = f.read()
    except:
        pass

del _PY5_NS_, _py5bot_settings, _py5bot_setup

_PY5BOT_OUTPUT_
"""


class Py5BotManager:

    def __init__(self):
        self.tempdir = Path(tempfile.TemporaryDirectory().name)
        self.tempdir.mkdir(parents=True, exist_ok=True)
        self.settings_filename = self.tempdir / "_PY5_STATIC_SETTINGS_CODE_.py"
        self.setup_filename = self.tempdir / "_PY5_STATIC_SETUP_CODE_.py"
        self.startup_code = PY5BOT_CODE_STARTUP
        self.run_code = PY5BOT_CODE.format(
            self.settings_filename.as_posix(), self.setup_filename.as_posix()
        )

    def write_code(self, global_code, settings_code, setup_code):
        with open(self.settings_filename, "w") as f:
            f.write("\n" * sum(c == "\n" for c in global_code))
            f.write(settings_code)

        with open(self.setup_filename, "w") as f:
            f.write(global_code)
            f.write("\n" * sum(c == "\n" for c in settings_code))
            f.write(setup_code)
