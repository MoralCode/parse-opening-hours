import unittest
from parse_opening_hours import *

class TestHoursParsing(unittest.TestCase):

	def test_create_entry(self):
		self.assertEqual(
			create_entry("monday", "9:00", "5:00"),
			{
				"day": "monday",
				"opens": "9:00",
				"closes": "5:00"
			}
		)

	def test_expand_day_range(self):
		self.assertEqual(
			expand_day_range(Weekday.MONDAY, Weekday.FRIDAY),
			[Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY]
		)

if __name__ == '__main__':
	unittest.main()