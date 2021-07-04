from opening_hours.models.day import Day, DaysEnum
import logging, os

logger = logging.getLogger(__name__)

class Days():
	"""
	This class represents a range of days (i.e monday to friday) and provides
	some helpful methods to interperet these ranges from shortcuts (like
	"weekdays"), iterate over the range of days to get a list of all the days
	that are covered by this range
	"""
	start_day = None
	end_day = None
	days = ()
	#TODO: support days with exceptions (like "Monday to friday but not thurdsays")
	@classmethod
	def from_shortcut_string(cls, days_string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating days object from shortcut: " + days_string)
		if days_string is None:
			raise TypeError("Cannot create Days Object from value None")
			
		day = days_string.lower()

		# set up some shortcut ranges
		allweek = cls(DaysEnum.MONDAY, DaysEnum.SUNDAY)
		workweek = cls(DaysEnum.MONDAY, DaysEnum.FRIDAY)

		if "weekday" in day:
			return workweek
		elif "business" in day:
			return workweek
		elif "work" in day:
			return workweek
		elif "5" in day:
			return workweek
		elif "7" in day:
			return allweek
		elif "all" in day and "week" in day:
			return allweek
		elif "every" in day:
			return allweek
		elif "daily" in day:
			return allweek
		elif "weekend" in day:
			return cls(DaysEnum.SATURDAY, DaysEnum.SUNDAY)
		elif day == "":
			# if no day is specified, assume the intention is all week
			return allweek

		raise ValueError("string '" + days_string + "' does not match a known pattern")
			
	@classmethod
	def from_parse_results(cls, result):
		days = []

		if "startday" in result:
			logger.info("range date detected")
			# this is a date range that includes the intervening days
			start_day = Day.from_string(result.get("startday")[0])
			end_day = result.get("endday")[0]
			logger.debug(end_day)
			end_day = Day.from_string(end_day) if end_day is not None else end_day
			days = cls(start_day, end_day)
		elif "day" in result:
			logger.info("list date detected")
			#TODO: have Days class support lists of individual days, as well as just ranges. as of now this is fine because both are iterable and give the same outputs when iterated over
			days = [ Day.from_string(day) for day in result.get("day") ]
		elif "day_shortcuts" in result:
			logger.info("shortcut date detected")
			days = cls.from_shortcut_string(result.get( "day_shortcuts")[0])
		else:
			logger.info("unspecified date detected ")
			# logger.debug(vars(result))
			# nothing specified, assumeit means every day
			return cls(DaysEnum.MONDAY, DaysEnum.SUNDAY)
		return days
		
	def __init__(self, start_day, end_day):
		if start_day is None or end_day is None:
			raise TypeError("Cannot create Days Object from value None")
	
		logger.debug("creating days from " + str(start_day) + " and " + str(end_day))


		if isinstance(start_day, DaysEnum):
			self.start_day = Day(start_day)

		if isinstance(end_day, DaysEnum):
			self.end_day = Day(end_day)

		self.start_day = start_day
		self.end_day = end_day

		self.days = set(_expand_day_range(start_day, end_day))
		
	def __str__(self):
		return self.start_day.value + to + self.end_day.value

	def _expand_day_range(self, start_day, end_day):
		# if end_day is None:
		# 	return [start_day]
		week = list(DaysEnum)
		start_index = week.index(start_day)
		end_index = week.index(end_day)

		if end_index < start_index:
			# if the end day is sooner in the week than the start
			end_index += start_index

		days = []
		for x in range(start_index, end_index+1):
			#ensure the indices wrap around to the beginning of the week
			day_index = x % 7
			days.append(Day(week[day_index]))
	
		return self.days

	def __iter__(self):
		return self.days
	
	def __eq__(self, other):
		if not isinstance(other, Days):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.start_day == other.start_day and self.end_day == other.end_day 


