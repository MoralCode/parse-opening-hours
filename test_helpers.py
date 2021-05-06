
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

if __name__ == '__main__':
	unittest.main()