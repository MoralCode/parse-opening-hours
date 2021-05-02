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


def str_to_day(day_string):
	if day_string is None:
		return None
	day = day_string.lower()
	if day in ["m", "mon", "monday"]:
		return Weekday.MONDAY
	elif day in ["t", "tue", "tues", "tuesday"]:
		return Weekday.TUESDAY
	elif day in ["w", "wed", "wednesday"]:
		return Weekday.WEDNESDAY
	elif day in ["th", "thu", "thurs", "thusday"]:
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

def int_from_parsed(parsed, key, default=0):
	num = result.get("hour")
	if num is None:
		return default
	
	try:
		return int(num[0], 10)
	except KeyError:
		return default