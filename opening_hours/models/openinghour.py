from opening_hours.models.day import Day, DaysEnum
from opening_hours.models.days import Days
from opening_hours.models.time import Time, TimeType
from opening_hours.models.times import Times
from opening_hours.models.dates import Dates

import os
import logging

logger = logging.getLogger(__name__)

if os.getenv("OH_DEBUG") == "Y":
	logging.basicConfig(level=logging.DEBUG)

class OpeningHour():
	"""
	this class represents a single set of open hours for a single day, day range, day list, or date. This is essentially [Day(s)/date(s)]: [Time(s)].

	Most importantly, this represents a grouping where the provided apply to every day and date listed.
	"""
	days = None
	dates = None
	times = None

	@classmethod
	def from_parse_results(cls, parse_results, assume_type=None):
		days = Days.from_parse_results(parse_results)

		dates = Dates.from_parse_results(parse_results)
		
		times = Times.from_parse_results(parse_results, assume_type=assume_type)

		return cls(days, dates, times)


	def __init__(self, days, dates, times):
		self.days = days
		self.dates = dates
		self.times = times