import unittest
from opening_hours import *
from opening_hours.models.time import TimeType
import logging

logger = logging.getLogger(__name__)

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
		"day": "thursday",
		"opens": "9:00",
		"closes": "17:00"
	}

	fri_9_to_5 = {
		"day": "friday",
		"opens": "9:00",
		"closes": "17:00"
	}

	sat_9_to_5 = {
		"day": "saturday",
		"opens": "9:00",
		"closes": "17:00"
	}

	sun_9_to_5 = {
		"day": "sunday",
		"opens": "9:00",
		"closes": "17:00"
	}

	workweek_9_to_5 = [mon_9_to_5, tue_9_to_5, wed_9_to_5,thurs_9_to_5, fri_9_to_5]
	weekend_9_to_5 = [sat_9_to_5, sun_9_to_5]
	allweek_9_to_5 = workweek_9_to_5.copy()
	allweek_9_to_5.extend(weekend_9_to_5)

	def test_time_assumption_fail(self):
		str_time = "Monday 9:00 - 5:00"
		expected_result = [ self.mon_9_to_5 ]
		with self.assertRaises(TypeError):
			OpeningHours.parse(str_time).json()

	def test_useless_prefixes(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Open Monday 9am - 5pm"
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result)

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
		self.run_tests(input_strings,expected_result, assume_type=TimeType.AM)



	def test_single_day_abbreveations(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = {
			"monday": [
				"Mondays' 9:00am - 5:00pm",
				"Monday's 9:00am - 5:00pm",
				"Mondays 9:00am - 5:00pm",
				"Monday 9:00am - 5:00pm",
				"Mon 9:00am - 5:00pm",
				"M 9:00am - 5:00pm",
				"Mon. 9:00am - 5:00pm",
				"M. 9:00am - 5:00pm"
			],
			"tuesday": [
				"Tuesdays' 9:00am - 5:00pm",
				"Tuesday's 9:00am - 5:00pm",
				"Tuesdays 9:00am - 5:00pm",
				"Tuesday 9:00am - 5:00pm",
				"Tues 9:00am - 5:00pm",
				"Tue 9:00am - 5:00pm",
				"T 9:00am - 5:00pm"
			],
			"wednesday": [
				"Wednesdays 9:00am - 5:00pm",
				"Wednesdays' 9:00am - 5:00pm",
				"Wednesday's 9:00am - 5:00pm",
				"Wednesday 9:00am - 5:00pm",
				"Wed 9:00am - 5:00pm",
				"W 9:00am - 5:00pm"
			],
			"thursday": [
				"Thursdays' 9:00am - 5:00pm",
				"Thursday's 9:00am - 5:00pm",
				"Thursdays 9:00am - 5:00pm",
				"Thursday 9:00am - 5:00pm",
				"Thurs 9:00am - 5:00pm",
				"Th 9:00am - 5:00pm",
				"H 9:00am - 5:00pm"
			],
			"friday": [
				"Fridays' 9:00am - 5:00pm",
				"Friday's 9:00am - 5:00pm",
				"Fridays 9:00am - 5:00pm",
				"Friday 9:00am - 5:00pm",
				"Fri 9:00am - 5:00pm",
				"F 9:00am - 5:00pm"
			],
			"saturday": [
				"Saturdays' 9:00am - 5:00pm",
				"Saturday's 9:00am - 5:00pm",
				"Saturdays 9:00am - 5:00pm",
				"Saturday 9:00am - 5:00pm",
				"Sat 9:00am - 5:00pm",
				"Sa 9:00am - 5:00pm"
			],
			"sunday": [
				"Sundays' 9:00am - 5:00pm",
				"Sunday's 9:00am - 5:00pm",
				"Sundays 9:00am - 5:00pm",
				"Sunday 9:00am - 5:00pm",
				"Sun 9:00am - 5:00pm",
				"Su 9:00am - 5:00pm"
			]
		}
		results = {
			"monday": self.mon_9_to_5,
			"tuesday": self.tue_9_to_5,
			"wednesday": self.wed_9_to_5,
			"thursday": self.thurs_9_to_5,
			"friday": self.fri_9_to_5,
			"saturday": self.sat_9_to_5,
			"sunday": self.sun_9_to_5
		}
		for day_of_week in list(input_strings.keys()):
			with self.subTest(day_of_week, day=day_of_week):
				expected_result = [ results[day_of_week] ]
				self.run_tests(input_strings[day_of_week],expected_result, assume_type=TimeType.AM)
	
	
	def test_day_time_separators(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday 9:00 - 5:00",
			"Monday from 9:00 - 5:00",
			"Monday: 9:00 - 5:00",
			"Monday, 9:00 - 5:00",
			
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result, assume_type=TimeType.AM)

	def test_time_formatting(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday 9:00 - 5:00",
			"Monday 9:00-5:00",
			"Monday 9:00am - 5:00pm",
			"Monday 9:00am-5:00pm",
			"Monday 9:00AM-5:00PM",
			"Monday 9:00 am - 5:00 pm",
			"Monday 9:00 am-5:00 pm",
			"Monday 9:00a.m. - 5:00 p.m.",
			"Monday 9:00 a.m.-5:00 p.m.",
			"Monday 9:00 - 5:00pm",
			"Monday 9:00-5:00pm",
			"Monday 9:00am - 5:00",
			"Monday 9:00am-5:00",
			"Monday 9am - 5pm",
			"Monday 9am-5pm",
			"Monday 9AM-5PM",
			"Monday 9am to 5pm",
			"Monday 9 am - 5 pm",
			"Monday 9 am-5 pm",
			"Monday 9a.m. - 5 p.m.",
			"Monday 9 a.m.-5 p.m.",
			"Monday 9 a.m. to 5 p.m.",
			"Monday 9a-5p",
			"Monday 9 a to 5 p",
			"Monday 9am through 5pm",
			"Monday 9am thru 5pm",
			"Monday 9am - 5pm",
			"Monday 9am – 5pm",
			"Monday 9am — 5pm",
			"Monday 9am \u2013 5pm",
			"Monday 9 a.m. \u2013 5 p.m.",
			"Monday 9-5",
			"Monday 900-1700",
			"Monday 0900-1700",
			"Monday 09:00AM-05:00PM"
			
		]
		expected_result = [ self.mon_9_to_5 ]
		self.run_tests(input_strings,expected_result, assume_type=TimeType.AM)


	def test_time_cutoff_regression(self):
		self.assertEqual(OpeningHours.parse("Monday 8am \u2013 11am").json(), [{'day': 'monday', 'opens': '8:00', 'closes': '11:00'}])
	
	
	def test_day_range(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday - Wednesday 9:00 - 5:00",
			"Mon - Wed 9:00 - 5:00",
			"M - W 9:00 - 5:00",
			"Monday-Wednesday 9:00 - 5:00",
			"Mon-Wed 9:00 - 5:00",
			"M-W 9:00 - 5:00",
			"Monday through Wednesday 9:00 - 5:00",
			"Monday to Wednesday 9:00 - 5:00",
			"Monday \u2013 Wednesday 9:00 - 5:00",
			"9 am to 5:00 pm Mondays through Wednesdays",
			"09:00AM-05:00PM Mon-Wed"

		]
		expected_result = [ self.mon_9_to_5, self.tue_9_to_5, self.wed_9_to_5 ]
		self.run_tests(input_strings, expected_result, assume_type=TimeType.AM)


	def test_day_list(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Monday Wednesday 9:00 - 5:00",
			"Monday and Wednesday 9:00 - 5:00",
			"Monday, Wednesday 9:00 - 5:00",
			"Monday/Wednesday 9:00 - 5:00",
			"Monday+Wednesday 9:00 - 5:00",
		]
		expected_result = [ self.mon_9_to_5, self.wed_9_to_5 ]
		self.run_tests(input_strings, expected_result, assume_type=TimeType.AM)

	def test_shortcuts(self):
		twenteyfourseven = OpeningHours.parse("Mon-sun 0am-11:59pm").json()
		input_strings = [
			"24 hours a day",
			"24 hours",
			"24hrs",
			"24h",
			"All Day",
			"Open 24 hours",
			"24/7",
			"24 hours a day",
			"24 hours a day, 7 days a week",
			"24 Hours/Day",
			# "24 Hours/Day, 7 Days/Week",
			"24 Hours per Day",
			# "24 Hours a Day, 7 Days a Week",
			# "Seven Days a Week"
		]
		self.run_tests(input_strings, twenteyfourseven, assume_type=TimeType.AM)

	def test_time_abbreviations(self):

		input_strings = {
			"noon": [
				"Monday noon - 1:00pm",
				"Monday Noon - 1:00pm",
				"Monday NOON - 1:00pm"
			],
			"midnight": [
				"Monday 11am - midnight",
				"Monday 11am - Midnight",
				"Monday 11am - MIDNIGHT"
			],
			"both": [
				"Monday noon - midnight",
				"Monday Noon - Midnight",
				"Monday NOON - MIDNIGHT"
			],
		}
		results = {
			"noon": {
				"day": "monday",
				"opens": "12:00",
				"closes": "13:00"
			},
			"midnight": {
				"day": "monday",
				"opens": "11:00",
				"closes": "0:00"
			},
			"both": {
				"day": "monday",
				"opens": "12:00",
				"closes": "0:00"
			}
		}
		for day_of_week in list(input_strings.keys()):
			with self.subTest(day_of_week, day=day_of_week):
				expected_result = [ results[day_of_week] ]
				self.run_tests(input_strings[day_of_week],expected_result, assume_type=TimeType.AM)

	
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
			"9:00am - 5:00pm Every Day",
			"9 a.m. \u2013 5 p.m.",
			"9 am \u2013 5 pm",
			"9-5",
			"9 - 5"
		]
		expected_result = self.allweek_9_to_5
		self.run_tests(input_strings, expected_result, assume_type=TimeType.AM)

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
			"9:00am - 5:00pm Business Days",
			"9-5 Weekdays"
		]
		expected_result = self.workweek_9_to_5
		self.run_tests(input_strings,expected_result, assume_type=TimeType.AM)

	def test_weekend(self):
		# TODO: implement assumption of pm if end time <= start time
		input_strings = [
			"Weekend 9:00am - 5:00pm",
			"Weekends 9:00am - 5:00pm",
			"9:00am - 5:00pm Weekend",
			"9:00am - 5:00pm Weekends",
		]
		expected_result = self.weekend_9_to_5
		self.run_tests(input_strings,expected_result)

# def test_multiple_days(self):
	# 	# TODO: implement assumption of pm if end time <= start time
	# 	input_strings = [
	# 		"Monday - Friday 9:00 am - 5:00 pm Saturdays 9:00 am - 5:00 pm",
	# 	]
	# 	expected_result = self.workweek_9_to_5.append(sat_9_to_5)
	# 	self.run_tests(input_strings,expected_result)

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

	def run_tests(self, input_strings, expected_result, **kwargs):
		for input_str in input_strings:
			logger.debug("Testing String: " + input_str)
			self.assertEqual(OpeningHours.parse(input_str, **kwargs).json(), expected_result)

if __name__ == '__main__':
	unittest.main()