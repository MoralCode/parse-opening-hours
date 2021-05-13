
import unittest
from models.days import *
from models.day import DaysEnum


class TestDays(unittest.TestCase):

	workweek = [Day(DaysEnum.MONDAY), Day(DaysEnum.TUESDAY), Day(DaysEnum.WEDNESDAY), Day(DaysEnum.THURSDAY), Day(DaysEnum.FRIDAY)]

	weekend = [Day(DaysEnum.SATURDAY), Day(DaysEnum.SUNDAY)]

	fullweek = workweek.copy()
	fullweek.extend(weekend)

	def test_expand_day_range(self):
		self.assertEqual(
			list(Days(DaysEnum.MONDAY, DaysEnum.FRIDAY)),
			self.workweek
		)

	
	def test_allweek_shortcuts(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"All Week",
			"7 days a week",
			"7 days",
			"Every Day",
			"",# no date present, just a time -> assume all week
			"daily",
		]
		expected_result = self.fullweek
		self.run_tests(input_strings, expected_result)

	def test_workweek(self):
		input_strings = [
			"Weekdays",
			"5 days a week",
			"5 days",
			"Business Days",
		]
		expected_result = self.workweek
		self.run_tests(input_strings,expected_result)

	def test_weekend(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Weekend",
			"Weekends",
		]
		expected_result = self.weekend
		self.run_tests(input_strings,expected_result)



	# def test_from_string_unknown(self):
	# 	test_str = "9:00"
	# 	test_9 = Time(9,0)
	# 	test_9_str = Time.from_string(test_str)
	# 	self.assertEqual(
	# 		test_9_str.hours,
	# 		test_9.hours
	# 	)
	# 	self.assertEqual(
	# 		test_9_str.minutes,
	# 		test_9.minutes
	# 	)
	# 	self.assertEqual(
	# 		test_9_str.time_type,
	# 		test_9.time_type
	# 	)


	# def test_from_string_am(self):
	# 	times_9am = [
	# 		"9:00am",
	# 		"9am",
	# 		# "0900",
	# 		# "900"
	# 	]
	# 	test_9am = Time(9,0, time_type=TimeType.AM)
	# 	for time_str in times_9am:
	# 		self.assertEqual(
	# 			Time.from_string(time_str),
	# 			test_9am
	# 		)


	# def test_stringify_time(self):
	# 	self.assertEqual(
	# 		str(Time(11,17,TimeType.MILITARY)),
	# 		"11:17"
	# 	)
	
	# def test_militarize_hours(self):
	# 	testTimeMil = Time(11,17,TimeType.MILITARY)
	# 	testTimePm = Time(11,17,TimeType.PM)
	# 	self.assertEqual(
	# 		testTimeMil.get_as_military_time().get_hours(),
	# 		11
	# 	)
	# 	self.assertEqual(
	# 		testTimePm.get_as_military_time().get_hours(),
	# 		23
	# 	)

	def run_tests(self, input_strings, expected_result, **kwargs):
		for input_str in input_strings:
			print("Testing String: '", input_str)
			self.assertEqual(list(Days.from_shortcut_string(input_str, **kwargs)), expected_result)

if __name__ == '__main__':
	unittest.main()