import enum
import logging, os
from models.day import DaysEnum

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)
	


	
def detect_if_pm(string):
	return "p" in string.lower()




def expand_day_range(start_day, end_day):
	if end_day is None:
		return [start_day]
	days = []
	count_day=False #flag to help determine which days should be included
	all_days = enumerate(DaysEnum)
	for _,day in all_days:
		if day == start_day:
			count_day = True

		if count_day:
			days.append(day)

		if day == end_day:
			count_day = False
		
	return days

def raw_from_parsed(parsed, key, default=None):
	if parsed is None:
		return default

	val = parsed.get(key)
	logger.debug("raw key: " + key)
	logger.debug(val)
	if val is None:
		return default
	try:
		return val
	except KeyError:
		return default

def value_from_parsed(parsed, key, default=None):
	val = raw_from_parsed(parsed, key, default=None)
	logger.debug("value key: " + key)
	logger.debug(val)
	if val is None:
		return default
	return val[0]

def concat_from_parsed(parsed, key, default=None):
	val = value_from_parsed(parsed, key, default=[])
	logger.debug("concat key: " + key)
	logger.debug(val)
	return "".join(val)

def int_from_parsed(parsed, key, default=0):
	val = value_from_parsed(parsed, key, default=default)
	logger.debug("int key: " + key)
	logger.debug(str(val))
	if val is None:
		return default
	if isinstance(val, int):
		return val
	return int(val, 10)

def str_from_parsed(parsed, key, default=""):
	val = value_from_parsed(parsed, key, default=default)
	logger.debug("str key: " + key)
	logger.debug(val)
	if val is None:
		return default
	return str(val)
