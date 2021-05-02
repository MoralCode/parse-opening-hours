
import unittest
from time import *

class TestTime(unittest.TestCase):

	def test_stringify_time(self):
		self.assertEqual(
			Time(11,17,TimeType.MILITARY),
			"11:17"
		)
	
	def test_militarize_hours(self):
		testTimeMil = Time(11,17,TimeType.MILITARY)
		testTimePm = Time(11,17,TimeType.PM)
		self.assertEqual(
			testTimeMil.get_as_military_time().get_hours(),
			11
		)
		self.assertEqual(
			testTimePm.get_as_military_time().get_hours(),
			23
		)

if __name__ == '__main__':
	unittest.main()