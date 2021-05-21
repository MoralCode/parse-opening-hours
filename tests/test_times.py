
import unittest
from opening_hours.models.time import Time, TimeType
from opening_hours.models.times import Times


# "24 hours a day",
# "24 hours" "24hrs" "24h" "All Day" "Open 24 hours"


class TestTimes(unittest.TestCase):

	def test_create_from_none(self):
		with self.assertRaises(TypeError):
			Times.from_shortcut_string(None)
		with self.assertRaises(TypeError):
			Times(None, None)

	def test_create_from_unknown(self):
		with self.assertRaises(ValueError):
			Times.from_shortcut_string("cheeseburger")

	# def test_from_parse_regular(self):
	# 	test_dict = {
	# 		"hour": 5,
	# 		"minute": 0,
	# 		"am_pm": "PM"
	# 	}
	# 	test_time_dict = Times.from_parse_results(test_dict)
	# 	self.assertEqual(
	# 		test_time_dict.hours,
	# 		5
	# 	)
	# 	self.assertEqual(test_time_dict.minutes, 0)

	# 	self.assertTrue(test_time_dict.is_pm())
	
	# def test_from_parse_shortcut(self):
	# 	test_dict = {
	# 		"time_shortcuts": "24 hours"
	# 	}
	# 	test_time_dict = Times.from_parse_results(test_dict)
	# 	self.assertEqual(
	# 		test_time_dict.hours,
	# 		12
	# 	)
	# 	self.assertEqual(test_time_dict.minutes, 0)

	# def test_from_parse_unknown(self):
	# 	test_dict = {
	# 		"unknown": "dont care"
	# 	}
	# 	with self.assertRaises(ValueError):
	# 		Times.from_parse_results(test_dict)

	def test_equals(self):
		allday = Times(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))
		with self.assertRaises(NotImplementedError):
			allday == "something else"
		
		self.assertEqual(allday, allday)


# 	workweek = [Day(DaysEnum.MONDAY), Day(DaysEnum.TUESDAY), Day(DaysEnum.WEDNESDAY), Day(DaysEnum.THURSDAY), Day(DaysEnum.FRIDAY)]

# 	weekend = [Day(DaysEnum.SATURDAY), Day(DaysEnum.SUNDAY)]

# 	fullweek = workweek.copy()
# 	fullweek.extend(weekend)

# 	def test_expand_day_range(self):
# 		self.assertEqual(
# 			list(Days(DaysEnum.MONDAY, DaysEnum.FRIDAY)),
# 			self.workweek
# 		)

	
# 	def test_allweek_shortcuts(self):
# 		# TODO: implement assumption of pm if end time <= start time
# 		input_strings = [
# 			"All Week",
# 			"7 days a week",
# 			"7 days",
# 			"Every Day",
# 			"",# no date present, just a time -> assume all week
# 			"daily",
# 		]
# 		expected_result = self.fullweek
# 		self.run_tests(input_strings, expected_result)

# 	def test_create_from_none(self):
# 		with self.assertRaises(TypeError):
# 			Days.from_shortcut_string(None)
# 		with self.assertRaises(TypeError):
# 			Days(None, None)

# 	def test_create_from_unknown(self):
# 		with self.assertRaises(ValueError):
# 			Days.from_shortcut_string("cheeseburger")

# 	def test_workweek(self):
# 		input_strings = [
# 			"Weekdays",
# 			"5 days a week",
# 			"5 days",
# 			"Business Days",
# 			"workdays"
# 		]
# 		expected_result = self.workweek
# 		self.run_tests(input_strings,expected_result)

# 	def test_weekend(self):
# 		# TODO: implement assumption of pm if end time <= start time
# 		input_strings = [
# 			"Weekend",
# 			"Weekends",
# 		]
# 		expected_result = self.weekend
# 		self.run_tests(input_strings,expected_result)

# 	def test_equals(self):
# 		workweek = Days(DaysEnum.MONDAY, DaysEnum.FRIDAY)
# 		with self.assertRaises(NotImplementedError):
# 			workweek == "something else"
		
# 		self.assertEqual(workweek, workweek)


	def run_tests(self, input_strings, expected_result, **kwargs):
		for input_str in input_strings:
			print("Testing String: '", input_str)
			self.assertEqual(list(Times.from_shortcut_string(input_str, **kwargs)), expected_result)

if __name__ == '__main__':
	unittest.main()