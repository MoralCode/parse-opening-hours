from pyparsing import Word, alphas, nums, oneOf, Optional, Or, OneOrMore, Char

range_separator = Or([Word(" –—‐-"), oneOf("to thru through until")])
#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")
day = Word(alphas)
time_number = Word(nums, max=2)
am_or_pm = Optional(Word("AaPpMm.").setResultsName('am_pm', listAllMatches=True))

hour = time_number("hour*")
minute = time_number("minute*")
time_minutes = Optional(time_separator + minute)
# miltime = milhour.setResultsName('hour_24') + time_minutes

time = hour + time_minutes + am_or_pm

daterange = day.setResultsName('startday', listAllMatches=True) + Optional(range_separator + day.setResultsName('endday', listAllMatches=True))

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

notes = section_separator + Optional(OneOrMore(Word(alphas))).setResultsName('notes', listAllMatches=True)
