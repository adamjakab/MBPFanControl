#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import subprocess
import logging
import os


class FanController:
    _config = None
    _algorithm = "linear"
    _algorithms = ["linear", "logarithmic", "squared"]

    def __init__(self, algorithm, fan_config):
        self.logger = logging.getLogger()
        self._config = fan_config
        if algorithm in self._algorithms:
            self._algorithm = algorithm


    def adjust_fan_speed(self, sensor_data):
        self.logger.info("Sensor data: {0}".format(sensor_data))
        avg_percent = self._get_average_thermal_percent(sensor_data)
        self.logger.info("Average Thermal Percent: {0}".format(avg_percent))
        fan_speeds = self._get_desired_fan_speeds(avg_percent)
        self._set_fan_speeds(fan_speeds)

    def _get_desired_fan_speeds(self, atp):
        answer = []
        for fan in self._config:
            range_min = int(fan["min_rpm"])
            range_max = int(fan["max_rpm"])
            range_tot = range_max - range_min
            if self._algorithm == "linear":
                range_value = range_min + int(range_tot * atp / 100)
            else:
                self.logger.warning("Unknown fan algorithm({0})!".format(self._algorithm))
                # Fall back to 50%
                range_value = range_min + int(range_tot / 2)

            answer.append(range_value)

        return answer

    def _set_fan_speeds(self, fan_speeds):
        for i in range(0, len(fan_speeds)):
            fan = self._config[i]
            rpm = fan_speeds[i]
            self.logger.info("Setting Fan({0}) speed to: {1}".format(i, fan_speeds[i]))
            self._set_fan_rpm(rpm, fan["sys_path"])

    def _set_fan_rpm(self, rpm, sys_path):
        cmd = 'echo {0} > {1}'.format(rpm, sys_path)
        self.logger.debug("EXEC: '{0}'".format(cmd))
        os.system(cmd)

        # try:
        #     subprocess.call([cmd], stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w"))
        # except Exception as e:
        #     self.logger.warning("OS Call error: {0}".format(e))
        #     pass

    @staticmethod
    def _get_average_thermal_percent(sensor_data):
        avg_percent = 0
        for sd in sensor_data:
            avg_percent += sd["range_percent"]

        avg_percent = int(avg_percent / len(sensor_data))
        return avg_percent





