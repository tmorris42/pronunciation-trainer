ECHO OFF
python -m isort -q --skip .\env\
python -m black -q --line-length 79 pronunciation_trainer.py 
python -m black -q --line-length 79 tests/test_pronunciation_trainer.py
python -m mypy --warn-unused-ignores .
python -m flake8 pronunciation_trainer.py
python -m flake8 tests/
python -m pylint pronunciation_trainer.py
python -m pylint tests/test_pronunciation_trainer.py
python -m pytest -q
python -m bandit pronunciation_trainer.py -q
ECHO ON
