
import unittest
from opening_hours.models.dates import *
from opening_hours.patterns import specific_dates
import datetime


class TestDates(unittest.TestCase):

	def test_init(self):
		result = [datetime.date(2021, 5, 6)]
		self.assertEqual(Dates().dates, set({}))

	def test_single_day_from_date(self):
		result = [datetime.date(2021, 5, 6)]
		self.assertEqual(list(Dates.from_date(result[0]).dates), result)

	def test_single_day_from_parse_results(self):
		test_str = "05/06/2021"
		result = [datetime.date(2021, 5, 6)]
		parsed = specific_dates.parseString(test_str)
		self.assertEqual(list(Dates.from_parse_results(parsed).dates), result)

	def test_multi_day_from_parse_results(self):
		test_str = "05/06/20, 05/07/2020"
		result = [datetime.date(20, 5, 6), datetime.date(2020, 5, 7)]
		parsed = specific_dates.parseString(test_str)
		self.assertEqual(Dates.from_parse_results(parsed).dates, set(result))

	def test_century_assumption_from_parse_results(self):
		test_str = "05/06/2021"
		result = [datetime.date(2021, 5, 6)]
		parsed = specific_dates.parseString(test_str)
		self.assertEqual(list(Dates.from_parse_results(parsed, assume_century=20).dates), result)
	
	def test_equals(self):
		dat_1 = Dates()
		self.assertEqual(Dates(), dat_1)
		dt_date = datetime.date(2021,5,5)
		dat_1.add(dt_date)
		self.assertNotEqual(Dates(), dat_1)
		with self.assertRaises(NotImplementedError):
			Dates() == dt_date
		


	def test_single_day_formats_from_parse_results(self):
		test_str = [
			"05/06/2021",
			"05-06-2021",
			"2021-05-06",
			"May 6, 2021",
			"May 6 2021",
			"May 6th, 2021",
			"May 6th 2021",
		]
		result = [datetime.date(2021, 5, 6)]
		for test in test_str:
			logger.debug(test)
			parsed = specific_dates.parseString(test)
			self.assertEqual(list(Dates.from_parse_results(parsed).dates), result)

	# def test_allweek_shortcuts(self):
	# 	# TODO: implement assumption of pm if end time <= start time
	# 	input_strings = [
	# 		"All Week",
	# 		"7 days a week",
	# 		"7 days",
	# 		"Every Day",
	# 		"",# no date present, just a time -> assume all week
	# 		"daily",
	# 		"24/7",
	# 		# "24 hours a day",
	# 		"24 hours a day, 7 days a week"
	# 	]
	# 	expected_result = self.fullweek
	# 	self.run_tests(input_strings, expected_result)

	# def test_create_from_none(self):
	# 	with self.assertRaises(TypeError):
	# 		Dates.from_shortcut_string(None)
	# 	with self.assertRaises(TypeError):
	# 		Dates(None, None)
	# 	with self.assertRaises(TypeError):
	# 		Dates.from_parse_results(None)

	# def test_create_from_empty(self):
	# 	with self.assertRaises(TypeError):
	# 		Dates("", "")

	# def test_create_from_unknown(self):
	# 	with self.assertRaises(ValueError):
	# 		Dates.from_shortcut_string("cheeseburger")
	
	# def test_from_parse_regular(self):
	# 	test_dict = {
	# 		"hour": 5,
	# 		"minute": 0,
	# 		"am_pm": "PM"
	# 	}
	# 	test_days_dict = Time.from_parse_results(test_dict)
	# 	self.assertEqual(
	# 		test_time_dict.hours,
	# 		5
	# 	)
	# 	self.assertEqual(test_time_dict.minutes, 0)

	# 	self.assertTrue(test_time_dict.is_pm())
	
	# def test_from_parse_shortcut(self):
	# 	test_dict = {
	# 		"time_shortcuts": "noon"
	# 	}
	# 	test_days_dict = Dates.from_parse_results(test_dict)
	# 	self.assertEqual(
	# 		test_days_dict.hours,
	# 		12
	# 	)
	# 	self.assertEqual(test_days_dict.minutes, 0)

	# def test_from_parse_unknown(self):
	# 	test_dict = {
	# 		"unknown": "dont care"
	# 	}
	# 	with self.assertRaises(ValueError):
	# 		Dates.from_parse_results(test_dict)

	# def test_workweek(self):
	# 	input_strings = [
	# 		"Weekdays",
	# 		"5 days a week",
	# 		"5 days",
	# 		"Business Dates",
	# 		"workdays"
	# 	]
	# 	expected_result = self.workweek
	# 	self.run_tests(input_strings,expected_result)

	# def test_weekend(self):
	# 	# TODO: implement assumption of pm if end time <= start time
	# 	input_strings = [
	# 		"Weekend",
	# 		"Weekends",
	# 	]
	# 	expected_result = self.weekend
	# 	self.run_tests(input_strings,expected_result)

	# def test_equals(self):
	# 	workweek = Dates(DatesEnum.MONDAY, DatesEnum.FRIDAY)
	# 	with self.assertRaises(NotImplementedError):
	# 		workweek == "something else"
		
	# 	self.assertEqual(workweek, workweek)


	def run_tests(self, input_strings, expected_result, **kwargs):
		for input_str in input_strings:
			print("Testing String: '", input_str)
			self.assertEqual(list(Dates.from_shortcut_string(input_str, **kwargs)), expected_result)

if __name__ == '__main__':
	unittest.main()