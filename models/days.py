

def str_to_days(day_string):
	logger.debug(day_string)

	if day_string is None:
		return None
	day = day_string.lower()

	allweek = expand_day_range(Day.MONDAY, Day.SUNDAY)
	workweek = expand_day_range(Day.MONDAY, Day.FRIDAY)

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
	elif "weekend" in day:
		return expand_day_range(Day.SATURDAY, Day.SUNDAY)
	elif "every" in day:
		return allweek
	elif "daily" in day:
		return allweek
	
