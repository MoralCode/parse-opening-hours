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
from helpers import detect_if_pm, str_to_day, str_to_days, day_to_str, expand_day_range, value_from_parsed, str_from_parsed, key_exists, concat_from_parsed
from models.time import Time, TimeType


class JsonOpeningHours():

	@classmethod
	def parse(self, hours_string, assume_type=None):

		opening_hours_format = Or([
			OneOrMore(dates + day_time_separators + timerange + notes),
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
		start.get_as_military_time().to_string(),
		end.get_as_military_time().to_string()
		)

# TODO: testme
def is_day_range(result):
	return key_exists(result, "startday")

def is_day_list(result):
	return key_exists(result, "day")

def is_day_shortcut(result):
	return key_exists(result, "day_shortcuts")

# TODO: testme
def parse_days(result):
	days = []

	if is_day_range(result):
		# this is a date range that includes the intervening days
		start_day = str_to_day(str_from_parsed(result, "startday"))
		end_day = str_from_parsed(result, "endday", default=None)
		end_day = str_to_day(end_day[0]) if end_day is not None else end_day
		days = expand_day_range(start_day, end_day)
	elif is_day_list(result):
		days = [ str_to_day(day) for day in value_from_parsed(result, "day") ]
	elif is_day_shortcut(result):
		days = str_to_days(concat_from_parsed(result, "day_shortcuts"))
	return days

def convert_to_dict(result, assume_type=None):

	opening_hours_json = []

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
