import enum

class Weekday(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

	
def detect_if_pm(string):
	return "p" in string.lower()


def str_to_days(day_string):
	print(day_string)

	if day_string is None:
		return None
	day = day_string.lower()

	allweek = expand_day_range(Weekday.MONDAY, Weekday.SUNDAY)

	if "weekday" in day:
		return expand_day_range(Weekday.MONDAY, Weekday.FRIDAY)
	elif "business" in day:
		return expand_day_range(Weekday.MONDAY, Weekday.FRIDAY)
	elif "work" in day:
		return expand_day_range(Weekday.MONDAY, Weekday.FRIDAY)
	elif "5" in day:
		return expand_day_range(Weekday.MONDAY, Weekday.FRIDAY)
	elif "7" in day:
		return allweek
	elif "all" in day and "week" in day:
		return allweek
	elif "weekend" in day:
		return expand_day_range(Weekday.SATURDAY, Weekday.SUNDAY)
	elif "every" in day:
		return allweek
	elif "daily" in day:
		return allweek



def str_to_day(day_string):
	if day_string is None:
		return None
	day = day_string.lower()
	# ignore anything after the "day" part, if present
	if "day" in day:
		day = day.split("day")[0]
		day += "day"

	if day in ["m", "mon", "monday"]:
		return Weekday.MONDAY
	elif day in ["t", "tue", "tues", "tuesday"]:
		return Weekday.TUESDAY
	elif day in ["w", "wed", "wednesday"]:
		return Weekday.WEDNESDAY
	elif day in ["th", "thu", "thurs", "thursday"]:
		return Weekday.THURSDAY
	elif day in ["f", "fri", "friday"]:
		return Weekday.FRIDAY
	elif day in ["sa", "sat", "saturday"]:
		return Weekday.SATURDAY
	elif day in ["su", "sun", "sunday"]:
		return Weekday.SUNDAY

def day_to_str(day):
	if day == Weekday.MONDAY:
		return "monday"
	elif day == Weekday.TUESDAY:
		return "tuesday"
	elif day == Weekday.WEDNESDAY:
		return "wednesday"
	elif day == Weekday.THURSDAY:
		return "thursday"
	elif day == Weekday.FRIDAY:
		return "friday"
	elif day == Weekday.SATURDAY:
		return "saturday"
	elif day == Weekday.SUNDAY:
		return "sunday"


def expand_day_range(start_day, end_day):
	if end_day is None:
		return [start_day]
	days = []
	start_index = start_day.value
	end_index = end_day.value

	for index in range(start_index, end_index+1, 1):
		days.append(Weekday(index))
	return days

def raw_from_parsed(parsed, key, default=None):
	if parsed is None:
		return default

	val = parsed.get(key)
	if val is None:
		return default
	try:
		return val
	except KeyError:
		return default

def value_from_parsed(parsed, key, default=None):
	val = raw_from_parsed(parsed, key, default=None)
	if val is None:
		return default
	return val[0]

def concat_from_parsed(parsed, key, default=None):
	val = value_from_parsed(parsed, key, default=[])
	return "".join(val)

def int_from_parsed(parsed, key, default=0):
	val = value_from_parsed(parsed, key, default=default)
	if val is None:
		return default
	if isinstance(val, int):
		return val
	return int(val, 10)

def str_from_parsed(parsed, key, default=""):
	val = value_from_parsed(parsed, key, default=default)
	if val is None:
		return default
	return str(val)

# TODO: testme
def key_exists(dictionary, key):
	value = dictionary.get(key)

	return value is not None