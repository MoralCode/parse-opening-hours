
import unittest
from opening_hours.models.time import *

class TestTime(unittest.TestCase):

	def test_from_string_unknown(self):
		test_str = "9:00"
		test_9 = Time(9,0)
		test_9_str = Time.from_string(test_str)
		self.assertEqual(
			test_9_str.hours,
			test_9.hours
		)
		self.assertEqual(
			test_9_str.minutes,
			test_9.minutes
		)
		self.assertEqual(
			test_9_str.time_type,
			test_9.time_type
		)

	def test_from_shortcut(self):
		test_str = "noon"
		test_9_str = Time.from_shortcut(test_str)
		self.assertEqual(
			test_9_str.hours,
			12
		)
		self.assertEqual(test_9_str.minutes, 0)

		test_str = "midnight"
		test_9_str = Time.from_shortcut(test_str)
		self.assertEqual(
			test_9_str.hours,
			0
		)
		self.assertEqual(test_9_str.minutes, 0)

	def test_from_parse_regular(self):
		test_dict = {
			"hour": 5,
			"minute": 0,
			"am_pm": "PM"
		}
		test_time_dict = Time.from_parse_results(test_dict)
		self.assertEqual(
			test_time_dict.hours,
			5
		)
		self.assertEqual(test_time_dict.minutes, 0)

		self.assertTrue(test_time_dict.is_pm())

	def test_from_string_and_assumption(self):
		test_time_dict = Time.from_string("5:00", assume_type=TimeType.AM)
		self.assertEqual(
			test_time_dict.hours,
			5
		)
		self.assertEqual(test_time_dict.minutes, 0)
		self.assertTrue(test_time_dict.is_am())
	
	def test_from_parse_shortcut(self):
		test_dict = {
			"time_shortcuts": "noon"
		}
		test_time_dict = Time.from_parse_results(test_dict)
		self.assertEqual(
			test_time_dict.hours,
			12
		)
		self.assertEqual(test_time_dict.minutes, 0)

	def test_from_parse_unknown(self):
		test_dict = {
			"unknown": "dont care"
		}
		with self.assertRaises(ValueError):
			Time.from_parse_results(test_dict)

	def test_from_string_None(self):
		with self.assertRaises(TypeError):
			Time.from_string(None)
		
		with self.assertRaises(ValueError):
			Time.from_string("")


	def test_from_string_am(self):
		times_9am = [
			"9:00am",
			"9am",
			# "0900",
			# "900"
		]
		test_9am = Time(9,0, time_type=TimeType.AM)
		for time_str in times_9am:
			self.assertEqual(
				Time.from_string(time_str),
				test_9am
			)

	def test_stringify_time(self):
		self.assertEqual(
			str(Time(11,17,TimeType.MILITARY)),
			"11:17"
		)
	
	def test_militarize_hours(self):
		testTimeMil = Time(11,17,TimeType.MILITARY)
		testTimePm = Time(11,17,TimeType.PM)
		self.assertEqual(
			testTimeMil.get_as_military_time().get_hours(),
			11
		)
		self.assertEqual(
			testTimePm.get_as_military_time().get_hours(),
			23
		)

	def test_noon_midnight_regression(self):
		
		self.assertEqual(
			Time.from_string("12pm").get_as_military_time().get_hours(),
			12
		)
		self.assertEqual(
			Time.from_string("12am").get_as_military_time().get_hours(),
			0
		)

	# def test_detect_pm(self):
	# 	input_strings = [
	# 		"pm",
	# 		"Pm",
	# 		"pM",
	# 		"p.m.",
	# 		"PM",
	# 	]
	# 	for instr in input_strings:
	# 		self.assertTrue(detect_if_pm(instr))
		
	# 	input_strings = [
	# 		"am",
	# 		"Am",
	# 		"aM",
	# 		"a.m.",
	# 		"AM",
	# 	]
	# 	for instr in input_strings:
	# 		self.assertFalse(detect_if_pm(instr))

if __name__ == '__main__':
	unittest.main()