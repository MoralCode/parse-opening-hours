from pyparsing import *

def caselessWord(some_str, **kwargs):
	return Word(some_str.lower() + some_str.upper(), **kwargs)

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

day_time_separators = Optional(Or([
	Word(": "),
	CaselessLiteral("from", )
]))

plural = caselessWord("s'", max=2)

#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")

# this is all the unique characters in the string
# "monday tuesday wednesday thursday friday saturday sunday"
day_of_week_start = caselessChar("mtwhfs")
day_of_week_rest = Optional(caselessWord("ondayuesrit'"))
day = Combine(day_of_week_start + day_of_week_rest)

day_shortcuts = Combine(Or([
	Or([
		CaselessLiteral("Work"),
		CaselessLiteral("All")
	]) + Optional(space) + CaselessLiteral("Week"),
	Char("57") + Optional(space) + CaselessLiteral("days") + Optional(space) + Optional(CaselessLiteral("a week")),
	CaselessLiteral("Every Day"),
	CaselessLiteral("daily"),
	CaselessLiteral("Week") + Optional(space) + Or([
		CaselessLiteral("day"),
		CaselessLiteral("end")
	]) + Optional(plural),
	CaselessLiteral("Business Day") + Optional(plural),
]), adjacent=False)

days = Or([day, day_shortcuts])

time_number = Word(nums, max=2)

possibly_dots = Optional(Char("."))

am_or_pm = Optional(Group(Or([CaselessLiteral("A"), CaselessLiteral("P")]) + possibly_dots + CaselessLiteral("M")  + possibly_dots).setResultsName('am_pm'))

time = Combine(time_number("hour") + time_separator + Optional(time_number("minute")) + am_or_pm,adjacent=False)

dateShortcuts = OneOrMore(days.setResultsName('day_shortcuts', listAllMatches=True) + Optional(list_separator))

dateList = OneOrMore(day.setResultsName('day', listAllMatches=True) + Optional(list_separator))

daterange = day.setResultsName('startday', listAllMatches=True) + range_separator + day.setResultsName('endday', listAllMatches=True)

dates = Optional(Or([daterange, dateList, dateShortcuts]))

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

notes = section_separator + Optional(OneOrMore(Word(alphas))).setResultsName('notes', listAllMatches=True)
