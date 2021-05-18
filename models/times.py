from models.time import Time, TimeType
import logging, os

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
	def from_shortcut_string(cls, times_string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating times object from shortcut: " + times_string)
		if times_string is None:
			raise TypeError("Cannot create Times Object from value None")
			
		day = times_string.lower()

		# set up some shortcut ranges
		allday = cls(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))
		workhours = cls(Time(9, 0, TimeType.AM), Time(5, 0, TimeType.PM))

		if "24" in day:
			return allday
		elif "business" in day:
			return workhours
		elif "work" in day:
			return workhours
		elif "all day" in day:
			return allday

		raise ValueError("string '" + times_string + "' does not match a known pattern")
			
	@classmethod
	def from_parse_results(cls, result, assume_type=None):
		""" Takes values from the pyparsing results and converts them to the appropriate internal objects """
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
		create a times object from a shortcut string
		"""
		logger.debug("creating times object from shortcut: " + times_shortcut)
		if times_shortcut is None:
			raise TypeError("Cannot create Times Object from value None")
			
		day = times_shortcut.lower()

		# set up some shortcut ranges
		allday = cls(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))

		if "all day" in day:
			return allday
		elif "24" in day:
			return allday
		elif day == "":
			# if no day is specified, assume the intention is all day
			return allday

		raise ValueError("string '" + times_shortcut + "' does not match a known pattern")

		
	def __init__(self, start_time, end_time):
		if start_time is None or end_time is None:
			raise TypeError("Cannot create Times Object from value None")
	
		logger.debug("creating times from " + str(start_time) + " and " + str(end_time))

		self.start_time = start_time
		self.end_time = end_time

	def get_start_time(self):
		return self.start_time
	
	def get_end_time(self):
		return self.end_time

	#TODO: possibly add a function to see if a single Time is within the range 
	# specified by this Times object 
	
	def __str__(self):
		return self.start_time + to + self.end_time

	
	def __eq__(self, other):
		if not isinstance(other, Times):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.start_time == other.start_time and self.end_time == other.end_time 


