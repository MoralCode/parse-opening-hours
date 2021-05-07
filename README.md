# Python Opening Hours parser

[![CircleCI](https://circleci.com/gh/MoralCode/jsonify-opening-hours.svg?style=shield)](https://circleci.com/gh/MoralCode/jsonify-opening-hours)
[![codecov](https://codecov.io/gh/MoralCode/jsonify-opening-hours/branch/main/graph/badge.svg?token=7JUFXSX43N)](https://codecov.io/gh/MoralCode/jsonify-opening-hours)
[![Downloads](https://pepy.tech/badge/jsonify-opening-hours/month)](https://pepy.tech/project/jsonify-opening-hours)

This library parses opening hours from various human-readable strings such as "Mon- Fri 9:00am - 5:30pm" into a more standard JSON format that can be processed more easily.

## The format
```json
opening_hours = [
	{
		"day": "monday",
		"opens": "9:00",
		"closes": "17:00"
	},
	//..
]
```
## Installation
`pip install jsonify-opening-hours`

## Usage

The simplest example is just printing the JSON for an opening hours string:
```python
from parse_opening_hours import JsonOpeningHours

print(JsonOpeningHours.parse("Mon- Fri 9:00am - 5:30pm"))
```

This should give you the below output:
```
[
	{'day': 'monday', 'opens': '9:00', 'closes': '17:30'},
	{'day': 'tuesday', 'opens': '9:00', 'closes': '17:30'},
	{'day': 'wednesday', 'opens': '9:00', 'closes': '17:30'},
	{'day': 'thursday', 'opens': '9:00', 'closes': '17:30'},
	{'day': 'friday', 'opens': '9:00', 'closes': '17:30'}
]
```

This has been tested using Python 3.8.5

## Tests and Coverage

run pytet and generate coverage database `pipenv run pytest --cov=./`

show coverage report: `pipenv run coverage report`

## Build and Release

This is pretty much here so I can copy-paste the commands to make a new release.

build: `python setup.py sdist bdist_wheel`
check: `twine check dist/*`
upload: `twine upload dist/*`