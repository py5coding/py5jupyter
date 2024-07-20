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
from . import widgets  # noqa
from ._version import __version__, version_info  # noqa

# def _jupyter_labextension_paths():
#     """Called by Jupyter Lab Server to detect if it is a valid labextension and
#     to install the widget
#     Returns
#     =======
#     src: Source directory name to copy files from. Webpack outputs generated files
#         into this directory and Jupyter Lab copies from this directory during
#         widget installation
#     dest: Destination directory name to install widget files to. Jupyter Lab copies
#         from `src` directory into <jupyter path>/labextensions/<dest> directory
#         during widget installation
#     """
#     return [
#         {
#             "src": "labextension",
#             "dest": "jupyter-py5",
#         }
#     ]


# def _jupyter_nbextension_paths():
#     """Called by Jupyter Notebook Server to detect if it is a valid nbextension and
#     to install the widget
#     Returns
#     =======
#     section: The section of the Jupyter Notebook Server to change.
#         Must be 'notebook' for widget extensions
#     src: Source directory name to copy files from. Webpack outputs generated files
#         into this directory and Jupyter Notebook copies from this directory during
#         widget installation
#     dest: Destination directory name to install widget files to. Jupyter Notebook copies
#         from `src` directory into <jupyter path>/nbextensions/<dest> directory
#         during widget installation
#     require: Path to importable AMD Javascript module inside the
#         <jupyter path>/nbextensions/<dest> directory
#     """
#     return [
#         {
#             "section": "notebook",
#             "src": "nbextension",
#             "dest": "py5jupyter",
#             "require": "py5jupyter/extension",
#         }
#     ]
