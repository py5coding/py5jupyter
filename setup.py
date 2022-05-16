# *****************************************************************************
#
#   Part of the py5jupyter (& py5) library
#   Copyright (C) 2022 Jim Schmitz
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
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
    skip_if_exists
)

HERE = os.path.dirname(os.path.abspath(__file__))

name = 'py5jupyter'

with open('README.md') as f:
    README = f.read()

VERSION = get_version(pjoin(name, '_version.py'))

# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, 'nbextension', 'index.js'),
    pjoin(HERE, name, 'labextension', 'package.json'),
]

package_data_spec = {
    name: [
        'nbextension/**js*',
        'labextension/**'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/py5jupyter', 'py5jupyter/nbextension', '**'),
    ('share/jupyter/labextensions/jupyter-py5', 'py5jupyter/labextension', '**'),
    ('share/jupyter/labextensions/jupyter-py5', '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'py5jupyter.json'),
]

cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
npm_install = combine_commands(
    install_npm(HERE, build_cmd='build:prod'),
    ensure_targets(jstargets),
)
cmdclass['jsdeps'] = skip_if_exists(jstargets, npm_install)

setup_args = dict(
    name=name,
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        'ipywidgets>=7.0.0',
        'py5>=0.7.2',
    ],
    description='Jupyter tools for py5',
    long_description=README,
    long_description_content_type='text/markdown',
    cmdclass=cmdclass,
    url='https://py5.ixora.io/',
    author='Jim Schmitz',
    author_email='jim@ixora.io',
    download_url='https://pypi.org/project/py5jupyter',
    project_urls={
        "Bug Tracker": 'https://github.com/py5coding/py5jupyter/issues',
        "Documentation": 'https://py5.ixora.io/',
        "Source Code": 'https://github.com/py5coding/py5jupyter',
    },
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython', 'Processing'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Java',
    ],
    extras_require={
        'test': [
            'pytest>=4.6',
            'pytest-cov',
            'nbval',
        ],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'jupyter_sphinx',
            'nbsphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
            'recommonmark',
            'sphinx>=1.5',
            'sphinx_rtd_theme',
        ],
    },
)

if __name__ == '__main__':
    setup(**setup_args)
