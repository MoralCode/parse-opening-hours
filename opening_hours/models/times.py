from opening_hours.models.time import Time, TimeType
from opening_hours.patterns import timerange
import logging, os
from opening_hours.helpers import normalize_string

logger = logging.getLogger(__name__)

class Times():
	"""
	Similar to Days, this class represents a range of times and provides methods
	to help reate them from common shortcuts. No iterator here though since
	there isnt really a need to iterate over every single time within a range.
	"""
	start_time = None
	end_time = None
	
	@classmethod
	def parse(cls, times_string, assume_type=None):
		"""
		parse a time object from a string using the pyparsing patterns for a time range
		This function will normalize the input value first and will raise a TypeError if None is given.
		"""
		logger.debug("creating times object from string: " + times_string)
		if times_string is None:
			raise TypeError("Cannot create Times Object from value None")
			
		times_string = normalize_string(times_string)

		return cls.from_parse_results(timerange.parseString(times_string), assume_type=assume_type)

	@classmethod
	def from_parse_results(cls, result, assume_type=None):
		"""
		Takes values from pyparsing results and converts them to an instance of this object. This makes heavy use of the output names defined for certain patterns to help pick out only the relevant data.
		This is primarily for internal use and is helpful when combined with the parse() functions of this or other objects.
		"""
		# assumes that all three (hours, minutes, am_pm) are the same length
		res_dct = result.asDict()
		if "starttime" in res_dct and "endtime" in res_dct: 
			logger.info("time range detected")
			start = res_dct.get("starttime")[0]
			starttime = Time.from_parse_results(start)
			
			end = res_dct.get("endtime")[0]
			endtime = Time.from_parse_results(end)
			
			if starttime.is_unknown() and assume_type is not None:
				starttime.set_type(assume_type)

			if endtime.is_unknown() and assume_type is not None:
				endtime.set_type(assume_type)


			if starttime.is_am() and endtime.is_am() and starttime.get_hours() > endtime.get_hours():
				endtime.set_type(TimeType.PM)

			return cls(starttime, endtime)
		elif "time_shortcuts" in res_dct: 
			logger.info("time shortcut detected")
			return cls.from_shortcut_string(result.get("time_shortcuts")[0])
		else:
			logger.info("unspecified time pattern detected")
			logger.debug(vars(result))
			# nothing specified, assumeit means every day
			return cls(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))

	@classmethod
	def from_shortcut_string(cls, times_shortcut, assume_type=None):
		"""
		create a times object from a shortcut string, such as are used to represent time ranges such as "24 hours", or "work hours".

		This is primarily for internal use and is helpful when combined with the parse() functions of this or other objects.

		"""
		logger.debug("creating times object from shortcut: " + (times_shortcut or "None"))
		if times_shortcut is None:
			raise TypeError("Cannot create Times Object from value None")
			
		times = times_shortcut.lower()

		# set up some shortcut ranges
		allday = cls(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))
		workhours = cls(Time(9, 0, TimeType.AM), Time(5, 0, TimeType.PM))
		closed = cls(None, None)

		if "24" in times:
			return allday
		elif "business" in times:
			return workhours
		elif "work" in times:
			return workhours
		elif "all day" in times:
			return allday
		elif "closed" in times:
			return closed
		elif "null" in times:
			return closed


		raise ValueError("string '" + times_shortcut or "[NoneType]" + "' does not match a known pattern")

		
	def __init__(self, start_time, end_time):
		"""
		Creates a Times object from two Time objects
		"""
		# if start_time is None or end_time is None:
		# 	raise TypeError("Cannot create Times Object from value None")
	
		logger.debug("creating times from " + str(start_time or "None") + " and " + str(end_time or "None"))

		self.start_time = start_time
		self.end_time = end_time

	def get_start_time(self):
		return self.start_time
	
	def get_end_time(self):
		return self.end_time
	
	def is_closed(self):
		has_none = self.start_time is None or self.end_time is None
		times_match = self.start_time == self.end_time
		return has_none or times_match

	#TODO: possibly add a function to see if a single Time is within the range 
	# specified by this Times object 


	#TODO: getduration function
	
	def __str__(self):
		if self.is_closed():
			return "closed"
		else:
			return self.start_time + " to " + self.end_time

	
	def __eq__(self, other):
		if not isinstance(other, Times):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.start_time == other.start_time and self.end_time == other.end_time 


