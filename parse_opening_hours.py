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
from models.times import Times
import unicodedata
import os
import logging

logger = logging.getLogger(__name__)

if os.getenv("OH_DEBUG") == "Y":
	logging.basicConfig(level=logging.DEBUG)

class OpeningHours():
	"""This is the main, class responsible for parsing and returning representations of opening hours strings. It's main responsibility is to store a representation of a string representing business opening hours using objects that represent more specific pieces of the opening hours string."""

	@classmethod
	def parse(cls, hours_string, assume_type=None):
		"""This parse function allows an OpeningHours instance to be created from most arbitrary strings representing opening hours using pyparsing."""

		hours_string = unicodedata.normalize('NFC', hours_string)

		hours_string = hours_string.strip()

		return cls(opening_hours_format.parseString(hours_string), assume_type=assume_type)

	
	def __init__(self, openinghours, assume_type=None):
		self.openinghours = openinghours
		self.assume_type = assume_type

	def json(self, assume_type=None):
		"""Converts the parsed results from pyparsing into the json output """
		opening_hours_json = []

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


