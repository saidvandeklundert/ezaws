# ezaws

An easy interface to work with the cloud.


To run the tests, make sure that the lib is installed first:
```
pip install -e src/
python -m pytest tests/ -v
python -m black --check .
python -m mypy src/
python -m coverage run -m pytest .\tests\
python -m coverage report -m
```



Work in progress