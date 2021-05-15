import enum
from patterns import *
import logging, os

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)

class TimeType(enum.Enum):
	UNKNOWN = None
	AM = "am"
	PM = "pm"
	MILITARY = "mil"
	

class Time:
	hours = None
	minutes = None
	time_type = TimeType.UNKNOWN

	@classmethod
	def from_string(cls, string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating time object from string: " + string)
		if string is None:
			raise TypeError("Cannot create Time from None")
		elif string == "":
			raise ValueError("Cannot create Time from empty string")
		
		result = clocktime.parseString(string)
		hours = result.get("hour")
		minutes = result.get("minute")
		am_pm = result.get("am_pm")
		
		time_obj = cls(hours, minutes)
		time_obj.set_type_from_string(am_pm)

		if time_obj.is_unknown() and assume_type is not None:
			time_obj.set_type(assume_type)

		return time_obj
	
	@classmethod
	def from_shortcut(cls, string):
		"""
		create a time object from a string
		"""
		logger.debug("creating time object from shortcut: " + string)
		if string is None:
			raise TypeError("Cannot create Time from None")
		elif string == "":
			raise ValueError("Cannot create Time from empty string")
			
		string = string.lower()

		if "midnight" in string:
			return cls(0,0,time_type=TimeType.MILITARY) 
		elif "noon" in string:
			return cls(12,0,time_type=TimeType.MILITARY) 
		
		raise ValueError("Cannot match given shortcut string '" + string + "' to a known time shortcut pattern")

	@classmethod
	def from_parse_results(cls, result_dict):
		time = None
		if "hour" in result_dict and "minute" in result_dict:
			time = cls(result_dict.get("hour"), result_dict.get("minute"))

			if "am_pm" in result_dict:
				time.set_type_from_string(result_dict.get("am_pm"))

		elif "time_shortcut" in result_dict:
			shortcut = result_dict.get("time_shortcut")
			time = cls.from_shortcut(shortcut)
		else:
			raise ValueError("No recognized keys found in provided parse results dict")

	def __init__(self, hours, minutes, time_type=TimeType.UNKNOWN):
		self.hours = hours
		self.minutes = minutes or 0
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
		if time_type_str is None and self.is_unknown():
			return # already unknown
		elif "p" in time_type_str.lower():
			self.set_type(TimeType.PM)
		elif "a" in time_type_str.lower():
			self.set_type(TimeType.AM)

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
			raise TypeError("Cannot convert a time of unknown type (AM, PM or 24H) without assuming its type.")

		elif self.is_24_hr():
			return self
		
		elif self.is_am():
			pass
		
		elif self.is_pm():
			hours = hours + 12
		
		return Time(hours, self.minutes, time_type=TimeType.MILITARY)
			
	
	def __str__(self, format_str='{:d}:{:02d}'):
		return format_str.format(self.hours, self.minutes)

	def __repr__(self):
		return 'H{:d} M{:02d} T{}'.format(self.hours, self.minutes, self.time_type.value)
	
	def __eq__(self, other):
		if not isinstance(other, Time):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.hours == other.hours and self.minutes == other.minutes and self.time_type == other.time_type