
import unittest
from helpers import *

class TestHelpers(unittest.TestCase):
	def test_expand_day_range(self):
		self.assertEqual(
			expand_day_range(Weekday.MONDAY, Weekday.FRIDAY),
			[Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
		)
	
	def test_str_to_day(self):
		input_strings = [
			"Monday",
			"Mondays",
			"Monday's",
			"Mondays'",
			"Mon",
			"mon",
			"M"
		]
		expected_result = Weekday.MONDAY
		for instr in input_strings:
			self.assertEqual(str_to_day(instr), expected_result)
		
		# Assert that "s" is explicitly not matched due to ambiguity
		self.assertEqual(str_to_day("s"), None)
		# Assert that "t" is explicitly matched to tuesday
		self.assertEqual(str_to_day("t"), Weekday.TUESDAY)
		#handles none values
		self.assertEqual(str_to_day(None), None)

	def test_detect_is_pm(self):
		input_strings = [
			"pm",
			"Pm",
			"pM",
			"p.m.",
			"PM",
		]
		for instr in input_strings:
			self.assertTrue(detect_if_pm(instr))
		
		input_strings = [
			"am",
			"Am",
			"aM",
			"a.m.",
			"AM",
		]
		for instr in input_strings:
			self.assertFalse(detect_if_pm(instr))

if __name__ == '__main__':
	unittest.main()