build_ts:
	npm run build

build_py:
	python setup.py build && pip install .

clean:
	rm -R build/
