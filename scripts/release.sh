#!/bin/bash

# make sure all tests pass
pipenv run pytest --cov=./

sleep 5

git stash --include-untracked

rm -rf dist/

python3 setup.py sdist bdist_wheel

twine check dist/*

twine upload dist/*