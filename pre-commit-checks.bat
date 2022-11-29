ECHO OFF
python -m isort -q pronunciation_trainer
python -m black -q --line-length 79 pronunciation_trainer
python -m black -q --line-length 79 tests/test_pronunciation_trainer.py
python -m mypy --warn-unused-ignores pronunciation_trainer
python -m flake8 pronunciation_trainer
python -m flake8 tests
python -m pylint pronunciation_trainer
python -m pylint tests/test_pronunciation_trainer.py
python -m pytest -q
python -m bandit -r pronunciation_trainer -q
ECHO ON
