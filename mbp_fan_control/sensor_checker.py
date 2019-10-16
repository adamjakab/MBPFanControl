#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import logging
import os


class SensorChecker:
    _config = None

    def __init__(self, sensor_config):
        self.logger = logging.getLogger()
        self._config = sensor_config

    def get_sensors_data(self):
        answer = []

        for sensor in self._config:
            raw_value = self._read_sensor_data(sensor["sys_path"])
            range_min = int(sensor["min_degrees"]) * 1000
            range_max = int(sensor["max_degrees"]) * 1000
            if raw_value < range_min:
                range_min = raw_value
            if raw_value > range_max:
                range_max = raw_value
            range_tot = range_max - range_min
            range_value = raw_value - range_min
            range_percent = int((range_value / range_tot) * 100)
            sd = {
                "alias": sensor["alias"],
                "sys_path": sensor["sys_path"],
                "raw_value": raw_value,
                "range_min": range_min,
                "range_max": range_max,
                "range_tot": range_tot,
                "range_value": range_value,
                "range_percent": range_percent,
            }

            answer.append(sd)

        return answer


    @staticmethod
    def _read_sensor_data(sys_path):
        cmd = 'cat {0}'.format(sys_path)
        answer = int(os.popen(cmd).read())
        return answer

