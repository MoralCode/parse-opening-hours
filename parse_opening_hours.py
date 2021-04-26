# parse various types of strings representing opening hours for a business into machine-readable JSON
# parse into the following format:
#  [
#     {
#       day: str as lowercase day of week e.g. monday,
#       opens: str as time with facility opens on this day in format hh:mm,
#       closes: str as time with facility closes on this day in format hh:mm,
#     },
#     ...
#   ]

from pyparsing import Word, alphas, nums, oneOf, Optional, Or, OneOrMore, Char
import enum

class Weekday(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class JsonOpeningHours():

	@classmethod
	def parse(self, hours_string):
		opening_hours_json = []

		greet = Word(alphas) + "," + Word(alphas) + "!"
		range_separator = oneOf("- to thru through")
		section_separator = Optional(",")
		time_separator = Optional(":")
		day = Word(alphas)
		am_or_pm = Optional(
			Or([
				Char("Aa"),
				Char("Pp")
			]) +
			Char("Mm")
		).setResultsName('am_pm')

		hour = Or([
			Char(nums),
			"0" + Char(nums),
			"1" + Char("012")
		])
		milhour = Or([
			hour,
			Or([
				"1" + Char("3456789"),
				"2" + Char("0123")
			])	
		])
		# twelve_hr =  hour
		minute = Char("012345") + Char(nums)
		time_minutes = Optional(time_separator + minute.setResultsName('minute'))
		miltime = milhour.setResultsName('hour_24') + time_minutes
		
		time_12hr = hour.setResultsName('hour_12') + time_minutes + am_or_pm

		daterange = day.setResultsName('startday') + range_separator + day.setResultsName('endday')

		anytime = Or([ miltime, time_12hr])

		timerange = anytime.setResultsName('starttime') + range_separator + anytime.setResultsName('endtime')

		opening_hours_format = Or([
			OneOrMore(daterange + timerange + section_separator),
			OneOrMore(timerange + daterange + section_separator)
		])	
		return opening_hours_json



def create_entry(day, opening, closing):
	return {
		"day": day,
		"opens": opening,
		"closes": closing
	}

def expand_day_range(start_day, end_day):
	days = []
	start_index = start_day.value
	end_index = end_day.value

	for index in range(start_index, end_index+1, 1):
		days.append(Weekday(index))
	return days

