MacBook Pro Fan Control
=======================

A simple application to provide a better and safer control over Mac Book Pro fans.

SETUP
-------------
```shell script

```

FAN SPEED ALGORITHMS
-------------
[![Fan Speed Algorithms](https://github.com/adamjakab/MBPFanControl/blob/master/doc/fan_speed_algorithms.png)](https://github.com/adamjakab/MBPFanControl)

X is the temperature expressed in percentage(0-100) between the minimum and the maximum temperature of the sensor.

Y is the speed of the fan expressed in percentage(0-100) between its minimum and the maximum speeds.

The 5 different curves provide 5 different response types of the fan:

- linear
- logarithmic
- squared
- sinh
- tanh

CONFIGURATION
-------------


USAGE
-------
Call as:

`$ python3 ./app.py --config CONFIGURATION_KEY`

TESTING
-------
TBD...

