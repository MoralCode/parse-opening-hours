# Python Opening Hours parser

[![CircleCI](https://circleci.com/gh/MoralCode/parse-opening-hours.svg?style=shield)](https://circleci.com/gh/MoralCode/parse-opening-hours)
[![codecov](https://codecov.io/gh/MoralCode/parse-opening-hours/branch/main/graph/badge.svg?token=7JUFXSX43N)](https://codecov.io/gh/MoralCode/parse-opening-hours)
[![Downloads](https://pepy.tech/badge/parse-opening-hours/month)](https://pepy.tech/project/parse-opening-hours)

This library parses opening hours from various human-readable strings such as "Mon- Fri 9:00am - 5:30pm" into a more standard JSON format that can be processed more easily.

## Usage
### What can/can't it do?

This library can currently handle most opening hours strings where there is a single range of times for a set of days.

For examples of what it can do, see the Changelog on the releases page or take a look at the unit tests.

The goal is to eventually support more different formats of strings but as of now, opening hours containing these things may not be supported:
- notes or arbitrary sentences such as "by appointment only"
- Specific dates, such as "4/27/21 at 9am"
- Lists of date-time opening hours, such as "Mon - Fri: 8am-2pm, Sat: 10am-2pm"
- Opening hours formats that are in formats that arent commonly used by English-speakers in the United States

### Installation
`pip install parse-opening-hours`

### Usage

The simplest example is just printing the JSON for an opening hours string:
```python
from opening_hours import OpeningHours

print(OpeningHours.parse("Mon- Fri 9:00am - 5:30pm").json())
```

This should give you the below output:
```json
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

Use this command to run pytest and generate coverage data `pipenv run pytest --cov=./`
To see all the logs during tests (for debugging. warning, there are a lot of them), add the `--log-cli-level=10 ` parameter

To show the coverage report: `pipenv run coverage report`

To generate an HTML coverage report: `pipenv run coverage html`

