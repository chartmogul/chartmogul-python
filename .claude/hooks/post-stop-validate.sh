#!/bin/bash
flake8 ./chartmogul 2>&1
python -m unittest 2>&1
python setup.py sdist 2>&1

exit 0
