# Python Opening Hours parser
This library parses opening hours from various human-readable strings such as "Mon- Fri 9:00am - 5:30pm" into a more standard JSON format that can be processed more easily.

## The format
```json
opening_hours = [
	{
		"day": "monday",
		"opens": "9:00",
		"closes": "5:00"
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

## Tests

run `python3 -m unittest`