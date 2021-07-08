import logging, os
from dateutil.parser import *
from datetime import datetime, date as dt_date

logger = logging.getLogger(__name__)

class Dates():
	"""
	This class represents a set of datetime.date objects and provides
	some helpful methods for using them
	"""
	dates = set({})
	@classmethod
	def from_datetime(cls, datetime):
		"""
		create a Dates object from a datetime
		"""
		result = cls()
		result.add(datetime)
		return result
			
	@classmethod
	def from_parse_results(cls, result, assume_century=None):
		logger.debug(vars(result))
		if result is None:
			raise TypeError("Cannot create Dates Object from value None")

		def _dmy_dict_to_date(dmy_dict):
			return 

		dates = None

		datesclass = cls()

		# single day
		# list of days

		if "date" in result:
			datevalues = result.asDict().get("date")
			if isinstance(datevalues, list):
				# logger.debug(datevalues)
				for date in datevalues:
					year = int(date.get("year"))
					if year < 1000 and assume_century:
						year = (assume_century*100) + year

					datesclass.add(
						dt_date(
							year=year,
							month=int(date.get("month")),
							day=int(date.get("day"))
						)
					)

			elif isinstance(datevalues, str):
				datesclass.add(datevalues)
		
		return datesclass

	
		
	def __init__(self):
		self.dates = set({})
		
	def __str__(self):
		daystrings = [str(Day(d)) for d in self.dates]
		return "Dates<" + ''.join(daystrings) + ">"


	def add(self, date):
		if isinstance(date, dt_date):
			self.dates.add(date)
		elif isinstance(date, str):
			self.dates.add(parse(date_str).date())
		else:
			# don't attempt to add unrelated types
			raise NotImplementedError()

	def __iter__(self):
		return iter(self.sort())

	def sort(self):
		return sorted(self.dates)
	
	def __eq__(self, other):
		if not isinstance(other, Dates):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.dates == other.dates


