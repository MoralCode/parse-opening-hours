import logging, os
from datetime import datetime, date as dt_date
from opening_hours.helpers import month_str_to_int

logger = logging.getLogger(__name__)

class Dates():
	"""
	This class represents a set of datetime.date objects and provides
	some helpful methods for using them
	"""
	dates = set({})
	@classmethod
	def from_date(cls, datetime):
		"""
		create a Dates object from a datetime
		"""
		result = cls()
		result.add(datetime)
		return result
			
	@classmethod
	def from_parse_results(cls, result, assume_century=None, assume_year=None):
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
				for date in datevalues:
					year = date.get("year")
					year = int(year) if year else assume_year
					month = date.get("month") or month_str_to_int(date.get("month_str"))
					month = int(month)
					if year and year < 1000 and assume_century:
						year = (assume_century*100) + year
					elif not year:
						raise TypeError("Year could not be parsed from date and one was not provided in the assume_year parameter")

					datesclass.add(
						dt_date(
							year=year,
							month=month,
							day=int(date.get("day"))
						)
					)

			elif isinstance(datevalues, str):
				datesclass.add(datevalues)
		
		return datesclass

	
		
	def __init__(self):
		self.dates = set({})
		
	def __str__(self):
		daystrings = [d.isoformat() for d in self.dates]
		return "Dates{" + ', '.join(daystrings) + "}"


	def add(self, date):
		if isinstance(date, dt_date):
			self.dates.add(date)
		else:
			# don't attempt to add unrelated types
			raise NotImplementedError()

	def __iter__(self):
		return iter(self.dates)
	
	def __eq__(self, other):
		if not isinstance(other, Dates):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.dates == other.dates


