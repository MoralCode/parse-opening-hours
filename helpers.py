import enum
import logging, os
from models.day import DaysEnum

logger = logging.getLogger(__name__)
if os.getenv("OH_DEBUG") == "Y":
	logger.setLevel(logging.DEBUG)
	


	




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

def str_from_parsed(parsed, key, default=""):
	val = value_from_parsed(parsed, key, default=default)
	logger.debug("str key: " + key)
	logger.debug(val)
	if val is None:
		return default
	return str(val)
