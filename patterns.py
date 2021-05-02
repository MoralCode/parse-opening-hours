from pyparsing import Word, alphas, nums, oneOf, Optional, Or, OneOrMore, Char

range_separator = Or([Word(" –—‐-"), oneOf("to thru through until")])
#TODO: support multiple sections like M 8am-2pm, W 9am-2pm
section_separator = Optional(",")
time_separator = Optional(":")
day = Word(alphas)
time_number = Word(nums, max=2)
am_or_pm = Optional(Word("AaPpMm.").setResultsName('am_pm', listAllMatches=True))

time = time_number("hour*") + time_separator + Optional(time_number("minute*")) + am_or_pm

daterange = day.setResultsName('startday', listAllMatches=True) + Optional(range_separator + day.setResultsName('endday', listAllMatches=True))

timerange = time.setResultsName('starttime', listAllMatches=True) + Optional(range_separator + time.setResultsName('endtime', listAllMatches=True))

notes = section_separator + Optional(OneOrMore(Word(alphas))).setResultsName('notes', listAllMatches=True)
