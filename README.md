# py5jupyter (& py5)

![py5 logo](https://py5.ixora.io/_static/logo.png)

[![py5jupyter monthly downloads](https://pepy.tech/badge/py5jupyter/month)](https://pepy.tech/project/py5jupyter)

[![py5jupyter weekly downloads](https://pepy.tech/badge/py5jupyter/week)](https://pepy.tech/project/py5jupyter)

py5 is a new version of [**Processing**][processing] for Python 3.8+. It makes the Java [**Processing**][processing] jars available to the CPython interpreter using [**JPype**][jpype]. It can do just about everything [**Processing**][processing] can do, except with Python instead of Java code.

The goal of py5 is to create a new version of Processing that is integrated into the Python ecosystem. Built into the library are thoughtful choices about how to best get py5 to work with other popular Python libraries such as [numpy](https://www.numpy.org/) or [Pillow](https://python-pillow.org/).

The py5jupyter library provides Jupyter-related functionality for py5. This contains the source code for the Jupyter kernels and Jupyter widgets.

For more in-depth information about py5, see the [py5generator][py5_generator_repo] github repo.

## Installation

You can install using `pip`:

```bash
pip install py5 py5jupyter
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:

```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] py5jupyter
```

## Get In Touch

Have a comment or question? We'd love to hear from you! The best ways to reach out are:

* github [discussions](https://github.com/hx2A/py5generator/discussions) and [issues](https://github.com/hx2A/py5generator/issues)
* twitter [@py5coding](https://twitter.com/py5coding)
* [processing foundation discourse](https://discourse.processing.org/)

[py5_generator_repo]: https://github.com/hx2A/py5generator
[processing]: https://github.com/processing/processing4
[jpype]: https://github.com/jpype-project/jpype
