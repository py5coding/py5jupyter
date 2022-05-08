#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jim Schmitz.
# Distributed under the terms of the Modified BSD License.

# https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Custom.html

"""
TODO: Add module docstring and proper header
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, CUnicode, Bytes
from ._frontend import module_name, module_version


class Py5SketchPortal(DOMWidget):
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('Py5SketchPortalView').tag(sync=True)
    _model_name = Unicode('Py5SketchPortalModel').tag(sync=True)

    # Define the custom state properties to sync with the front-end
    value = Bytes(help="The frame image as bytes.").tag(sync=True)
    format = Unicode('jpeg', help="The format of the image.").tag(sync=True)
    width = CUnicode(help="Width of the image in pixels. Use layout.width "
                          "for styling the widget.").tag(sync=True)
    height = CUnicode(help="Height of the image in pixels. Use layout.height "
                           "for styling the widget.").tag(sync=True)

    def __init__(self, sketch, *args, **kwargs):
        super(Py5SketchPortal, self).__init__(*args, **kwargs)
        self.sketch = sketch
        self.on_msg(self._handle_frontend_event)

    # # Events
    def _handle_frontend_event(self, _, content, buffers):
        import py5
        from py5 import Py5MouseEvent, Py5KeyEvent

        event_type = content.get("event", "")
        event_x = int(content["x"])
        event_y = int(content["y"])

        if event_type == "mouse_enter":
            self.sketch._instance.fakeMouseEvent(Py5MouseEvent.ENTER, 0, event_x, event_y, py5.LEFT, 0)
        elif event_type == "mouse_down":
            self.sketch._instance.fakeMouseEvent(Py5MouseEvent.PRESS, 0, event_x, event_y, py5.LEFT, 1)
        elif event_type == "mouse_move":
            self.sketch._instance.fakeMouseEvent(Py5MouseEvent.MOVE, 0, event_x, event_y, py5.LEFT, 0)
        elif event_type == "mouse_up":
            self.sketch._instance.fakeMouseEvent(Py5MouseEvent.RELEASE, 0, event_x, event_y, py5.LEFT, 1)
        elif event_type == "mouse_leave":
            self.sketch._instance.fakeMouseEvent(Py5MouseEvent.EXIT, 0, event_x, event_y, py5.LEFT, 0)
