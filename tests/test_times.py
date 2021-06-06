
import unittest
from opening_hours.models.time import Time, TimeType
from opening_hours.models.times import Times


# "24 hours a day",
# "24 hours" "24hrs" "24h" "All Day" "Open 24 hours"


class TestTimes(unittest.TestCase):

	def test_create_closed(self):
		closed_list = [
			Times(None, None),
			Times(Time(12,0), Time(12,0))
		]
		for time in closed_list:
			self.assertTrue(time.is_closed())
		
	def test_create_from_none(self):
		with self.assertRaises(TypeError):
			Times.from_shortcut_string(None)

		with self.assertRaises(TypeError):
			Times.parse(None)

	def test_create_from_unknown(self):
		with self.assertRaises(ValueError):
			Times.from_shortcut_string("cheeseburger")

	
	def test_create_from_shortcut(self):
		allday = Times(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))
		workhours = Times(Time(9, 0, TimeType.AM), Time(5, 0, TimeType.PM))
		closed = Times(None, None)


		test_values = {

			"allday": [
				"24h",
				"all day"
			],
			"workhours": [
				"business hours",
				"work hours",
			],
			"closed": [
				"closed",
				"null"
			]
		}
		result_values = {
			"allday": allday,
			"workhours": workhours,
			"closed": closed
		}
		for result_key in list(test_values.keys()):
			result = result_values[result_key]
			with self.subTest(result_key, result=result):
				for instr in test_values[result_key]:
					self.assertEqual(Times.from_shortcut_string(instr), result)

	def test_parse_time_formats(self):
		expected_value = Times(Time(7,0, TimeType.AM), Time(5,0, TimeType.PM)) 
		input_strings = [
			"700AM-500PM",
		]

		self.run_tests(input_strings, expected_value)

	# def test_shortcuts(self):
		# "24/7",
		# "Closed",
		# for time in input_strings:
		# 	self.assertTrue(Times.from_shortcut_string(time).is_closed())


	def test_is_closed(self):
		input_strings = [
			"Closed",
			"null"
		]
		for time in input_strings:
			self.assertTrue(Times.from_shortcut_string(time).is_closed())
	
	def test_str(self):
		self.assertEqual(str(Times(None, None)), "closed")
		self.assertEqual(str(Times(
			Time(9,0,TimeType.AM),
			Time(5,0,TimeType.PM))
		), "9:00 to 17:00")


	def test_json(self):
		self.assertEqual(Times(None, None).json(), {})

		
		self.assertEqual(Times(
			Time(9,0,TimeType.AM),
			Time(5,0,TimeType.PM)
		).json(), 
		{
		"opens": "9:00",
		"closes": "17:00"
		}
		)

		
	def test_equals(self):
		allday = Times(Time(0, 0, TimeType.AM), Time(11, 59, TimeType.PM))
		with self.assertRaises(NotImplementedError):
			allday == "something else"
		
		self.assertEqual(allday, allday)


	def run_tests(self, input_strings, expected_result, **kwargs):
		for input_str in input_strings:
			print("Testing String: '"+ input_str + "'")
			self.assertEqual(Times.parse(input_str, **kwargs), expected_result)

if __name__ == '__main__':
	unittest.main()