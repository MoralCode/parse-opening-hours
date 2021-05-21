
import unittest
from opening_hours.models.day import *

class TestDay(unittest.TestCase):

	def test_from_string(self):

		input_strings = {
			"monday": [
				"Monday",
				"Mondays",
				"Monday's",
				"Mondays'",
				"Mon",
				"mon",
				"M"
			],
			"tuesday":  [
				"Tuesdays'",
				"Tuesday's",
				"Tuesdays",
				"Tuesday",
				"Tues",
				"Tue",
				"Tu",
				"T"
			],
			"wednesday": [
				"Wednesdays",
				"Wednesdays'",
				"Wednesday's",
				"Wednesday",
				"Wed",
				"W"
			],
			"thursday": [
				"Thursdays'",
				"Thursday's",
				"Thursdays",
				"Thursday",
				"Thurs",
				"Th",
				"H"
			],
			"friday": [
				"Fridays'",
				"Friday's",
				"Fridays",
				"Friday",
				"Fri",
				"F"
			],
			"saturday":[
				"Saturdays'",
				"Saturday's",
				"Saturdays",
				"Saturday",
				"Sat",
				"Sa"
			],
			"sunday": [
				"Sundays'",
				"Sunday's",
				"Sundays",
				"Sunday",
				"Sun",
				"Su"
			]
		}
		for day_of_week in list(input_strings.keys()):
			with self.subTest(day_of_week, day=day_of_week):
				expected_result = Day(day_of_week)
				for instr in input_strings[day_of_week]:
					self.assertEqual(Day.from_string(instr), expected_result)
		
	def test_from_string_edge_cases(self):
		# Assert that "s" is explicitly not matched due to ambiguity
		with self.assertRaises(ValueError):
			Day.from_string("s")
		# Assert that "t" is explicitly matched to tuesday
		self.assertEqual(Day.from_string("t"), Day(DaysEnum.TUESDAY))
		#handles none values
		with self.assertRaises(TypeError):
			Day.from_string(None)


	def test_equals(self):
		self.assertEqual(Day("monday"), Day("monday"))
		self.assertEqual(Day("monday"), DaysEnum.MONDAY)
		self.assertNotEqual(Day("monday"), Day("tuesday"))
		self.assertNotEqual(Day("monday"), DaysEnum.TUESDAY)
		with self.assertRaises(NotImplementedError):
			Day("monday") == "some other value"
	

	def test_init(self):
		self.assertEqual(Day("monday"), Day(DaysEnum("monday")))

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

if __name__ == '__main__':
	unittest.main()