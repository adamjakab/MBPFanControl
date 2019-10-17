#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import logging
import os
from math import log10, sinh, tanh


class FanController:
    _config = None
    _algorithm = "linear"
    _algorithms = ["linear", "logarithmic", "squared", "sinh", "tanh"]

    def __init__(self, algorithm, fan_config):
        self.logger = logging.getLogger()
        self._config = fan_config
        if algorithm in self._algorithms:
            self._algorithm = algorithm
        self._enable_manual_fan_control()

    def adjust_fan_speed(self, sensor_data):
        # self.logger.info("Sensor data: {0}".format(sensor_data))
        avg_percent = self._get_average_thermal_percent(sensor_data)
        self.logger.info("Average Thermal Percent(ATP): {0}%".format(avg_percent))
        fan_speeds = self._get_desired_fan_speeds(avg_percent)
        self._set_fan_speeds(fan_speeds)

    def _get_desired_fan_speeds(self, atp):
        answer = []
        for fan in self._config:
            range_min = int(fan["min_rpm"])
            range_max = int(fan["max_rpm"])
            range_tot = range_max - range_min
            if self._algorithm == "linear":
                y = atp
            elif self._algorithm == "logarithmic":
                y = 96.025 * log10((atp+10)/10)
            elif self._algorithm == "squared":
                y = (atp ** 2) / 100
            elif self._algorithm == "sinh":
                y = 50 + sinh((atp - 50) / 10.85)
            elif self._algorithm == "tanh":
                y = 50 + 50.5 * (tanh((atp - 50) / 17))
            else:
                self.logger.warning("Unknown fan algorithm({0})!".format(self._algorithm))
                # Fall back to 50%
                y = 50

            range_value = int(range_min + int(range_tot * y / 100))
            if range_value < range_min:
                range_value = range_min
            if range_value > range_max:
                range_value = range_max

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
        # self.logger.debug("EXEC: '{0}'".format(cmd))
        os.system(cmd)

    def _enable_manual_fan_control(self):
        for fan in self._config:
            if "enable_manual_sys_path" in fan:
                sys_path = fan["enable_manual_sys_path"]
                self.logger.debug("Enabling manual fan control: '{0}'".format(sys_path))
                cmd = 'echo {0} > {1}'.format(1, sys_path)
                os.system(cmd)

    def _get_average_thermal_percent(self, sensor_data):
        avg_percent = 0
        for sd in sensor_data:
            avg_percent += sd["range_percent"]
            self.logger.debug(
                "Sensor[{0}]: {1}°C ({2}%)".format(sd["alias"], int(sd["raw_value"] / 1000), sd["range_percent"]))

        avg_percent = int(avg_percent / len(sensor_data))
        return avg_percent
