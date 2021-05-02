import enum
from ..patterns import *
from helpers import int_from_parsed, str_from_parsed

class TimeType(enum.Enum):
	UNKNOWN = 0
	AM = 1
	PM = 2
	MILITARY = 3
	

class Time:
	hours = None
	minutes = None
	time_type = TimeType.UNKNOWN

	@classmethod
	def from_string(cls, string, assume_type=None):
		"""
		create a time object from a string
		"""
		result = time.parseString(string)
		hours = int_from_parsed(result, "hour")
		minutes = int_from_parsed(result, "minute")
		am_pm = str_from_parsed(result, "am_pm")
		
		time_obj = cls(hours, minutes)
		time_obj.set_type_from_string(am_pm)

		return time_obj

	def __init__(self, hours, minutes, time_type=TimeType.UNKNOWN):
		self.hours = hours
		self.minutes = minutes
		self.time_type = time_type or TimeType.UNKNOWN

		# automatically detect the time as military time if the hours are set to a value > 12
		if self.is_unknown() and self.hours > 12:
			self.set_type(TimeType.MILITARY)

	def get_type(self):
		return self.time_type
	
	def get_hours(self):
		return self.hours

	def get_minutes(self):
		return self.minutes
	
	def set_type(self, time_type):
		self.time_type = time_type

	def set_type_from_string(self, time_type_str):
		if "p" in time_type_str.lower():
			self.set_type(TimeType.PM)
		elif "a" in time_type_str.lower():
			self.set_type(TimeType.AM)
		else:
			self.set_type(TimeType.UNKNOWN)

	def is_24_hr(self):
		return self.time_type == TimeType.MILITARY

	def is_unknown(self):
		return self.time_type == TimeType.UNKNOWN
	
	def is_12_hour(self):
		return not self.is_24_hour() and not self.is_unknown()

	def is_am(self):
		return self.time_type == TimeType.AM

	def is_pm(self):
		return self.time_type == TimeType.PM

	def get_as_military_time(self):
		hours = self.hours

		if self.is_unknown():
			raise TypeError("Cannot convert a time of unknown type without assuming its type.")

		elif self.is_24_hr():
			return self
		
		elif self.is_am():
			pass
		
		elif self.is_pm():
			hours = hours + 12
		
		return Time(hours, self.minutes, time_type=TimeType.MILITARY)
			
	
	def to_string(self, format_str='{:d}:{:02d}'):
		return format_str.format(self.hours, self.minutes)