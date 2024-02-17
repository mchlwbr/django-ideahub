reqs: requirements.txt requirements-dev.txt

requirements.txt: pyproject.toml
	pip-compile \
	--generate-hashes \
	--no-emit-index-url \
	--strip-extras \
	--output-file requirements.txt \
	pyproject.toml

requirements-dev.txt: pyproject.toml
	echo "--constraint $(shell pwd)/requirements.txt" | \
	pip-compile \
	--generate-hashes \
	--no-emit-index-url \
	--output-file requirements-dev.txt \
	--extra dev \
	- \
	pyproject.toml