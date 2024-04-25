.PHONY: install test coverage publish clean

install:
	@poetry install --no-root --no-interaction

clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
	@rm -f coverage.xml
	@rm -rf dist

test:
	@poetry run pytest -s -vv

coverage:
	@poetry run pytest -s -vv --cov=debrid --cov-report term --cov-report xml

publish:
	@poetry publish --build
