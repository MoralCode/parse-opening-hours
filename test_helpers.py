
import unittest
from helpers import *

class TestHelpers(unittest.TestCase):
	def test_expand_day_range(self):
		self.assertEqual(
			expand_day_range(Day.MONDAY, Day.FRIDAY),
			[Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]
		)
	
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