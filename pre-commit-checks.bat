ECHO OFF
python -m isort -q --skip .\env\
python -m black -q --line-length 79 .
python -m mypy --warn-unused-ignores .
python -m flake8 .
python -m flake8 .\tests\
python -m pylint speechrecog.py
python -m pylint .\tests\test_speechrecog.py
python -m pytest -q
ECHO ON
