# Python Opening Hours parser

[![CircleCI](https://circleci.com/gh/MoralCode/parse-opening-hours.svg?style=shield)](https://circleci.com/gh/MoralCode/parse-opening-hours)
[![codecov](https://codecov.io/gh/MoralCode/parse-opening-hours/branch/main/graph/badge.svg?token=7JUFXSX43N)](https://codecov.io/gh/MoralCode/parse-opening-hours)
[![Downloads](https://pepy.tech/badge/parse-opening-hours/month)](https://pepy.tech/project/parse-opening-hours)

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
`pip install parse-opening-hours`

## Usage

The simplest example is just printing the JSON for an opening hours string:
```python
from opening_hours import OpeningHours

print(OpeningHours.parse("Mon- Fri 9:00am - 5:30pm").json())
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
### Documentation
In addition to this README, there is some documentation generated from inline documentation comments. This is available at https://moralcode.github.io/parse-opening-hours/ 
### Environment variables
Setting the environment variable `OH_DEBUG` to a value of `Y` will set the root logging level to debug and will cause log entries to appear in stdout for debugging purposes

## Troubleshooting
### Assumptions
When specifying a time without AM or PM indicators, you may get an error that reads `TypeError: Cannot convert a time of unknown type (AM, PM or 24H) without assuming its type.`. To resolve this, pass `assume_type=TimeType.AM` when calling the `parse()` function. This will use AM in place of an unknown AM or PM designation. In cases like the string "9-5", if the second value in the range (in this case the `5` is smaller than the first (i.e. the `9`) then it will be converted to PM automatically

## Tests and Coverage

run pytet and generate coverage database `pipenv run pytest --cov=./`

show coverage report: `pipenv run coverage report`