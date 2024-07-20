# *****************************************************************************
#
#   Part of the py5jupyter (& py5) library
#   Copyright (C) 2022-2024 Jim Schmitz
#
#   This library is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published by
#   the Free Sotware Foundation, either version 2.1 of the License, or (at
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
import time

import numpy as np

# from ipywidgets import DOMWidget
from traitlets import Bytes, CUnicode, Unicode

from ._frontend import module_name, module_version


class Py5SketchPortal:
    pass


class Py5SketchPortalArchived:  # (DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("Py5SketchPortalView").tag(sync=True)
    _model_name = Unicode("Py5SketchPortalModel").tag(sync=True)

    # Define the custom state properties to sync with the front-end
    value = Bytes(help="The frame image as bytes.").tag(sync=True)
    random_number = CUnicode(help="random number to force change event").tag(sync=True)
    width = CUnicode(
        help="Width of the image in pixels. Use layout.width " "for styling the widget."
    ).tag(sync=True)
    height = CUnicode(
        help="Height of the image in pixels. Use layout.height "
        "for styling the widget."
    ).tag(sync=True)

    def __init__(self, sketch, w, h, *args, **kwargs):
        super(Py5SketchPortal, self).__init__(*args, **kwargs)
        self.width = w
        self.height = h

        self._sketch = sketch
        self._last_event_button = 0
        self._click_count = 0
        self._last_click_time = 0
        self.on_msg(self._handle_frontend_event)

    # # Events
    def _handle_frontend_event(self, _, content, buffers):
        import py5
        from py5 import Py5KeyEvent, Py5MouseEvent

        event_type = content.get("event", "")
        event_x = int(content.get("x", 0))
        event_y = int(content.get("y", 0))
        event_mod = content.get("mod", 0)
        is_gl = self._sketch.get_graphics()._instance.isGL()

        if event_type.startswith("mouse"):
            event_button = (
                bool((b := content.get("buttons", 0)) & 1) * py5.LEFT
                or bool(b & 4) * py5.CENTER
                or bool(b & 2) * py5.RIGHT
            )

            if event_type == "mouse_enter":
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.ENTER, event_mod, event_x, event_y, event_button, 0
                )
            elif event_type == "mouse_down":
                self._note_mouse_down(event_button)
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.PRESS,
                    event_mod,
                    event_x,
                    event_y,
                    event_button,
                    self._click_count,
                )
            elif event_type == "mouse_move":
                if event_button:
                    self._sketch._instance.fakeMouseEvent(
                        Py5MouseEvent.DRAG,
                        event_mod,
                        event_x,
                        event_y,
                        event_button,
                        1 if is_gl else 0,
                    )
                else:
                    self._sketch._instance.fakeMouseEvent(
                        Py5MouseEvent.MOVE, event_mod, event_x, event_y, event_button, 0
                    )
            elif event_type == "mouse_up":
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.RELEASE,
                    event_mod,
                    event_x,
                    event_y,
                    self._last_event_button,
                    self._click_count,
                )
            elif event_type == "mouse_leave":
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.EXIT, event_mod, event_x, event_y, event_button, 0
                )
            elif event_type == "mouse_click":
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.CLICK,
                    event_mod,
                    event_x,
                    event_y,
                    self._last_event_button,
                    self._click_count,
                )
            elif event_type == "mouse_wheel":
                event_wheel = np.sign(content.get("wheel", 0))
                self._sketch._instance.fakeMouseEvent(
                    Py5MouseEvent.WHEEL,
                    event_mod,
                    event_x,
                    event_y,
                    event_button,
                    event_wheel,
                )

        elif event_type.startswith("key"):
            event_key = content.get("key", "")
            event_repeat = content.get("repeat", False)

            if event_type == "key_down":
                self._sketch._instance.fakeKeyEvent(
                    Py5KeyEvent.PRESS, event_mod, event_key, event_repeat
                )
            elif event_type == "key_press":
                self._sketch._instance.fakeKeyEvent(
                    Py5KeyEvent.TYPE, event_mod, event_key, event_repeat
                )
            elif event_type == "key_up":
                self._sketch._instance.fakeKeyEvent(
                    Py5KeyEvent.RELEASE, event_mod, event_key, event_repeat
                )

    def _note_mouse_down(self, event_button):
        t = time.time()
        if t < self._last_click_time + 0.5:
            self._click_count += 1
        else:
            self._click_count = 1
        self._last_click_time = t
        self._last_event_button = event_button
