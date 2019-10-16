#!/usr/bin/env python3
#
#  Author: Adam Jakab
#  Copyright: Copyright (c) 2019., Adam Jakab
#  License: See LICENSE.txt
#  Email: adaja at itu dot dk
#
#

import argparse
import json
import logging.config
import os
import signal
import sys
from time import sleep

from deepmerge import always_merger

from mbp_fan_control.fan_controller import FanController
from mbp_fan_control.sensor_checker import SensorChecker

__script_dir__ = os.path.dirname(os.path.realpath(__file__))
config_file = __script_dir__ + '/config.json'

# Load configuration file
try:
    with open(config_file) as config_file:
        full_configuration = json.load(config_file)
except Exception as e:
    print("The configuration file cannot be opened! Fatal error: {0}".format(e))
    sys.exit(201)

# Add command line arguments and run
parser = argparse.ArgumentParser(description='MBP Fan Control')
parser.add_argument('--config', type=str, default="default", help='The configuration section to use.')
args = parser.parse_args()

# Default configuration - use "default" section from configuration file if it exists
config = json.loads('{}')
if "default" in full_configuration:
    config = full_configuration["default"]

# Check selected configuration
if args.config not in full_configuration:
    print("Fatal error: The configuration section '{0}' does not exist.".format(args.config))
    sys.exit(202)

# Merge the default configuration with the selected configuration section
if args.config != "default":
    config = always_merger.merge(config, full_configuration[args.config])

# Set up logging
log_configuration_file = config["log_configuration_file"]
if os.path.isfile(log_configuration_file) is False:
    print("Fatal error: The log configuration file does not exist: '{0}'".format(log_configuration_file))
    sys.exit(203)

logging.config.fileConfig(__script_dir__ + '/' + log_configuration_file)
logger = logging.getLogger(__name__)

___KEEP_RUNNING___ = True


def interrupt(sig, frame):
    global ___KEEP_RUNNING___
    # subscriber.interrupt()
    # destination.interrupt()
    logger.warning("INTERRUPT!")
    ___KEEP_RUNNING___ = False


# Run main
if __name__ == '__main__':
    # Handle interruption Ctrl+C or other to cleanly close the connection to broker
    signal.signal(signal.SIGINT, interrupt)

    checker = SensorChecker(config["sensors"])
    ctrl = FanController(config["fan_speed_algorithm"], config["fans"])

    while ___KEEP_RUNNING___:
        sensor_data = checker.get_sensors_data()
        ctrl.adjust_fan_speed(sensor_data)
        sleep(config["poll_interval_sec"])

