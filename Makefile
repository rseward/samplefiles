lint:
	ruff check

test:
	python -m unittest discover -s tests

clean:
	rm -rf test_src test_dst
	find . -name "__pycache__" -exec rm -rf {} \;
