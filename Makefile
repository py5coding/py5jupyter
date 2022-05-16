py5jupyter_ts = $(shell find src/ -name "*.ts")
py5jupyter_ts_lib = lib/
py5jupyter_py = $(shell find py5jupyter/ -name "*.py")
py5jupyter_py_build = build/
py5jupyter_installed = .install_py5jupyter.nogit
py5jupyter_sdist = sdist/

all: install

init:
	npm install

build_ts: $(py5jupyter_ts_lib)
$(py5jupyter_ts_lib): $(py5jupyter_ts)
	npm run build
	touch $(py5jupyter_ts_lib)

build_py: $(py5jupyter_py_build)
$(py5jupyter_py_build): $(py5jupyter_py) $(py5jupyter_ts_lib)
	python setup.py build
	touch $(py5jupyter_py_build)

install: $(py5jupyter_installed)
$(py5jupyter_installed): $(py5jupyter_py_build) $(py5jupyter_ts_lib)
	python -m pip install .
	touch $(py5jupyter_installed)

distributions: $(py5jupyter_sdist)
$(py5jupyter_sdist): $(py5jupyter_installed)
	rm -Rf $(py5jupyter_sdist)
	python setup.py sdist -d $(py5jupyter_sdist) && python setup.py bdist_wheel -d $(py5jupyter_sdist)
	touch $(py5jupyter_sdist)

clean:
	rm -Rf $(py5jupyter_py_build)
	rm -Rf $(py5jupyter_ts_lib)
	rm -Rf dist/
	rm -Rf $(py5jupyter_sdist)
	rm -f $(py5jupyter_installed)
