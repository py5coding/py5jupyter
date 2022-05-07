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

import jpype
import py5

MouseEvent = jpype.JClass('processing.event.MouseEvent')


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
        if content.get("event", "") == "mouse_move":
            me = MouseEvent(None, 0, MouseEvent.MOVE, 0, int(content["x"]), int(content["y"]), py5.LEFT, 0)
            self.sketch._instance.postEvent(me)
        # if content.get("event", "") == "mouse_down":
