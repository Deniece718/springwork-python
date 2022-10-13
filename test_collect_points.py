import unittest
from collect_points import Row, Position

class Test(unittest.TestCase):
    def test_exceed_speed_limit(self):
        sample1 = Row("2016-06-21T12:00:05.000Z", {"latitude": 59.3337, "longitude": 18.0662}, 9.4, 8.33)
        sample2 = Row("2016-06-21T12:00:10.000Z", {"latitude": 59.3331, "longitude": 18.0664}, 11.1, 8.33)
        expected_speeding_distance = 0.068
        expected_speeding_time = 5.0
        self.assertEqual(Row.time_from(sample1, sample2), expected_speeding_time)
        self.assertEqual(round(Position.distance_from(sample1.position, sample2.position), 3), expected_speeding_distance)

    def test_below_speed_limit(self):
        sample1 = Row("2016-06-21T12:00:15.000Z", {"latitude": 59.3327, "longitude": 18.0665}, 8.32, 8.33)
        sample2 = Row("2016-06-21T12:00:20.000Z", {"latitude": 59.3323, "longitude": 18.0666}, 8.33, 8.33)
        expected_speeding_distance = 0.045
        expected_total_time = 5.0
        self.assertEqual(Row.time_from(sample1, sample2), expected_total_time)
        self.assertEqual(round(Position.distance_from(sample1.position, sample2.position), 3), expected_speeding_distance)
