from datetime import datetime
import json
from math import atan2, cos, radians, sin, sqrt

class Position:
    def __init__(self, lat, long):
        self.lat = radians(lat)
        self.long = radians(long)
    
    def distance_from(self, pos_b: 'Position'):
        dlat = pos_b.lat - self.lat
        dlong = pos_b.long - self.long
        a = (sin(dlat/2))**2 + cos(self.lat) * cos(pos_b.lat) * (sin(dlong/2))**2
        distance = 6373.0 * 2 * atan2(sqrt(a), sqrt(1-a))
        return distance

class Row:
    def __init__(self, timestamp_str, position, speed, speed_limit):
        self.timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
        self.position = Position(position['latitude'], position['longitude'])
        self.speed = speed
        self.speed_limit = speed_limit
    
    def time_from(self, row_b: 'Row'):
        return abs(row_b.timestamp - self.timestamp)


def main():
    rows = []
    data_categories = {}
    speeding_time = 0
    speeding_distance = 0
    total_distance = 0
    total_time = 0

    with open('waypoints.json', 'r') as f:
        row_date = json.load(f)

        for each_row in row_date:
            rows.append(Row(each_row['timestamp'], each_row['position'], each_row['speed'], each_row['speed_limit']))

    for i in range(len(rows) - 1):
        first_row = rows[i]
        second_row = rows[i + 1]

        if first_row.speed > first_row.speed_limit:
            speeding_time += first_row.time_from(second_row)
            speeding_distance += first_row.position.distance_from(second_row.position)

        total_distance += first_row.position.distance_from(second_row.position)
        total_time += first_row.time_from(second_row)

    data_categories['speeding_distance(km)'] = speeding_distance
    data_categories['speeding_duration(s)'] = speeding_time
    data_categories['total_distance(km)'] = total_distance
    data_categories['total_duration(s)'] = total_time
 
    print(data_categories)

if __name__ == "__main__":
    main()