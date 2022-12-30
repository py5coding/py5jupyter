py5jupyter_ts = $(shell find src/ -name "*.ts")
py5jupyter_py = $(shell find py5jupyter/ -name "*.py")
py5jupyter_build = dist/
py5jupyter_installed = .install_py5jupyter.nogit

all: install

# YOU MUST INITIALIZE NPM BEFORE ATTEMPTING TO RUN THE BUILD
init:
	npm install

build: $(py5jupyter_build)
$(py5jupyter_build): $(py5jupyter_ts) $(py5jupyter_py)
	hatch build
	touch $(py5jupyter_build)

install: $(py5jupyter_installed)
$(py5jupyter_installed): $(py5jupyter_build)
	pip install ./dist/py5jupyter*.tar.gz
	touch $(py5jupyter_installed)

clean:
	hatch clean
	rm -Rf $(py5jupyter_build)
	rm -f $(py5jupyter_installed)
