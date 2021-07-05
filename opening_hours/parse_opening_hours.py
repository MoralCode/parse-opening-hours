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
from opening_hours.patterns import *
from opening_hours.models.day import Day, DaysEnum
from opening_hours.models.days import Days
from opening_hours.models.time import Time, TimeType
from opening_hours.models.times import Times
from opening_hours.helpers import normalize_string
import os
import logging

logger = logging.getLogger(__name__)

if os.getenv("OH_DEBUG") == "Y":
	logging.basicConfig(level=logging.DEBUG)

class OpeningHours():
	"""This is the main, class responsible for parsing and returning representations of opening hours strings. It's main responsibility is to store a representation of a string representing business opening hours using objects that represent more specific pieces of the opening hours string.
	
	It is similar to Days in that its ultimate goal is/will be to store (possibly) multiple sets of opening hours """

	@classmethod
	def parse(cls, hours_string, assume_type=None):
		"""This parse function allows an OpeningHours instance to be created from most arbitrary strings representing opening hours using pyparsing."""
		if hours_string is None or hours_string == "":
			# TODO
			return cls(None, assume_type=None)

		hours_string = normalize_string(hours_string)
		# TODO: handle unicode confuseables
		# TODO: handle special cases taht apply to beoth data and time, like "24/7"
		
		pattern = note+opening_hours_format
		# Or([
			
			# opening_hours_format + notes_end
		# ])
		logger.debug(hours_string)
		for p in pattern.scanString(hours_string):
			logger.debug(p)


		return cls(opening_hours_format.parseString(hours_string), assume_type=assume_type)

	
	def __init__(self, openinghours, assume_type=None):
		self.openinghours = openinghours
		self.assume_type = assume_type #temporary

	def json(self, assume_type=None, default=[]):
		"""Converts the parsed results from pyparsing into the json output """
		opening_hours_json = []

		if not self.openinghours:
			return default

		# TODO: move parse days and parse times out of the json() function
		days = Days.from_parse_results(self.openinghours)
		
		times = Times.from_parse_results(self.openinghours, assume_type=assume_type or self.assume_type)
		

		for day in days:
			opening_hours_json.append(
				create_entry(
					str(day),
					str(times.get_start_time().get_as_military_time()),
					str(times.get_end_time().get_as_military_time())
				)
			)

		return opening_hours_json

	# TODO: normalize function to return the opening hours string as a string in a consistent, predictable format


def create_entry(day, opening, closing, notes=None):
	"""Creates a new JSON object representing a single time slot for a single day"""
	entry = {
		"day": day,
		"opens": opening,
		"closes": closing
	}
	if notes:
		entry["notes"] = notes
	return entry

# print(OpeningHours.parse("by appointment Sunday \u2013 Wednesday from 9 a.m. to 5 p.m."))
