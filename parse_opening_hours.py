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
from helpers import detect_if_pm, str_to_day, str_to_days, day_to_str, expand_day_range, value_from_parsed, str_from_parsed, concat_from_parsed, raw_from_parsed, Day
from models.time import Time, TimeType
import os
import logging
logging.basicConfig()

logger = logging.getLogger(__name__)

if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)

class JsonOpeningHours():

	@classmethod
	def parse(self, hours_string, assume_type=None):

		opening_hours_format = Or([
			OneOrMore(dates + day_time_separators + timerange),
			OneOrMore(timerange + dates + notes)
		])	
		parsed = opening_hours_format.parseString(hours_string)
		opening_hours_json = convert_to_dict(parsed, assume_type=assume_type)


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


def parse_times(result, assume_type=None):
	# assumes that all three (hours, minutes, am_pm) are the same length
	start = concat_from_parsed(result, "starttime")
	end = concat_from_parsed(result, "endtime")
	start = Time.from_string(start, assume_type=assume_type)
	end = Time.from_string(end, assume_type=assume_type)

	if start.is_am() and end.is_am() and start.get_hours() > end.get_hours():
		end.set_type(TimeType.PM)


	return (
		str(start.get_as_military_time()),
		str(end.get_as_military_time())
		)

# TODO: testme
def is_day_range(result):
	return "startday" in result

def is_day_list(result):
	return "day" in result

def is_day_shortcut(result):
	return "day_shortcuts" in result

# TODO: testme
def parse_days(result):
	days = []

	if is_day_range(result):
		logger.info("range date detected")
		# this is a date range that includes the intervening days
		start_day = str_to_day(str_from_parsed(result, "startday"))
		end_day = str_from_parsed(result, "endday", default=None)
		end_day = str_to_day(end_day[0]) if end_day is not None else end_day
		days = expand_day_range(start_day, end_day)
	elif is_day_list(result):
		logger.info("list date detected")

		days = [ str_to_day(day) for day in raw_from_parsed(result, "day") ]
	elif is_day_shortcut(result):
		logger.info("shortcut date detected")
		days = str_to_days(concat_from_parsed(result, "day_shortcuts"))
	else:
		logger.info("unspecified date detected")
		# nothing specified, assumeit means every day
		return expand_day_range(Day.MONDAY, Day.SUNDAY)
	return days

def convert_to_dict(result, assume_type=None):

	opening_hours_json = []
	logger.debug(result.dump())
	logger.debug(vars(result))
	logger.debug(result["starttime"])
	logger.debug(result.get("starttime").get("hours"))

	days = parse_days(result)
	
	start_time, end_time = parse_times(result, assume_type=assume_type)
	

	for day in days:
		opening_hours_json.append(
			create_entry(
				day_to_str(day),
				start_time,
				end_time
			)
		)
	
	
	return opening_hours_json
