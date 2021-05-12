import enum
import logging, os

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)
	
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
	workweek = expand_day_range(Weekday.MONDAY, Weekday.FRIDAY)

	if "weekday" in day:
		return workweek
	elif "business" in day:
		return workweek
	elif "work" in day:
		return workweek
	elif "5" in day:
		return workweek
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

	# length checks to deal with ambiguous cases
	if len(day) == 1:
		if day_enum in [Weekday.SATURDAY, Weekday.SUNDAY]:
			return None
		elif day_enum == Weekday.THURSDAY:
			return Weekday.TUESDAY
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
	logger.debug("raw key: " + key)
	logger.debug(val)
	if val is None:
		return default
	try:
		return val
	except KeyError:
		return default

def value_from_parsed(parsed, key, default=None):
	val = raw_from_parsed(parsed, key, default=None)
	logger.debug("value key: " + key)
	logger.debug(val)
	if val is None:
		return default
	return val[0]

def concat_from_parsed(parsed, key, default=None):
	val = value_from_parsed(parsed, key, default=[])
	logger.debug("concat key: " + key)
	logger.debug(val)
	return "".join(val)

def int_from_parsed(parsed, key, default=0):
	val = value_from_parsed(parsed, key, default=default)
	logger.debug("int key: " + key)
	logger.debug(str(val))
	if val is None:
		return default
	if isinstance(val, int):
		return val
	return int(val, 10)

def str_from_parsed(parsed, key, default=""):
	val = value_from_parsed(parsed, key, default=default)
	logger.debug("str key: " + key)
	logger.debug(val)
	if val is None:
		return default
	return str(val)
