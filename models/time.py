import enum
from ..patterns import *

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
		hours = int(result.get("hour"), 10)
		minutes = int(result.get("minute"), 10)
		am_pm = result.get("am_pm")
		
		time_obj = cls(hours, minutes)
		time_obj.set_type_from_string(am_pm)
		
		return time_obj

	def __init__(self, hours, minutes, time_type=TimeType.UNKNOWN):
		self.hours = hours
		self.minutes = minutes
		self.time_type = time_type or TimeType.UNKNOWN

	def get_type(self):
		return self.time_type
	
	def get_hours(self):
		return self.hours

	def get_minutes(self):
		return self.minutes

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
		
		return new Time(hours, self.minutes, time_type=TimeType.MILITARY)
			
	
	def to_string(self, format_str='{:d}:{:02d}'):
		return format_str.format(self.hours, self.minutes)