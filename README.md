# Python Opening Hours parser
This library parses opening hours from various human-readable strings into a more standard JSON format.

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

## Usage

The simplest example is just printing the JSON for an opening hours string:
```python
print(JsonOpeningHours.parse("Mon- Fri 9:00am - 5:30pm"))
```


## Tests

run `python3 -m unittest`