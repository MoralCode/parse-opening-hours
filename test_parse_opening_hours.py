import unittest
from parse_opening_hours import *

class TestHoursParsing(unittest.TestCase):

	mon_9_to_5 = {
		"day": "monday",
		"opens": "9:00",
		"closes": "17:00"
	}

	tue_9_to_5 = {
		"day": "tuesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	wed_9_to_5 = {
		"day": "wednesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	thurs_9_to_5 = {
		"day": "wednesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	fri_9_to_5 = {
		"day": "wednesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	sat_9_to_5 = {
		"day": "wednesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	sun_9_to_5 = {
		"day": "wednesday",
		"opens": "9:00",
		"closes": "17:00"
	}

	workweek_9_to_5 = [mon_9_to_5, tue_9_to_5, wed_9_to_5,thurs_9_to_5, fri_9_to_5]
	allweek_9_to_5 = workweek_9_to_5.extend([sat_9_to_5, sun_9_to_5])


	def test_single_day_miltime(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday 9:00 - 5:00",
			"Mon 9:00 - 5:00",
			"M 9:00 - 5:00",
			"Monday 9:00-5:00",
			"Mon 9:00-5:00",
			"M 9:00-5:00",
			"Monday 9 - 5",
			"Mon 9 - 5",
			"M 9 - 5",
			"Monday 9-5",
			"Mon 9-5",
			"M 9-5"
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result)



	def test_single_day_abbreveations(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday 9:00am - 5:00pm",
			"Mon 9:00am - 5:00pm",
			"M 9:00am - 5:00pm"
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result)

	def test_time_formatting(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday 9:00 - 5:00",
			"Monday 9:00-5:00",
			"Monday 9:00am - 5:00pm",
			"Monday 9:00am-5:00pm",
			"Monday 9:00 - 5:00pm",
			"Monday 9:00-5:00pm",
			"Monday 9:00am - 5:00",
			"Monday 9:00am-5:00",
			"Monday 9am - 5pm",
			"Monday 9am-5pm",
			"Monday 9am to 5pm",
			"Monday 9am through 5pm"
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result)
	
	
	def test_multi_day(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday - Wednesday 9:00 - 5:00",
			"Mon - Wed 9:00 - 5:00",
			"M - W 9:00 - 5:00",
			"Monday-Wednesday 9:00 - 5:00",
			"Mon-Wed 9:00 - 5:00",
			"M-W 9:00 - 5:00",
			"Monday through Friday 9:00 - 5:00",
			"Monday to Friday 9:00 - 5:00",

		]
		expected_result = [ self.mon_9_to_5, self.tue_9_to_5, self.wed_9_to_5 ]
		self.run_tests(input_strings,expected_result)

	def test_allweek(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"All Week 9:00am - 5:00pm",
			"7 days a week 9:00am - 5:00pm",
			"7 days 9:00am - 5:00pm",
			"Every Day 9:00am - 5:00pm",
			"9:00am - 5:00pm",
			"daily 9:00am - 5:00pm",
			"9:00am - 5:00pm daily",
			"9:00am - 5:00pm All Week",
			"9:00am - 5:00pm 7 days a week",
			"9:00am - 5:00pm 7 days",
			"9:00am - 5:00pm Every Day"
		]
		expected_result = self.allweek_9_to_5
		self.run_tests(input_strings,expected_result)

	def test_workweek(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Weekdays 9:00am - 5:00pm",
			"5 days a week 9:00am - 5:00pm",
			"5 days 9:00am - 5:00pm",
			"Business Days 9:00am - 5:00pm",
			"9:00am - 5:00pm Weekdays",
			"9:00am - 5:00pm 5 days a week",
			"9:00am - 5:00pm 5 days",
			"9:00am - 5:00pm Business Days"
		]
		expected_result = self.workweek_9_to_5
		self.run_tests(input_strings,expected_result)

	def test_create_entry(self):
		self.assertEqual(
			create_entry("monday", "9:00", "17:00"),
			self.mon_9_to_5
		)
		notestest = {
			"day": "monday",
			"opens": "9:00",
			"closes": "17:00",
			"notes": "hi"
		}
		self.assertEqual(
			create_entry("monday", "9:00", "17:00", notes="hi"),
			notestest
		)

	
	def test_stringify_time(self):
		self.assertEqual(
			stringify_time((11,17)),
			"11:17"
		)
	
	def test_militarize_hours(self):
		self.assertEqual( militarize_hours(11, False), 11)
		self.assertEqual( militarize_hours(11, True), 23)

	def run_tests(self, input_strings, expected_result):
		for input_str in input_strings:
			print("Testing String: ", input_str)
			self.assertEqual(JsonOpeningHours.parse(input_str), expected_result)

if __name__ == '__main__':
	unittest.main()