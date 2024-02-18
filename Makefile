reqs: constraint.txt requirements.txt requirements-dev.txt

PIP_COMPILE_ARGS=--no-emit-index-url \
	--constraint=constraint.txt \
	--strip-extras \
	--allow-unsafe

constraint.txt: pyproject.toml
	pip-compile \
	${PIP_COMPILE_ARGS} \
	--all-extras  \
	--output-file constraint.txt

requirements.txt: pyproject.toml
	pip-compile \
	${PIP_COMPILE_ARGS} \
	--output-file requirements.txt

requirements-dev.txt: pyproject.toml
	pip-compile \
	${PIP_COMPILE_ARGS} \
	--output-file requirements-dev.txt \
	--extra dev

requirements-prod.txt: pyproject.toml
	pip-compile \
	${PIP_COMPILE_ARGS} \
	--output-file requirements-prod.txt \
	--extra prod