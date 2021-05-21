#!/bin/bash


git stash --include-untracked

rm -rf ./jsonify_opening_hours.egg-info/ build/ 

# make sure all tests pass
pipenv run pytest --cov=./

sleep 5

rm -rf dist/

python3 setup.py sdist bdist_wheel

twine check dist/*

twine upload dist/*