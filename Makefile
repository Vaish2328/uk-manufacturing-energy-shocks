.PHONY: install all test clean

install:
	python -m pip install -r requirements.txt

all:
	python -m src.pipeline

test:
	pytest -q

clean:
	rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
