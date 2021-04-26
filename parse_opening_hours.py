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

		timerange = anytime + range_separator + anytime

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

def str_to_day(day_string):
	day = day_string.lower()
	if day in ["m", "mon", "monday"]:
		return Weekday.MONDAY
	elif day in ["t", "tue", "tues", "tuesday"]:
		return Weekday.TUESDAY
	elif day in ["w", "wed", "wednesday"]:
		return Weekday.WEDNESDAY
	elif day in ["th", "thu", "thurs", "thusday"]:
		return Weekday.THURSDAY
	elif day in ["f", "fri", "friday"]:
		return Weekday.FRIDAY
	elif day in ["sa", "sat", "saturday"]:
		return Weekday.SATURDAY
	elif day in ["su", "sun", "sunday"]:
		return Weekday.SUNDAY

def day_to_str(day):
	if day == Weekday.MONDAY:
		return "monday"
	elif day == Weekday.TUESDAY:
		return "tuesday"
	elif day == Weekday.WEDNESDAY:
		return "wednesday"
	elif day == Weekday.THURSDAY:
		return "thursday"
	elif day == Weekday.FRIDAY:
		return "friday"
	elif day == Weekday.SATURDAY:
		return "saturday"
	elif day == Weekday.SUNDAY:
		return "sunday"


def expand_day_range(start_day, end_day):
	days = []
	start_index = start_day.value
	end_index = end_day.value

	for index in range(start_index, end_index+1, 1):
		days.append(Weekday(index))
	return days

def parse_times(result):
	# assumes that all three (hours, minutes, am_pm) are the same length
	hours=None
	minutes=result.get("minute")
	is_24_hr=None
	am_pm=None
	if (result.get("hour_12")):
		is_24_hr=False
		hours = result.get("hour_12")
		am_pm = result.get("am_pm")

	elif (result.get("hour_24")):
		is_24_hr=True
		hours = result.get("hour_24")

	hours = join_parsed_parts(hours)
	minutes = join_parsed_parts(minutes)
	hours = [int(t, 10) for t in hours]
	minutes = [int(t, 10) for t in minutes]
	print(hours)
	print(minutes)

	if not is_24_hr:
		am_pm = join_parsed_parts(am_pm)
		is_pm = [s == "pm" for s in am_pm]

		hours = [militarize_hours(hours[t], am_pm[t]) for t in range(len(hours)+1)]
	print(hours)
	print(minutes)
	return [(hours[t], minutes[t]) for t in range(len(hours)+1)]



def join_parsed_parts(parsed):
	if parsed is None:
		return
	times = [] 
	for time in parsed:
		times.append("".join(time))
	
	return times



def militarize_hours(hours, is_pm):
	# hours = int(hours, 10)
	if is_pm:
		hours = hours + 12
	
	return hours

def stringify_time(time):
	return str(time[0]) + ":" + str(time[1])

