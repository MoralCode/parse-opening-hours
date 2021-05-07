from pyparsing import Word, alphas, nums, oneOf, Optional, Or, OneOrMore, Char, Combine

def caselessWord(some_str):
	return Word(some_str.lower() + some_str.upper())

def caselessChar(some_str):
	return Char(some_str.lower() + some_str.upper())

space = Word(" ")
words_for_range = Or([
	caselessWord("to"),
	caselessWord("thru"),
	caselessWord("through"),
	caselessWord("until"),
	caselessWord("'til")
])
word_range_separators = Optional(space) + words_for_range + Optional(space)
range_separator = Or([Word(" –—‐-"), word_range_separators])

word_list_separators = Optional(space) + oneOf("and") + Optional(space)
list_separator = Or([Word(" ,+/"), word_list_separators])

day_time_separators = Optional(Word(": "))

#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")

# this is all the unique characters in the string
# "monday tuesday wednesday thursday friday saturday sunday"
day_of_week_start = caselessChar("mtwhfs")
day_of_week_rest = Optional(caselessWord("ondayuesrit'"))
day = Combine(day_of_week_start + day_of_week_rest)

day_shortcuts = Or([
	Or([
		caselessWord("Work"),
		caselessWord("All")
	]) + caselessWord("Week"),
	Char("57") + caselessWord("days") + Optional(caselessWord("a week")),
	caselessWord("Every Day"),
	caselessWord("daily"),
	caselessWord("Week") + Or([
		caselessWord("day"),
		caselessWord("end")
	]) + Optional(caselessWord("'s")),
	caselessWord("Business Days"),
])

days = Or([day, day_shortcuts])

time_number = Word(nums, max=2)
am_or_pm = Optional(Word("AaPpMm.").setResultsName('am_pm', listAllMatches=True))

time = time_number("hour*") + time_separator + Optional(time_number("minute*")) + am_or_pm

dateShortcuts = OneOrMore(days.setResultsName('day_shortcuts', listAllMatches=True) + Optional(list_separator))

dateList = OneOrMore(day.setResultsName('day', listAllMatches=True) + Optional(list_separator))

daterange = day.setResultsName('startday', listAllMatches=True) + range_separator + day.setResultsName('endday', listAllMatches=True)

dates = Or([daterange, dateList, dateShortcuts])

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

notes = section_separator + Optional(OneOrMore(Word(alphas))).setResultsName('notes', listAllMatches=True)
