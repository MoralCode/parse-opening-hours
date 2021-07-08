import unicodedata
import calendar

def normalize_string(string):
	string = unicodedata.normalize('NFC', string)
	string = string.strip()
	return string

def month_str_to_int(month_str):
	month_str = month_str.lower().capitalize()
	names = {month: index for index, month in enumerate(calendar.month_name) if month}
	abbrs = {month: index for index, month in enumerate(calendar.month_abbr) if month}
	print(names)
	print(abbrs)
	print(month_str)
	if month_str in calendar.month_name:
		return names[month_str]
	elif  month_str in calendar.month_abbr:
		return abbrs[month_str]
	
	return
	
