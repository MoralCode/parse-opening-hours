from models.day import Day, DaysEnum
import logging, os

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)

class Days():
	start_day = None
	end_day = None
	
	@classmethod
	def from_shortcut_string(cls, days_string, assume_type=None):
		"""
		create a time object from a string
		"""
		logger.debug("creating days object from string: " + days_string)
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

		logger.debug("unable to process days string: " + days_string)
			
		return None
		
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
	
	def __str__(self):
		return self.start_day.value + to + self.end_day.value

	def __iter__(self):
		# if end_day is None:
		# 	return [start_day]
		week = list(DaysEnum)
		start_index = week.index(self.start_day)
		end_index = week.index(self.end_day)

		if end_index < start_index:
			# if the end day is sooner in the week than the start
			end_index += start_index

		days = []
		for x in range(start_index, end_index+1):
			#ensure the indices wrap around to the beginning of the week
			day_index = x % 7
			days.append(Day(week[day_index]))
	
		return iter(days)
	
	def __eq__(self, other):
		if not isinstance(other, Days):
			# don't attempt to compare against unrelated types
			raise NotImplementedError()
		return self.start_day == other.start_day and self.end_day == other.end_day 


