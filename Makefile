full-install:
	poetry install
	poetry build
	python3 -m pip install dist/*.whl
install:
	poetry install
csv-parser-run:
	poetry run csv-parser-run
csv-parser-training:
	poetry run csv-parser-training
csv-parser-alt:
	poetry run csv-parser-alt
build:
	poetry build
package-install:
	python3 -m pip install dist/*.whl
package-reinstall:
	python3 -m pip install --force-reinstall dist/*.whl
build-reinstall:
	poetry build
	python3 -m pip install --force-reinstall dist/*.whl
uninstall:
	pip uninstall csv-parser
