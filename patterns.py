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
range_separator = Or([Word(" –—‐-"), word_range_separators]).suppress()

word_list_separators = Optional(space) + oneOf("and") + Optional(space)
list_separator = Or([Word(" ,+/"), word_list_separators])

day_time_separators = Optional(Or([
	Literal(":"),
	CaselessLiteral("from"),
	Literal(",")
])).suppress()

plural = caselessWord("s'", max=2)
possibly_dots = Optional(Char(".")).suppress()


#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")

day = Combine(Or([
	MatchFirst([
		CaselessLiteral("Monday") + Optional(plural),
		CaselessLiteral("Mon") + possibly_dots,
		CaselessLiteral("M") + possibly_dots
	]),
	MatchFirst([
		CaselessLiteral("Tuesday") + Optional(plural),
		CaselessLiteral("Tues") + possibly_dots,
		CaselessLiteral("Tue") + possibly_dots,
		CaselessLiteral("T") + possibly_dots
	]),
	MatchFirst([
		CaselessLiteral("Wednesday") + Optional(plural),
		CaselessLiteral("Wed") + possibly_dots,
		CaselessLiteral("W") + possibly_dots
	]),
	MatchFirst([
		CaselessLiteral("Thursday") + Optional(plural),
		CaselessLiteral("Thurs") + possibly_dots,
		CaselessLiteral("Th") + possibly_dots,
		CaselessLiteral("H") + possibly_dots
	]),
	MatchFirst([
		CaselessLiteral("Friday") + Optional(plural),
		CaselessLiteral("Fri") + possibly_dots,
		CaselessLiteral("F") + possibly_dots + ~CaselessLiteral("rom"),
	]),
	MatchFirst([
		CaselessLiteral("Saturday") + Optional(plural),
		CaselessLiteral("Sat") + possibly_dots,
		CaselessLiteral("Sa") + possibly_dots
	]),
	MatchFirst([
		CaselessLiteral("Sunday") + Optional(plural),
		CaselessLiteral("Sun") + possibly_dots,
		CaselessLiteral("Su") + possibly_dots
	]),
]))


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

days = OneOrMore(day)

# the r is here because of https://stackoverflow.com/questions/50504500/deprecationwarning-invalid-escape-sequence-what-to-use-instead-of-d#50504635
hour = Regex(r'[01]\d|2[0-3]|\d').setParseAction(pyparsing_common.convertToInteger).setResultsName("hour")
minute = Regex(r'[0-5]\d').setParseAction(pyparsing_common.convertToInteger).setResultsName("minute")


am_or_pm = Optional(Combine(Or([CaselessLiteral("A"), CaselessLiteral("P")]) + possibly_dots + CaselessLiteral("M")  + possibly_dots).setResultsName('am_pm'))

time_shortcut = Combine(Or([
	CaselessLiteral("noon"),
	CaselessLiteral("midnight"),
	CaselessLiteral("CLOSED")
]), adjacent=False).setResultsName("time_shortcut")

clocktime = Combine(hour + time_separator + Optional(minute) + am_or_pm, adjacent=False)

dateShortcuts = day_shortcuts.setResultsName('day_shortcuts', listAllMatches=True) + Optional(list_separator)

dateList = OneOrMore(day.setResultsName('day', listAllMatches=True) + Optional(list_separator))

daterange = day.setResultsName('startday', listAllMatches=True) + range_separator + day.setResultsName('endday', listAllMatches=True)

dates = Optional(Or([daterange, dateList, dateShortcuts]))

time = Group(Or([clocktime, time_shortcut]))

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

opening_hours_format = Or([
	OneOrMore(dates + day_time_separators + timerange),
	OneOrMore(timerange + dates)
])	

notes = section_separator + Optional(OneOrMore(Word(alphas))).setResultsName('notes', listAllMatches=True)
