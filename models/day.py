import enum
from patterns import *
from helpers import int_from_parsed, str_from_parsed
import logging, os

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)

class DaysEnum(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
	

class Day(DaysEnum):

	@classmethod
	def from_string(cls, string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating time object from string: " + string)
		result = time.parseString(string)
		hours = int_from_parsed(result, "hour")
		minutes = int_from_parsed(result, "minute")
		am_pm = str_from_parsed(result, "am_pm")
		
		time_obj = cls(hours, minutes)
		time_obj.set_type_from_string(am_pm)

		if time_obj.is_unknown() and assume_type is not None:
			time_obj.set_type(assume_type)

		return time_obj

	def __init__(self):
		pass
			
	
	def to_string(self, format_str='{:d}:{:02d}'):
		return format_str.format(self.hours, self.minutes)
	
	def __eq__(self, other):
		if not isinstance(other, Time):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		pass




def str_to_days(day_string):
	logger.debug(day_string)

	if day_string is None:
		return None
	day = day_string.lower()

	allweek = expand_day_range(Day.MONDAY, Day.SUNDAY)
	workweek = expand_day_range(Day.MONDAY, Day.FRIDAY)

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
		return expand_day_range(Day.SATURDAY, Day.SUNDAY)
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
	for weekday in list(Day):
		if weekday.value.startswith(day):
			day_enum = weekday

	# length checks to deal with ambiguous cases
	if len(day) == 1:
		if day_enum in [Day.SATURDAY, Day.SUNDAY]:
			return None
		elif day_enum == Day.THURSDAY:
			return Day.TUESDAY
	return day_enum

# @PendingDeprecationWarning
def day_to_str(day):
	return day.value