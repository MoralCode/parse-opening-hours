import enum
import logging

logger = logging.getLogger(__name__)
class Weekday(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

	
def detect_if_pm(string):
	return "p" in string.lower()


def str_to_days(day_string):
	logger.debug(day_string)

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

	day_enum = None

	# TODO: change to if "tuesday".startswith(day)
	for weekday in list(Weekday):
		if weekday.value.startswith(day):
			day_enum = weekday

	# length checks guard against matching a single "s", since this is ambiguous
	if day_enum == Weekday.SATURDAY and len(day) == 1:
		return None
	else:
		return day_enum


def day_to_str(day):
	return day.value


def expand_day_range(start_day, end_day):
	if end_day is None:
		return [start_day]
	days = []
	count_day=False #flag to help determine which days should be included
	all_days = enumerate(Weekday)
	for _,day in all_days:
		if day == start_day:
			count_day = True

		if count_day:
			days.append(day)

		if day == end_day:
			count_day = False
		
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