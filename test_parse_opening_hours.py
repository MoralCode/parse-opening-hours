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

if __name__ == '__main__':
	unittest.main()