freeze:
	pip freeze > requirements.txt

check:
	ruff check .

format:
	ruff format .
