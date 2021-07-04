import enum
from opening_hours.patterns import *
import logging, os

logger = logging.getLogger(__name__)

class DaysEnum(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
	

class Day():
	""" Represents a single day - kinda like an enum with extra steps.
	This class essentially provides additional ways to instantiate a day enum
	from strings. Thats pretty much it. """
	day = None
	
	@classmethod
	def from_string(cls, day_string, assume_type=None):
		"""
		create a time object from a string
		"""
		if day_string is None:
			raise TypeError("Cannot create Day Object from value None")
		logger.debug("creating day object from string: " + day_string)
			
		day = day_string.lower()
		# ignore anything after the "day" part, if present
		logger.debug(day)
		if "day" in day:
			day = day.split("day")[0]
			day += "day"

		day_enum = None

		for weekday in list(DaysEnum):
			if weekday.value.startswith(day):
				day_enum = weekday

		# length checks to deal with ambiguous cases
		if len(day) == 1:
			if day_enum in [DaysEnum.SATURDAY, DaysEnum.SUNDAY]:
				raise ValueError("not enough information provided to resolve ambiguous day")
			elif day_enum == DaysEnum.THURSDAY:
				# most people will understand a day value of "T" to mean tuesday rather than thursday.
				day_enum = DaysEnum.TUESDAY
			elif day == "h":
				day_enum = DaysEnum.THURSDAY
		return cls(day_enum)
		
	def __init__(self, day):
		if day is None:
			raise TypeError("Cannot create Day Object from value None")

		if isinstance(day, str):
			self.day = DaysEnum(day)
		else:
			self.day = day
	
	def __str__(self):
		return self.day.value
	
	def __eq__(self, other):
		if isinstance(other, Day):
			return self.day == other.day
		elif isinstance(other, DaysEnum):
			return self.day == other
		else:
			# don't attempt to compare against unrelated types
			raise NotImplementedError()

	def as_enum(self):
		return self.day
		



