# parse various types of strings representing opening hours for a business into machine-readable JSON
# parse into the following format:
#  [
#     {
#       day: str as lowercase day of week e.g. monday,
#       opens: str as time with facility opens on this day in format hh:mm,
#       closes: str as time with facility closes on this day in format hh:mm,
#     },
#     ...
#   ]

from pyparsing import Word, alphas, nums, oneOf, Optional, Or, OneOrMore, Char
from patterns import *
from helpers import detect_if_pm
import enum

class Weekday(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class JsonOpeningHours():

	@classmethod
	def parse(self, hours_string):

		opening_hours_format = Or([
			OneOrMore(daterange + timerange + notes),
			OneOrMore(timerange + daterange + notes)
		])	
		parsed = opening_hours_format.parseString(hours_string)
		opening_hours_json = convert_to_dict(parsed)


		return opening_hours_json



def create_entry(day, opening, closing, notes=None):
	entry = {
		"day": day,
		"opens": opening,
		"closes": closing
	}
	if notes:
		entry["notes"] = notes
	return entry

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

def parse_times(result):
	# assumes that all three (hours, minutes, am_pm) are the same length
	hours=result.get("hour")
	minutes=result.get("minute") or [0,0] # if no minutes provided, assume 0 minutes
	am_pm=result.get("am_pm")
	is_24_hr=(am_pm is None)

	hours = [int(t, 10) for t in hours]

	if not is_24_hr:
		is_pm = [detect_if_pm(s) for s in am_pm]

		hours = [militarize_hours(hours[t], is_pm[t]) for t in range(len(hours))]

	minutes = [int(t, 10) for t in minutes]
		
	return [(hours[t], minutes[t]) for t in range(len(hours))]



def militarize_hours(hours, is_pm):
	# hours = int(hours, 10)
	if is_pm:
		hours = hours + 12
	
	return hours

def stringify_time(time):
	return '{:d}:{:02d}'.format(time[0], time[1])

def convert_to_dict(result):

	opening_hours_json = []

	start_day = str_to_day(result["startday"][0])
	end_day = result.get("endday")
	end_day = str_to_day(end_day[0]) if end_day is not None else end_day
	times = parse_times(result)
	start_time = times[0]
	end_time = times[1]
	days = expand_day_range(start_day, end_day)

	for day in days:
		opening_hours_json.append(
			create_entry(
				day_to_str(day),
				stringify_time(start_time),
				stringify_time(end_time)
			)
		)

	return opening_hours_json
