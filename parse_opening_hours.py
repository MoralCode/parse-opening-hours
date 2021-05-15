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
from models.day import Day, DaysEnum
from models.days import Days
from models.time import Time, TimeType
import unicodedata
import os
import logging
logging.basicConfig()

logger = logging.getLogger(__name__)

if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)

class OpeningHours():

	@classmethod
	def parse(self, hours_string, assume_type=None):

		hours_string = unicodedata.normalize('NFC', hours_string)

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
	res_dct = result.asDict()

	start = res_dct.get("starttime")[0]
	starttime = Time.from_parse_results(start)
	
	end = res_dct.get("endtime")[0]
	endtime = Time.from_parse_results(end)
	
	if starttime.is_unknown() and assume_type is not None:
		starttime.set_type(assume_type)

	if endtime.is_unknown() and assume_type is not None:
		endtime.set_type(assume_type)


	if starttime.is_am() and endtime.is_am() and starttime.get_hours() > endtime.get_hours():
		endtime.set_type(TimeType.PM)

	return (
		str(starttime.get_as_military_time()),
		str(endtime.get_as_military_time())
		)

# TODO: testme

def convert_to_dict(result, assume_type=None):

	opening_hours_json = []
	logger.debug(result.dump())
	logger.debug(vars(result))
	logger.debug(result["starttime"])
	logger.debug(result.get("starttime").get("hours"))

	days = Days.from_parse_results(result)
	
	start_time, end_time = parse_times(result, assume_type=assume_type)
	

	for day in days:
		opening_hours_json.append(
			create_entry(
				str(day),
				start_time,
				end_time
			)
		)
	
	
	return opening_hours_json
