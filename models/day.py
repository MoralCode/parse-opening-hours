import enum
from patterns import *
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
	

class Day():
	day = None
	
	@classmethod
	def from_string(cls, day_string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating day object from string: " + string)
		if day_string is None:
			raise TypeError("Cannot create Day Object from value None")
			
		day = day_string.lower()
		# ignore anything after the "day" part, if present
		if "day" in day:
			day = day.split("day")[0]
			day += "day"

		day_enum = None

		for weekday in list(DaysEnum):
			if weekday.value.startswith(day):
				day_enum = weekday

		# length checks to deal with ambiguous cases
		if len(day) == 1:
			if day_enum in [Day.SATURDAY, Day.SUNDAY]:
				raise ValueError("not enough information provided to resolve ambiguous day")
			elif day_enum == Day.THURSDAY:
				# most people will understand a day value of "T" to mean tuesday rather than thursday.
				day_enum = Day.TUESDAY
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
		if not isinstance(other, Day):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.day == other.day



