from pyparsing import *

def caselessWord(some_str, **kwargs):
	return Word(some_str.lower() + some_str.upper(), **kwargs)

def caselessChar(some_str):
	return Char(some_str.lower() + some_str.upper())

space = Word(" ")

useless_optional_prefixes = Optional(Or([
	CaselessLiteral("Open")
])).suppress()

hyphens = Char("–—‐-\u2013")

words_for_range = Or([
	caselessWord("to"),
	caselessWord("thru"),
	caselessWord("through"),
	caselessWord("until"),
	caselessWord("'til")
])
word_range_separators = Optional(space) + words_for_range + Optional(space)
range_separator = Or([hyphens, word_range_separators])#.suppress()

word_list_separators = Optional(space) + oneOf("and") + Optional(space)
list_separator = Or([Char(",+/&"), word_list_separators])

day_time_separators = Optional(Or([
	Literal(":"),
	CaselessLiteral("from"),
	Literal(",")
])).suppress()

plural = Or([
	Optional("'") + CaselessLiteral("s"),
	CaselessLiteral("s") + Optional("'")
])
possibly_dots = Optional(Char(".")).suppress()


#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")

ymd_separator = Or([Char("/"), hyphens]).suppress()
# TODO: use CaselessCloseMatch here once implemented to handle typos, particularly for the longer names
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

# TODO: use CaselessCloseMatch here once implemented to handle typos, particularly for the longer names
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
hour = Combine(Or([
	Char("01") + Char(nums),
	"2" + Char("0123"),
	Char(nums)
])).setParseAction(pyparsing_common.convertToInteger).setResultsName("hour")

minute = Combine(
	Char("012345") + Char(nums)
).setParseAction(pyparsing_common.convertToInteger).setResultsName("minute")


am_or_pm = Optional(Combine(Or([CaselessLiteral("A"), CaselessLiteral("P")]) + possibly_dots + Optional(CaselessLiteral("M")  + possibly_dots)).setResultsName('am_pm'))

per = Or([
	Literal("/"),
	CaselessLiteral("a"),
	CaselessLiteral("per")
]).suppress()


hours_shortcuts = Optional(
	MatchFirst([
		CaselessLiteral("hour") + Optional(plural),
		CaselessLiteral("hr") + Optional(plural),
		CaselessLiteral("h")
	]) + Optional(per) + Optional(CaselessLiteral("day"))
)

time_range_shortcuts = Or([
	Literal("24") + hours_shortcuts,
	CaselessLiteral("All Day")
])

# TODO: use CaselessCloseMatch here once implemented to handle typos, particularly for the longer names
single_time_shortcut = Combine(Or([
	CaselessLiteral("noon"),
	CaselessLiteral("midnight"),
	CaselessLiteral("CLOSED")
]), adjacent=False)

time_shortcuts = Or([single_time_shortcut, time_range_shortcuts]).setResultsName("time_shortcuts")

clocktime = Combine(hour + time_separator + Optional(minute) + am_or_pm, adjacent=False)

dayShortcuts = day_shortcuts.setResultsName('day_shortcuts', listAllMatches=True) + Optional(list_separator)

dayList = OneOrMore(day.setResultsName('day', listAllMatches=True) + Optional(list_separator))

dayRange = day.setResultsName('startday', listAllMatches=True) + range_separator + day.setResultsName('endday', listAllMatches=True)

dates = Or([OneOrMore(Or([dayRange, dayList]) + Optional(list_separator)), dayShortcuts])

time = Group(Or([clocktime, time_shortcuts]))

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

opening_hours_format = Or([
	useless_optional_prefixes + OneOrMore(Optional(dates) + day_time_separators + timerange),
	useless_optional_prefixes + OneOrMore(timerange + dates)
])	

note = Optional(Group(OneOrMore(caselessWord(alphas + " "), stopOn=opening_hours_format)).setResultsName('note', listAllMatches=True))

notes_start = note #+ FollowedBy(Or([dates, timerange]))
notes_end = FollowedBy(opening_hours_format) + note
